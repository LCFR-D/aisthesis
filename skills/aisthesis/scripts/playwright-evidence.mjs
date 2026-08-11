#!/usr/bin/env node

import { createRequire } from 'node:module';
import { lstat, mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const USAGE = `Aisthesis Playwright evidence adapter

Usage:
  node scripts/playwright-evidence.mjs --url <http(s)://...> --output <new-directory> [options]

Options:
  --engines <list>       Comma-separated chromium,firefox,webkit (default: chromium,firefox)
  --profiles <list>      Comma-separated name:WIDTHxHEIGHT values
                         (default: desktop:1440x900,mobile:390x844)
  --theme <value>        light or dark (default: light)
  --reduced-motion <v>   no-preference or reduce (default: no-preference)
  --timeout <ms>         Navigation and readiness timeout (default: 30000)
  --help                 Show this help

The adapter resolves Playwright from the host project at process.cwd(). It never
installs dependencies. Run it from a project that already pins Playwright.`;

function fail(message, code = 2) {
  process.stderr.write(`ERROR: ${message}\n`);
  process.exitCode = code;
}

function parseArgs(argv) {
  const values = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (token === '--help') return { help: true };
    if (!token.startsWith('--')) throw new Error(`unexpected argument: ${token}`);
    const value = argv[index + 1];
    if (!value || value.startsWith('--')) throw new Error(`${token} requires a value`);
    if (values.has(token)) throw new Error(`duplicate argument: ${token}`);
    values.set(token, value);
    index += 1;
  }
  const known = new Set([
    '--url',
    '--output',
    '--engines',
    '--profiles',
    '--theme',
    '--reduced-motion',
    '--timeout',
  ]);
  for (const key of values.keys()) {
    if (!known.has(key)) throw new Error(`unknown option: ${key}`);
  }
  if (!values.has('--url')) throw new Error('--url is required');
  if (!values.has('--output')) throw new Error('--output is required');

  const url = new URL(values.get('--url'));
  if (!['http:', 'https:'].includes(url.protocol)) {
    throw new Error('--url must use http or https');
  }

  const engines = (values.get('--engines') ?? 'chromium,firefox')
    .split(',')
    .map((value) => value.trim())
    .filter(Boolean);
  if (engines.length === 0 || engines.some((name) => !['chromium', 'firefox', 'webkit'].includes(name))) {
    throw new Error('--engines must contain only chromium, firefox, or webkit');
  }

  const profiles = (values.get('--profiles') ?? 'desktop:1440x900,mobile:390x844')
    .split(',')
    .map((entry) => {
      const match = /^([a-z0-9-]+):(\d+)x(\d+)$/.exec(entry.trim());
      if (!match) throw new Error(`invalid profile: ${entry}`);
      const width = Number(match[2]);
      const height = Number(match[3]);
      if (width < 240 || height < 240 || width > 7680 || height > 4320) {
        throw new Error(`profile dimensions are outside the supported range: ${entry}`);
      }
      return { name: match[1], width, height };
    });

  const theme = values.get('--theme') ?? 'light';
  if (!['light', 'dark'].includes(theme)) throw new Error('--theme must be light or dark');
  const reducedMotion = values.get('--reduced-motion') ?? 'no-preference';
  if (!['no-preference', 'reduce'].includes(reducedMotion)) {
    throw new Error('--reduced-motion must be no-preference or reduce');
  }
  const timeout = Number(values.get('--timeout') ?? '30000');
  if (!Number.isInteger(timeout) || timeout < 1000 || timeout > 300000) {
    throw new Error('--timeout must be an integer from 1000 to 300000');
  }

  return {
    help: false,
    url: url.href,
    output: path.resolve(values.get('--output')),
    engines: [...new Set(engines)],
    profiles,
    theme,
    reducedMotion,
    timeout,
  };
}

async function rejectLinkedAncestors(destination) {
  let current = destination;
  while (true) {
    try {
      const details = await lstat(current);
      if (details.isSymbolicLink()) throw new Error(`output path traverses a symbolic link: ${current}`);
      if (current === destination) throw new Error(`output directory already exists: ${destination}`);
    } catch (error) {
      if (error.code !== 'ENOENT') throw error;
    }
    const parent = path.dirname(current);
    if (parent === current) break;
    current = parent;
  }
}

async function loadProjectPlaywright() {
  const projectRequire = createRequire(path.join(process.cwd(), 'package.json'));
  let modulePath;
  try {
    modulePath = projectRequire.resolve('playwright');
  } catch {
    throw new Error(
      'Playwright is not installed in the host project. Pin it there first, then rerun from that project root.',
    );
  }
  const loaded = await import(pathToFileURL(modulePath).href);
  return loaded.default ?? loaded;
}

async function waitForRenderedMedia(page, timeout) {
  return page.evaluate(async (maximumWait) => {
    if (document.fonts?.ready) {
      await Promise.race([
        document.fonts.ready,
        new Promise((resolve) => setTimeout(resolve, maximumWait)),
      ]);
    }
    const visibleImages = [...document.images].filter((image) => {
      const rect = image.getBoundingClientRect();
      return rect.bottom > 0 && rect.right > 0 && rect.top < innerHeight && rect.left < innerWidth;
    });
    await Promise.race([
      Promise.all(
        visibleImages.map(async (image) => {
          if (!image.complete) {
            await new Promise((resolve) => {
              image.addEventListener('load', resolve, { once: true });
              image.addEventListener('error', resolve, { once: true });
            });
          }
          if (typeof image.decode === 'function') await image.decode().catch(() => undefined);
        }),
      ),
      new Promise((resolve) => setTimeout(resolve, maximumWait)),
    ]);
    return visibleImages
      .filter((image) => !image.complete || image.naturalWidth === 0)
      .map((image) => image.currentSrc || image.src || '(unknown image)');
  }, Math.min(timeout, 5000));
}

async function capture(playwright, options, engineName, profile) {
  const launcher = playwright[engineName];
  if (!launcher) throw new Error(`Playwright does not expose engine: ${engineName}`);
  const browser = await launcher.launch({ headless: true });
  const errors = [];
  try {
    const context = await browser.newContext({
      viewport: { width: profile.width, height: profile.height },
      colorScheme: options.theme,
      reducedMotion: options.reducedMotion,
      locale: 'en-US',
      timezoneId: 'UTC',
    });
    const page = await context.newPage();
    page.on('console', (message) => {
      if (message.type() === 'error') errors.push({ type: 'console', text: message.text() });
    });
    page.on('pageerror', (error) => errors.push({ type: 'pageerror', text: error.message }));
    page.on('requestfailed', (request) =>
      errors.push({
        type: 'requestfailed',
        url: request.url(),
        text: request.failure()?.errorText ?? 'request failed',
      }),
    );
    page.on('response', (response) => {
      if (response.status() >= 400) {
        errors.push({ type: 'http', status: response.status(), url: response.url() });
      }
    });

    const response = await page.goto(options.url, { waitUntil: 'networkidle', timeout: options.timeout });
    if (!response) errors.push({ type: 'navigation', text: 'navigation returned no main response' });
    const incompleteVisibleImages = await waitForRenderedMedia(page, options.timeout);
    for (const url of incompleteVisibleImages) {
      errors.push({ type: 'media', url, text: 'visible image did not render before capture' });
    }

    const geometry = await page.evaluate(() => ({
      url: location.href,
      title: document.title,
      viewport: { width: innerWidth, height: innerHeight, devicePixelRatio },
      document: {
        scrollWidth: document.documentElement.scrollWidth,
        clientWidth: document.documentElement.clientWidth,
        scrollHeight: document.documentElement.scrollHeight,
        clientHeight: document.documentElement.clientHeight,
      },
      checkpoints: [...document.querySelectorAll('[data-aisthesis-checkpoint]')].map((element) => {
        const rect = element.getBoundingClientRect();
        return {
          id: element.getAttribute('data-aisthesis-checkpoint'),
          x: rect.x,
          y: rect.y,
          width: rect.width,
          height: rect.height,
        };
      }),
    }));

    const stem = `${engineName}-${profile.name}`;
    const screenshot = `${stem}.png`;
    await page.screenshot({ path: path.join(options.output, screenshot), fullPage: false });
    await context.close();
    return {
      engine: engineName,
      profile,
      theme: options.theme,
      reducedMotion: options.reducedMotion,
      screenshot,
      geometry,
      errors,
      passed: errors.length === 0 && geometry.document.scrollWidth <= geometry.document.clientWidth,
    };
  } finally {
    await browser.close();
  }
}

async function main() {
  let options;
  try {
    options = parseArgs(process.argv.slice(2));
  } catch (error) {
    fail(error.message);
    return;
  }
  if (options.help) {
    process.stdout.write(`${USAGE}\n`);
    return;
  }

  try {
    const playwright = await loadProjectPlaywright();
    await rejectLinkedAncestors(options.output);
    await mkdir(options.output, { recursive: true });
    const records = [];
    for (const engine of options.engines) {
      for (const profile of options.profiles) {
        records.push(await capture(playwright, options, engine, profile));
      }
    }
    const evidence = {
      schema: 'aisthesis-browser-evidence/v1',
      candidate: process.env.AISTHESIS_CANDIDATE ?? null,
      requestedUrl: options.url,
      projectRoot: process.cwd(),
      records,
      passed: records.every((record) => record.passed),
    };
    await writeFile(
      path.join(options.output, 'evidence.json'),
      `${JSON.stringify(evidence, null, 2)}\n`,
      { encoding: 'utf8', flag: 'wx' },
    );
    process.stdout.write(`${path.join(options.output, 'evidence.json')}\n`);
    if (!evidence.passed) process.exitCode = 1;
  } catch (error) {
    fail(error.message, 1);
  }
}

await main();

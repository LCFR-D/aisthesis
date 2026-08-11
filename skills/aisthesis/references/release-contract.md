# Functional, performance, security, and release contract

## Dogfood pass

Exercise the interface as a visitor: fresh entry, primary task, alternate path, keyboard-only path, touch path, invalid input, slow and failed network, refresh, deep link, back/forward, retry, cancellation, undo, logout and permission boundary where relevant, and route teardown. Preserve URLs, screenshots, console output, and exact reproductions for defects.

Test real content extremes: shortest, longest, missing, localized, untrusted, and high-volume values. Confirm analytics, consent, and legal behavior only from actual implementation evidence.

### Exploratory charter and defect ledger

Before browsing, define the surface, personas, accounts/permissions, routes, high-risk journeys, excluded areas and evidence directory. Explore by journey rather than clicking every element once. After each meaningful interaction, check visible state, URL/history, focus, accessibility state, network and console.

Classify defects by user impact:

- **Critical:** security/privacy failure, destructive loss, blocked primary journey with no recovery, or public release integrity failure.
- **High:** primary journey materially broken, inaccessible to a supported input/AT path, or severe cross-browser/responsive failure.
- **Medium:** secondary journey, state, clarity or performance failure with a workaround.
- **Low:** localized polish issue that does not alter task success or meaning.

Each issue records candidate identity, severity, route/state/profile, preconditions, exact reproduction, expected versus observed behavior, console/network evidence, screenshot or trace, likely ownership, and verification after the fix. Deduplicate by cause and user impact, not by screenshot similarity.

## Accessibility gate

Run automated checks and manual keyboard/semantics review. Verify focus order and restoration, names/roles/states, headings and landmarks, zoom/reflow, contrast, touch targets, error association, live announcements, reduced motion, themes, and assistive alternatives for charts, canvas, drag, and rich media.

Automated tools find candidates; they do not prove usability.

## Security and privacy gate

Review the exact frontend trust boundaries:

- untrusted HTML, markdown, URLs, SVG, images, and rich text;
- DOM injection and unsafe rendering APIs;
- authentication and authorization assumptions exposed in UI logic;
- tokens, secrets, source maps, logs, analytics, and error payloads;
- cross-origin requests, redirects, downloads, uploads, and file previews;
- dependency integrity, licence, known vulnerabilities, and bundle provenance;
- consent, tracking, storage, clipboard, camera, microphone, location, and notification use;
- clickjacking, opener relationships, external links, and embedded third-party content.

Client-side hiding is never authorization. Do not include secrets in frontend bundles. Sensitive actions require server-side enforcement and clear human scope.

## Performance pass

Measure loading and runtime separately. Capture:

- Core Web Vitals or equivalent field/lab evidence;
- transferred bytes and request count by type;
- responsive-image and font selection;
- rendering, hydration, long tasks, memory, and layout shifts;
- animation frame stability and scroll responsiveness;
- third-party, analytics, canvas, video, and WebGL cost;
- cache, compression, preloading, and route-splitting behavior.

Fix source ownership before compressing symptoms. Performance optimization cannot silently lower visual fidelity, remove content, or regress accessibility.

### Default budgets

Replace these only with documented product-specific budgets. For representative 75th-percentile or accepted lab proxies, target:

- LCP at or below 2.5 seconds;
- INP at or below 200 milliseconds;
- CLS at or below 0.1;
- critical interaction tasks below 50 milliseconds where possible and no unexplained long task above 200 milliseconds;
- no unbounded animation, listener, timer, canvas or WebGL work while offscreen or hidden;
- route-level JavaScript, image, font and third-party byte budgets recorded before implementation.

Capture at least three comparable runs after warm-up and preserve the median plus variance. Use the same browser, device profile, network/CPU settings, route, cache state and candidate identity for before/after claims.

Typical pinned-tool commands:

```bash
npx lighthouse http://127.0.0.1:4173 --output=json --output-path=artifacts/lighthouse.json
npx playwright test --project=chromium
```

Use the host repository's lockfile and scripts rather than installing latest packages in the gate. Inspect the network waterfall, coverage, performance trace, layout-shift sources, long tasks, image `currentSrc`, font requests and cache/compression headers. Field Web Vitals outrank optimistic lab scores when field data is available and comparable.

## Diff-bounded code and security review

1. Freeze the candidate revision and show the merge-base diff, changed generated artifacts and dependency/lock changes.
2. Run the repository's baseline tests, formatters, linters, type checks, security scans, dependency audit and build. Distinguish pre-existing findings from new ones.
3. Review data flow, state ownership, cleanup, errors, async cancellation, trust boundaries, authorization assumptions, accessibility and performance ownership in changed code.
4. Ask an independent reviewer to inspect the exact revision with a fail-closed `PASS` or `BLOCKED` verdict and concrete reproductions.
5. Apply bounded fixes, rerun affected and full gates, freeze a new revision, and obtain review of that new revision. Approval never transfers between commits.

Do not auto-fix beyond the reviewed scope, suppress findings without a reason, or publish from an uncommitted working tree.

## Cross-browser matrix

Choose browsers from audience and risk. For high-risk interaction, scrolling, media, forms, or new platform APIs, include Chromium and Firefox-derived engines plus WebKit where supported. Distinguish product failure, browser variance, harness failure, and unsupported capability.

Use real input for critical behavior. Synthetic DOM mutation is not evidence that keyboard, pointer, touch, wheel, drag, clipboard, upload, or focus behavior works.

## Preview gate

1. Freeze and identify the candidate.
2. Build locally from a clean environment.
3. Deploy an isolated immutable preview.
4. Run the complete required browser/evidence matrix against the exact preview URL.
5. Inspect rendered screenshots at full resolution.
6. Compare served asset hashes with the verified build when practical.
7. Treat any code, configuration, content, dependency, or asset change as a new candidate requiring rerun.

## Independent review

For material changes, request a review of the exact commit, tree, immutable build, or deployment. Ask for concrete blockers with reproductions, not generic impressions. Reproduce returned findings on current files before editing; stale line numbers and older candidates are not evidence about the current artifact.

## Production gate

Deploy only the verified candidate. Read back the production route, settings, assets, headers, and critical user journey. Confirm custom-domain and DNS targets where applicable. Verify rollback or previous deployment availability. Never report deployment success from command exit alone.

## Release evidence minimum

- exact revision, tree/build, environment, lock state, and deployment identity;
- commands and exit results;
- routes, browsers, profiles, themes, locale, and states covered;
- screenshots, traces, reports, and hashes where useful;
- functional, accessibility, security, and performance results;
- console, network, overflow, hydration, and resource status;
- known limitations and blocked decisions;
- preview and production URLs with read-back evidence;
- rollback path;
- human acceptance status stated explicitly, never inferred.

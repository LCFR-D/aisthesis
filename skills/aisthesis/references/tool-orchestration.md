# Tool orchestration and executable adapters

Aisthesis is the single operating contract. Host tools are adapters: use them when available, verify their outputs, and keep the same product-truth, evidence, judgment, and release boundaries when an adapter is absent.

## Detect before invoking

At the start of a task, inspect the repository and the agent's actual tool schemas. Record only capabilities that are demonstrably available:

- package manager, framework, build, test, lint, typecheck, and deployment commands;
- browser automation such as Playwright;
- accessibility, performance, visual-regression, component-preview, and bundle-analysis tooling;
- approved image, video, canvas, WebGL, design-token, and document tools;
- project-owned scripts, MCP servers, plugins, and custom functions;
- specialist host tools for design direction, visual judgment, dogfooding, security, or release review.

Never invent a command from a product name. Read its help or schema first. Never install a replacement merely because the preferred adapter is absent; use the host browser and screenshot tools when they can satisfy the contract, or report the missing capability as a blocker.

## One entry point, many adapters

| Aisthesis responsibility | Preferred adapter | Valid fallback | Required evidence |
|---|---|---|---|
| Product truth and scope | Repository sources, issue/brief, Metis contract | User-approved brief | Claims and preservation boundary |
| Direction and craft | Aisthesis Taste/Impeccable/Hallmark methods | Approved references plus bundled direction method | Direction brief and anti-template criteria |
| Implementation | Incumbent framework and project commands | Standards-based HTML/CSS/JS | Running code and executable assertions |
| Browser evidence | Project-pinned Playwright via `scripts/playwright-evidence.mjs` | Trusted host browser automation | Exact engine/profile frames, geometry, console/network record |
| Accessibility | Project's axe/AT harness and manual keyboard/screen-reader checks | Browser semantics plus documented manual checks | WCAG criterion-linked findings |
| Visual judgment | Aisthesis passes and optional repository CLI | Full-resolution human/model inspection | Localized observations separated from hypotheses |
| Motion/scroll evidence | Playwright native wheel plus deterministic checkpoints | Host browser trusted input | Physical travel, authored progress, reduced-motion parity |
| Performance | Project Lighthouse/Web Vitals/bundle tools | Browser timing and asset inspection | Budgets, environment, before/after measurements |
| Dogfood | Playwright journeys or host browser tools | Manual reproducible charter | Steps, state, console/network output, screenshots |
| Release | Project CI/deploy tooling | Documented preview/production workflow | Immutable candidate identity and production read-back |

Named methods are integrated capability layers, not installation dependencies. Loading a separately installed Impeccable, Taste, Kinetograph, dogfood, accessibility, performance, or security tool is optional acceleration; it never replaces Aisthesis's authority order or completion gates.

## Portable Playwright capture

The bundled adapter deliberately resolves Playwright from the host project at `process.cwd()`. It never downloads a browser or mutates dependencies. Run it from a project that already pins Playwright:

```bash
AISTHESIS_CANDIDATE="$(git rev-parse HEAD)" \
node /path/to/aisthesis/scripts/playwright-evidence.mjs \
  --url http://127.0.0.1:4173 \
  --output ./aisthesis-evidence \
  --engines chromium,firefox \
  --profiles desktop:1440x900,mobile:390x844
```

Use a new output directory. The adapter refuses overwrite, records viewport geometry, captures viewport screenshots, listens for console errors, page errors, failed requests and HTTP failures, and writes `evidence.json`. It fails when errors or horizontal overflow remain. It is a baseline capture adapter, not a complete acceptance oracle.

For project-specific flows, copy the adapter into a temporary harness or extend the project's existing Playwright suite rather than editing the installed skill. Add route setup, authentication supplied by the project's approved secret mechanism, trusted pointer/keyboard/touch/wheel input, state fixtures, axe checks, performance marks, deterministic progress hooks, and assertions required by the brief. Never type or embed secrets in the skill or evidence.

## Custom functions and project-owned tools

Treat custom functions as typed adapters:

1. inspect the current schema, help output, source, or project documentation;
2. map each function to one Aisthesis responsibility and acceptance criterion;
3. run the smallest read-only probe first;
4. capture exact inputs, outputs, version, and failure mode;
5. verify side effects through an independent read-back;
6. keep human acceptance separate from tool success.

Prefer project-owned functions when they embody approved product behavior, asset generation, deployment, or evidence capture. Do not replace them with generic equivalents without an explicit redesign or migration decision.

## Browser evidence minimum

For material frontend work, browser evidence covers:

- Chromium and Firefox-derived engines for high-risk interaction or scroll behavior;
- desktop, intermediate, and mobile profiles appropriate to the product;
- light/dark, reduced motion, localization, zoom, keyboard, touch, and forced-colors states where applicable;
- real pointer, keyboard, touch, and native-wheel paths rather than DOM-only event simulation;
- console, page, request, response, selected-resource, overflow, and accessibility outputs;
- direct full-resolution frames plus a machine-readable index.

The adapter's defaults are a starting matrix. The brief decides the complete matrix.

## Failure rules

- A missing adapter is not permission to fabricate results.
- A green Playwright run is not visual acceptance.
- A screenshot is not proof of keyboard, network, accessibility, or performance behavior.
- A specialist tool's score cannot overrule product truth or user rejection.
- A host-tool success without output read-back is unverified.
- Any candidate change invalidates browser and release evidence tied to the prior revision.

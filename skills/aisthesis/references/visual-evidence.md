# Deterministic capture and Aisthesis judgment

## Capture contract

Freeze the candidate and record environment identity: commit/build, URL, browser engine/version, viewport, DPR, theme, reduced motion, locale, timezone, fonts, selected assets, and service-worker state.

Capture exact checkpoints plus physical interaction:

- desktop, mobile, intermediate, ultrawide;
- each supported theme;
- reduced motion;
- primary route states;
- native wheel/scroll in Chromium and Firefox-derived engines for scroll-led work;
- full-resolution viewport screenshots, not only contact sheets;
- console, page, network, critical-resource, overflow, and accessibility results.

For authored progress, include named keyframes in the sample grid rather than relying on nearest uniform samples. Record requested and actual progress. Use at least two frames around every concealed swap.

## Execution adapters

Aisthesis does not assume a separately installed private skill or CLI. Implement the capture contract with the host project's pinned browser tooling. A minimal Playwright-compatible sequence is:

1. launch each required engine with an explicit viewport, DPR, color scheme, locale and reduced-motion value;
2. attach page-error, console, response and request-failure listeners before navigation;
3. wait for fonts and required media to decode;
4. reach the state through trusted keyboard, pointer, touch or native-wheel input;
5. capture URL, scroll position, DOM geometry, computed state, accessibility results and a full-resolution screenshot;
6. write a machine-readable record containing the candidate and environment identity;
7. close the context and fail on any unexplained error.

For scroll narratives, run real wheel input in Chromium and Firefox as well as deterministic progress capture. Compare requested versus actual travel and retain dense frames around occlusion, swaps and phase boundaries. The separately available Kinetograph CLI may automate this interface, but it is not required for the bundled method.

The repository's public Python toolkit can inspect saved frames and pacing plans:

```bash
aisthesis inspect frame.png --output findings.json
aisthesis pacing --plan phase-plan.json --output pacing.json
```

Use equivalent project-native tools when the Python toolkit is unavailable. The evidence schema and acceptance boundary remain the same.

## Deterministic candidates

Useful measurements include DOM geometry, fixed-position tolerance, painted occlusion variants, CIEDE2000 long-boundary detection, repeated-motif candidates, changed-pixel ratio, SSIM, optical flow, entropy, edge density, physical viewport travel, image alpha/coverage, and selected responsive sources.

Metrics rank review targets. They do not establish visual quality.

## Four visual passes

1. **Object/overlap:** identity, clipping, duplication, masks, collisions, concealment.
2. **Palette/material:** temperature, value, saturation, texture, lighting, pixel scale, seams.
3. **Composition/hierarchy:** focal order, balance, negative space, grouping, landmark legibility, product/narrative coherence.
4. **Temporal/responsive:** dead travel, rushed beats, holds, reversals, transitions, cross-profile parity.

For every finding record observation, profile/frame/progress/region, confidence, owner candidate, causal hypothesis labelled separately, and acceptance condition. Inspect direct frames as well as overview and phase boards.

Generate an overview contact sheet for navigation, a phase board for every authored segment, and keep each direct frame independently inspectable. Contact sheets never replace source frames. Preserve a JSON or CSV index that maps frame ID to route, profile, requested/actual progress, state, timestamp, screenshot path and errors.

## Calibration

Before treating a detector or model rubric as a gate, run it against known accepted and rejected examples. It must surface known defects without receiving the user's wording as a hint. Reduce noisy detectors. Human acceptance remains an external label.

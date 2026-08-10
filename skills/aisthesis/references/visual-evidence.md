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

## Deterministic candidates

Useful measurements include DOM geometry, fixed-position tolerance, painted occlusion variants, CIEDE2000 long-boundary detection, repeated-motif candidates, changed-pixel ratio, SSIM, optical flow, entropy, edge density, physical viewport travel, image alpha/coverage, and selected responsive sources.

Metrics rank review targets. They do not establish visual quality.

## Four visual passes

1. **Object/overlap:** identity, clipping, duplication, masks, collisions, concealment.
2. **Palette/material:** temperature, value, saturation, texture, lighting, pixel scale, seams.
3. **Composition/hierarchy:** focal order, balance, negative space, grouping, landmark legibility, product/narrative coherence.
4. **Temporal/responsive:** dead travel, rushed beats, holds, reversals, transitions, cross-profile parity.

For every finding record observation, profile/frame/progress/region, confidence, owner candidate, causal hypothesis labelled separately, and acceptance condition. Inspect direct frames as well as overview and phase boards.

## Calibration

Before treating a detector or model rubric as a gate, run it against known accepted and rejected examples. It must surface known defects without receiving the user's wording as a hint. Reduce noisy detectors. Human acceptance remains an external label.

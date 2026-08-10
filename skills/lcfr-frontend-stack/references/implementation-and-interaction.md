# Implementation, interaction, and motion

## Build order

1. Semantic structure and content truth
2. Tokens, typography, containers, and primitives
3. Complete states and recovery paths
4. Responsive transformations
5. Interaction and motion
6. Visual polish and asset optimization

Preserve working infrastructure. Choose the smallest change surface that satisfies the contract. Add behavioral tests before claiming a fix.

## Interaction contract

Every control needs semantic purpose, keyboard operation, visible focus, touch target, disabled/loading behavior, error recovery, and parity across mouse, touch, and keyboard. Hover may enhance but cannot reveal required information alone.

## Motion contract

Motion explains state, continuity, spatial relationships, or hierarchy. Prefer transform and opacity. Avoid layout thrash and decorative loops without purpose. Define entry, hold, exit, interruption, route cleanup, and reduced-motion behavior.

### Native scroll first

- Do not intercept `wheel` or force `scrollTo` to repair pacing.
- Express authored state as a pure function of normalized progress when deterministic capture is needed.
- Measure physical travel in viewport heights, not percentages alone.
- Distinguish CSS capability fallback from reduced motion. A missing CSS scroll-timeline feature must not disable a working JavaScript driver.
- Exercise actual wheel input in Chromium and Firefox-derived engines.
- For reduced motion, remove long pinning and present essential content in ordinary flow; do not delete required narrative beats.

## Concealed transitions

A visibility swap is valid only when painted cover—not DOM opacity alone—conceals it. Record pre-swap, concealed-swap, trailing-reveal, and clear checkpoints. Alpha opacity does not prove visual continuity when RGB interiors contain flat voids. Inspect real pixels and keep the outgoing subject until cover is proven.

## Cleanup

Scope listeners, observers, animation contexts, media queries, timers, and routes. Verify teardown through navigation and remounting. Prevent duplicate semantic copies hidden only through opacity.

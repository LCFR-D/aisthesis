# Repeatable animation systems

Use this module when motion spans several scenes, routes, recurring characters, generated assets, or repeated production runs.

## Canonical contracts

Freeze before scaling production:

- **subjects:** proportions, silhouettes, variants, expressions and prohibited drift;
- **rig:** named parts, pivots, constraints, deformation limits and coordinate system;
- **scene:** logical dimensions, safe regions, depth planes, lighting and theme rules;
- **camera:** framing, movement axes, zoom limits and continuity rules;
- **state:** stable identifiers, allowed transitions and interruption behavior;
- **timeline:** beats, durations, easing, holds and audio synchronization;
- **rights:** source, creator, licence, model, prompt, consent and usage limits for every asset.

## Deterministic versus generative work

Use deterministic rendering for continuity-critical geometry, UI demonstrations, text, camera paths, compositing and acceptance frames. Use generative output for bounded texture, atmosphere or exploration only when variation is acceptable and provenance is recorded.

Generated frames never define the canonical rig by themselves. Promote approved output into source-controlled masters or regenerate from a locked recipe.

## State machine

For every state record:

- entry condition;
- initial frame;
- active loop or progression;
- exit condition;
- interruption and reversal behavior;
- reduced-motion/static equivalent;
- accessibility announcement if meaning changes;
- deterministic evidence checkpoints.

Avoid animation chains whose state exists only in completion callbacks. The current state must be recoverable after resize, route change, backgrounding or interrupted input.

## Camera and responsive composition

- Keep camera intent separate from asset dimensions.
- Define protected subjects and minimum visible ratios.
- Author portrait and ultrawide compositions where cropping would change meaning.
- Test short landscape viewports, browser chrome changes and dynamic safe areas.
- Do not scale text or controls as pixels inside a scene when semantic HTML can remain available.

## Double-render proof

1. Render the same version, inputs, seed, viewport, device scale and timeline twice.
2. Compare frame identities or pixel metrics at required checkpoints.
3. Explain tolerated nondeterminism before accepting it.
4. Compare state transitions, not just the final frame.
5. Store renderer, browser, font and asset versions with the evidence.

## Delivery

- Pause offscreen loops and when the document is hidden.
- Cap raster size and device-pixel ratio.
- Preload only the opening assets required for the first meaningful frame.
- Provide poster frames, no-motion reading order and failure fallbacks.
- Validate decoding, memory use, dropped frames and input latency on representative low-power hardware.

## Acceptance

A repeatable animation is accepted only when identity, composition, timing, state, responsive behavior, accessibility, performance, provenance and rights remain controlled across the required matrix.
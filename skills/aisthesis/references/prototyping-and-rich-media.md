# Prototyping, generated assets, and rich media

Use this reference when the task needs divergent concepts, a disposable prototype, generative visuals, canvas/WebGL, data graphics, branded illustration, or a portable design specification.

## Choose the artifact by the question

- **Static direction board:** compare type, palette, material, composition, imagery, and voice before implementation.
- **Throwaway HTML prototype:** test information architecture, responsive structure, interaction feel, or two to three materially different directions.
- **Live component preview:** prove real states and integration in the incumbent stack.
- **SVG or diagram:** explain architecture, flow, sequence, or relationships with inspectable vectors and text.
- **Canvas/p5.js/WebGL experiment:** validate generative behavior, shaders, particles, spatial interaction, or performance before production integration.
- **Text-first browser demo:** test hierarchy, pacing, and interaction when graphical assets would distract from the core idea.
- **Generated-image study:** explore approved art direction or produce a source candidate with explicit provenance and human selection.
- **Design specification:** encode tokens, themes, components, and state rules in a machine-readable or human-readable contract.

A prototype answers a bounded question. It is not production merely because it runs.

## Divergence before convergence

When direction is genuinely open, produce two or three variants that differ in structure, not just color:

- one conservative interpretation closest to incumbent truth;
- one recommended interpretation that sharpens the product-specific idea;
- one high-contrast alternative that tests the boundary of the brief.

Keep content and success criteria constant so the comparison is meaningful. Record what each variant is testing. Select or combine only after inspecting rendered evidence.

## Generated assets

Before generation, define:

- intended role and exact dimensions;
- subject, composition, camera/view, material, palette, lighting, and level of detail;
- text-safe, focal, transparent, cropped, or protected regions;
- desktop/mobile and light/dark relationships;
- prohibited content, trademarks, people, data, or unsupported product depiction;
- source model/tool, date, prompt lineage, selected output, and allowed use.

Treat output as a candidate. Inspect typography, hands/faces where relevant, seams, transparency, repetition, hidden artifacts, brand fit, and responsive crops. Keep only selected source files and derived production assets. Do not silently replace approved masters.

## Generative and interactive graphics

- Separate deterministic seeds and parameters from presentation.
- Give canvas and WebGL explicit dimensions and device-pixel-ratio budgets.
- Pause or reduce work offscreen and under reduced motion.
- Preserve keyboard, text, semantics, and fallback content in the DOM.
- Avoid continuous React/render-state updates for frame-by-frame values.
- Test resize, visibility changes, route teardown, low-power devices, and context loss.
- Record frame cost, memory, bundle size, and visual evidence before shipping.

Use p5.js, canvas, SVG, CSS, WebGL, or a rendering framework based on the artifact and incumbent stack, not habit.

## Diagrams and data graphics

Every visual encoding needs a reason and a textual equivalent. Define entities, relationships, sequence, units, scales, uncertainty, source, and interaction. Do not imply precision the data does not support. Ensure palettes remain distinguishable without color alone and labels survive narrow layouts.

## Design specifications

A reusable design spec should capture:

- semantic color and typography tokens;
- spacing, container, shape, border, elevation, and motion systems;
- responsive rules and breakpoint behavior;
- component anatomy, variants, states, content rules, and accessibility;
- theme inheritance and overrides;
- source assets and provenance;
- version, migration notes, tests, and examples.

Validate machine-readable specs against their schema and render representative components before claiming portability.

## Prototype graduation gate

Before moving prototype code into production:

1. restate the product question it answered;
2. replace mock data and invented claims with product truth;
3. map structure into the incumbent framework and system;
4. implement semantics, states, error/recovery, accessibility, localization, security, and analytics;
5. remove exploratory dependencies and dead variants;
6. add tests and release evidence;
7. independently review the exact candidate.

# Implementation, interaction, and motion

## Build order

1. Semantic structure, factual content, routes, and data contracts
2. Tokens, typography, containers, primitives, and system ownership
3. Complete states, validation, permissions, and recovery
4. Responsive transformations and asset selection
5. Interaction and motion
6. Visual polish, performance, and cleanup

Preserve working infrastructure. Choose the smallest change surface that satisfies the contract. Add behavioral tests before claiming a fix.

## State ownership

Keep state as local as its consequences. Separate server state, URL state, form state, local UI state, and continuous animation values.

- URLs own shareable navigation, filter, sort, tab, and search state when appropriate.
- The server or query layer owns remote truth, caching, invalidation, retries, and stale behavior.
- Forms own draft input and validation until submission changes remote truth.
- Local state owns transient disclosure and selection that need not survive navigation.
- Motion values, CSS custom properties, or animation timelines own continuous pointer and scroll values; do not drive them through render state each frame.

Avoid global state used only to bypass component design. Preserve browser history, deep links, refresh, and multi-tab expectations.

## Interaction contract

Every control defines:

- semantic purpose and accessible name;
- pointer, touch, and keyboard operation;
- visible focus and focus restoration;
- target size and coarse-pointer behavior;
- default, hover, focus, active, selected, disabled, loading, error, and success behavior where relevant;
- latency, cancellation, retry, undo, and interruption;
- behavior during navigation, remount, and reconnection.

Hover may enhance but cannot reveal required information alone. Disabled controls should not hide why the action is unavailable when that reason matters.

## Interaction feel

Polish is the consistency of small causal relationships:

- A press responds immediately without shifting surrounding layout.
- Focus appears immediately and does not animate into visibility.
- Menus and popovers originate from their trigger and return focus on close.
- Dragging preserves object ownership and supplies a keyboard alternative when the operation is essential.
- Optimistic updates expose rollback or undo when the action is reversible.
- Destructive actions state the affected object and scope, not generic danger language.
- Tooltips are delayed for pointer exploration but immediate for keyboard focus.
- Route and modal transitions maintain continuity without delaying access to the next task.

Use spring or easing curves to express material and distance, not as decoration. Fast frequent actions should feel direct; large spatial changes may take longer but remain interruptible.

## Motion contract

Motion communicates state, continuity, spatial relationships, hierarchy, or authored narrative. Define:

- trigger and information conveyed;
- property ownership;
- entry, hold, exit, reversal, and interruption;
- duration and easing family;
- concurrent-animation behavior;
- route cleanup and remount behavior;
- reduced-motion equivalent;
- performance budget and evidence.

Prefer transform and opacity. Animate layout only with a measured technique that preserves accessibility and performance. Remove decorative loops that do not serve the direction.

## Native scroll first

- Do not intercept `wheel`, force `scrollTo`, or replace native scrolling to repair pacing.
- Use sticky positioning, scroll-driven CSS, IntersectionObserver, or an isolated animation driver without taking input authority.
- Express authored state as a pure function of normalized progress when deterministic capture is needed.
- Measure physical travel in viewport heights, not percentages alone.
- Distinguish CSS capability fallback from reduced motion. A missing CSS scroll-timeline feature must not disable a working JavaScript driver.
- Exercise actual wheel input in Chromium and Firefox-derived engines.
- For reduced motion, remove long pinning and present essential content in ordinary flow; do not delete narrative beats.

Horizontal presentation may respond to vertical progress only when the content and brief justify it, the section remains keyboard/touch accessible, native page scrolling remains intact, and reduced motion receives ordinary flow.

## Concealed transitions

A visibility swap is valid only when painted cover, not DOM opacity alone, conceals it. Record pre-swap, concealed-swap, trailing-reveal, and clear checkpoints. Alpha opacity does not prove visual continuity when RGB interiors contain flat voids. Inspect real pixels and keep the outgoing subject until cover is proven.

## Rendering and framework boundaries

- Isolate client-only interaction from server-rendered structure.
- Clean up listeners, observers, timers, animation contexts, media queries, and subscriptions.
- Avoid hydration differences caused by viewport, time, randomness, or browser-only state.
- Reserve geometry for images, fonts, embeds, and asynchronous content.
- Virtualize only when measurement shows the list needs it; preserve semantics and focus.
- Keep canvas/WebGL as a progressive layer with a meaningful DOM alternative.
- Verify dependencies before import and use framework-native image, font, routing, and data primitives when they satisfy the contract.

## Cleanup gate

Navigate away and back, remount, resize, change theme, toggle reduced motion, suspend the network, and repeat the primary interaction. Confirm there are no duplicate listeners, hidden semantic copies, stale timers, orphaned focus, animation contention, or state leaks.

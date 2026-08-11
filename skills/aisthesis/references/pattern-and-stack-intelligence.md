# Pattern and stack intelligence

Use this reference to choose a neutral interaction pattern, map it to the host stack, and avoid importing somebody else's visual identity.

## Query keys

Search this file by surface, structure, interaction or stack. Combine one entry from each relevant column rather than treating a pattern as a template.

### Surface archetypes

| Surface | Primary pressure | Useful structures | Failure to avoid |
|---|---|---|---|
| Marketing | comprehension and trust | proposition spine, evidence band, comparison, decisive CTA | interchangeable hero plus decorative card grid |
| Portfolio | authorship and judgment | thesis, selected work, process evidence, reflective close | gallery with no reasoning or role clarity |
| Documentation | retrieval and orientation | persistent hierarchy, local TOC, search, runnable example, next step | walls of prose and dead-end pages |
| Editorial | reading rhythm and argument | strong deck, narrow measure, section markers, citations, pull evidence | oversized display type displacing the article |
| Dashboard | scan, compare and act | summary strip, filters, data view, exception queue, detail drawer | equal-weight cards and color-only status |
| Operational tool | throughput and error recovery | worklist, primary canvas, inspector, command path, activity history | hidden state, modal chains and irreversible bulk actions |
| Settings | confidence and reversibility | grouped sections, defaults, validation, impact preview, save state | unlabeled toggles and ambiguous scope |
| Onboarding | progressive commitment | value preview, minimum input, verification, first success | long mandatory tour before value |
| Commerce | evaluation and transaction | product evidence, variants, terms, cart state, recovery | urgency theater and layout shift around price |
| Data story | guided interpretation | narrative beats, annotated chart, source notes, static fallback | motion without a readable conclusion |
| Immersive | presence and exploration | controlled canvas, discoverable controls, fallback narrative | cursor traps, unreadable text and no reduced-motion path |

### Structural vocabulary

- **Spine:** one continuous argument with explicit evidence at each turn.
- **Workbench:** primary object plus tools, inspector and history.
- **Atlas:** navigable collection with overview, filters and detail.
- **Ledger:** dense comparable records with totals and exceptions.
- **Dialogue:** alternating prompt, response, status and correction.
- **Stage:** focused scene with controlled transitions and a static equivalent.
- **Split proof:** claim and inspectable artifact remain visible together.
- **Progressive disclosure:** essentials first; complexity opens in place.

A layout should have one dominant structure. Secondary structures may support it but must not make every section a new visual genre.

## Component choice rules

- Use a table when comparison across rows or columns matters; use cards for independent objects.
- Use tabs only for peer views of one object; use navigation for distinct destinations.
- Use a dialog for a bounded interruption; use a page or drawer for deep work.
- Use a tooltip for nonessential explanation; never hide required instructions in it.
- Use a toast for passive confirmation; use inline status for actions that can fail or need recovery.
- Use charts when shape or relationship is the message; use exact values when precision is the message.
- Use icons to reinforce known actions, not replace unfamiliar labels.

## Data visualization

1. State the decision or question the chart supports.
2. Select the smallest encoding that preserves comparisons.
3. Label units, timeframe, source and missing data.
4. Keep color semantic and redundant with labels, shape or position.
5. Provide a table or textual summary where accessibility or precision requires it.
6. Test zero, negative, extreme, sparse, loading and error data.

## Stack adapters

### React and Next.js

- Keep render output deterministic; avoid deriving state in effects when it can be computed.
- Preserve server/client boundaries and hydration equivalence.
- Use semantic routing and framework image/font primitives only when they preserve required behavior.
- Test suspense, route loading, error boundaries and back/forward restoration.

### Vue and Nuxt

- Keep reactive ownership explicit; avoid watchers that duplicate computed state.
- Verify server-rendered markup matches client state.
- Test route transitions, async component failures and retained view state.

### Svelte and SvelteKit

- Keep reactive statements bounded and lifecycle cleanup explicit.
- Verify load functions, form actions, navigation state and hydration.
- Prefer platform semantics over custom action abstractions for basic controls.

### Astro and content-led systems

- Default to static HTML; add islands only where interaction earns their cost.
- Verify content collections, generated routes, image output and no-JavaScript reading.

### Plain HTML, CSS and JavaScript

- Start with semantic HTML and native controls.
- Use progressive enhancement; the essential path should survive script delay or failure.
- Keep state transitions and cleanup explicit rather than relying on global listeners.

### Tailwind or utility CSS

- Centralize tokens and component variants; do not let arbitrary values become a hidden design system.
- Check generated class discovery, responsive ordering, dark mode and focus styles.

### CSS modules, CSS-in-JS or component styles

- Preserve cascade ownership, deterministic class generation and server rendering.
- Avoid runtime styling work for values that can be tokens or static CSS.

### Canvas, WebGL and shaders

- Keep semantic controls and an equivalent textual/static representation outside the canvas.
- Cap device-pixel ratio, pause offscreen work, handle context loss and respect reduced motion.

## Original pattern record

For a reusable pattern, capture:

- problem and surface;
- information hierarchy;
- semantic structure;
- states and transitions;
- responsive transformations;
- accessibility contract;
- performance budget;
- evidence from real use;
- conditions where the pattern should not be used.

Do not name the pattern after a company or preserve a recognizable branded composition.
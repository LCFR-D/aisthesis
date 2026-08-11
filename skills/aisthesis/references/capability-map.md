# Aisthesis capability map

Aisthesis is standalone. Every capability below is available inside this skill; none is a runtime dependency on another Agent Skill.

## Named LCFR layers

| Layer | Owns | Bundled location |
|---|---|---|
| Metis | Mode, scope, product truth, authority, provenance, evidence, stop conditions | `SKILL.md`, `methodology.md` |
| Taste and craft | Brief inference, direction, anti-template decisions, typography, composition, imagery, copy, final craft floor | `direction-and-taste.md`, `design-and-brand.md`, `typography-and-copy.md` |
| Kinetograph | Deterministic browser capture, authored progress, physical travel, geometry, real-wheel behavior, cross-engine evidence | `visual-evidence.md`, `tool-orchestration.md`, `scripts/playwright-evidence.mjs` |
| Aisthesis Judgment | Localized composition, material, hierarchy, continuity, pacing, and calibrated human acceptance | `visual-evidence.md`, repository Python package |

## Absorbed capability families

The names in this table identify the source capability family and make provenance legible. The public bundle uses independently written LCFR instructions rather than requiring or silently copying another skill.

| Capability family | What Aisthesis absorbs | Where |
|---|---|---|
| Impeccable | Production completeness, explicit surface modes, bounded polish, hardening, responsive adaptation, typography, color, layout, motion, delight, copy clarity, and live evidence | `SKILL.md`, `direction-and-taste.md`, `systems-and-product-ui.md` |
| Taste | Brief inference, audience and vibe reading, direction controls, anti-default discipline, pattern vocabulary, imagery expectations, and pre-flight checks | `direction-and-taste.md`, `design-and-brand.md` |
| Hallmark | Structural variety, incumbent pre-flight, study without pixel copying, token discipline, responsive non-negotiables, state completeness, and anti-generated fingerprints | `direction-and-taste.md`, `systems-and-product-ui.md` |
| Frontend Design | Subject-grounded visual worlds, a clear point of view, justified aesthetic risk, and memorable composition | `direction-and-taste.md` |
| UI/UX pattern intelligence | Surface classification, neutral structural patterns, stack-aware component choices, charts, icons, design-system routing, UX heuristics, and implementation checks | `pattern-and-stack-intelligence.md`, `systems-and-product-ui.md` |
| Interaction craft | Motion purpose, timing, easing, interruption, hover/focus/active feel, optimistic feedback, direct manipulation, and micro-behavior polish | `implementation-and-interaction.md`, `repeatable-animation-systems.md` |
| Popular web-pattern study | Pattern naming and reference comparison without turning a brand into a visual copy | `direction-and-taste.md`, `design-and-brand.md` |
| Sketch and HTML prototyping | Structurally different concepts, bounded questions, comparison evidence, and safe graduation into production | `prototyping-and-rich-media.md` |
| Generative browser work | p5.js, canvas, SVG, WebGL, text-first demos, deterministic seeds, semantic fallbacks, performance, and teardown | `prototyping-and-rich-media.md` |
| Generated media | Art direction, source locking, responsive masters, human selection, provenance, and production derivation | `prototyping-and-rich-media.md`, `design-and-brand.md` |
| Portable design specifications | Semantic tokens, themes, components, state rules, schema validation, contrast pairs, and migration evidence | `prototyping-and-rich-media.md`, `systems-and-product-ui.md`, `templates/design-system.yaml` |
| Brand System Development | Source truth, reusable grammar, semantic tokens, geometry, provenance, and consistency | `design-and-brand.md` |
| Responsive Generated Brand Art | Breakpoint masters, paired modes, focal protection, text-safe regions, and selected-source verification | `design-and-brand.md`, `responsive-and-accessibility.md` |
| Scrolltelling QA | Beat architecture, native scrolling, fallbacks, responsive pacing, and real-wheel verification | `implementation-and-interaction.md`, `visual-evidence.md` |
| Accessibility | WCAG 2.2 AA traceability, semantics, keyboard, focus, zoom/reflow, touch, contrast, forced colors, automated candidates, and assistive-technology evidence | `responsive-and-accessibility.md`, `templates/accessibility-audit.md` |
| Performance | Core Web Vitals, asset delivery, runtime cost, bundle discipline, and visual-fidelity protection | `release-contract.md` |
| Dogfood | Exploratory charters, primary journeys, failure and recovery, history navigation, touch, keyboard, severity, reproducibility, and visitor-perspective defects | `release-contract.md`, `templates/issue-ledger.md` |
| Code and security review | Logic, injection boundaries, dependencies, privacy, maintainability, regression, and release readiness | `release-contract.md` |
| Tool and function orchestration | Project-pinned Playwright, host browser tools, specialist adapters, project scripts, and custom functions under one verified authority and evidence contract | `tool-orchestration.md`, `scripts/playwright-evidence.mjs` |

## Coverage by surface

Aisthesis supports:

- marketing and campaign pages;
- portfolios, editorial and documentation;
- product shells, dashboards, settings, forms, onboarding, empty states, and dense operational UI;
- design systems, tokens, component libraries, and isolated components;
- responsive art, generated imagery, rich media, motion, scroll narratives, canvas and WebGL surfaces;
- audits, refinements, redesigns, design studies, performance work, and release verification.

Framework guidance is adaptive. Preserve the incumbent stack unless the task explicitly includes a migration. Use official design-system packages where the product contract requires them, but verify the package, version, licence, and project fit before importing.

## Provenance boundary

Aisthesis does not redistribute third-party skill prose, paid templates, protected examples, or hidden assets. General methods are independently expressed and governed by the hierarchy in `SKILL.md`. Named products and projects remain the property of their owners. See `external-capability-ledger.md`, `provenance.md`, and the repository's third-party notices.

---
name: aisthesis
description: Use for any frontend task from product truth and design direction through implementation, visual judgment, and verified release.
license: MIT
compatibility: Works with Agent Skills clients; execution needs filesystem, shell, browser automation, and screenshot-inspection capabilities.
metadata:
  author: LCFR
  version: 1.0.0
  tags: frontend, design, product-ui, responsive, accessibility, motion, visual-qa, performance, release
---

# Aisthesis

Aisthesis is LCFR's complete portable frontend operating system. It is one standalone skill for designing, building, inspecting, repairing, and releasing any web interface without installing a second design skill.

The system combines four named layers:

- **Metis** governs product truth, mode, scope, authority, evidence, and stopping conditions.
- **Taste and craft** choose a subject-specific direction, prevent template-shaped output, and enforce production completeness.
- **Kinetograph** turns interaction, scrolling, motion, geometry, and browser state into reproducible frames and physical evidence.
- **Aisthesis Judgment** interprets rendered evidence without reducing taste to a score or overruling human acceptance.

It also contains product-UI architecture, component and design-system methods, responsive art direction, accessibility, performance, dogfooding, security review, and release engineering. External design tools may still be consulted, but none is required.

## Non-negotiable contract

1. The approved brief and factual product evidence outrank style advice.
2. Choose a mode before editing: **Greenfield**, **Refinement**, **Redesign**, **Audit**, or **Study**. "Improve", "polish", and "scan" default to Refinement.
3. Never invent product claims, metrics, users, testimonials, integrations, or proof.
4. Preserve native platform behavior. Do not hijack the wheel, force scrolling, hide focus, disable zoom, or add motion without a communicative job.
5. Build every applicable state, not only the successful screenshot.
6. Keep deterministic measurements, model observations, and human acceptance separate.
7. A build is incomplete until it runs, representative states are exercised, rendered evidence is inspected, and release claims can be reproduced.
8. User rejection outranks every passing metric. No automated system may infer acceptance.

## Authority order

Resolve conflicts in this order:

1. explicit user brief and approved references;
2. factual product and source evidence;
3. safety, accessibility, privacy, legal, and licence constraints;
4. approved brand, design-system, content, and interaction contracts;
5. acceptance criteria;
6. measured runtime or user evidence;
7. this operating system;
8. optional specialist opinion;
9. generic convention or trend.

Record unresolved conflicts. Never silently let a lower authority replace a higher one.

## Route the request

Choose the smallest route that owns the work:

| Request | Route | Required reference |
|---|---|---|
| New page, app, flow, or component | **Build** | `direction-and-taste.md`, `pattern-and-stack-intelligence.md`, then applicable implementation references |
| Plan UX/UI before code | **Shape** | `methodology.md`, `systems-and-product-ui.md`, `typography-and-copy.md` |
| Improve an existing surface | **Refine** | incumbent capture, then the narrow owning reference |
| Replace the visual or interaction world | **Redesign** | `direction-and-taste.md`; preserve product truth and route contracts |
| Diagnose without editing | **Audit** | `visual-evidence.md`, `release-contract.md` |
| Learn from a URL or screenshot | **Study** | `direction-and-taste.md`; extract principles and structure, never pixels |
| Compare concepts or prove rich media | **Prototype** | `prototyping-and-rich-media.md`; keep the question and graduation gate explicit |
| Final fit-and-finish | **Polish** | `direction-and-taste.md`, `implementation-and-interaction.md` |
| Errors, edge cases, i18n, recovery | **Harden** | `systems-and-product-ui.md`, `responsive-and-accessibility.md` |
| Responsive correction | **Adapt** | `responsive-and-accessibility.md` |
| Motion or scroll narrative | **Animate** | `implementation-and-interaction.md`, `repeatable-animation-systems.md`, `visual-evidence.md` |
| Performance work | **Optimize** | `release-contract.md` |
| Extract tokens/components | **Extract** | `design-and-brand.md`, `systems-and-product-ui.md`, `templates/design-system.yaml` |
| Ship | **Release** | `release-contract.md` and all required evidence |

Do not run every lens on every task. The bundle is complete because the right capability is locally available, not because every capability fires at once.

## Operating loop

### 1. Frame the job with Metis

Read repository instructions, routes, content, tests, tokens, assets, analytics contracts, deployment configuration, and live behavior. Select one mode. Complete `templates/brief.md` and state:

- audience and the job they must complete;
- product truth and claim boundaries;
- what must be preserved, may change, and is out of scope;
- required states, platforms, breakpoints, and evidence;
- provenance and rights for references, code, fonts, assets, and copy.

**Gate:** another implementer could explain both the intended outcome and the forbidden changes.

### 2. Capture the incumbent

For existing work, run the current build and tests before editing. Capture representative desktop, intermediate, mobile, theme, keyboard, touch, zoom, and reduced-motion states. Record console, network, accessibility, overflow, and performance defects separately from harness failures.

**Gate:** the baseline is reproducible and every failure has a concrete payload.

### 3. Choose direction with Taste

Read `references/direction-and-taste.md`, `references/design-and-brand.md`, and `references/typography-and-copy.md`. For a new or structurally weak surface, also query `references/pattern-and-stack-intelligence.md` by surface, structure and host stack.

Infer the surface mode: **Persuade**, **Operate**, **Read**, or **Experience**. Define:

- one subject-specific structural idea;
- one justified aesthetic risk;
- an explicit anti-template list;
- typography, palette, material, spacing, imagery, motion, and content voice;
- the page or flow architecture;
- what is deliberately quiet.

Do not default to a fashionable visual family. Do not replace an approved identity to demonstrate design skill. Complete `templates/design-direction.md`.

**Gate:** the direction is specific enough to reject an off-direction implementation.

### 4. Define the system and complete states

Read `references/systems-and-product-ui.md` and complete `templates/system-contract.md`. For reusable systems, also complete `templates/design-system.yaml`; keep token references acyclic and validate required contrast pairs.

Define semantic tokens, containers, type roles, action hierarchy, component ownership, data density, interaction grammar, motion grammar, and responsive transformations. Model every applicable state: loading, skeleton, empty, partial, stale, offline, unauthorized, error, success, hover, focus, active, disabled, selected, pending, destructive confirmation, undo, and recovery.

Use the incumbent stack unless change is justified. Verify dependencies before importing them. Prefer semantic HTML and native behavior over a custom abstraction.

### 5. Build the smallest valid change

Map requirements to files, components, assets, tests, and rollback. Add executable assertions before claiming behavior. Build foundations before responsive behavior, interaction, motion, and polish. For risky interactions, prove a thin tracer path before broad implementation.

Read `references/implementation-and-interaction.md` before changing scrolling, motion, state ownership, focus, gestures, or component architecture.

For recurring scenes, characters, camera systems, generated animation or multi-run production, read `references/repeatable-animation-systems.md` and complete `templates/motion-contract.yaml`.

### 6. Integrate visual systems and assets

When brand art, generated imagery, responsive crops, or multiple themes are involved:

- lock authoritative source geometry and provenance;
- use dedicated responsive compositions when one crop cannot preserve hierarchy;
- derive paired themes from shared geometry when appropriate;
- protect focal landmarks and text-safe regions;
- verify browser-selected assets and rendered pixels;
- use real product evidence or clearly labelled placeholders, never fabricated proof.

Never regenerate approved art before proving whether the defect belongs to source pixels, CSS geometry, runtime overlays, or composition.

### 7. Verify responsiveness and accessibility

Read `references/responsive-and-accessibility.md`. Exercise the required matrix, including narrow, mobile, intermediate, desktop, and wide states where relevant. Test keyboard, focus order, screen-reader semantics, touch targets, zoom, contrast, forced colors where relevant, reduced motion, dark/light themes, localization expansion, and horizontal overflow.

Complete `templates/verification-matrix.md` and `templates/accessibility-audit.md` for material or public work.

### 8. Capture with Kinetograph

Read `references/visual-evidence.md`. Freeze the candidate. Exercise real browser behavior across required engines. For scroll-led work, test actual wheel input in Chromium and Firefox-derived engines plus deterministic progress checkpoints.

Capture exact viewport frames, DOM geometry, selected resources, physical travel, interaction state, console and network output. Deterministic checks localize risk; they do not establish taste.

### 9. Judge with Aisthesis

Inspect full-resolution evidence in separate passes:

1. identity, overlap, clipping, duplication, concealment, and state correctness;
2. palette, material, texture, lighting, source boundaries, and asset continuity;
3. hierarchy, balance, grouping, density, negative space, and narrative coherence;
4. temporal pacing, dead travel, rushed beats, holds, reversals, and responsive parity;
5. copy clarity, factual support, action clarity, and trust.

Every finding cites profile, frame or state, region, confidence, visible observation, suspected owner, separately labelled causal hypothesis, and acceptance condition. Detectors create candidates, never aesthetic scores.

### 10. Dogfood, optimize, and review

Exercise primary journeys as a visitor, including keyboard, touch, refresh, deep-link, back/forward, failure, and recovery. Measure loading and runtime separately. Review security, privacy, accessibility, maintainability, dependency risk, content integrity, and regression scope.

Use the severity and reproduction contract in `references/release-contract.md`; record findings in `templates/issue-ledger.md`. A clean initial render is not a dogfood pass: inspect console, network, focus and state after meaningful interactions.

Protect visual fidelity while optimizing. A faster but visibly degraded or less usable interface is not a passing optimization.

### 11. Release with evidence

Read `references/release-contract.md`. Use an isolated preview before production when deployment exists. Rerun the full required matrix against the exact preview. Any code or asset change invalidates earlier evidence.

Complete `templates/release-evidence.md`, run independent review for material releases, deploy only the frozen candidate, then read back production URLs, assets, settings, and telemetry.

**Gate:** an independent reviewer can reproduce every success claim from commands, URLs, hashes, screenshots, and artifacts.

## Craft floor

Every delivered frontend must satisfy these constraints unless the brief explicitly requires a different choice:

- The subject, audience, and product create the visual world; the model's defaults do not.
- Hierarchy is legible without decorative labels on every section.
- Components exist because they encode a relationship or behavior, not because cards are convenient.
- Typography has explicit roles, measure, line-height, wrapping, and fallback behavior.
- Color is tokenized, contrast-safe, and coherent across themes.
- Layouts have intentional rhythm and do not repeat one section archetype mechanically.
- Motion communicates hierarchy, continuity, feedback, or state. Otherwise remove it.
- Copy is concrete, grammatical, concise, and free of invented precision.
- Real imagery, product captures, or labelled placeholders replace fake browser chrome and decorative pseudo-products.
- Mobile behavior is designed per component rather than assumed from framework defaults.
- Every interaction has focus, keyboard, touch, reduced-motion, error, and recovery behavior where applicable.
- The exact rendered result is inspected before handoff.

## Bounded execution

Use one batched audit, one consolidated fix pass, and one confirmation pass. Do not enter perpetual visual tweaking. Stop when the contract passes or when a real blocker is documented with owner, evidence, and next decision.

## Capability map

`references/capability-map.md` records the operating layers. `references/external-capability-ledger.md` records every reviewed method, observed provenance, capability absorbed, and clean-room reuse decision. They are provenance maps, not runtime dependency lists.

## Completion checklist

- [ ] Mode, scope, preservation boundary, authority order, and claims recorded
- [ ] External influences and assets have provenance and reuse decisions
- [ ] Baseline build/tests and representative incumbent evidence captured
- [ ] Direction, architecture, system contract, and complete states implemented
- [ ] Required responsive, theme, localization, keyboard, touch, zoom, and reduced-motion profiles covered
- [ ] Chromium and Firefox-derived native behavior exercised for high-risk interaction or scroll work
- [ ] Console, network, overflow, accessibility, security, and performance gates passed
- [ ] Full-resolution evidence inspected through separate Aisthesis passes
- [ ] Preview and production parity read back where deployment exists
- [ ] Release evidence identifies commands, artifacts, URLs, hashes, limitations, and human acceptance status

## Pitfalls

- Smuggling a redesign into refinement
- Loading every lens instead of routing one question
- Copying a reference instead of extracting a general principle
- Treating screenshots, scores, or model critique as human acceptance
- Desktop-and-one-phone testing
- Polishing the happy path while recovery states are absent
- Hidden responsive assets still downloading
- Scroll interception used to hide pacing defects
- Full-page screenshots used to judge sticky states
- Regenerating source art to fix a runtime-overlay defect
- Reporting implementation, deployment, accessibility, or performance without read-back evidence

---
name: lcfr-frontend-stack
description: Use for complete evidence-led frontend delivery from brief to verified release.
license: MIT
compatibility: Works with Agent Skills clients; execution requires filesystem, shell, browser automation, and screenshot inspection capabilities.
metadata:
  author: LCFR
  version: 1.0.0
  tags:
    - frontend
    - design-systems
    - responsive
    - accessibility
    - visual-qa
    - performance
    - release
---

# LCFR Frontend Stack

One standalone operating system for frontend design, implementation, visual judgment, and verified release. It combines LCFR's Metis governance, brand-system methods, responsive art direction, scroll and interaction QA, deterministic capture, Aisthesis judgment, accessibility, performance, dogfooding, and release evidence without requiring another skill.

## Non-negotiable contract

1. Product truth and the approved brief outrank style advice.
2. Choose **Greenfield**, **Refinement**, **Redesign**, **Audit**, or **Study** before editing. "Improve" defaults to Refinement.
3. Preserve evidence boundaries: deterministic measurements, multimodal observations, and human acceptance are different things.
4. Use native platform behavior by default. Never add scroll hijacking, forced wheel interception, inaccessible motion, or decorative complexity to satisfy a screenshot.
5. A build is not complete until the artifact runs, required states are exercised, rendered evidence is inspected, and release claims are reproducible.
6. User rejection outranks a passing metric. No automated system may infer human acceptance.

## Authority order

Resolve conflicts in this order:

1. explicit user brief and approved references;
2. factual product/source evidence;
3. safety, accessibility, privacy, legal, and licence constraints;
4. approved brand and interaction contracts;
5. task acceptance criteria;
6. measured user or runtime evidence;
7. this skill's workflow and templates;
8. optional specialist opinions;
9. generic convention or trend.

Record unresolved conflicts. Never silently let a lower authority replace a higher one.

## Operating loop

### 1. Frame the job

- Read repository instructions, routes, content, tests, tokens, assets, and live behavior.
- Select one mode and state what must be preserved, may change, and is out of scope.
- Complete `templates/brief.md`.
- Inventory every external influence as principle, pattern, token, asset, code, or protected expression. Unknown provenance blocks copying, not original synthesis.

**Gate:** audience, page job, product truth, constraints, non-goals, claims, and acceptance evidence are explicit.

### 2. Capture the incumbent

For an existing interface, run its build and tests before editing. Capture the current desktop, mobile, intermediate-width, theme, keyboard, touch, and reduced-motion states. Record console, network, accessibility, overflow, and performance failures separately from harness failures.

**Gate:** the baseline is reproducible and every failure has a concrete payload.

### 3. Define direction and architecture

Read `references/design-and-brand.md`. Define:

- one structural idea tied to the subject;
- one justified aesthetic risk;
- explicit anti-template constraints;
- route, hierarchy, state, and recovery architecture;
- semantic tokens, typography, spacing, containers, action hierarchy, motion grammar, and responsive transformations.

Complete `templates/system-contract.md`. A direction must be specific enough that another implementer can reject an off-direction choice.

### 4. Plan the smallest valid change

Map requirements to files, components, assets, tests, and rollback. Build foundations before responsive behavior, interaction, motion, and polish. Add executable assertions before claiming behavior. For risky interactions, prove a thin tracer path before broad implementation.

Read `references/implementation-and-interaction.md` before changing motion, scrolling, state, or component architecture.

### 5. Build complete states

Implement every applicable state: loading, empty, partial, error, offline, unauthorized, success, focus, hover, active, disabled, destructive confirmation, and recovery. Preserve semantic HTML, keyboard operation, touch targets, focus visibility, zoom, reduced motion, and contrast as release requirements rather than aesthetic options.

Read `references/responsive-and-accessibility.md` and complete the state section of `templates/verification-matrix.md`.

### 6. Create and integrate visual systems

When brand art, generated imagery, or multiple modes are involved:

- lock authoritative source geometry and provenance;
- use dedicated responsive compositions when one crop cannot preserve hierarchy;
- derive paired themes from shared geometry;
- protect focal landmarks and text-safe regions;
- deliver one responsive image candidate per context rather than downloading hidden masters;
- verify browser-selected assets and rendered pixels.

Never regenerate approved art before proving whether the defect belongs to source pixels, CSS geometry, runtime overlays, or composition.

### 7. Run deterministic QA

Freeze the candidate. Exercise real browser behavior across the required matrix. For scroll-led work, test actual wheel input in Chromium and Firefox-derived engines as well as deterministic progress checkpoints. Capture exact viewport screenshots, DOM geometry, resource failures, console errors, accessibility results, selected image sources, horizontal overflow, and performance evidence.

Read `references/visual-evidence.md`. Deterministic checks localize risk; they do not establish taste.

### 8. Run Aisthesis judgment

Inspect full-resolution frames in separate passes:

1. object identity, overlap, clipping, duplication, and concealment;
2. palette, material, texture, lighting, and source-boundary continuity;
3. hierarchy, balance, negative space, grouping, and narrative coherence;
4. temporal pacing, dead travel, rushed beats, holds, reversals, and responsive parity.

Every finding cites profile, frame, progress, region, confidence, visible observation, suspected owner, separately labelled causal hypothesis, and acceptance condition. Use Aisthesis detectors for candidates; never turn their outputs into an aesthetic score.

### 9. Dogfood and performance

Exercise primary journeys as a visitor, including keyboard, touch, refresh, back/forward, failure, and recovery paths. Then measure loading and runtime separately. Protect responsive-art fidelity while improving delivery; a lighter but visibly degraded hero is not a valid optimization.

### 10. Release with evidence

Read `references/release-contract.md`. Use an isolated preview before production when deployment exists. Rerun the full required matrix against the exact preview. Any code or asset change invalidates earlier evidence. Complete `templates/release-evidence.md`, run independent review for material releases, deploy only the frozen candidate, then read back the production URL/assets/settings.

**Gate:** an independent reviewer can reproduce every success claim from commands, URLs, hashes, and artifacts.

## Bounded execution

Use one batched audit, one consolidated fix pass, and one confirmation pass. Do not enter perpetual visual tweaking. Stop when the contract passes or when a real blocker is documented with owner, evidence, and next decision.

## Role map

This single skill contains the full workflow. `references/skill-map.md` records how the original LCFR specialist roles were absorbed and where optional external lenses may contribute without becoming authorities.

## Completion checklist

- [ ] Mode, scope, preservation boundary, and authority order recorded
- [ ] Product claims and external influences have provenance
- [ ] Baseline build/tests and representative incumbent evidence captured
- [ ] Direction, architecture, system contract, and complete states implemented
- [ ] 320, 375, 414, 768, 1280, and wide profiles covered when relevant
- [ ] Themes, keyboard, touch, focus, zoom, and reduced motion verified
- [ ] Chromium and Firefox-derived native behavior exercised for high-risk interaction/scroll work
- [ ] Console, network, overflow, accessibility, and performance gates passed
- [ ] Full-resolution visual evidence inspected through four separate Aisthesis passes
- [ ] Preview and production parity read back where deployment exists
- [ ] Release evidence identifies commands, artifacts, URLs, hashes, limitations, and human acceptance status

## Pitfalls

- Smuggling a redesign into a refinement
- Copying a reference instead of extracting a general principle
- Loading many specialists without one decision owner
- Treating screenshots, scores, or model critique as human acceptance
- Desktop-and-one-phone testing
- Polishing the happy path while recovery states are absent
- Hidden responsive images still downloading
- CSS capability fallbacks disabling JavaScript behavior that still works
- Direct scroll listeners or wheel interception used to hide pacing defects
- Full-page screenshots used to judge sticky states
- Regenerating source art to fix a runtime overlay defect
- Reporting implementation, deployment, or accessibility without read-back evidence

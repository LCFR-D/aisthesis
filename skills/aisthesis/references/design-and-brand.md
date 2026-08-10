# Design direction, systems, and responsive art

## Direction contract

Write one sentence for each:

- **Subject truth:** materials, language, domain, and audience the interface must embody.
- **Structural idea:** the memorable organizing device, tied to content rather than trend.
- **Aesthetic risk:** one deliberate departure that earns attention without harming use.
- **Anti-template constraints:** patterns that would make the product generic or misleading.
- **Preservation boundary:** visual, content, and interaction elements that cannot drift.

Avoid aesthetic labels without observable rules. “Editorial” is insufficient; define hierarchy, rhythm, density, contrast, and interaction behavior.

## System contract

Define semantic—not palette-number—tokens for background, surface, text, muted text, borders, actions, focus, status, and decoration. Define typography roles, spacing rhythm, container logic, action hierarchy, component ownership, responsive transformations, motion grammar, and state behavior.

Repeated decisions get one source of truth. Exceptions are named and justified. Prefer a small composable primitive set over one-off card variants.

## Brand and generated-art rules

1. Designate the authoritative source and checksum when practical.
2. List immutable geometry, motifs, contact points, palette roles, lighting, pixel/texture scale, and text-safe regions.
3. Treat generated outputs as proposals until integrated browser captures pass visual review.
4. Generate or approve one dominant geometry, then derive paired modes from it.
5. Create dedicated portrait or ultrawide masters when cropping or scaling loses identity.
6. Separate scene context: opening master, transition atmosphere, product/feature world, and decorative foreground should not share one global overlay.
7. Protect landmarks with normalized regions and assert them after runtime overlays.
8. Store dimensions, source hashes, prompts or transformation steps, and output hashes.

## Responsive image delivery

Use one responsive `<picture>` candidate per visual role. Provide width/DPR variants only after native-size inspection. Media-gate ultrawide continuations. Hidden sibling `<img>` elements may still download. Verify `currentSrc`, transfer entries, intrinsic dimensions, rendered bounds, and crop at each breakpoint.

Do not use `image-rendering: pixelated` on generated pixel art unless browser comparison proves it improves fidelity. Do not shrink an opaque master into a floating rectangle if a native crop preserves the visual world better.

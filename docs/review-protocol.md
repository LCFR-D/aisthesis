# Review protocol

Aisthesis keeps three evidence classes separate.

## 1. Deterministic evidence

Record browser, viewport, state, frame, normalized progress, geometry, network failures and detector output. Measurements can localize a candidate. They cannot decide whether the design is good.

## 2. Multimodal review

Run separate passes for object overlap, palette and material continuity, composition and hierarchy, and temporal or responsive behavior. Every finding must name the profile, frame, progress and visible region. Keep the visible observation separate from the suspected implementation cause.

## 3. Human calibration

Keep accepted and rejected examples as labelled calibration evidence. Human rejection overrides a passing metric or model opinion. Machine outputs must not rewrite the acceptance history.

## Finding schema

```json
{
  "profile": "desktop-night",
  "frame": 24,
  "progress": 0.4,
  "region": [0.0, 0.55, 1.0, 0.08],
  "observation": "A hard horizontal palette boundary crosses most of the viewport.",
  "confidence": 0.94,
  "ownerHypothesis": ".cloud-curtain",
  "acceptanceCondition": "No long source boundary remains visible at equivalent progress."
}
```

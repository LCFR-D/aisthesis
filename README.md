# Aisthesis

Aisthesis is an evidence-led visual judgment layer for rendered interfaces. It helps teams find the failures that pass ordinary frontend tests: pasted imagery, hard source seams, repeated wallpaper motifs, dead scroll distance, weak hierarchy and responsive scenes that technically fit but do not hold together.

It does not produce an "aesthetic score." Aisthesis keeps three kinds of evidence separate:

1. deterministic browser and image measurements;
2. localized multimodal critique;
3. explicit human acceptance or rejection.

The name comes from the Greek *aisthesis*: perception.

## Why

A page can pass accessibility, geometry and screenshot assertions while still looking wrong. A smooth animation can still be dull. Four visible product landmarks can still feel pasted together. One scalar hides the evidence needed to fix those problems.

Aisthesis turns visual review into a traceable process. Measurements stay measurements. Model observations cite frames and regions. Human judgment remains authoritative.

## Included in 0.1

- CIEDE2000 detection for long horizontal palette boundaries;
- spatial self-similarity candidates for repeated imagery;
- physical viewport-travel budgets for authored phases;
- causal clustering for repeated detector hits;
- a CLI for inspecting frames and checking phase pacing;
- a review protocol for localized multimodal findings and human calibration.

## Install

```bash
python -m pip install -e .
```

Python 3.11 or newer is required.

## Inspect a rendered frame

```bash
aisthesis inspect frame.png --output findings.json
```

The result reports seam and repetition candidates. It does not claim the frame is good or bad.

## Check physical pacing

```bash
aisthesis pace \
  --profile desktop-night \
  --travel 3420 \
  --viewport-height 900 \
  --start 0.25 \
  --end 0.70 \
  --maximum 1.40
```

This measures the phase in viewport heights. Reduced-motion profiles can be excluded from animated pacing budgets with `--reduced-motion`.

## Python API

```python
from PIL import Image
import numpy as np
from aisthesis import detect_horizontal_seams, repetition_score

frame = np.asarray(Image.open("frame.png").convert("RGB"))
seams = detect_horizontal_seams(frame)
repetition = repetition_score(frame)
```

## Review boundary

Aisthesis can establish where a long palette boundary appears, whether a motif repeats, and how much physical scroll a phase consumes. It cannot establish taste, intent or acceptance from those measurements.

Use `docs/review-protocol.md` to run separate overlap, palette, composition and temporal passes. Every finding should cite a profile, frame, normalized progress and region. Record the suspected owner separately from the visible observation.

## Relationship to Kinetograph

Aisthesis began as the visual judgment layer above Kinetograph, LCFR's deterministic scroll-narrative capture system. Kinetograph establishes what rendered, where and when. Aisthesis combines that evidence with localized visual review and human calibration. The Python API also works independently on image arrays and phase metadata.

## Test

```bash
python -m pip install -e . pytest
pytest -q
```

## Status

Version 0.1 is an early public release. The deterministic detectors are useful now, but they produce candidates rather than verdicts. Planned work includes a stable finding schema, DOM-to-pixel ownership maps, optional semantic-mask adapters and a calibration corpus.

## Principles

- Human rejection outranks a passing metric.
- A model observation is not an implementation cause.
- Exact frames are evidence; sparse contact sheets are summaries.
- Visual quality should not collapse into one score.
- Public examples must not contain private product evidence or customer data.

## License

MIT. See [LICENSE](LICENSE).

## Community and security

- [Contributing](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security policy and private reporting](SECURITY.md)

Aisthesis was developed at [LCFR](https://lcfr.xyz).

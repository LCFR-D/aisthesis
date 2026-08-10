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
- temporal clustering for adjacent detector hits;
- a CLI for inspecting frames and checking phase pacing;
- a review protocol for localized multimodal findings and human calibration.

## LCFR Frontend Stack skill

The repository also ships **one standalone Agent Skill for LCFR's complete frontend workflow**: [`lcfr-frontend-stack`](skills/lcfr-frontend-stack/SKILL.md).

It consolidates Metis governance, brand and responsive-art direction, interaction and native-scroll engineering, deterministic browser QA, Aisthesis visual judgment, accessibility, performance, dogfooding, independent review and verified release. The archive has no dependency on LCFR's private workspaces or separately installed design skills.

### Install the skill

Download the immutable `frontend-stack-v1.0.0` release assets:

```bash
curl -LO https://github.com/LCFR-D/aisthesis/releases/download/frontend-stack-v1.0.0/lcfr-frontend-stack-1.0.0.zip
curl -LO https://github.com/LCFR-D/aisthesis/releases/download/frontend-stack-v1.0.0/lcfr-frontend-stack-1.0.0.zip.sha256
sha256sum -c lcfr-frontend-stack-1.0.0.zip.sha256
unzip lcfr-frontend-stack-1.0.0.zip -d <your-agent-skills-directory>
```

Use the user or project skills directory recognized by your Agent Skills-compatible client. The extracted directory is self-contained and starts at `lcfr-frontend-stack/SKILL.md`. Source, templates, provenance and deterministic packaging tests remain visible in this repository.

Trigger it with a request such as: `Use lcfr-frontend-stack to take this interface from brief through a verified release.`

### Validate or build the skill archive

```bash
uv sync --locked --dev
uv run python -m scripts.validate_skill
uv run python -m scripts.build_skill_release --output dist
```

The builder creates a deterministic ZIP, a SHA-256 checksum and an internal file manifest.

## Install the Aisthesis package

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
- [Frontend-stack changelog](CHANGELOG.md)
- [Skill provenance](provenance.toml)
- [Third-party notices](THIRD_PARTY_NOTICES.md)

Aisthesis was developed at [LCFR](https://lcfr.xyz).

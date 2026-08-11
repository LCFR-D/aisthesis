# Aisthesis

Aisthesis is LCFR's complete portable frontend operating system: one repository and one standalone Agent Skill for taking any web interface from product truth and design direction through implementation, deterministic browser evidence, visual judgment, and verified release.

The name comes from the Greek *aisthesis*: perception.

## One bundled frontend system

Aisthesis combines:

- **Metis** for mode, scope, product truth, authority, provenance, and release governance;
- **Taste and craft** for brief inference, subject-specific direction, structural variety, anti-template constraints, typography, composition, imagery, copy, and bounded polish;
- **Kinetograph** for deterministic browser capture, authored progress, physical pacing, geometry, native input, and cross-engine evidence, including a portable project-resolved Playwright adapter;
- **Aisthesis Judgment** for localized composition, material, hierarchy, continuity, and temporal review while keeping human acceptance authoritative;
- product-UI architecture, complete states, forms, dashboards, dense interfaces, design systems, tokens, components, responsive art, accessibility, performance, dogfooding, security review, and release engineering.

It absorbs the functional coverage of LCFR's full frontend stack, including Impeccable, Taste, Hallmark, Frontend Design, UI/UX pattern intelligence, interaction craft, brand-system development, responsive generated art, scrolltelling QA, performance, dogfooding, and code review. The public instructions are independently written and provenance-safe. No separately installed design skill is required.

The extracted skill is standalone procedural guidance with its own templates, schemas, tool-orchestration contract, and portable Playwright evidence adapter. It adapts to verified host tools and custom functions; the repository's Python judgment toolkit and external specialist CLIs remain optional accelerators, not runtime requirements.

## Agent Skill

The canonical standalone skill is [`skills/aisthesis`](skills/aisthesis/SKILL.md). It supports Build, Shape, Refine, Redesign, Audit, Study, Prototype, Polish, Harden, Adapt, Animate, Optimize, Extract, and Release routes across marketing sites, product interfaces, dashboards, documentation, portfolios, design systems, components, motion, and scroll narratives.

### Install the skill

Download the immutable `aisthesis-v1.0.0` release assets. The reviewed archive SHA-256 is `355584b61e31789e011387481c3b84f0e377f3c8e03be8e0e463b90a79cea6b0`.

**POSIX shell:**

```bash
set -eu
SKILLS_DIR="<your-agent-skills-directory>"
TARGET="$SKILLS_DIR/aisthesis"
assert_no_link_ancestor() {
  candidate=$1
  while :; do
    if [ -L "$candidate" ]; then
      echo "Refusing destination through link or junction: $candidate" >&2
      exit 1
    fi
    if command -v fsutil.exe >/dev/null 2>&1 && command -v cygpath >/dev/null 2>&1; then
      if fsutil.exe reparsepoint query "$(cygpath -w "$candidate")" >/dev/null 2>&1; then
        echo "Refusing destination through link or junction: $candidate" >&2
        exit 1
      fi
    fi
    parent=$(dirname -- "$candidate")
    [ "$parent" != "$candidate" ] || break
    candidate=$parent
  done
}
assert_no_link_ancestor "$TARGET"
if [ -e "$TARGET" ] || [ -L "$TARGET" ]; then
  echo "Refusing to replace $TARGET" >&2
  exit 1
fi
curl -LO https://github.com/LCFR-D/aisthesis/releases/download/aisthesis-v1.0.0/aisthesis-1.0.0.zip
curl -LO https://github.com/LCFR-D/aisthesis/releases/download/aisthesis-v1.0.0/aisthesis-1.0.0.zip.sha256
sha256sum -c aisthesis-1.0.0.zip.sha256
STAGING="$(mktemp -d)"
trap 'rm -rf "$STAGING"' EXIT HUP INT TERM
unzip -q aisthesis-1.0.0.zip -d "$STAGING"
assert_no_link_ancestor "$TARGET"
[ ! -e "$TARGET" ] && [ ! -L "$TARGET" ] || {
  echo "Refusing to replace $TARGET" >&2
  exit 1
}
mkdir -p "$SKILLS_DIR"
mv "$STAGING/aisthesis" "$TARGET"
```

**PowerShell:**

```powershell
$SkillsDir = "C:\path\to\your-agent-skills-directory"
$Target = Join-Path $SkillsDir "aisthesis"
function Assert-NoReparseAncestor {
    param([Parameter(Mandatory)][string]$Path)
    $Current = [System.IO.Path]::GetFullPath($Path)
    while ($true) {
        $Item = Get-Item -LiteralPath $Current -Force -ErrorAction SilentlyContinue
        if ($null -ne $Item) {
            if (($Item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
                throw "Refusing destination through link or junction: $Current"
            }
        }
        $Parent = [System.IO.Directory]::GetParent($Current)
        if ($null -eq $Parent) { break }
        $Current = $Parent.FullName
    }
}
Assert-NoReparseAncestor -Path $Target
if ($null -ne (Get-Item -LiteralPath $Target -Force -ErrorAction SilentlyContinue)) {
    throw "Refusing to replace $Target"
}
$Archive = "aisthesis-1.0.0.zip"
$Expected = "355584b61e31789e011387481c3b84f0e377f3c8e03be8e0e463b90a79cea6b0"
Invoke-WebRequest "https://github.com/LCFR-D/aisthesis/releases/download/aisthesis-v1.0.0/$Archive" -OutFile $Archive
if ((Get-FileHash $Archive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $Expected) {
    throw "Archive checksum mismatch"
}
$Staging = Join-Path ([System.IO.Path]::GetTempPath()) ([System.Guid]::NewGuid())
Expand-Archive -LiteralPath $Archive -DestinationPath $Staging
Assert-NoReparseAncestor -Path $Target
if ($null -ne (Get-Item -LiteralPath $Target -Force -ErrorAction SilentlyContinue)) {
    throw "Refusing to replace $Target"
}
New-Item -ItemType Directory -Path $SkillsDir -Force | Out-Null
Move-Item -LiteralPath (Join-Path $Staging "aisthesis") -Destination $Target
Remove-Item -LiteralPath $Staging -Recurse -Force
```

Use the user or project skills directory recognized by your Agent Skills-compatible client. The extracted directory is self-contained and starts at `aisthesis/SKILL.md`.

Trigger it with a request such as:

```text
Use Aisthesis to take this interface from product truth and direction through a verified release.
```

### Validate or build the skill archive

```bash
uv sync --locked --dev
uv run python -m scripts.validate_skill
uv run python -m scripts.build_skill_release --output dist
```

The builder creates a deterministic ZIP, SHA-256 checksum, and internal per-file manifest. Repository tests reject path traversal, non-portable paths, duplicate YAML, malformed manifests, symlinks, Windows junctions and reparse points, unsafe overwrite, and provenance drift.

## Aisthesis Judgment toolkit

The repository also contains the Python evidence toolkit used by the Aisthesis Judgment layer. It keeps three evidence classes separate:

1. deterministic browser and image measurements;
2. localized multimodal observations;
3. explicit human acceptance or rejection.

It does not produce an aesthetic score.

### Included detectors

- CIEDE2000 candidates for long horizontal palette boundaries;
- spatial self-similarity candidates for repeated imagery;
- physical viewport-travel budgets for authored phases;
- temporal grouping for adjacent detector hits;
- a CLI for inspecting frames and checking phase pacing.

### Install the toolkit

```bash
python -m pip install -e .
```

Python 3.11 or newer is required.

### Inspect a rendered frame

```bash
aisthesis inspect frame.png --output findings.json
```

The result reports seam and repetition candidates. It does not claim the frame is good or bad.

### Check physical pacing

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

### Python API

```python
from PIL import Image
import numpy as np
from aisthesis import detect_horizontal_seams, repetition_score

frame = np.asarray(Image.open("frame.png").convert("RGB"))
seams = detect_horizontal_seams(frame)
repetition = repetition_score(frame)
```

## Review boundary

Aisthesis can establish where a long palette boundary appears, whether a motif repeats, how much physical scroll a phase consumes, and where a rendered composition deserves inspection. It cannot establish taste, intent, usefulness, or acceptance from those measurements.

Use `docs/review-protocol.md` to run separate identity, overlap, palette/material, composition, temporal, and content-trust passes. Record the suspected implementation owner separately from the visible observation.

## Test

```bash
uv sync --locked --dev
uv run pytest -q
```

## Principles

- Product truth and the approved brief outrank style advice.
- Human rejection outranks a passing metric.
- A model observation is not an implementation cause.
- Exact frames are evidence; sparse contact sheets are summaries.
- Visual quality must not collapse into one score.
- Public examples must not contain private product evidence or customer data.
- One portable bundle must be enough to execute the complete frontend workflow.

## License

MIT. See [LICENSE](LICENSE).

## Community and security

- [Contributing](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security policy and private reporting](SECURITY.md)
- [Changelog](CHANGELOG.md)
- [Skill provenance](provenance.toml)
- [Third-party notices](THIRD_PARTY_NOTICES.md)

Aisthesis was developed at [LCFR](https://lcfr.xyz).

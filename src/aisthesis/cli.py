from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image

from .perception import detect_horizontal_seams, evaluate_phase_pacing, repetition_score


def _write(result: dict, output: str | None) -> None:
    payload = json.dumps(result, indent=2, allow_nan=False)
    if output:
        Path(output).write_text(payload + "\n", encoding="utf-8")
    print(payload)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="aisthesis",
        description="Evidence-led visual judgment for rendered interfaces",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    inspect = sub.add_parser("inspect", help="Inspect one rendered RGB frame")
    inspect.add_argument("image")
    inspect.add_argument("--minimum-coverage", type=float, default=0.65)
    inspect.add_argument("--minimum-delta-e", type=float, default=10.0)
    inspect.add_argument("--output")

    pace = sub.add_parser(
        "pace", help="Evaluate one authored phase in physical viewport travel"
    )
    pace.add_argument("--profile", default="default")
    pace.add_argument("--travel", type=float, required=True)
    pace.add_argument("--viewport-height", type=float, required=True)
    pace.add_argument("--start", type=float, required=True)
    pace.add_argument("--end", type=float, required=True)
    pace.add_argument("--minimum", type=float)
    pace.add_argument("--maximum", type=float)
    pace.add_argument("--reduced-motion", action="store_true")
    pace.add_argument("--output")

    args = parser.parse_args()
    if args.command == "inspect":
        try:
            with Image.open(args.image) as source:
                image = np.asarray(source.convert("RGB"))
            result = {
                "image": str(Path(args.image)),
                "horizontalSeams": detect_horizontal_seams(
                    image,
                    minimum_coverage=args.minimum_coverage,
                    minimum_delta_e=args.minimum_delta_e,
                ),
                "repetition": repetition_score(image),
                "judgmentBoundary": "Candidates are measurements, not an aesthetic verdict or human acceptance.",
            }
            _write(result, args.output)
        except (OSError, TypeError, ValueError) as error:
            parser.exit(2, f"ERROR: {error}\n")
        return
    profile = {
        "id": args.profile,
        "travel": args.travel,
        "viewport": {"height": args.viewport_height},
    }
    if args.reduced_motion:
        profile["reducedMotion"] = "reduce"
    phase = {
        "id": "phase",
        "range": [args.start, args.end],
        "minViewportTravel": args.minimum,
        "maxViewportTravel": args.maximum,
    }
    try:
        _write(evaluate_phase_pacing(profile, phase), args.output)
    except (OSError, TypeError, ValueError) as error:
        parser.exit(2, f"ERROR: {error}\n")


if __name__ == "__main__":
    main()

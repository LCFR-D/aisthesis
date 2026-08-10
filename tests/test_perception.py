import sys

import numpy as np
import pytest

from aisthesis import (
    cluster_visual_issues,
    detect_horizontal_seams,
    evaluate_phase_pacing,
    repetition_score,
)
from aisthesis.cli import main


def test_detects_long_horizontal_palette_boundary():
    image = np.zeros((120, 200, 3), dtype=np.uint8)
    image[:70] = (30, 60, 90)
    image[70:] = (230, 225, 210)
    seams = detect_horizontal_seams(image, minimum_coverage=0.8, minimum_delta_e=12)
    assert seams and abs(seams[0]["y"] - 70) <= 1


def test_repetition_distinguishes_tile_from_noise():
    rng = np.random.default_rng(7)
    tile = rng.integers(0, 256, size=(16, 16, 3), dtype=np.uint8)
    tiled = np.tile(tile, (6, 8, 1))
    noise = rng.integers(0, 256, size=tiled.shape, dtype=np.uint8)
    assert repetition_score(tiled)["score"] > 0.95
    assert repetition_score(noise)["score"] < 0.2


def test_phase_pacing_uses_viewport_travel():
    profile = {"id": "desktop", "travel": 3420, "viewport": {"height": 900}}
    phase = {"id": "corridor", "range": [0.25, 0.70], "maxViewportTravel": 1.4}
    result = evaluate_phase_pacing(profile, phase)
    assert result["viewportTravel"] == pytest.approx(1.71)
    assert result["passed"] is False


def test_reduced_motion_skips_animated_budget():
    profile = {
        "id": "reduced-motion",
        "travel": 920,
        "viewport": {"height": 1000},
        "reducedMotion": "reduce",
    }
    phase = {"id": "corridor", "range": [0.25, 0.70], "maxViewportTravel": 0.1}
    result = evaluate_phase_pacing(profile, phase)
    assert result["skipped"] and result["passed"]


def test_invalid_phase_ranges_fail_closed():
    profile = {"id": "desktop", "travel": 1000, "viewport": {"height": 500}}
    with pytest.raises(ValueError):
        evaluate_phase_pacing(profile, {"id": "backwards", "range": [0.8, 0.2]})


@pytest.mark.parametrize(
    ("profile", "phase", "message"),
    [
        (
            {"id": "desktop", "travel": float("nan"), "viewport": {"height": 500}},
            {"id": "phase", "range": [0.2, 0.8]},
            "travel",
        ),
        (
            {"id": "desktop", "travel": -1, "viewport": {"height": 500}},
            {"id": "phase", "range": [0.2, 0.8]},
            "travel",
        ),
        (
            {"id": "desktop", "travel": 1000, "viewport": {"height": 0}},
            {"id": "phase", "range": [0.2, 0.8]},
            "viewport height",
        ),
        (
            {"id": "desktop", "travel": 1000, "viewport": {"height": 500}},
            {"id": "phase", "range": [0.2, float("inf")]},
            "range",
        ),
        (
            {"id": "desktop", "travel": 1000, "viewport": {"height": 500}},
            {"id": "phase", "range": [0.2, 0.8], "minViewportTravel": -0.1},
            "minimum",
        ),
        (
            {"id": "desktop", "travel": 1000, "viewport": {"height": 500}},
            {"id": "phase", "range": [0.2, 0.8], "maxViewportTravel": float("nan")},
            "maximum",
        ),
    ],
)
def test_invalid_pacing_numbers_fail_closed(profile, phase, message):
    with pytest.raises(ValueError, match=message):
        evaluate_phase_pacing(profile, phase)


def test_cli_rejects_non_finite_pacing_as_valid_json_error(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "aisthesis",
            "pace",
            "--travel",
            "nan",
            "--viewport-height",
            "900",
            "--start",
            "0.2",
            "--end",
            "0.8",
        ],
    )
    with pytest.raises(SystemExit) as raised:
        main()
    assert raised.value.code == 2
    captured = capsys.readouterr()
    assert "travel" in captured.err
    assert captured.out == ""


def test_json_writer_rejects_non_standard_numbers(tmp_path):
    from aisthesis.cli import _write

    with pytest.raises(ValueError):
        _write({"notJson": float("nan")}, str(tmp_path / "result.json"))
    assert not (tmp_path / "result.json").exists()


def test_detector_thresholds_fail_closed():
    image = np.zeros((16, 16, 3), dtype=np.uint8)
    with pytest.raises(ValueError, match="minimum_coverage"):
        detect_horizontal_seams(image, minimum_coverage=float("nan"))
    with pytest.raises(ValueError, match="minimum_delta_e"):
        detect_horizontal_seams(image, minimum_delta_e=-1)
    with pytest.raises(ValueError, match="minimum_shift"):
        repetition_score(image, minimum_shift=0)
    with pytest.raises(ValueError, match="maximum_progress_gap"):
        cluster_visual_issues([], maximum_progress_gap=float("inf"))


def test_clusters_one_moving_seam():
    issues = [
        {
            "type": "hard-horizontal-seam",
            "profile": "desktop",
            "frame": 20,
            "progress": 0.25,
            "deltaE": 17,
        },
        {
            "type": "hard-horizontal-seam",
            "profile": "desktop",
            "frame": 22,
            "progress": 0.276,
            "deltaE": 22,
        },
    ]
    clustered = cluster_visual_issues(issues)
    assert len(clustered) == 1
    assert clustered[0]["frameRange"] == [20, 22]

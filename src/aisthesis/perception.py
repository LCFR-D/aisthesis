from __future__ import annotations

import cv2
import numpy as np
from skimage.color import deltaE_ciede2000, rgb2lab


def detect_horizontal_seams(
    image: np.ndarray,
    *,
    minimum_coverage: float = 0.65,
    minimum_delta_e: float = 10.0,
    edge_margin: int = 8,
) -> list[dict]:
    """Return long horizontal palette discontinuities, excluding viewport-edge chrome."""
    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError("image must be an RGB array")
    rgb = image
    if rgb.shape[1] > 640:
        rgb = cv2.resize(rgb, (640, rgb.shape[0]), interpolation=cv2.INTER_AREA)
    lab = rgb2lab(rgb.astype(np.float32) / 255.0)
    candidates = []
    for y in range(max(1, edge_margin), max(edge_margin, rgb.shape[0] - edge_margin)):
        delta = deltaE_ciede2000(lab[y - 1], lab[y])
        coverage = float(np.mean(delta >= minimum_delta_e))
        median = float(np.median(delta))
        if coverage >= minimum_coverage and median >= minimum_delta_e:
            candidates.append({"y": y, "coverage": coverage, "deltaE": median})
    return sorted(candidates, key=lambda item: item["deltaE"], reverse=True)


def repetition_score(image: np.ndarray, *, minimum_shift: int | None = None) -> dict:
    """Find the strongest repeated horizontal or vertical image offset."""
    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError("image must be an RGB array")
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY).astype(np.float32)
    if gray.shape[1] > 320:
        scale = 320 / gray.shape[1]
        gray = cv2.resize(
            gray,
            (320, max(1, round(gray.shape[0] * scale))),
            interpolation=cv2.INTER_AREA,
        )
    minimum_shift = minimum_shift or max(8, round(gray.shape[1] * 0.08))
    best = {"score": 0.0, "axis": None, "shift": 0}
    for axis, limit in (("x", gray.shape[1] // 2), ("y", gray.shape[0] // 2)):
        maximum = min(192, limit)
        dense_end = min(maximum, minimum_shift + 32)
        shifts = list(range(minimum_shift, dense_end + 1)) + list(
            range(dense_end + 4, maximum + 1, 4)
        )
        for shift in shifts:
            first, second = (
                (gray[:, :-shift], gray[:, shift:])
                if axis == "x"
                else (gray[:-shift, :], gray[shift:, :])
            )
            a, b = first.ravel(), second.ravel()
            a, b = a - a.mean(), b - b.mean()
            denominator = float(np.linalg.norm(a) * np.linalg.norm(b))
            score = float(np.dot(a, b) / denominator) if denominator else 0.0
            if score > best["score"]:
                best = {"score": score, "axis": axis, "shift": shift}
    return best


def evaluate_phase_pacing(profile: dict, phase: dict) -> dict:
    """Evaluate a narrative phase against an authored physical-distance budget."""
    start, end = phase["range"]
    minimum = phase.get("minViewportTravel")
    maximum = phase.get("maxViewportTravel")
    if end <= start:
        raise ValueError(f"phase {phase['id']} range must increase")
    if minimum is not None and maximum is not None and minimum > maximum:
        raise ValueError(f"phase {phase['id']} minimum travel exceeds maximum")
    viewport_height = float(profile["viewport"]["height"])
    viewport_travel = float(profile["travel"]) * (end - start) / viewport_height
    skipped = (
        profile.get("reducedMotion") == "reduce" or "reduced-motion" in profile["id"]
    )
    passed = skipped or (
        (minimum is None or viewport_travel >= minimum)
        and (maximum is None or viewport_travel <= maximum)
    )
    return {
        "phase": phase["id"],
        "profile": profile["id"],
        "range": [start, end],
        "viewportTravel": viewport_travel,
        "minimum": minimum,
        "maximum": maximum,
        "skipped": skipped,
        "passed": passed,
    }


def cluster_visual_issues(
    issues: list[dict], *, maximum_progress_gap: float = 0.06
) -> list[dict]:
    """Collapse consecutive detector hits into one causal interval."""
    frame_types = {"hard-horizontal-seam", "repeated-motif"}
    candidates = sorted(
        (
            item
            for item in issues
            if item.get("type") in frame_types and item.get("frame") is not None
        ),
        key=lambda item: (item["profile"], item["type"], item["progress"]),
    )
    groups: list[list[dict]] = []
    for item in candidates:
        if (
            not groups
            or groups[-1][-1]["profile"] != item["profile"]
            or groups[-1][-1]["type"] != item["type"]
            or item["progress"] - groups[-1][-1]["progress"] > maximum_progress_gap
        ):
            groups.append([item])
        else:
            groups[-1].append(item)
    clustered = []
    for group in groups:
        score_key = "deltaE" if group[0]["type"] == "hard-horizontal-seam" else "score"
        representative = max(group, key=lambda item: item.get(score_key, 0)).copy()
        representative.update(
            frameRange=[group[0]["frame"], group[-1]["frame"]],
            progressRange=[group[0]["progress"], group[-1]["progress"]],
            occurrences=len(group),
        )
        clustered.append(representative)
    clustered.extend(
        item
        for item in issues
        if item.get("type") not in frame_types or item.get("frame") is None
    )
    return clustered

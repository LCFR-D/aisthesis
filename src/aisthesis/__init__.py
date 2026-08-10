"""Aisthesis Judgment: visual-evidence primitives for the frontend operating system."""

from .perception import (
    cluster_visual_issues,
    detect_horizontal_seams,
    evaluate_phase_pacing,
    repetition_score,
)

__all__ = [
    "cluster_visual_issues",
    "detect_horizontal_seams",
    "evaluate_phase_pacing",
    "repetition_score",
]
__version__ = "1.0.0"

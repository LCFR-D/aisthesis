"""Aisthesis: evidence-led visual judgment for rendered interfaces."""

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
__version__ = "0.1.0"

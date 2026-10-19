"""Score /100 per distribution network (UDI) and per commune — implemented in phase 3.

Method: docs/CAHIER_DES_CHARGES.md §4 and decisions in docs/AVANCEMENT.md.
"""
from __future__ import annotations

import config


def grade(score: float | None) -> str | None:
    """Letter grade A–E from a score /100 (thresholds in config.GRADES)."""
    if score is None:
        return None
    for threshold, letter in config.GRADES:
        if score >= threshold:
            return letter
    return config.GRADES[-1][1]

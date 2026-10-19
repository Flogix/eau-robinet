"""Shared chart style (palette, axes, source caption). Completed in phase 4."""
from __future__ import annotations

# Okabe–Ito palette: distinguishable with the common forms of colour blindness.
PALETTE = {
    "blue": "#0072B2",
    "orange": "#E69F00",
    "green": "#009E73",
    "vermillion": "#D55E00",
    "sky": "#56B4E9",
    "purple": "#CC79A7",
    "yellow": "#F0E442",
    "grey": "#7F7F7F",
}
FAMILY_COLORS = {
    "micro": PALETTE["vermillion"],
    "chem": PALETTE["blue"],
    "comfort": PALETTE["orange"],
    "info": PALETTE["grey"],
}

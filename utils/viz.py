"""Shared chart style: palette, layout, threshold lines, and the "chart + caption + source" pattern.

Colour rules (checked with a palette validator for colour-vision deficiencies):
- categories use the Okabe–Ito palette in a fixed order; three of its colours have low contrast on a white
  background, so values are also written on bars or given in the hover / table;
- magnitudes use one hue from light to dark (Blues); good/bad is never shown by colour alone (grade letter,
  icon or text next to it).
"""
from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from utils.io import SOURCE_SHORT

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
SERIES = [PALETTE[k] for k in ("blue", "orange", "green", "vermillion", "sky", "purple")]
FAMILY_COLORS = {
    "micro": PALETTE["vermillion"],
    "chem": PALETTE["blue"],
    "comfort": PALETTE["orange"],
    "info": PALETTE["grey"],
}
FAMILY_LABELS = {"micro": "Microbiology", "chem": "Health chemistry", "comfort": "Comfort / indicators"}
# Grades: ordered sequential-like scale (green -> vermillion), always printed with the letter.
GRADE_COLORS = {"A": "#009E73", "B": "#56B4E9", "C": "#F0E442", "D": "#E69F00", "E": "#D55E00"}
SEQUENTIAL = "Blues"
NEUTRAL = "#7F7F7F"


def layout(fig: go.Figure, x: str | None = None, y: str | None = None, height: int = 380,
           legend: bool = True) -> go.Figure:
    """Common layout: titled axes with units, recessive grid, horizontal legend above the plot."""
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=40, b=10), hovermode="closest",
                      showlegend=legend, legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, title=None),
                      font=dict(size=13))
    if x is not None:
        fig.update_xaxes(title_text=x)
    if y is not None:
        fig.update_yaxes(title_text=y)
    return fig


def threshold(fig: go.Figure, value: float, text: str, axis: str = "y", color: str = NEUTRAL) -> go.Figure:
    """Dashed reference line for a regulatory threshold, labelled in words."""
    if axis == "y":
        fig.add_hline(y=value, line_dash="dash", line_color=color, annotation_text=text,
                      annotation_position="top left")
    else:
        fig.add_vline(x=value, line_dash="dash", line_color=color, annotation_text=text,
                      annotation_position="top")
    return fig


def event(fig: go.Figure, x, text: str, y_pos: float = 1.0) -> go.Figure:
    """Vertical dotted line + label for a dated change (new monitoring rule, reclassification…)."""
    fig.add_shape(type="line", x0=x, x1=x, y0=0, y1=1, yref="paper", line=dict(dash="dot", color=NEUTRAL, width=1))
    fig.add_annotation(x=x, y=y_pos, yref="paper", text=text, showarrow=False, xanchor="left", yanchor="top",
                       font=dict(size=11), bgcolor="rgba(127,127,127,0.15)")
    return fig


def show(fig: go.Figure, caption: str, source: str = SOURCE_SHORT, key: str | None = None) -> None:
    """Render a chart with its alt text, a one-sentence caption describing it, and the source."""
    st.plotly_chart(fig, key=key, alt=caption, config={"displaylogo": False})
    st.caption(f"{caption} {source}")


def headline(text: str) -> None:
    """Headline sentence that opens a section: the insight, computed from the data."""
    st.markdown(f"#### {text}")


def pct(x: float, digits: int = 1) -> str:
    return f"{100 * x:.{digits}f}%"


def fmt_int(x) -> str:
    return f"{int(round(x)):,}"

# Visual identity, typography, CSS styling, and Plotly charting helpers for Au robinet.
"""Visual identity "Au robinet" (a lab notebook / newspaper data page) and the shared chart pattern.

Every chart is shown with chart(): a title that says what it shows, the figure, a caption underneath that tells how to
read it (also used as alt text), and a short paragraph that says what to take away and why the chart is there.

Colours: the categorical palette below passes a colour-vision-deficiency check (lightness band, chroma, separation of
neighbouring colours for protanopia, deuteranopia and tritanopia, contrast >= 3:1) on both the paper background
(#F6F2E9) and the ink background (#11161F). Good and bad are never told by colour alone: a word, a letter or a hatch
pattern always goes with it.
"""
from __future__ import annotations

import re

import plotly.graph_objects as go
import streamlit as st

from utils.i18n import t

TEAL, BRICK, BLUE, OCHRE, PLUM, GREEN = "#0095A3", "#C8452F", "#3F73C9", "#B07E00", "#A8479A", "#4E9431"
SERIES = [TEAL, BRICK, BLUE, OCHRE, PLUM, GREEN]
NEUTRAL = "#8A8578"          # warm grey, readable on paper and on ink
LIGHT_NEUTRAL = "#C9C2B1"
PALETTE = {"teal": TEAL, "brick": BRICK, "blue": BLUE, "ochre": OCHRE, "plum": PLUM, "green": GREEN,
           "grey": NEUTRAL}
FAMILY_COLORS = {"micro": BRICK, "chem": BLUE, "comfort": OCHRE, "info": NEUTRAL}
# Grades: an ordered scale from water-teal (A) to brick (E), always printed with the letter.
GRADE_COLORS = {"A": "#0E7C86", "B": "#5FA8AE", "C": "#C9A24A", "D": "#D07A45", "E": "#B5452F"}
FONT = "IBM Plex Sans, Helvetica, Arial, sans-serif"
SERIF = "Fraunces, Georgia, serif"
MONO = "IBM Plex Mono, Consolas, monospace"

LOGO = ('<svg class="ar-logo" viewBox="0 0 32 40" aria-hidden="true"><path d="M16 3 C16 3 6 16 6 24 a10 10 0 0 0 20 0 '
        'C26 16 16 3 16 3 Z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>'
        '<path d="M11 25 a5 5 0 0 0 5 5" fill="none" stroke="#0095A3" stroke-width="2.2" stroke-linecap="round"/>'
        '<line x1="1" y1="38" x2="31" y2="38" stroke="currentColor" stroke-width="1.4"/></svg>')

CSS = """
<style>
.ar-header {display:flex; align-items:center; gap:.8rem; margin:-1.2rem 0 1.6rem 0; padding-bottom:.9rem;
            border-bottom:1px solid rgba(127,127,127,.35);}
.ar-logo {width:30px; height:38px; flex:none;}
.ar-brand {font-family:Fraunces, Georgia, serif; font-size:1.55rem; font-weight:700; letter-spacing:.01em; line-height:1;}
.ar-tagline {font-size:.9rem; opacity:.8; font-style:italic; line-height:1.3;}
.ar-kicker {font-family:"IBM Plex Mono", monospace; font-size:.78rem; letter-spacing:.12em; text-transform:uppercase;
            opacity:.78; margin:2rem 0 .75rem 0; line-height:1.5;}
/* a title right under a kicker: no extra space above the title, the kicker's own margin is enough */
[data-testid="stElementContainer"]:has(.ar-kicker) + [data-testid="stElementContainer"] :is(h1, h2, h3) {
    padding-top:0 !important;}
.ar-kicker::before {content:""; display:inline-block; width:1.6rem; height:2px; background:#0095A3;
                    vertical-align:middle; margin-right:.6rem;}
.ar-lede {font-family:Fraunces, Georgia, serif; font-size:1.28rem; line-height:1.45; margin:.4rem 0 1rem 0;}
.ar-headline {font-family:Fraunces, Georgia, serif; font-size:1.12rem; font-weight:600; line-height:1.4; margin:.6rem 0 .8rem 0;}
.ar-chart-title {font-family:Fraunces, Georgia, serif; font-size:1.08rem; font-weight:600; margin:1.2rem 0 .1rem 0;}
.ar-takeaway {border-left:3px solid #0095A3; padding:.2rem 0 .2rem .9rem; margin:.2rem 0 1.4rem 0; line-height:1.55;}
.ar-badge {display:inline-block; min-width:6.6rem; text-align:center; font-family:"IBM Plex Mono", monospace;
           font-size:.72rem; letter-spacing:.06em; text-transform:uppercase; color:#fff; border-radius:.2rem;
           padding:.1rem .45rem; margin-right:.55rem; vertical-align:.1rem;}
.ar-badge.ok {background:#0E7C86;} .ar-badge.limit {background:#B5452F;} .ar-badge.watch {background:#8A6200;}
.ar-badge.info {background:#4A5D7A;} .ar-badge.unknown {background:#6B6658;}
.ar-report p {margin:.35rem 0;}
.ar-footer {margin-top:3rem; padding-top:1rem; border-top:1px solid rgba(127,127,127,.35); font-size:.85rem;
            opacity:.85; line-height:1.6;}
.ar-num {font-family:"IBM Plex Mono", monospace;}
[data-testid="stMetricValue"] {font-family:"IBM Plex Mono", monospace; font-weight:500;}
[data-testid="stSidebarNav"] a span {font-size:.95rem;}
.ar-side-head {margin:-1.4rem 0 0 0; padding:.2rem .1rem .4rem .1rem; line-height:1.4; font-size:.84rem;}
.ar-side-head > div {margin-top:.3rem;}
/* EFREI logo: the shape of the PNG is a mask, its colour follows the active theme at once (Streamlit sets color-scheme
   on the app: light-dark() reads it, no rerun needed): black on the light theme, white on the dark one */
.ar-side-logo {display:block; width:150px; aspect-ratio:400 / 146; margin:0 0 .85rem 0;
               background-color:currentColor; background-color:light-dark(#000000, #FFFFFF);
               -webkit-mask-repeat:no-repeat; mask-repeat:no-repeat; -webkit-mask-size:contain; mask-size:contain;}
.ar-side-name {font-weight:600; font-size:.98rem; margin-top:0 !important;}
.ar-side-email {margin-top:.15rem !important;}
.ar-side-links {margin-top:.45rem !important;}
.ar-side-course {margin-top:.7rem !important; opacity:.8;}
.ar-side-course div {margin-top:.1rem;}
.ar-side-head a {text-decoration:none; border-bottom:1px solid currentColor;}
.st-key-ar_filters {border-color:rgba(14,124,134,.55) !important; background:rgba(14,124,134,.06);}
.st-key-ar_filters strong {font-family:Fraunces, Georgia, serif; font-size:1.08rem; font-weight:600;}
.ar-filter-hint {font-size:.86rem; margin:-.6rem 0 .2rem 0; padding:.15rem 0 .15rem .7rem;
                  border-left:2px solid #0095A3; opacity:.88;}
.ar-preview {margin:.8rem 0 .3rem 0; font-size:1.02rem;}
.ar-grade {display:inline-block; min-width:1.6rem; text-align:center; color:#fff; font-family:Fraunces, Georgia, serif;
           font-weight:700; border-radius:.2rem; padding:0 .35rem; margin-right:.5rem;}
.ar-nav-section {font-size:.8rem; font-weight:600; opacity:.75; margin:2rem 0 1.05rem .1rem;}
.ar-nav-section.first {margin-top:1.6rem;}
[data-testid="stSidebar"] [data-testid="stPageLink"] {margin:-.35rem 0;}
</style>
"""


def inject_css() -> None:
    """Inject global stylesheet and custom CSS classes into active Streamlit view."""
    st.markdown(CSS, unsafe_allow_html=True)


def _data_uri(name: str) -> str:
    """Encode an image asset as a Base64 data URI string."""
    import base64
    from pathlib import Path
    data = (Path(__file__).resolve().parents[1] / "assets" / name).read_bytes()
    return "data:image/png;base64," + base64.b64encode(data).decode()


# EFREI logo: the original PNGs (transparent background, 2560 px, kept out of git) reduced to 400 px and 16 colours.
# The black and the white one have the same shape; the page uses that shape as a CSS mask and paints it black or white
# with the active theme (see .ar-side-logo in CSS), so the switch is instant, whatever changed the theme.
LOGO_MASK = _data_uri("efrei-logo-black.png")


LINKEDIN = "https://www.linkedin.com/in/florian-giraud-67883a291/"
GITHUB = "https://github.com/Flogix/eau-robinet"
AUTHOR_EMAIL = "florian.giraud@efrei.net"
COORD_EMAIL = "mano.mathew@efrei.fr"


def sidebar_menu(sections: dict) -> None:
    """Top of the sidebar: the author block, then the menu (sections of st.Page drawn with st.page_link, the current
    page highlighted). Streamlit's own menu always sits at the very top, which would put the author block below it."""
    link = '<a href="{u}" target="_blank" rel="noopener noreferrer">{t}</a>'
    mailto = '<a href="mailto:{e}">{e}</a>'
    email_author = mailto.format(e=AUTHOR_EMAIL)
    email_coord = mailto.format(e=COORD_EMAIL)
    with st.sidebar:
        st.markdown(
            f'<div class="ar-side-head"><div class="ar-side-logo" role="img" aria-label="{t("side.author.logo")}" '
            f'style="-webkit-mask-image:url({LOGO_MASK}); mask-image:url({LOGO_MASK})"></div>'
            f'<div class="ar-side-name">Florian Giraud</div>'
            f'<div>{t("side.author.program")}</div>'
            f'<div class="ar-side-email">{email_author}</div>'
            f'<div class="ar-side-links">{link.format(u=LINKEDIN, t="LinkedIn")} · {link.format(u=GITHUB, t="GitHub")}</div>'
            f'<div class="ar-side-course"><div>{t("side.author.course")}</div><div>{t("side.author.coord")}</div>'
            f'<div>{t("side.author.proposed", email=email_coord)}</div></div>'
            f'</div>', unsafe_allow_html=True)
        for i, (title, pages) in enumerate(sections.items()):
            first = " first" if i == 0 else ""
            st.markdown(f'<div class="ar-nav-section{first}">{title}</div>', unsafe_allow_html=True)
            for pg in pages:
                st.page_link(pg, label=pg.title, icon=pg.icon)
        st.divider()


def header() -> None:
    """Render primary top branding bar with logo, title, and tagline."""
    st.markdown(f'<div class="ar-header">{LOGO}<div><div class="ar-brand">Au robinet</div>'
                f'<div class="ar-tagline">{t("brand.tagline")}</div></div></div>', unsafe_allow_html=True)


def footer() -> None:
    """Render standard page footer with credits and repository link."""
    st.markdown(f'<div class="ar-footer">{_md(t("footer.text"))}</div>', unsafe_allow_html=True)


def _md(text: str) -> str:
    """Minimal Markdown for HTML blocks: **bold**, *italic*, [link](url)."""
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", text)
    return re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>', text)


def kicker(text: str) -> None:
    """Small mono label above a section title, like a newspaper section name."""
    st.markdown(f'<div class="ar-kicker">{text}</div>', unsafe_allow_html=True)


def lede(text: str) -> None:
    """Render large introductory lede paragraph in serif font."""
    st.markdown(f'<div class="ar-lede">{_md(text)}</div>', unsafe_allow_html=True)


def headline(text: str) -> None:
    """The insight of a section in one sentence, computed from the data."""
    st.markdown(f'<div class="ar-headline">{_md(text)}</div>', unsafe_allow_html=True)


def takeaway(text: str) -> None:
    """Render highlighted takeaway callout block with teal accent border."""
    st.markdown(f'<div class="ar-takeaway">{_md(text)}</div>', unsafe_allow_html=True)


def badge(kind: str) -> str:
    """HTML badge for the report: ok, limit, watch, info, unknown (a word, never a colour alone)."""
    return f'<span class="ar-badge {kind}">{t("badge." + kind)}</span>'


def layout(fig: go.Figure, x: str | None = None, y: str | None = None, height: int = 380,
           legend: bool = True) -> go.Figure:
    """House style: Plex Sans, recessive grid, legend above the plot, titled axes with units."""
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=30, b=10), hovermode="closest", showlegend=legend,
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, title=None, font=dict(size=12)),
                      font=dict(family=FONT, size=13), colorway=SERIES,
                      hoverlabel=dict(font=dict(family=FONT, size=13)))
    fig.update_xaxes(showgrid=False, zeroline=False, ticks="outside", ticklen=4)
    fig.update_yaxes(gridcolor="rgba(127,127,127,0.18)", zeroline=False)
    if x is not None:
        fig.update_xaxes(title_text=x)
    if y is not None:
        fig.update_yaxes(title_text=y)
    return fig


def threshold(fig: go.Figure, value: float, text: str, axis: str = "y", color: str = BRICK) -> go.Figure:
    """Dashed line for a regulatory threshold, labelled in words."""
    if axis == "y":
        fig.add_hline(y=value, line_dash="dash", line_color=color, line_width=1.5, annotation_text=text,
                      annotation_position="top left", annotation_font=dict(color=color, size=12))
    else:
        fig.add_vline(x=value, line_dash="dash", line_color=color, line_width=1.5, annotation_text=text,
                      annotation_position="top", annotation_font=dict(color=color, size=12))
    return fig


def event(fig: go.Figure, x, text: str, y_pos: float = 1.0) -> go.Figure:
    """Dotted vertical line and an italic note for a dated change (new monitoring, reclassification)."""
    fig.add_shape(type="line", x0=x, x1=x, y0=0, y1=1, yref="paper", line=dict(dash="dot", color=NEUTRAL, width=1))
    fig.add_annotation(x=x, y=y_pos, yref="paper", text=f"<i>{text}</i>", showarrow=False, xanchor="left",
                       yanchor="top", font=dict(size=11, family=SERIF), bgcolor="rgba(127,127,127,0.12)")
    return fig


def partial_year(fig: go.Figure, year: int, text: str) -> go.Figure:
    """Highlight incomplete final year column with translucent vertical band."""
    fig.add_vrect(x0=year - 0.5, x1=year + 0.5, fillcolor=NEUTRAL, opacity=0.12, line_width=0,
                  annotation_text=f"<i>{text}</i>", annotation_position="top left", annotation_font=dict(size=11))
    return fig


def chart(fig: go.Figure, title: str, caption: str, take: str | None = None, key: str | None = None) -> None:
    """Title, chart, caption (how to read it, also the alt text) with the source, then what to take away."""
    st.markdown(f'<div class="ar-chart-title">{title}</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, key=key, alt=caption, config={"displaylogo": False})
    st.caption(f"{caption} {t('common.source_short')}")
    if take:
        takeaway(take)


def analysis(seen: str, why: str, limits: str) -> None:
    """Interpretation under a chart: what we observe, why it is probably so (with sources), and the limits."""
    from utils.i18n import t as _t
    takeaway(f"**{_t('an.seen')}** {seen}<br><br>**{_t('an.why')}** {why}<br><br>**{_t('an.limits')}** {limits}")

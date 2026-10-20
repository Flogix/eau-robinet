"""Global sidebar: language, filters (only the ones that act on the open page are active), disclaimer."""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import streamlit as st

import config
from utils.i18n import LANGS, t
from utils.io import departments

VARIABLES = ["bact_official", "chem_official", "nitrates", "pesticides", "pfas", "metals", "disinfection_byproducts",
             "comfort"]
OFFICIAL = {"bact_official", "chem_official"}
COMMUNE_TYPES = ["all", "urban_dense", "urban_inter", "rural", "mountain", "med"]

ALL_FRANCE = "all"   # value of the region filter for the whole country (the Filters object says None)
FILTER_KEYS = ("f_years", "f_region_code", "f_ctype", "map_view")   # map_view: the map's own control
# Which filters change something on each page (url path -> filters), checked by tests/test_app_pages.py.
# Only these are drawn; a page without any has no Filters section.
PAGE_FILTERS = {
    "": {"years", "region", "ctype"},
    "reading": {"years"},
    "town": set(),
    "compare": {"region"},
    "map": {"years", "region", "ctype"},
    "monitor": {"years"},
    "explore": set(),
    "quality": {"years"},
    "my-score": set(),
    "conclusions": set(),
    "about": set(),
}


@dataclass(frozen=True)
class Filters:
    years: tuple[int, int]
    region: str | None          # region code, None = all France
    region_name: str
    variable: str
    commune_type: str

    @property
    def variable_label(self) -> str:
        return t(f"var.{self.variable}")

    @property
    def type_label(self) -> str:
        return t(f"ctype.{self.commune_type}")

    @property
    def period_label(self) -> str:
        a, b = self.years
        txt = str(a) if a == b else f"{a}–{b}"
        return txt + (t("period.partial") if b == config.PARTIAL_YEAR else "")

    @property
    def scope_label(self) -> str:
        return self.region_name if self.region else t("side.region.all")


def regions() -> pd.DataFrame:
    return departments()[["reg", "reg_nom"]].drop_duplicates().sort_values("reg_nom")


def init_language() -> None:
    """Language of the session, before any text is written: English (official) unless ?lang=fr is in the URL."""
    if "lang" not in st.session_state:
        q = st.query_params.get("lang")
        st.session_state["lang"] = q if q in LANGS else "en"


def language_selector() -> None:
    """EN / FR switch in the sidebar, under the menu (English is the official version)."""
    init_language()
    with st.sidebar:
        st.segmented_control(t("side.lang"), list(LANGS), format_func=LANGS.get, key="lang", required=True)


def _keep_filter_values() -> None:
    """A widget that is not drawn during a run loses its value at the end of that run. The filters are only drawn on the
    pages where they act, so their values are re-assigned at every run (the pattern documented by Streamlit) to survive a
    visit to a page without filters. Their defaults are set here once, never through the widgets' value= argument."""
    st.session_state.setdefault("f_years", (config.YEARS[0], config.COMPLETE_YEARS[-1]))
    if st.session_state.get("f_region_code") is None:    # "all" and not None: None would show an empty selectbox
        st.session_state["f_region_code"] = ALL_FRANCE
    st.session_state.setdefault("f_ctype", "all")
    for key in FILTER_KEYS:
        if key in st.session_state:
            st.session_state[key] = st.session_state[key]


def sidebar(page: str) -> Filters:
    """Draw the filters that act on `page`, and only those; on a page where none acts, the Filters section is hidden.
    Values are kept across pages."""
    active = PAGE_FILTERS.get(page, set())
    _keep_filter_values()
    reg = regions()
    codes = [ALL_FRANCE] + reg["reg"].tolist()
    names = dict(zip(reg["reg"], reg["reg_nom"]))
    # labels computed once per run (a format_func must not depend on state read later)
    reg_labels = {ALL_FRANCE: t("side.region.all"), **names}
    type_labels = {c: t(f"ctype.{c}") for c in COMMUNE_TYPES}
    with st.sidebar:
        if active:
            st.markdown(f"**{t('side.filters')}**")
            st.caption(t("side.intro"))
        if "years" in active:
            st.slider(t("side.years"), min_value=config.YEARS[0], max_value=config.YEARS[-1], key="f_years",
                      help=t("side.years.help"))
        if "region" in active:
            st.selectbox(t("side.region"), codes, key="f_region_code", help=t("side.region.help"),
                         format_func=reg_labels.get)
        if "ctype" in active:
            st.selectbox(t("side.ctype"), COMMUNE_TYPES, format_func=type_labels.get, key="f_ctype",
                         help=t("side.ctype.help"))
        st.session_state["_page_controls"] = st.container()   # filled by the open page (variable selection)
        st.divider()
        st.caption(t("side.disclaimer"))
    years = st.session_state["f_years"]
    region = None if st.session_state["f_region_code"] == ALL_FRANCE else st.session_state["f_region_code"]
    variable = "bact_official"   # the variable of the map is chosen in page_controls() by the map page
    f = Filters(tuple(years), region, names.get(region, ""), variable, st.session_state["f_ctype"])
    st.session_state["filters"] = f
    return f


def page_controls():
    """Sidebar slot, right under the filters, for a control that belongs to the open page (the map's variable)."""
    return st.session_state.get("_page_controls") or st.sidebar


def get_filters() -> Filters:
    f = st.session_state.get("filters")
    if f is None:   # page run on its own (tests): defaults
        f = Filters((config.YEARS[0], config.COMPLETE_YEARS[-1]), None, "", "bact_official", "all")
    return f


def commune_mask(d: pd.DataFrame, f: Filters) -> pd.Series:
    """Rows of a commune table (with dim_communes columns) that match the region and commune-type filters."""
    m = pd.Series(True, index=d.index)
    if f.region is not None:
        m &= d["reg"] == f.region
    ct = f.commune_type
    if ct == "urban_dense":
        m &= d["density3"] == 1
    elif ct == "urban_inter":
        m &= d["density3"] == 2
    elif ct == "rural":
        m &= d["density3"] == 3
    elif ct == "mountain":
        m &= d["mountain"].fillna(False).astype(bool)
    elif ct == "med":
        m &= d["mediterranean_coast"].fillna(False).astype(bool)
    return m


def dept_mask(d: pd.DataFrame, f: Filters, dep_col: str = "dep") -> pd.Series:
    if f.region is None:
        return pd.Series(True, index=d.index)
    deps = departments()
    return d[dep_col].isin(deps.loc[deps["reg"] == f.region, "dep"])

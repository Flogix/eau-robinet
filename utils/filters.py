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

# Note shown when no filter is active, for the pages that do not show the score of a town
NO_FILTER_NOTE = {"explore": "side.none.explore", "about": "side.none.about"}
# Which filters change something on each page (url path -> filters). The others are greyed out.
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


def language_selector() -> None:
    """EN / FR switch at the top of the sidebar (English is the official version). ?lang=fr in the URL works too."""
    if "lang" not in st.session_state:
        q = st.query_params.get("lang")
        st.session_state["lang"] = q if q in LANGS else "en"
    with st.sidebar:
        st.segmented_control(t("side.lang"), list(LANGS), format_func=LANGS.get, key="lang", required=True)


def sidebar(page: str) -> Filters:
    """Draw the filters; the ones that do nothing on `page` are disabled. Values are kept across pages."""
    active = PAGE_FILTERS.get(page, set())
    reg = regions()
    codes = [None] + reg["reg"].tolist()
    names = dict(zip(reg["reg"], reg["reg_nom"]))
    # labels computed once per run (a format_func must not depend on state read later)
    reg_labels = {None: t("side.region.all"), **names}
    type_labels = {c: t(f"ctype.{c}") for c in COMMUNE_TYPES}
    with st.sidebar:
        st.markdown(f"**{t('side.filters')}**")
        st.caption(t("side.intro") if active else t(NO_FILTER_NOTE.get(page, "side.none")))
        years = st.slider(t("side.years"), min_value=config.YEARS[0], max_value=config.YEARS[-1],
                          value=(config.YEARS[0], config.COMPLETE_YEARS[-1]), key="f_years",
                          help=t("side.years.help"), disabled="years" not in active)
        region = st.selectbox(t("side.region"), codes, key="f_region_code", help=t("side.region.help"),
                              format_func=reg_labels.get,
                              disabled="region" not in active)
        variable = "bact_official"   # the variable of the map is chosen in page_controls() by the map page
        ctype = st.selectbox(t("side.ctype"), COMMUNE_TYPES, format_func=type_labels.get, key="f_ctype",
                             help=t("side.ctype.help"), disabled="ctype" not in active)
        st.session_state["_page_controls"] = st.container()   # filled by the open page (variable selection)
        st.divider()
        st.caption(t("side.disclaimer"))
    f = Filters(tuple(years), region, names.get(region, ""), variable, ctype)
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

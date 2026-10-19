"""Global sidebar filters (drawn once in app.py, read by every page through st.session_state)."""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import streamlit as st

import config
from utils.io import departments

VARIABLES = {   # key -> label (dept_family_year.variable)
    "bact_official": "Bacteria — official conformity",
    "chem_official": "Chemistry — official conformity",
    "nitrates": "Nitrates",
    "pesticides": "Pesticides",
    "pfas": "PFAS (sum of 20)",
    "metals": "Metals (lead, arsenic…)",
    "disinfection_byproducts": "Disinfection by-products",
    "comfort": "Comfort indicators (references)",
}
OFFICIAL = {"bact_official", "chem_official"}

COMMUNE_TYPES = {
    "all": "All communes",
    "urban_dense": "Urban — dense",
    "urban_inter": "Urban — intermediate",
    "rural": "Rural",
    "mountain": "Mountain (loi Montagne)",
    "med": "Mediterranean coast (approx.)",
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
        return VARIABLES[self.variable]

    @property
    def type_label(self) -> str:
        return COMMUNE_TYPES[self.commune_type]

    @property
    def period_label(self) -> str:
        a, b = self.years
        txt = str(a) if a == b else f"{a}–{b}"
        return txt + (" (2026 partial)" if b == config.PARTIAL_YEAR else "")

    @property
    def scope_label(self) -> str:
        return self.region_name


def regions() -> pd.DataFrame:
    return departments()[["reg", "reg_nom"]].drop_duplicates().sort_values("reg_nom")


def sidebar() -> Filters:
    """Draw the global filters in the sidebar and keep them in st.session_state['filters']."""
    reg = regions()
    reg_names = ["All France"] + reg["reg_nom"].tolist()
    with st.sidebar:
        st.header("Filters")
        years = st.slider("Period (years)", min_value=config.YEARS[0], max_value=config.YEARS[-1],
                          value=(config.YEARS[0], config.COMPLETE_YEARS[-1]), key="f_years",
                          help="Calendar years of the samples. 2026 is partial (samples up to 31 August 2026). "
                               "The score always uses the latest 12/36 months, whatever the period.")
        region_name = st.selectbox("Region", reg_names, key="f_region",
                                   help="Restricts KPIs, maps, rankings and distributions to one region.")
        variable = st.selectbox("Parameter family", list(VARIABLES), format_func=VARIABLES.get, key="f_variable",
                                help="What the map and the trend charts show. 'Official conformity' = the ARS "
                                     "conclusion on each sample. The other families are recomputed by us: a result "
                                     "above the threshold written on the result row.")
        ctype = st.selectbox("Type of commune", list(COMMUNE_TYPES), format_func=COMMUNE_TYPES.get, key="f_ctype",
                             help="INSEE density grid (urban/rural), Mountain Act communes (Cerema), and Mediterranean "
                                  "departments outside mountain areas — an approximation of the coast. Applies to "
                                  "commune-level KPIs, score distributions and rankings.")
    region = None if region_name == "All France" else reg.set_index("reg_nom").loc[region_name, "reg"]
    f = Filters(tuple(years), region, region_name, variable, ctype)
    st.session_state["filters"] = f
    return f


def get_filters() -> Filters:
    f = st.session_state.get("filters")
    if f is None:   # page run on its own (tests): defaults
        f = Filters((config.YEARS[0], config.COMPLETE_YEARS[-1]), None, "All France", "bact_official", "all")
    return f


def commune_mask(d: pd.DataFrame, f: Filters) -> pd.Series:
    """Rows of a commune table (with dim_communes columns) that match the region and commune-type filters."""
    m = pd.Series(True, index=d.index)
    if f.region is not None:
        m &= d["reg"] == f.region
    t = f.commune_type
    if t == "urban_dense":
        m &= d["density3"] == 1
    elif t == "urban_inter":
        m &= d["density3"] == 2
    elif t == "rural":
        m &= d["density3"] == 3
    elif t == "mountain":
        m &= d["mountain"].fillna(False).astype(bool)
    elif t == "med":
        m &= d["mediterranean_coast"].fillna(False).astype(bool)
    return m


def dept_mask(d: pd.DataFrame, f: Filters, dep_col: str = "dep") -> pd.Series:
    if f.region is None:
        return pd.Series(True, index=d.index)
    deps = departments()
    return d[dep_col].isin(deps.loc[deps["reg"] == f.region, "dep"])

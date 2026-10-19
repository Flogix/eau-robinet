"""Aggregates computed in the app from the small tables (KPIs, department metrics), all tied to the filters."""
from __future__ import annotations

import pandas as pd

import config
from utils.filters import Filters, commune_mask, dept_mask
from utils.io import cached_resource, communes, departments, load_table


def _years(d: pd.DataFrame, f: Filters, col: str = "annee") -> pd.Series:
    return d[col].between(*f.years)


@cached_resource
def commune_year_typed() -> pd.DataFrame:
    """commune_year + typology of the current commune (old codes mapped to their current commune)."""
    cy = load_table("commune_year")
    dim = load_table("dim_communes")[["insee", "insee_current"]]
    cur = load_table("dim_communes").set_index("insee")[["reg", "dep", "density3", "mountain", "mediterranean_coast",
                                                         "population", "nom"]]
    d = cy.merge(dim, on="insee", how="left")
    d["insee_current"] = d["insee_current"].fillna(d["insee"])
    return d.join(cur, on="insee_current")


def sample_compliance(f: Filters, kind: str = "bact") -> dict:
    """Share of samples officially compliant (dept_year: one count per sample), for the period and region,
    with the change of the last year of the period vs the year before (percentage points)."""
    dy = load_table("dept_year")
    dy = dy[dept_mask(dy, f)]
    n, nc = f"n_{kind}", f"n_{kind}_nc"
    p = dy[_years(dy, f)]
    rate = 1 - p[nc].sum() / max(p[n].sum(), 1)
    by_year = dy.groupby("annee")[[n, nc]].sum()
    by_year["rate"] = 1 - by_year[nc] / by_year[n]
    last = f.years[1]
    delta = None
    if last - 1 in by_year.index and last in by_year.index:
        delta = 100 * (by_year.loc[last, "rate"] - by_year.loc[last - 1, "rate"])
    return {"rate": rate, "n": int(p[n].sum()), "n_nc": int(p[nc].sum()), "delta_pp": delta, "last": last}


def communes_with_nc(f: Filters, kind: str = "bact") -> dict:
    """Communes (current) with at least one officially non-compliant sample over the period."""
    d = commune_year_typed()
    d = d[_years(d, f) & commune_mask(d, f)]
    g = d.groupby("insee_current").agg(n=(f"n_{kind}", "sum"), nc=(f"n_{kind}_nc", "sum"),
                                        pop=("population", "first"))
    g = g[g["n"] > 0]
    hit = g[g["nc"] > 0]
    return {"n_communes": len(g), "n_hit": len(hit), "share": len(hit) / max(len(g), 1),
            "pop_hit": float(hit["pop"].sum()), "pop_all": float(g["pop"].sum())}


def scored_communes(f: Filters) -> pd.DataFrame:
    d = communes()
    d = d[d["is_current"] & d["score"].notna()]
    return d[commune_mask(d, f)]


def dept_variable(f: Filters, variable: str | None = None) -> pd.DataFrame:
    """Per department over the period: share of network-years with at least one exceedance of the variable."""
    v = variable or f.variable
    t = load_table("dept_family_year")
    t = t[(t["variable"] == v) & _years(t, f)]
    g = t.groupby("dep", as_index=False)[["n_networks", "n_networks_exceed"]].sum()
    g["share"] = g["n_networks_exceed"] / g["n_networks"]
    g = g.merge(departments(), on="dep", how="left")
    return g[dept_mask(g, f)]


def national_variable_by_year(f: Filters, variable: str | None = None) -> pd.DataFrame:
    """Share of networks with at least one exceedance per year, France and the selected region."""
    v = variable or f.variable
    t = load_table("dept_family_year")
    t = t[t["variable"] == v]
    out = [t.groupby("annee", as_index=False)[["n_networks", "n_networks_exceed"]].sum().assign(scope="France")]
    if f.region is not None:
        r = t[dept_mask(t, f)]
        out.append(r.groupby("annee", as_index=False)[["n_networks", "n_networks_exceed"]].sum()
                   .assign(scope=f.region_name))
    d = pd.concat(out, ignore_index=True)
    d["share"] = d["n_networks_exceed"] / d["n_networks"]
    d["partial"] = d["annee"] == config.PARTIAL_YEAR
    return d


def dept_scores(f: Filters) -> pd.DataFrame:
    """Median current score of the scored communes of each department (with the commune-type filter)."""
    d = scored_communes(f)
    g = d.groupby("dep").agg(median_score=("score", "median"), n_communes=("insee", "size"),
                             share_de=("grade", lambda s: s.isin(["D", "E"]).mean())).reset_index()
    return g.merge(departments(), on="dep", how="left")


def render_kpis(f: Filters) -> None:
    """Metrics header tied to the filters (period, region, type of commune), with deltas and help texts."""
    import streamlit as st

    from utils.viz import fmt_int, headline, pct

    bact = sample_compliance(f, "bact")
    chem = sample_compliance(f, "chem")
    hit = communes_with_nc(f, "bact")
    sc = scored_communes(f)

    def delta(k):
        return None if k["delta_pp"] is None else f"{k['delta_pp']:+.2f} pp vs {k['last'] - 1}"

    headline(f"{pct(bact['rate'])} of bacteriological samples and {pct(chem['rate'])} of chemical samples complied "
             f"with the health limits ({f.scope_label}, {f.period_label}).")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Bacteriological samples compliant", pct(bact["rate"], 2), delta(bact), border=True,
              help=f"Share of the {fmt_int(bact['n'])} samples that the ARS declared compliant with the bacteriological "
                   f"limits (E. coli, enterococci). Delta = {bact['last']} vs the year before, in percentage points. "
                   "Filters: period, region.")
    c2.metric("Chemical samples compliant", pct(chem["rate"], 2), delta(chem), border=True,
              help=f"Share of the {fmt_int(chem['n'])} samples declared compliant with the chemical limits (samples "
                   "under a temporary derogation count as compliant, as in the official conclusion). "
                   "Filters: period, region.")
    c3.metric("Communes with ≥ 1 bacterial non-compliance", fmt_int(hit["n_hit"]),
              f"{pct(hit['share'])} of {fmt_int(hit['n_communes'])} communes", delta_color="off", border=True,
              help=f"Communes served by a network where at least one sample was non-compliant over the period. They "
                   f"have {hit['pop_hit'] / 1e6:.1f} million inhabitants — an upper bound: a commune is counted whole "
                   "even if only one of its networks or districts was affected. Filters: period, region, type.")
    c4.metric("Median score of communes (now)", f"{sc['score'].median():.0f}/100" if len(sc) else "—",
              f"{pct(sc['grade'].isin(['D', 'E']).mean())} graded D or E" if len(sc) else None, delta_color="off",
              border=True, help="Current score (last 12/36 months to 31/08/2026), whatever the period. "
                                "Filters: region, type of commune.")

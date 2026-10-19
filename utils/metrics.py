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


def yearly_rates(f: Filters) -> pd.DataFrame:
    """Non-compliance rates per year (bacteria, chemistry) for the region filter."""
    dy = load_table("dept_year")
    d = dy[dept_mask(dy, f)].groupby("annee")[["n_bact", "n_bact_nc", "n_chem", "n_chem_nc"]].sum()
    d["bact"] = d["n_bact_nc"] / d["n_bact"]
    d["chem"] = d["n_chem_nc"] / d["n_chem"]
    return d.reset_index()


def render_kpis(f: Filters, explain: bool = True) -> None:
    """Metrics header tied to the filters, then (explain=True) how to read each number and whether it improves."""
    import streamlit as st

    from utils.i18n import num, pct, pp, t
    from utils.viz import headline

    bact = sample_compliance(f, "bact")
    chem = sample_compliance(f, "chem")
    hit = communes_with_nc(f, "bact")
    sc = scored_communes(f)

    def delta(k):
        return None if k["delta_pp"] is None else t("kpi.delta", d=pp(k["delta_pp"]), y=k["last"] - 1)

    headline(t("kpi.headline", period=f.period_label, scope=f.scope_label, bact=pct(bact["rate"]),
               chem=pct(chem["rate"])))
    r1, r2 = st.columns(2), st.columns(2)   # 2 x 2: values stay readable on medium screens
    c1, c2, c3, c4 = r1[0], r1[1], r2[0], r2[1]
    c1.metric(t("kpi.bact"), pct(bact["rate"], 2), delta(bact), border=True, help=t("kpi.bact.help", n=num(bact["n"])))
    c2.metric(t("kpi.chem"), pct(chem["rate"], 2), delta(chem), border=True, help=t("kpi.chem.help", n=num(chem["n"])))
    c3.metric(t("kpi.hit"), num(hit["n_hit"]), t("kpi.hit.delta", share=pct(hit["share"]), n=num(hit["n_communes"])),
              delta_color="off", border=True, help=t("kpi.hit.help"))
    c4.metric(t("kpi.score"), f"{sc['score'].median():.0f}/100" if len(sc) else "?",
              t("kpi.score.delta", share=pct(sc["grade"].isin(["D", "E"]).mean())) if len(sc) else None,
              delta_color="off", border=True, help=t("kpi.score.help"))
    if not explain:
        return
    c1, c2 = st.columns(2)
    c1.markdown(t("kpi.read.bact"))
    c1.markdown(t("kpi.read.chem"))
    c2.markdown(t("kpi.read.hit", pop=num(hit["pop_hit"] / 1e6, 1)))
    c2.markdown(t("kpi.read.score"))
    y0, y1 = f.years[0], min(f.years[1], config.COMPLETE_YEARS[-1])
    r = yearly_rates(f).set_index("annee")
    if y1 <= y0 or y0 not in r.index or y1 not in r.index:
        st.markdown(t("kpi.trend.short"))
        return
    b0, b1, c0, c1_ = r.loc[y0, "bact"], r.loc[y1, "bact"], r.loc[y0, "chem"], r.loc[y1, "chem"]
    msg = t("kpi.trend.better_bact" if b1 < b0 else "kpi.trend.worse_bact", a=pct(b0, 2), b=pct(b1, 2), y0=y0, y1=y1)
    msg += " " + t("kpi.trend.chem_up" if c1_ > c0 else "kpi.trend.chem_down", a=pct(c0, 2), b=pct(c1_, 2), y0=y0)
    st.markdown(msg)


def town_causes(insee: str) -> dict:
    """What pulls the score of a town down, family by family, from its networks (current windows):
    {"micro": (n_nc, n), "chem": code or None, "comfort": code or None}."""
    from utils.io import commune_network_links
    links = commune_network_links()
    nets = links.loc[links["insee"] == insee, "cdreseau"]
    u = load_table("udi_scores").set_index("cdreseau").reindex(nets).dropna(subset=["score"])
    out = {"micro": (int(u["n_bact_nc"].sum()), int(u["n_bact"].sum()))}
    for k in ("chem", "comfort"):
        w = u[u[f"worst_{k}_penalty"] > 0].sort_values(f"worst_{k}_penalty", ascending=False)
        out[k] = w[f"worst_{k}_code"].iloc[0] if len(w) else None
    return out

"""How to read a water test: samples, results, thresholds, families, and how often each threshold is crossed."""
import plotly.graph_objects as go
import streamlit as st

import config
from utils.filters import get_filters
from utils.i18n import num, pct, t
from utils.io import load_table
from utils.score import label
from utils.viz import FAMILY_COLORS, chart, headline, kicker, layout, lede

f = get_filters()
kicker(t("read.kicker"))
st.title(t("read.title"))
lede(t("read.lede"))

rs = load_table("dq_result_status")
nq = rs.loc[rs["status"] == "not_quantified", "n"].sum() / rs["n"].sum()
st.markdown(t("read.p1"))
st.markdown(t("read.p2", share=pct(nq, 0)))
st.markdown(t("read.p3"))

# --- Families ---------------------------------------------------------------------------------------
cat = load_table("params_catalog")
kicker(t("read.families.kicker"))
st.header(t("read.families.title"))
for fam in ("micro", "chem", "comfort", "info"):
    st.markdown(t(f"read.fam.{fam}") + " " + t("read.fam.count", n=num((cat["family"] == fam).sum()),
                                                 total=num(len(cat))))
st.caption(t("read.fam.sources"))

# --- How often each threshold is crossed ---------------------------------------------------------------
year = min(f.years[1], config.COMPLETE_YEARS[-1])
py = load_table("param_year")
y = py[py["annee"] == year]
KEYS = {"ECOLI": "micro", "STRF": "micro",
        "NO3": "chem", "PESTOT": "chem", "CLDZ_D": "chem", "ADET": "chem", "SPFAS": "chem", "AS": "chem", "PB": "chem",
        "CLVYL": "chem", "THM4": "chem", "BRATE": "chem",
        "CTF": "comfort", "TURBNFU": "comfort", "FET": "comfort", "MN": "comfort", "ALTMICR": "comfort",
        "471811R": "comfort", "MTCESA": "comfort"}
g = (y[y["code_merged"].isin(KEYS)].groupby("code_merged")
     .agg(n=("n_samples", "sum"), lim=("n_exceed_limit", "sum"), ind=("n_exceed_indicative", "sum"),
          ref=("n_exceed_reference", "sum"), thr=("typical_threshold", "first"),
          kind=("typical_threshold_kind", "first")).reset_index())
g["n_exceed"] = g["lim"] + g["ind"] + g["ref"]
g["share"] = g["n_exceed"] / g["n"]
g["family"] = g["code_merged"].map(KEYS)
labels = dict(zip(cat["code"], cat["label"]))
g["label"] = g["code_merged"].map(lambda c: label(c, labels))
g = g.sort_values("share")

kicker(t("read.chart.kicker"))
top = g.iloc[-1]
headline(t("read.chart.headline", year=year, label=top["label"], share=pct(top["share"]),
           k=int((g["share"] < 0.01).sum()), n=len(g)))
fig = go.Figure()
for fam in ("micro", "chem", "comfort"):
    d = g[g["family"] == fam]
    hover = [t("read.chart.hover", label=lab, k=num(k), n=num(n), kind=t(f"read.kind.{kd}"), thr=f"{thr:g}")
             for lab, k, n, kd, thr in zip(d["label"], d["n_exceed"], d["n"], d["kind"], d["thr"])]
    fig.add_trace(go.Bar(y=d["label"], x=100 * d["share"], orientation="h", name=t(f"fam.{fam}"),
                         marker_color=FAMILY_COLORS[fam], text=[pct(v, 2) for v in d["share"]],
                         textposition="outside", hovertext=hover, hoverinfo="text"))
layout(fig, t("read.chart.x"), None, height=580)
fig.update_layout(barmode="overlay", yaxis=dict(categoryorder="array", categoryarray=g["label"].tolist()))
fig.update_xaxes(range=[0, 100 * g["share"].max() * 1.25])
chart(fig, t("read.chart.title", year=year), t("read.chart.caption"), t("read.chart.take"))

with st.expander(t("read.table.title")):
    unit = [cat.set_index("code")["limit_unit"].get(c) if k == "limit" else
            cat.set_index("code")["ref_unit"].get(c) if k == "reference" else "µg/L"
            for c, k in zip(g["code_merged"], g["kind"])]
    tbl = g.assign(fam=g["family"].map(lambda x: t(f"fam.{x}")), kd=g["kind"].map(lambda x: t(f"read.kind.{x}")),
                   unit=unit)[["label", "fam", "thr", "kd", "unit"]]
    tbl.columns = [t("read.col.param"), t("read.col.family"), t("read.col.thr"), t("read.col.kind"), t("read.col.unit")]
    st.dataframe(tbl.sort_values([t("read.col.family"), t("read.col.param")]), hide_index=True)

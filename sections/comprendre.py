# Parameter reading guide: educational concepts, parameter search engine, and fact sheets.
"""How to read a water test: the basics, a search engine of parameters with sourced fact sheets, how often each
threshold is crossed, and the thresholds used."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import config
from utils.filters import get_filters
from utils.i18n import lang, num, pct, t
from utils.io import cached_resource, load_table
from utils.score import label
from utils.texts.factsheets import FACTS, FIELDS, SOURCES
from utils.viz import FAMILY_COLORS, chart, headline, kicker, layout, lede, takeaway

f = get_filters()
kicker(t("read.kicker"))
st.title(t("read.title"))
lede(t("read.lede"))

rs = load_table("dq_result_status")
nq = rs.loc[rs["status"] == "not_quantified", "n"].sum() / rs["n"].sum()
st.markdown(t("read.p1"))
st.markdown(t("read.p2", share=pct(nq, 0)))
st.markdown(t("read.p3"))

cat = load_table("params_catalog")
cat_labels = dict(zip(cat["code"], cat["label"]))
py = load_table("param_year")
last = config.COMPLETE_YEARS[-1]


@cached_resource
def param_totals() -> pd.DataFrame:
    """Per merged code and year: samples, quantified, above threshold, highest value (twin codes added up)."""
    d = load_table("param_year")
    d = d.assign(exceed=d["n_exceed_limit"] + d["n_exceed_indicative"] + d["n_exceed_reference"])
    return (d.groupby(["code_merged", "annee"])
            .agg(n=("n_samples", "sum"), det=("n_detected", "sum"), exc=("exceed", "sum"), mx=("max_value", "max"),
                 thr=("typical_threshold", "first"), kind=("typical_threshold_kind", "first")).reset_index())


def fmt_value(v) -> str:
    """Format numeric measurement value with localized decimal separator."""
    if v is None or pd.isna(v):
        return "?"
    s = f"{v:.3g}"
    return s.replace(".", ",") if lang() == "fr" else s


# --- Search engine ----------------------------------------------------------------------------------
kicker(t("read.search.kicker"))
st.header(t("read.search.title"))
st.markdown(t("read.search.text", n=num(len(cat))))
codes_fact = list(FACTS)
others = (cat[~cat["code_merged"].isin(codes_fact) & (cat["code"] == cat["code_merged"])]
          .assign(lab=lambda d: d["code"].map(lambda c: label(c, cat_labels)))
          .sort_values("lab")["code"].tolist())
options = codes_fact + others
opt_labels = {c: f"{label(c, cat_labels)} ({c})" for c in options}
code = st.selectbox(t("read.search.box"), options, index=codes_fact.index("NO3"), format_func=opt_labels.get,
                    key="param_pick", help=t("read.search.help"))

row = cat.set_index("code").loc[code] if code in set(cat["code"]) else None
tot = param_totals()
h = tot[tot["code_merged"] == code]
with st.container(border=True):
    fam = row["family"] if row is not None else "info"
    st.subheader(label(code, cat_labels))
    st.caption(t("read.fs.family", fam=t(f"fam.{fam}")))
    if code in FACTS:
        sheet = FACTS[code]
        for field in FIELDS:
            st.markdown(f"**{t('read.fs.' + field)}.** {sheet[field][lang()]}")
    else:
        st.info(t("read.fs.none"))
        unit = row["unit"] if row is not None and isinstance(row["unit"], str) else "?"
        thr = row["limit_max"] if row is not None and pd.notna(row["limit_max"]) else (
            row["ref_max"] if row is not None and pd.notna(row["ref_max"]) else None)
        st.markdown(t("read.fs.meta", label=cat_labels.get(code, code), fam=t(f"fam.{fam}"), unit=unit,
                      thr=t("read.fs.nothr") if thr is None else fmt_value(thr),
                      n=num(row["n_results"]) if row is not None else "0",
                      d=num(row["n_detected"]) if row is not None else "0",
                      y0=int(row["first_year"]) if row is not None else "?",
                      y1=int(row["last_year"]) if row is not None else "?"))
    # what the data says (computed for every parameter)
    if len(h):
        unit = row["unit"] if row is not None and isinstance(row["unit"], str) else ""
        n_all = h.loc[h["annee"] <= last, "n"].sum()
        first = int(h.loc[h["n"] > 0, "annee"].min())
        y = h[h["annee"] == last]
        if y.empty or y["n"].iloc[0] == 0:
            text = t("read.fs.notlast", n=num(n_all), first=first, last=last)
        else:
            y = y.iloc[0]
            if pd.notna(y["thr"]):
                text = t("read.fs.datatext", n=num(n_all), last=last, first=first, k=num(y["exc"]), m=num(y["n"]),
                         thr=f"{fmt_value(y['thr'])} {unit}", share=pct(y["exc"] / y["n"], 2), max=fmt_value(y["mx"]),
                         unit=unit)
            else:
                text = t("read.fs.datatext.nothr", n=num(n_all), last=last, first=first, d=num(y["det"]),
                         m=num(y["n"]), max=fmt_value(y["mx"]), unit=unit)
        st.markdown(f"**{t('read.fs.data')}.** {text}")
    if code in FACTS:
        links = " · ".join(f"[{SOURCES[s][0]}]({SOURCES[s][1]})" for s in FACTS[code]["sources"])
        st.caption(f"{t('read.fs.sources')} (docs/sources.md): {links}")

# --- Families ---------------------------------------------------------------------------------------
kicker(t("read.families.kicker"))
st.header(t("read.families.title"))
for fam_ in ("micro", "chem", "comfort", "info"):
    st.markdown(t(f"read.fam.{fam_}") + " " + t("read.fam.count", n=num((cat["family"] == fam_).sum()),
                                                  total=num(len(cat))))
st.caption(t("read.fam.sources"))

# --- How often each threshold is crossed ---------------------------------------------------------------
year = min(f.years[1], last)
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
g["label"] = g["code_merged"].map(lambda c: label(c, cat_labels))
g = g.sort_values("share")

kicker(t("read.chart.kicker"))
st.markdown(t("read.chart.intro"))
top = g.iloc[-1]
headline(t("read.chart.headline", year=year, label=top["label"], share=pct(top["share"]),
           k=int((g["share"] < 0.01).sum()), n=len(g)))
fig = go.Figure()
for fam_ in ("micro", "chem", "comfort"):
    d = g[g["family"] == fam_]
    hover = [t("read.chart.hover", label=lab, k=num(k), n=num(n), kind=t(f"read.kind.{kd}"), thr=f"{thr:g}")
             for lab, k, n, kd, thr in zip(d["label"], d["n_exceed"], d["n"], d["kind"], d["thr"])]
    fig.add_trace(go.Bar(y=d["label"], x=100 * d["share"], orientation="h", name=t(f"fam.{fam_}"),
                         marker_color=FAMILY_COLORS[fam_], text=[pct(v, 2) for v in d["share"]],
                         textposition="outside", hovertext=hover, hoverinfo="text"))
layout(fig, t("read.chart.x"), None, height=580)
fig.update_layout(barmode="overlay", yaxis=dict(categoryorder="array", categoryarray=g["label"].tolist()))
fig.update_xaxes(range=[0, 100 * g["share"].max() * 1.25])
chart(fig, t("read.chart.title", year=year), t("read.chart.caption"), t("read.chart.take"))

st.markdown(f'<div class="ar-chart-title">{t("read.table.title")}</div>', unsafe_allow_html=True)
st.markdown(t("read.table.intro"))
cat_i = cat.set_index("code")
unit = [cat_i["limit_unit"].get(c) if k == "limit" else cat_i["ref_unit"].get(c) if k == "reference" else "µg/L"
        for c, k in zip(g["code_merged"], g["kind"])]
tbl = g.assign(fam=g["family"].map(lambda x: t(f"fam.{x}")), kd=g["kind"].map(lambda x: t(f"read.kind.{x}")),
               unit=unit)[["label", "fam", "thr", "kd", "unit"]]
tbl.columns = [t("read.col.param"), t("read.col.family"), t("read.col.thr"), t("read.col.kind"), t("read.col.unit")]
st.dataframe(tbl.sort_values([t("read.col.kind"), t("read.col.param")]), hide_index=True)
takeaway(t("read.table.take"))

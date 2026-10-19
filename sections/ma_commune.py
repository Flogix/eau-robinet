"""The water of my town: one searchable list, score, gauge, sub-scores, the report per network, history."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import config
from utils import score as S
from utils.i18n import lang, num, t, tn
from utils.io import commune_network_links, communes, load_table, network_history, town_options
from utils.viz import (BRICK, FAMILY_COLORS, GRADE_COLORS, SERIES, badge, chart, headline, kicker, layout, lede,
                       partial_year, threshold)

kicker(t("town.kicker"))
st.title(t("town.title"))
lede(t("town.lede"))

DEFAULT_INSEE = "75056"   # Paris
options, labels = town_options()


def _sync_choice():
    st.session_state["insee"] = st.session_state["town_pick"]


current = st.session_state.get("insee") or st.query_params.get("insee") or DEFAULT_INSEE
if current not in labels:
    current = DEFAULT_INSEE
if st.session_state.get("town_pick") != current:
    st.session_state["town_pick"] = current
st.selectbox(t("town.pick"), options, format_func=labels.get, key="town_pick", on_change=_sync_choice,
             help=t("town.pick.help"))
insee = st.session_state["town_pick"]
st.session_state["insee"] = insee
st.query_params["insee"] = insee

com = communes().set_index("insee")
c = com.loc[insee]
udi = load_table("udi_scores").set_index("cdreseau")
links = commune_network_links()
nets = links[links["insee"] == insee]
names = load_table("dim_udi").set_index("cdreseau")["nomreseau"]

facts = [t("town.facts.pop", n=num(c["population"])) if pd.notna(c["population"]) else None,
         t(f"dens7.{int(c['density7'])}") if pd.notna(c.get("density7")) else None, t("town.facts.mountain") if c.get("mountain") else None,
         t("town.facts.med") if c.get("mediterranean_coast") else None, tn("town.facts.nets", len(nets), n=len(nets))]
st.caption(" · ".join(str(x) for x in facts if x))

if pd.isna(c.get("score")):
    st.warning(t("town.noscore"))
    st.stop()

# --- Score --------------------------------------------------------------------------------------------
town, grade, score = c["nom"], c["grade"], float(c["score"])
fmt1 = (lambda v: f"{v:.1f}".replace(".", ",")) if lang() == "fr" else (lambda v: f"{v:.1f}")
headline(t("town.headline", town=town, score=fmt1(score), grade=grade, conf=t(f"conf.{c['confidence']}")))
st.markdown(t("town.how"))

median = communes()["score"].median()
left, right = st.columns([1, 1.25])
with left:
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=round(score, 1),
        number=dict(suffix="/100", valueformat=".1f", font=dict(family="IBM Plex Mono")),
        title=dict(text=f"{t('grade')} <b>{grade}</b>"),
        gauge=dict(axis=dict(range=[0, 100], tickvals=[0, 40, 60, 75, 90, 100]),
                   bar=dict(color="#8A8578", thickness=0.3),
                   steps=[dict(range=[lo, hi], color=GRADE_COLORS[g]) for lo, hi, g in
                          ((0, 40, "E"), (40, 60, "D"), (60, 75, "C"), (75, 90, "B"), (90, 100, "A"))])))
    fig.update_layout(height=260, margin=dict(l=30, r=40, t=50, b=10), font=dict(family="IBM Plex Sans"))
    gap = abs(score - median)
    take = t("town.gauge.take.above" if score >= median else "town.gauge.take.below", median=fmt1(median),
             town=town, gap=fmt1(gap))
    chart(fig, t("town.gauge.title", town=town), t("town.gauge.caption"), take)
with right:
    fams = ["micro", "chem", "comfort"]
    vals = [c[k] for k in fams]
    ylab = [t("town.subs.weight", fam=t(f"fam.{k}"), w=f"{int(100 * config.WEIGHTS[k])}%") for k in fams]
    fig = go.Figure(go.Bar(x=[0 if pd.isna(v) else v for v in vals], y=ylab, orientation="h",
                           marker_color=[FAMILY_COLORS[k] for k in fams],
                           text=[f"{v:.0f}" if pd.notna(v) else t("town.notmeasured") for v in vals],
                           textposition="outside", hoverinfo="skip"))
    layout(fig, t("town.subs.x"), None, height=260, legend=False)
    fig.update_xaxes(range=[0, 118])
    fig.update_yaxes(autorange="reversed")
    measured = {k: v for k, v in zip(fams, vals) if pd.notna(v)}
    weakest = min(measured, key=measured.get)
    take = (t("town.subs.take.perfect") if measured[weakest] >= 99.95 else
            t("town.subs.take", fam=t(f"fam.{weakest}").lower(), v=f"{measured[weakest]:.0f}", town=town))
    chart(fig, t("town.subs.title"), t("town.subs.caption"), take)

# --- Report per network ---------------------------------------------------------------------------------
kicker(t("town.why.kicker"))
st.header(t("town.why.title"))
n = nets.merge(udi.reset_index(), on="cdreseau", how="left")
n["name"] = n["cdreseau"].map(names).fillna(n["cdreseau"])
if len(n) > 1:
    st.markdown(t("town.why.several", town=town, n=len(n)))
    tbl = n[["name", "cdreseau", "score", "grade", "confidence", "n_bact", "districts"]].sort_values("score").copy()
    tbl["confidence"] = tbl["confidence"].map(lambda x: t(f"conf.{x}") if isinstance(x, str) else "")
    tbl["districts"] = tbl["districts"].fillna("")
    tbl.columns = [t("town.col.net"), t("town.col.code"), t("town.col.score"), t("town.col.grade"), t("town.col.conf"),
                   t("town.col.nbact"), t("town.col.districts")]
    st.dataframe(tbl, hide_index=True, column_config={t("town.col.score"): st.column_config.NumberColumn(format="%.1f")})
else:
    st.markdown(t("town.why.one", town=town))

params = load_table("udi_param_window")
fam = load_table("udi_family_window")
p95 = load_table("udi_param_p95")
cat = load_table("params_catalog")
cat_labels = dict(zip(cat["code"], cat["label"]))
ranges = S.reference_ranges(cat)
ordered = n.sort_values("score")
tabs = st.tabs([f"{r['name']} · {r['score']:.0f} ({r['grade']})" if pd.notna(r["score"])
                else t("town.tab.nodata", net=r["name"]) for _, r in ordered.iterrows()])
for tab, (_, r) in zip(tabs, ordered.iterrows()):
    with tab:
        if pd.isna(r["score"]):
            st.write(t("town.nodata"))
            continue
        row = udi.loc[r["cdreseau"]].copy()
        row["cdreseau"] = r["cdreseau"]
        rep = S.why_report(row, params[params["cdreseau"] == r["cdreseau"]], fam[fam["cdreseau"] == r["cdreseau"]],
                           p95[p95["cdreseau"] == r["cdreseau"]], cat_labels, ranges=ranges)
        html = "".join(f"<p>{badge(kind)}{text}</p>" for kind, text in rep)
        st.markdown(f'<div class="ar-report">{html}</div>', unsafe_allow_html=True)
        if isinstance(r.get("districts"), str):
            st.caption(t("town.districts", d=r["districts"]))
st.caption(t("town.legend"))

# --- History ----------------------------------------------------------------------------------------------
kicker(t("town.hist.kicker"))
hist = network_history(tuple(n["cdreseau"]))
if hist.empty:
    st.info(t("town.hist.none"))
else:
    avail = hist.groupby("code")["n"].sum().sort_values(ascending=False)
    pref = [k for k in ("NO3", "PESTOT", "SPFAS", "ECOLI", "TH", "CLDZ_D", "PB", "AS") if k in avail.index]
    codes = pref + [k for k in avail.index if k not in pref]
    code_labels = {k: S.label(k, cat_labels) for k in codes}
    code = st.selectbox(t("town.hist.pick"), codes, format_func=code_labels.get, help=t("town.hist.pick.help"),
                        key="hist_code")
    h = hist[hist["code"] == code].copy()
    h["name"] = h["cdreseau"].map(names).fillna(h["cdreseau"])
    lab = S.label(code, cat_labels)
    unit = cat.set_index("code")["unit"].get(code)
    unit = unit if isinstance(unit, str) else ""
    fig = go.Figure()
    for i, (net, d) in enumerate(h.groupby("name")):
        col = SERIES[i % len(SERIES)]
        hover = [t("town.hist.hover", y=y, v=f"{v:.3g}", unit=unit, n=k1, k=k2)
                 for y, v, k1, k2 in zip(d["annee"], d["max"], d["n"], d["n_exceed"])]
        fig.add_trace(go.Scatter(x=d["annee"], y=d["max"], name=t("town.hist.max", net=net), mode="lines+markers",
                                 line=dict(color=col, width=2.2), marker=dict(size=8), hovertext=hover,
                                 hoverinfo="text"))
        fig.add_trace(go.Scatter(x=d["annee"], y=d["mean"], name=t("town.hist.mean", net=net), mode="lines",
                                 line=dict(color=col, width=1.6, dash="dot"), hoverinfo="skip"))
    thr = h["threshold"].dropna()
    thr_part = ""
    if len(thr):
        kind = t(f"town.kind.{h['threshold_kind'].dropna().iloc[-1]}")
        threshold(fig, float(thr.iloc[-1]), f"{kind} {thr.iloc[-1]:g} {unit}", color=BRICK)
        thr_part = t("town.hist.thr_part", kind=kind, thr=f"{thr.iloc[-1]:g}", unit=unit)
    if h["annee"].max() == config.PARTIAL_YEAR:
        partial_year(fig, config.PARTIAL_YEAR, t("common.partial2026"))
    layout(fig, t("common.year"), f"{lab} ({unit})" if unit else lab, height=400)
    fig.update_xaxes(dtick=1)
    top = h.loc[h["max"].idxmax()]
    chart(fig, t("town.hist.title", param=lab, town=town), t("town.hist.caption"),
          t("town.hist.take", max=f"{top['max']:.3g}", unit=unit, year=int(top["annee"]), thr_part=thr_part))

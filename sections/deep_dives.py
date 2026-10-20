"""What we look for, what we find: H3 told as three clues, then nitrates, PFAS, seasons, hardness (H4), what-if."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import config
from utils import score as S
from utils.filters import get_filters
from utils.i18n import lang, months, num, pct, t
from utils.io import departments, dep_of_network, load_table
from utils.viz import (BLUE, BRICK, LIGHT_NEUTRAL, NEUTRAL, OCHRE, PLUM, TEAL, analysis, chart, event, headline,
                       kicker, layout, lede, threshold)

f = get_filters()
kicker(t("mon.kicker"))
st.title(t("mon.title"))
lede(t("mon.lede"))
py = load_table("param_year")
ny = load_table("national_year")
nc = ny.set_index("annee")["n_chem_nc"]

# --- exceedances by group of substances ------------------------------------------------------------------------
GROUPS = {"CLDZ_D": "cldz", "CLDZ_MD": "cldz", "MTCESA": "esa", "MTCNOA": "esa", "471811R": "chlo", "CLTHALS": "chlo",
          "NO3": "no3", "NO2": "no3", "NO3_NO2": "no3"}
ORDER = ["cldz", "esa", "chlo", "pest", "no3", "other"]
COLORS = {"cldz": BRICK, "esa": OCHRE, "chlo": PLUM, "pest": TEAL, "no3": BLUE, "other": LIGHT_NEUTRAL}
chem = py[py["family"] == "chem"].copy()
chem["group"] = chem["code_merged"].map(GROUPS)
chem.loc[chem["group"].isna() & (chem["subfamily"] == "pesticides"), "group"] = "pest"
chem["group"] = chem["group"].fillna("other")
# metabolites compared with the 0.9 µg/L value are in the comfort family: keep their rows that carried a limit
twins = py[py["code"].isin(["ESAMTC", "NOAMTC", "R471811", "471811R", "MTCESA", "MTCNOA"]) & (py["family"] == "comfort")]
twins = twins.assign(group=twins["code_merged"].map(GROUPS))
by = (pd.concat([chem, twins]).groupby(["annee", "group"])["n_exceed_limit"].sum().unstack(fill_value=0)
      .reindex(columns=ORDER, fill_value=0))
meta = by.loc[2021:2024, ["cldz", "esa", "chlo"]].sum().sum() / by.loc[2021:2024].sum().sum()
headline(t("mon.headline", before=num(nc.loc[2016:2020].mean()), during=num(nc.loc[2021:2024].mean()),
           y2025=num(nc.loc[2025]), meta=pct(meta, 0)))

# --- Clue 1 ------------------------------------------------------------------------------------------------------
kicker(t("mon.s1.kicker"))
st.header(t("mon.s1.title"))
# every parameter code of the yearly file (the same count as the data dictionary and Explore the data); the tables
# of figures keep only the parameters with a numeric result, a dozen fewer each year (odour, aspect...)
n_par = load_table("explore_volume").set_index("annee")["n_params"]
n_pest = py[(py["n_samples"] > 0) & (py["subfamily"] == "pesticides")].groupby("annee")["code"].nunique()
ch = load_table("explore_param_changes").pivot(index="group", columns="change", values="n").fillna(0).astype(int)
st.markdown(t("mon.s1.text", a=num(n_par.loc[2016]), b=num(n_par.loc[2025]), new=num(ch["new"].sum()),
              gone=num(ch["gone"].sum()), pest=num(ch.loc["pesticides", "new"]), cyano=num(ch.loc["cyanobacteria", "new"]),
              pfas=num(ch.loc["pfas", "new"]), other=num(ch.loc["other", "new"])))
fig = go.Figure()
for s_, name, color, sym in ((n_par, t("mon.s1.all"), TEAL, "circle"), (n_pest, t("mon.s1.pest"), OCHRE, "square")):
    fig.add_trace(go.Scatter(x=s_.index, y=s_.values, name=name, mode="lines+markers", line=dict(color=color, width=2.2),
                             marker=dict(size=8, symbol=sym), hoverinfo="text",
                             hovertext=[t("mon.s1.hover", y=y, v=num(v)) for y, v in zip(s_.index, s_.values)]))
layout(fig, t("common.year"), t("mon.s1.y"), height=340)
fig.update_yaxes(rangemode="tozero")
fig.update_xaxes(dtick=1)
chart(fig, t("mon.s1.chart"), t("mon.s1.caption"))
analysis(t("an.mon.s1.seen", a=num(n_par.loc[2016]), b=num(n_par.loc[2025])), t("an.mon.s1.why"), t("an.mon.s1.lim"))

# --- Clue 2 ------------------------------------------------------------------------------------------------------
kicker(t("mon.s2.kicker"))
st.header(t("mon.s2.title"))
st.markdown(t("mon.s2.text"))
fig = go.Figure()
for g in ORDER:
    name = t(f"mon.grp.{g}")
    fig.add_trace(go.Bar(x=by.index, y=by[g], name=name, marker_color=COLORS[g], marker_line_color="rgba(255,255,255,0.5)",
                         marker_line_width=1, hoverinfo="text",
                         hovertext=[f"{name}<br>" + t("mon.s2.hover", y=y, v=num(v)) for y, v in zip(by.index, by[g])]))
fig.add_trace(go.Scatter(x=nc.index, y=nc.values, name=t("mon.s2.official"), mode="lines+markers",
                         line=dict(color="#5E5A50", width=2.6), marker=dict(size=9, symbol="diamond"), hoverinfo="text",
                         hovertext=[t("mon.s2.hover.off", y=y, v=num(v)) for y, v in zip(nc.index, nc.values)]))
event(fig, 2020.55, t("mon.ev.cldz"), 0.99)
event(fig, 2022.75, t("mon.ev.esa"), 0.80)
event(fig, 2024.33, t("mon.ev.chlo"), 0.99)
event(fig, 2025.55, t("mon.ev.pfas"), 0.62)
fig.add_vrect(x0=config.PARTIAL_YEAR - 0.5, x1=config.PARTIAL_YEAR + 0.5, fillcolor=NEUTRAL, opacity=0.10, line_width=0)
fig.update_layout(barmode="stack")
layout(fig, t("mon.s2.x"), t("mon.s2.y"), height=540)
fig.update_xaxes(dtick=1)
chart(fig, t("mon.s2.chart"), t("mon.s2.caption"))
analysis(t("an.mon.s2.seen"), t("an.mon.s2.why"), t("an.mon.s2.lim"))

# --- Clue 3 ------------------------------------------------------------------------------------------------------
kicker(t("mon.s3.kicker"))
st.header(t("mon.s3.title"))
st.markdown(t("mon.s3.text"))
m = py[py["code_merged"].isin(["MTCESA", "471811R"])].groupby(["annee", "code_merged"])[
    ["n_samples", "n_detected", "n_exceed_limit", "n_exceed_indicative"]].sum().reset_index()
mols = {"MTCESA": S.label("MTCESA"), "471811R": S.label("471811R")}
code = st.segmented_control(t("mon.s3.pick"), list(mols), format_func=mols.get, default="MTCESA", key="h3_meta") or "MTCESA"
mm = m[m["code_merged"] == code]
fig = go.Figure()
fig.add_trace(go.Bar(x=mm["annee"], y=mm["n_exceed_limit"], name=t("mon.s3.limit"), marker_color=BRICK,
                     hovertemplate="%{x}: %{y:,}<extra></extra>"))
fig.add_trace(go.Bar(x=mm["annee"], y=mm["n_exceed_indicative"], name=t("mon.s3.ind"), marker_color=TEAL,
                     marker_pattern_shape="/", hovertemplate="%{x}: %{y:,}<extra></extra>"))
fig.add_trace(go.Scatter(x=mm["annee"], y=mm["n_detected"], name=t("mon.s3.det"), mode="lines+markers",
                         line=dict(color="#5E5A50", width=2.2, dash="dot"), marker=dict(size=8),
                         hovertemplate="%{x}: %{y:,}<extra></extra>"))
event(fig, 2022.75 if code == "MTCESA" else 2024.33, t("mon.s3.ev"), 0.99)
layout(fig, t("common.year"), t("mon.s3.y"), height=380)
fig.update_xaxes(dtick=1)
det2025 = mm.loc[mm["annee"] == 2025, "n_detected"]
chart(fig, t("mon.s3.chart", mol=mols[code]), t("mon.s3.caption"))
analysis(t("an.mon.s3.seen", n=num(det2025.iloc[0]) if len(det2025) else "?"), t("an.mon.s3.why"),
         t("an.mon.s3.lim"))
st.caption(t("mon.sources"))
st.success(t("mon.verdict"))

# --- Other things we looked at ------------------------------------------------------------------------------------
kicker(t("mon.focus.kicker"))
st.header(t("mon.focus.title"))
win = load_table("udi_param_window")
t_no3, t_pfas, t_season, t_hard = st.tabs([t("mon.tab.no3"), t("mon.tab.pfas"), t("mon.tab.season"), t("mon.tab.hard")])
with t_no3:
    no3 = win[win["code"] == "NO3"]
    headline(t("mon.no3.headline", low=pct((no3["max_value"] <= 25).mean(), 0), above=pct((no3["max_value"] > 50).mean())))
    fig = go.Figure(go.Histogram(x=no3["max_value"].clip(upper=100), xbins=dict(start=0, end=100.01, size=2.5),
                                 marker_color=BLUE, marker_line_color="rgba(255,255,255,0.6)", marker_line_width=1,
                                 hovertemplate=t("mon.no3.hover") + "<extra></extra>"))
    threshold(fig, 50, t("mon.no3.thr"), axis="x")
    layout(fig, t("mon.no3.x"), t("mon.no3.y"), height=360, legend=False)
    chart(fig, t("mon.no3.chart"), t("mon.no3.caption"))
    analysis(t("an.mon.no3.seen", low=pct((no3["max_value"] <= 25).mean(), 0), above=pct((no3["max_value"] > 50).mean())),
             t("an.mon.no3.why"), t("an.mon.no3.lim"))
with t_pfas:
    pf = py[py["code"] == "SPFAS"].set_index("annee")[["n_samples", "n_exceed_limit"]]
    headline(t("mon.pfas.headline", a=num(pf["n_samples"].get(2022, 0)), b=num(pf["n_samples"].get(2025, 0)),
               c=num(pf["n_exceed_limit"].get(2025, 0))))
    fig = go.Figure()
    fig.add_trace(go.Bar(x=pf.index, y=pf["n_samples"], name=t("mon.pfas.n"), marker_color=TEAL,
                         text=[num(v) for v in pf["n_samples"]], textposition="outside",
                         hovertemplate="%{x}: %{y:,}<extra></extra>"))
    fig.add_trace(go.Bar(x=pf.index, y=pf["n_exceed_limit"], name=t("mon.pfas.k"), marker_color=BRICK,
                         marker_pattern_shape="/", text=[num(v) for v in pf["n_exceed_limit"]], textposition="outside",
                         hovertemplate="%{x}: %{y:,}<extra></extra>"))
    event(fig, 2025.55, t("mon.ev.pfas"), 0.95)
    layout(fig, t("mon.s2.x"), t("mon.pfas.y"), height=360)
    fig.update_xaxes(dtick=1)
    chart(fig, t("mon.pfas.chart"), t("mon.pfas.caption"))
    analysis(t("an.mon.pfas.seen", a=num(pf["n_samples"].get(2022, 0)), b=num(pf["n_samples"].get(2025, 0)),
               c=num(pf["n_exceed_limit"].get(2025, 0))), t("an.mon.pfas.why"), t("an.mon.pfas.lim"))
with t_season:
    c_last = config.COMPLETE_YEARS[-1]
    m0, m1 = min(f.years[0], c_last), min(f.years[1], c_last)   # seasons need the twelve months
    if (m0, m1) != tuple(f.years):
        st.caption(t("mon.season.note", a=m0, b=m1))
    nm = load_table("national_month")
    mo = nm[nm["annee"].between(m0, m1)].groupby("month")[["n_bact", "n_bact_nc"]].sum()
    mo["rate"] = mo["n_bact_nc"] / mo["n_bact"]
    names_m = months()
    hi_m, lo_m = mo["rate"].idxmax(), mo["rate"].idxmin()
    headline(t("mon.season.headline", hi=names_m[hi_m - 1], hv=pct(mo.loc[hi_m, "rate"], 2), lo=names_m[lo_m - 1],
               lv=pct(mo.loc[lo_m, "rate"], 2), a=m0, b=m1))
    fig = go.Figure(go.Bar(x=names_m, y=100 * mo["rate"].values, marker_color=BRICK,
                           text=[pct(v, 2) for v in mo["rate"]], textposition="outside", hoverinfo="text",
                           hovertext=[t("mon.season.hover", m=mn, v=pct(v, 2), k=num(k), n=num(n))
                                      for mn, v, k, n in zip(names_m, mo["rate"], mo["n_bact_nc"], mo["n_bact"])]))
    layout(fig, t("mon.season.x"), t("mon.season.y"), height=360, legend=False)
    fig.update_yaxes(range=[0, 100 * mo["rate"].max() * 1.2])
    ratio = mo.loc[hi_m, "rate"] / mo.loc[lo_m, "rate"]
    chart(fig, t("mon.season.chart"), t("mon.season.caption"))
    analysis(t("an.mon.season.seen", ratio=f"{ratio:.1f}".replace(".", ",") if lang() == "fr" else f"{ratio:.1f}",
               hi=names_m[hi_m - 1], lo=names_m[lo_m - 1]), t("an.mon.season.why"), t("an.mon.season.lim"))
with t_hard:
    th = win[win["code"] == "TH"][["cdreseau", "mean"]].copy()
    th["dep"] = dep_of_network(th["cdreseau"].astype(str))
    th = th.merge(departments(), on="dep", how="left").dropna(subset=["reg_nom"])
    med = th.groupby("reg_nom")["mean"].median().sort_values()
    st.markdown(t("mon.hard.text"))
    headline(t("mon.hard.headline", lo_v=f"{med.iloc[0]:.0f}", lo=med.index[0], hi_v=f"{med.iloc[-1]:.0f}",
               hi=med.index[-1]))
    fig = go.Figure()
    for reg in med.index:
        fig.add_trace(go.Box(x=th.loc[th["reg_nom"] == reg, "mean"], name=reg, orientation="h", boxpoints=False,
                             marker_color=OCHRE, hoverinfo="x+name"))
    layout(fig, t("mon.hard.x"), None, height=580, legend=False)
    chart(fig, t("mon.hard.chart"), t("mon.hard.caption"))
    analysis(t("an.mon.hard.seen", lo_v=f"{med.iloc[0]:.0f}", lo=med.index[0], hi_v=f"{med.iloc[-1]:.0f}",
               hi=med.index[-1]), t("an.mon.hard.why"), t("an.mon.hard.lim"))

# --- What if: the interactive version lives on the page "Build your own score" ----------------------------------------
kicker(t("mon.whatif.kicker"))
st.header(t("mon.whatif.title"))
st.markdown(t("mon.whatif.link.text"))
st.page_link("sections/mon_score.py", label=t("mon.whatif.link"), icon=":material/tune:")

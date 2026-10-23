# France overview map page: choropleth maps, departmental rankings, and regional distributions.
"""The map of France: KPIs, department map, rankings, H2 (two maps), H1 (small networks), distribution, trend."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import config
from utils import metrics
from utils.filters import OFFICIAL, dept_mask, get_filters, page_controls
from utils.i18n import lang, num, pct, t
from utils.io import dep_of_network, departments, departments_geojson, load_table
from utils.score import label
from utils.viz import (BLUE, BRICK, GRADE_COLORS, NEUTRAL, OCHRE, TEAL, chart, headline, kicker, layout, lede,
                       partial_year)

f = get_filters()
kicker(t("map.kicker"))
st.title(t("map.title"))
lede(t("map.lede"))
metrics.render_kpis(f, explain=False)
st.caption(t("map.kpi.note"))
fmt1 = (lambda v: f"{v:.1f}".replace(".", ",")) if lang() == "fr" else (lambda v: f"{v:.1f}")

# --- Map ------------------------------------------------------------------------------------------------
SCORE_VIEWS = ["score_all", "score_micro", "score_chem", "score_comfort"]
PERIOD_VIEWS = ["bact_official", "chem_official", "pesticides", "nitrates", "pfas", "metals", "disinfection_byproducts",
                "comfort"]
HYP = {"score_all": "score_all", "score_micro": "micro", "bact_official": "micro", "score_chem": "chem",
       "chem_official": "chem", "pesticides": "chem", "nitrates": "nitrates", "pfas": "pfas", "metals": "metals",
       "disinfection_byproducts": "dbp", "score_comfort": "comfort", "comfort": "comfort"}
TREND_VAR = {"score_all": "chem_official", "score_micro": "bact_official", "score_chem": "chem_official",
             "score_comfort": "comfort"}
view_labels = {**{v: t(f"map.view.{v}") for v in SCORE_VIEWS},
               **{v: f"{t('var.' + v)}, {f.period_label}" for v in PERIOD_VIEWS}}
with page_controls():   # the brief's "variable selection" lives in the sidebar, with the other filters
    view = st.selectbox(t("map.view"), SCORE_VIEWS + PERIOD_VIEWS, format_func=view_labels.get, key="map_view",
                        help=t("map.view.help"))
by_score = view in SCORE_VIEWS
variable = TREND_VAR.get(view, view)
if by_score:
    col = {"score_all": "score", "score_micro": "micro", "score_chem": "chem", "score_comfort": "comfort"}[view]
    sc_all = metrics.scored_communes(f)
    d = (sc_all.groupby("dep").agg(value=(col, "median"), n=("insee", "size")).reset_index()
         .merge(departments(), on="dep", how="left"))
    d = d[d["n"] >= 5].copy()
    hover = [t("map.hover.score", dep=f"{nm} ({c})", v=fmt1(v), n=num(n))
             for nm, c, v, n in zip(d["dep_nom"], d["dep"], d["value"], d["n"])]
    value_label = t("map.value.score") if view == "score_all" else t("map.value.subscore")
    scale = [[0, "#E8E2D4"], [1, "#0E5A61"]]
else:
    d = metrics.dept_variable(f, variable)
    d = d[d["n_networks"] >= 10].copy()
    d["value"], d["n"] = 100 * d["share"], d["n_networks"]
    hover = [t("map.hover.var", dep=f"{nm} ({c})", v=pct(v / 100), n=num(n))
             for nm, c, v, n in zip(d["dep_nom"], d["dep"], d["value"], d["n"])]
    value_label, scale = t("map.value.var"), [[0, "#F2E6DC"], [1, "#8C2D1C"]]
d["hover"] = hover
metro = d[~d["dep"].str.startswith("97")]
overseas = d[d["dep"].str.startswith("97")]
fmt_v = (lambda v: fmt1(v)) if by_score else (lambda v: pct(v / 100))

if not metro.empty:
    hi, lo = metro.loc[metro["value"].idxmax()], metro.loc[metro["value"].idxmin()]
    if by_score:
        headline(t("map.headline.score", lo=lo["dep_nom"], lo_v=f"{lo['value']:.0f}", hi=hi["dep_nom"],
                   hi_v=f"{hi['value']:.0f}"))
    else:
        headline(t("map.headline.var", var=t("var." + view), lo=lo["dep_nom"], lo_v=pct(lo["value"] / 100),
                   hi=hi["dep_nom"], hi_v=pct(hi["value"] / 100), period=f.period_label))
    fig = go.Figure(go.Choropleth(
        geojson=departments_geojson(), featureidkey="properties.code", locations=metro["dep"], z=metro["value"],
        colorscale=scale, marker_line_color="rgba(127,127,127,0.6)", marker_line_width=0.5,
        hovertext=metro["hover"], hoverinfo="text",
        colorbar=dict(title=dict(text=value_label.replace(" (", "<br>("), side="right"), thickness=12)))
    fig.update_geos(fitbounds="locations", visible=False, bgcolor="rgba(0,0,0,0)")
    fig.update_layout(height=580, margin=dict(l=0, r=0, t=10, b=0), font=dict(family="IBM Plex Sans"))
    take = (t("map.take.score", k=int((metro["value"] >= 75).sum()), n=len(metro)) if view == "score_all"
            else None if by_score else t("map.take.var"))
    title = (t("map.title.score") if view == "score_all" else
             t("map.title.subscore", view=view_labels[view]) if by_score else
             t("map.title.var", var=t("var." + view), period=f.period_label))
    chart(fig, title, t("map.caption", dir=t("map.dir.score") if by_score else t("map.dir.var")), take)
    if not overseas.empty:
        st.caption(t("map.overseas", list=" · ".join(f"{r['dep_nom']} {fmt_v(r['value'])}" for _, r in overseas.iterrows())))
    if not by_score and view not in OFFICIAL:
        st.caption(t("map.recomputed"))

    # --- What the map says, and careful hypotheses ----------------------------------------------------------
    st.markdown(f'<div class="ar-chart-title">{t("map.see.title")}</div>', unsafe_allow_html=True)
    ordered = metro.sort_values("value", ascending=by_score)   # worst first
    worst = ", ".join(f"{r['dep_nom']} ({fmt_v(r['value'])})" for _, r in ordered.head(5).iterrows())
    best = ", ".join(f"{r['dep_nom']} ({fmt_v(r['value'])})" for _, r in ordered.tail(3).iloc[::-1].iterrows())
    reg = metro.groupby("reg_nom")["value"].mean().dropna()
    see = t("map.see.score" if by_score else "map.see.var", worst=worst, best=best, reg_lo=reg.idxmin(),
            reg_lo_v=fmt_v(reg.min()), reg_hi=reg.idxmax(), reg_hi_v=fmt_v(reg.max()))
    uy_ = load_table("udi_year")
    uy_ = uy_[uy_["annee"].between(*f.years) & (uy_["n_bact"] > 0)]
    small_share = (uy_.assign(dep=dep_of_network(uy_["cdreseau"].astype(str)), small=uy_["n_bact"] < 12)
                   .groupby("dep")["small"].mean())
    both = metro.set_index("dep")["value"].to_frame().join(small_share, how="inner")
    if len(both) >= 10:
        rho_s = both["value"].rank().corr(both["small"].rank())
        strength = "strong" if abs(rho_s) >= 0.5 else "moderate" if abs(rho_s) >= 0.25 else "weak"
        rho_txt = f"{rho_s:.2f}".replace(".", ",") if lang() == "fr" else f"{rho_s:.2f}"
        see += " " + t("map.see.small", rho=rho_txt, strength=t(f"map.strength.{strength}"))
    st.markdown(see)
    st.markdown(f"**{t('map.hyp.title')}.** {t('map.hyp.' + HYP[view])} {t('map.hyp.caution')}")

    # --- Rankings ---------------------------------------------------------------------------------------
    kicker(t("map.rank.kicker"))
    n_rank = st.slider(t("map.rank.n"), 3, 15, 8, key="rank_n")
    asc = not by_score
    best = d.sort_values("value", ascending=asc).head(n_rank)
    worst = d.sort_values("value", ascending=not asc).head(n_rank)
    r = pd.concat([best.assign(group="best"), worst.assign(group="worst")]).drop_duplicates("dep")
    r = r.sort_values("value", ascending=not by_score)
    fig = go.Figure(go.Bar(
        x=r["value"], y=r["dep_nom"] + " (" + r["dep"] + ")", orientation="h",
        marker_color=[TEAL if g == "best" else BRICK for g in r["group"]],
        marker_pattern_shape=["" if g == "best" else "/" for g in r["group"]],
        text=[(fmt1(v) if by_score else pct(v / 100)) + f"  {t('map.rank.' + g)}" for v, g in zip(r["value"], r["group"])],
        textposition="outside", hovertext=r["hover"], hoverinfo="text"))
    layout(fig, value_label, None, height=max(320, 28 * len(r)), legend=False)
    fig.update_xaxes(range=[0, r["value"].max() * 1.3])
    chart(fig, t("map.rank.title", n=n_rank),
          t("map.rank.caption", min=t("map.rank.min.score") if by_score else t("map.rank.min.var")), t("map.rank.take"))

# --- H2: two different maps -----------------------------------------------------------------------------------
kicker(t("map.h2.kicker"))
st.header(t("map.h2.title"))
dy = load_table("dept_year")
dd = dy[dy["annee"].between(*f.years)].groupby("dep")[["n_bact", "n_bact_nc", "n_chem", "n_chem_nc"]].sum()
dd = dd[~dd.index.str.startswith("97")]
dd["b"], dd["c"] = dd["n_bact_nc"] / dd["n_bact"], dd["n_chem_nc"] / dd["n_chem"]
rho = dd["b"].rank().corr(dd["c"].rank())
names = departments().set_index("dep")["dep_nom"]
headline(t("map.h2.headline", rho=f"{rho:.2f}".replace(".", ",") if lang() == "fr" else f"{rho:.2f}"))
top_b, top_c = dd["b"].nlargest(5).index, dd["c"].nlargest(5).index
named = set(top_b) | set(top_c)
fig = go.Figure(go.Scatter(
    x=100 * dd["b"], y=100 * dd["c"], mode="markers+text",
    marker=dict(size=9, color=[BRICK if k in top_b else BLUE if k in top_c else NEUTRAL for k in dd.index],
                symbol=["circle" if k in top_b else "diamond" if k in top_c else "circle-open" for k in dd.index]),
    text=[names.get(k, k) if k in named else "" for k in dd.index], textposition="top center",
    textfont=dict(size=11), hovertext=[f"{names.get(k, k)} ({k})<br>{pct(b, 2)} / {pct(c, 2)}"
                                       for k, b, c in zip(dd.index, dd["b"], dd["c"])], hoverinfo="text"))
layout(fig, t("map.h2.x"), t("map.h2.y"), height=460, legend=False)
chart(fig, t("map.h2.chart", period=f.period_label), t("map.h2.caption"),
      t("map.h2.take", top_b=", ".join(names.get(k, k) for k in top_b[:3]),
        top_c=", ".join(names.get(k, k) for k in top_c[:3])))

# --- H1: small networks -----------------------------------------------------------------------------------------
kicker(t("map.h1.kicker"))
st.header(t("map.h1.title"))
uy = load_table("udi_year")
y0, y1 = f.years[0], min(f.years[1], config.COMPLETE_YEARS[-1])
u = uy[uy["annee"].between(y0, y1) & (uy["n_bact"] > 0)]
u = u.assign(dep=dep_of_network(u["cdreseau"].astype(str)))
u = u[dept_mask(u, f)]
classes = ["< 6", "6–11", "12–51", "≥ 52"]
u = u.assign(size=pd.cut(u["n_bact"], [0, 6, 12, 52, np.inf], right=False, labels=classes))
h1 = u.groupby("size", observed=True).agg(samples=("n_bact", "sum"), nc=("n_bact_nc", "sum")).reindex(classes)
h1["rate"] = h1["nc"] / h1["samples"]
if h1["samples"].isna().any() or h1["rate"].fillna(0).eq(0).any():
    st.info(t("map.h1.few"))
else:
    small = h1.loc[["< 6", "6–11"]]
    headline(t("map.h1.headline", share_nc=pct(small["nc"].sum() / h1["nc"].sum(), 0),
               share_s=pct(small["samples"].sum() / h1["samples"].sum(), 0)))
    fig = go.Figure(go.Bar(x=classes, y=100 * h1["rate"], marker_color=[BRICK, BRICK, OCHRE, TEAL],
                           text=[pct(v, 2) for v in h1["rate"]], textposition="outside",
                           hovertext=[t("map.h1.hover", c=c, v=pct(v, 2), k=num(k), n=num(n))
                                      for c, v, k, n in zip(classes, h1["rate"], h1["nc"], h1["samples"])],
                           hoverinfo="text"))
    layout(fig, t("map.h1.x"), t("map.h1.y"), height=360, legend=False)
    fig.update_yaxes(range=[0, 100 * h1["rate"].max() * 1.25])
    chart(fig, t("map.h1.chart", period=f"{y0}–{y1}"), t("map.h1.caption"),
          t("map.h1.take", ratio=f"{h1.loc['< 6', 'rate'] / h1.loc['≥ 52', 'rate']:.0f}",
            a=pct(h1.loc["< 6", "rate"]), b=pct(h1.loc["≥ 52", "rate"], 2)))

# --- Distribution of scores ----------------------------------------------------------------------------------------
kicker(t("map.dist.kicker"))
sc = metrics.scored_communes(f)
if len(sc):
    headline(t("map.dist.headline", a=pct((sc["grade"] == "A").mean(), 0), n=num(len(sc)),
               de=pct(sc["grade"].isin(["D", "E"]).mean(), 0), type=f.type_label.lower(), scope=f.scope_label))
    fig = go.Figure(go.Histogram(x=sc["score"], xbins=dict(start=0, end=100.01, size=2.5), marker_color=BLUE,
                                 marker_line_color="rgba(255,255,255,0.6)", marker_line_width=1,
                                 hovertemplate=t("map.dist.hover") + "<extra></extra>"))
    for lo_, hi_, g in ((0, 40, "E"), (40, 60, "D"), (60, 75, "C"), (75, 90, "B"), (90, 100, "A")):
        fig.add_vrect(x0=lo_, x1=hi_, fillcolor=GRADE_COLORS[g], opacity=0.13, line_width=0,
                      annotation_text=f"<b>{g}</b>", annotation_position="top")
    layout(fig, t("map.dist.x"), t("map.dist.y"), height=360, legend=False)
    chart(fig, t("map.dist.title"), t("map.dist.caption"),
          t("map.dist.take", share=pct((sc["score"] >= 85).mean(), 0), low=num((sc["score"] < 60).sum())))

# --- Trend ---------------------------------------------------------------------------------------------------------
kicker(t("map.trend.kicker"))
tr = metrics.national_variable_by_year(f, variable)
tr = tr[tr["annee"].between(*f.years)]
tr["scope"] = tr["scope"].replace({"France": t("map.trend.france")})
if len(tr):
    fr = tr[tr["scope"] == t("map.trend.france")].set_index("annee")["share"]
    if len(fr) >= 2:
        headline(t("map.trend.headline", a=pct(fr.iloc[0]), y0=fr.index[0], b=pct(fr.iloc[-1]), y1=fr.index[-1],
                   partial=t("map.trend.partial") if fr.index[-1] == config.PARTIAL_YEAR else ""))
    fig = go.Figure()
    for i, (scope, s) in enumerate(tr.groupby("scope", sort=False)):
        fig.add_trace(go.Scatter(
            x=s["annee"], y=100 * s["share"], name=scope, mode="lines+markers",
            line=dict(width=2.2, color=[BLUE, OCHRE][i]), marker=dict(size=8, symbol=["circle", "square"][i]),
            hovertext=[t("map.trend.hover", y=y, v=pct(v), k=num(k), n=num(n))
                       for y, v, k, n in zip(s["annee"], s["share"], s["n_networks_exceed"], s["n_networks"])],
            hoverinfo="text"))
    if tr["annee"].max() == config.PARTIAL_YEAR:
        partial_year(fig, config.PARTIAL_YEAR, t("common.partial2026"))
    layout(fig, t("common.year"), t("map.trend.y"), height=360)
    fig.update_yaxes(rangemode="tozero")
    fig.update_xaxes(dtick=1)
    chart(fig, t("map.trend.title", var=t("var." + variable)),
          t("map.trend.caption", region=f" / {f.region_name}" if f.region else ""), t("map.trend.take"))

# --- Lowest networks -----------------------------------------------------------------------------------------------
with st.expander(t("map.low.title")):
    u = load_table("udi_scores")
    nm = load_table("dim_udi").set_index("cdreseau")["nomreseau"]
    cat = load_table("params_catalog")
    cat_labels = dict(zip(cat["code"], cat["label"]))
    u = u[u["n_bact"] >= config.MIN_SAMPLES_RANKING].copy()
    u["dep"] = dep_of_network(u["cdreseau"])
    u = u[dept_mask(u, f)]
    low = u.nsmallest(15, "score")
    tbl = pd.DataFrame({t("map.col.net"): low["cdreseau"].map(nm), t("map.col.code"): low["cdreseau"],
                        t("map.col.dep"): low["dep"], t("map.col.score"): low["score"], t("map.col.grade"): low["grade"],
                        t("map.col.worst"): low["worst_chem_code"].map(lambda c: label(c, cat_labels) if isinstance(c, str) else ""),
                        t("map.col.nbact"): low["n_bact"]})
    st.dataframe(tbl, hide_index=True, column_config={t("map.col.score"): st.column_config.NumberColumn(format="%.1f")})
    st.caption(t("map.low.caption"))

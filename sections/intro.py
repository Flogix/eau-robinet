"""Home: the problem (sourced), why water is tested, look up your town, method and hypotheses, national indicators."""
import plotly.graph_objects as go
import streamlit as st

import config
from utils import metrics
from utils.filters import get_filters
from utils.i18n import num, pct, t
from utils.io import load_table, town_options
from utils.viz import BRICK, BLUE, chart, kicker, layout, lede, partial_year

f = get_filters()
kicker(t("home.kicker"))
st.title(t("home.title"))
lede(t("home.lede"))

# --- Why it matters -------------------------------------------------------------------------------
ny = load_table("national_year")
rs = load_table("dq_result_status")
last = config.COMPLETE_YEARS[-1]
n_results = rs[(rs["annee"] == last) & (rs["status"] != "not_measured")]["n"].sum()
n_samples = int(ny.loc[ny["annee"] == last, "n_samples"].iloc[0])

kicker(t("home.why.kicker"))
st.header(t("home.why.title"))
st.markdown(t("home.why.world"))
st.markdown(t("home.why.france"))
st.markdown(t("home.why.nodeaths"))
st.markdown(t("home.why.control", year=last, samples=num(n_samples), results=num(n_results / 1e6, 1)))
st.caption(t("home.why.sources"))

# --- Look up your town -------------------------------------------------------------------------------
with st.container(border=True):
    st.markdown(f"**{t('home.find.title')}**")
    st.caption(t("home.find.text"))
    options, labels = town_options()

    def _go_to_town():   # keep the choice for the town page, clear the box so that coming back does not redirect
        st.session_state["insee"] = st.session_state["home_town"]
        st.session_state["home_town"] = None
        st.session_state["_goto_town"] = True

    st.selectbox(t("home.find.title"), options, index=None, format_func=labels.get, on_change=_go_to_town,
                 placeholder=t("home.find.placeholder"), label_visibility="collapsed", key="home_town")
    if st.session_state.pop("_goto_town", False):
        st.switch_page("sections/ma_commune.py")

# --- Method and hypotheses -----------------------------------------------------------------------------
kicker(t("home.method.kicker"))
st.header(t("home.method.title"))
st.markdown(t("home.method.p1"))
st.markdown(t("home.method.p2"))
st.markdown(t("home.method.p3"))
for h in ("home.h1", "home.h2", "home.h3", "home.h4"):
    st.markdown(t(h))

# --- National indicators ---------------------------------------------------------------------------------
kicker(t("home.kpi.kicker"))
st.header(t("home.kpi.title"))
metrics.render_kpis(f)

r = metrics.yearly_rates(f)
r = r[r["annee"].between(*f.years)]
fig = go.Figure()
for col, name, color, symbol in (("bact", t("home.trend.bact"), BRICK, "circle"),
                                 ("chem", t("home.trend.chem"), BLUE, "diamond")):
    hover = [t("home.trend.hover", y=y, v=pct(v, 2), k=num(k), n=num(n))
             for y, v, k, n in zip(r["annee"], r[col], r[f"n_{col}_nc"], r[f"n_{col}"])]
    fig.add_trace(go.Scatter(x=r["annee"], y=100 * r[col], name=name, mode="lines+markers+text",
                             line=dict(color=color, width=2.2), marker=dict(size=8, symbol=symbol),
                             text=[pct(v) if a in (r["annee"].min(), r["annee"].max()) else ""
                                   for a, v in zip(r["annee"], r[col])],
                             textposition="top center", hovertext=hover, hoverinfo="text"))
if f.years[1] == config.PARTIAL_YEAR:
    partial_year(fig, config.PARTIAL_YEAR, t("common.partial2026"))
layout(fig, t("common.year"), t("home.trend.y"))
fig.update_yaxes(rangemode="tozero")
fig.update_xaxes(dtick=1)
chart(fig, t("home.trend.title"), t("home.trend.caption", scope=f.scope_label), t("home.trend.take"))

st.info(t("home.caveat"))

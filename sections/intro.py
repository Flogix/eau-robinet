# Landing page: problem statement, public health stakes, town search preview, and methodology.
"""Home: the problem (sourced), why water is tested, look up your town, method and hypotheses, national indicators."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import config
from utils import metrics
from utils import town_report as R
from utils.filters import get_filters
from utils.i18n import num, pct, t
from utils.io import commune_network_links, communes, load_table
from utils.town_search import town_search
from utils.viz import BLUE, BRICK, GRADE_COLORS, chart, kicker, layout, lede, partial_year

f = get_filters()


def town_preview(insee: str) -> None:
    """Score, grade, confidence and the sentence on the points lost (the same rules as the town page), then a link."""
    c = communes().set_index("insee").loc[insee].copy()
    c["insee"] = insee
    name = f"{c['nom']} ({c['dep']})"
    if pd.isna(c["score"]):
        st.markdown(f"**{name}** · {t('town.noscore')}")
    else:
        links = commune_network_links()
        nets = links.loc[links["insee"] == insee, "cdreseau"]
        u_rows = load_table("udi_scores").set_index("cdreseau").reindex(nets).dropna(subset=["score"])
        cat = load_table("params_catalog")
        st.markdown(f'<div class="ar-preview"><span class="ar-grade" style="background:{GRADE_COLORS[c["grade"]]}">'
                    f'{c["grade"]}</span><strong>{name}</strong> · '
                    + t("home.find.score", score=num(c["score"], 1), grade=c["grade"],
                        conf=t(f"conf.{c['confidence']}")) + "</div>", unsafe_allow_html=True)
        st.markdown(R.points_lost(c, u_rows, dict(zip(cat["code"], cat["label"]))))
    st.page_link("sections/ma_commune.py", label=t("home.find.report"), icon=":material/arrow_forward:")


kicker(t("home.kicker"))
st.title(t("home.title"))
lede(t("home.lede"))

# --- Why it matters -------------------------------------------------------------------------------
ny = load_table("national_year")
last = config.COMPLETE_YEARS[-1]
vol = load_table("explore_volume").set_index("annee")      # rows of the yearly files: the counts used everywhere
n_results = int(vol.loc[last, "result_rows"])
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
    # choosing a town shows a preview here and stays on the home page (the reader would miss the rest of it);
    # the town page opens only from the link below, on the same town
    town_search(None, "home_search", lambda i: st.session_state.update(insee=i, home_insee=i),
                placeholder=t("home.find.placeholder"))
    picked = st.session_state.get("home_insee")
    if picked:
        town_preview(picked)

# --- Method and hypotheses -----------------------------------------------------------------------------
kicker(t("home.method.kicker"))
st.header(t("home.method.title"))
st.markdown(t("home.method.p1", samples=num(vol["samples"].sum() / 1e6), results=num(vol["result_rows"].sum() / 1e6),
               nets=num(vol.loc[last, "networks_sampled"]), year=last, codes=num(len(load_table("dim_udi")))))
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

"""Behind the numbers: missing values, kinds of results, official vs recomputed verdicts, coverage, checks, limits."""
import numpy as np
import plotly.graph_objects as go
import streamlit as st

import config
from utils.filters import get_filters
from utils.i18n import num, pct, t
from utils.io import load_table
from utils.viz import BLUE, BRICK, NEUTRAL, SERIES, chart, headline, kicker, layout, lede

f = get_filters()
kicker(t("dq.kicker"))
st.title(t("dq.title"))
lede(t("dq.lede"))

checks = load_table("dq_checks")
rs = load_table("dq_result_status")
headline(t("dq.headline", ok=int(checks["ok"].sum()), n=len(checks), m=num(rs["n"].sum() / 1e6)))
st.markdown(t("dq.pipeline"))

# --- Missing values ---------------------------------------------------------------------------------------
kicker(t("dq.missing.kicker"))
mi = load_table("dq_missing")
table = st.segmented_control(t("dq.missing.file"), ["PLV", "RESULT", "COM_UDI"], default="RESULT", key="dq_table",
                             help=t("dq.missing.help")) or "RESULT"
m = mi[mi["table"] == table].pivot(index="column", columns="annee", values="share_missing")
m = m.loc[m.max(axis=1).sort_values(ascending=False).index]
fig = go.Figure(go.Heatmap(z=100 * m.values, x=m.columns, y=m.index, zmin=0, zmax=100,
                           colorscale=[[0, "rgba(127,127,127,0.06)"], [1, "#0E5A61"]],
                           colorbar=dict(title=t("dq.missing.cb")), hovertemplate=t("dq.missing.hover") + "<extra></extra>"))
layout(fig, t("dq.missing.x"), None, height=max(320, 22 * len(m)), legend=False)
fig.update_xaxes(dtick=1)
chart(fig, t("dq.missing.title", file=table), t("dq.missing.caption"), t("dq.missing.take"))

# --- Kinds of results ---------------------------------------------------------------------------------------
kicker(t("dq.status.kicker"))
r = rs.pivot_table(index="annee", columns="status", values="n", aggfunc="sum").fillna(0)
order = r.sum().sort_values(ascending=False).index
headline(t("dq.status.headline", share=pct(r["not_quantified"].sum() / r.values.sum(), 0)))
fig = go.Figure()
colors = SERIES + [NEUTRAL] * 6
for i, s in enumerate(order[:6]):
    name = t(f"st.{s}")
    fig.add_trace(go.Bar(x=r.index, y=r[s] / 1e6, name=name, marker_color=colors[i],
                         marker_line_color="rgba(255,255,255,0.5)", marker_line_width=1, hoverinfo="text",
                         hovertext=[f"{name}<br>" + t("dq.status.hover", y=y, v=num(v / 1e6, 2))
                                    for y, v in zip(r.index, r[s])]))
fig.update_layout(barmode="stack")
layout(fig, t("mon.s2.x"), t("dq.status.y"), height=380)
fig.update_xaxes(dtick=1)
chart(fig, t("dq.status.title"), t("dq.status.caption"), t("dq.status.take"))

# --- Official vs recomputed ---------------------------------------------------------------------------------
kicker(t("dq.verdict.kicker"))
cc = load_table("dq_conformity_check")
headline(t("dq.verdict.headline", agree=pct(cc["bact_both"].sum() / cc["bact_nc_official"].sum())))
fig = go.Figure()
for col, key, color, dash in (("chem_nc_official", "chem_off", BLUE, "solid"), ("chem_nc_recomputed", "chem_rec", BLUE, "dot"),
                              ("bact_nc_official", "bact_off", BRICK, "solid"), ("bact_nc_recomputed", "bact_rec", BRICK, "dot")):
    name = t(f"dq.verdict.{key}")
    fig.add_trace(go.Scatter(x=cc["annee"], y=cc[col], name=name, mode="lines+markers",
                             line=dict(color=color, dash=dash, width=2.2), marker=dict(size=7),
                             hovertemplate="%{x}: %{y:,}<extra>" + name + "</extra>"))
layout(fig, t("mon.s2.x"), t("dq.verdict.y"), height=380)
fig.update_xaxes(dtick=1)
chart(fig, t("dq.verdict.title"), t("dq.verdict.caption"), t("dq.verdict.take"))
st.caption(t("dq.verdict.sources"))
with st.expander(t("dq.gap.title")):
    st.dataframe(load_table("dq_chem_gap").sort_values(["annee", "n_samples"], ascending=[True, False]), hide_index=True)

# --- Coverage ---------------------------------------------------------------------------------------------------
kicker(t("dq.cov.kicker"))
uy = load_table("udi_year")
yr = min(f.years[1], config.COMPLETE_YEARS[-1])
u = uy[(uy["annee"] == yr) & (uy["n_samples"] > 0)]
headline(t("dq.cov.headline", y=yr, n=num(len(u)), med=f"{u['n_samples'].median():.0f}", max=num(u["n_samples"].max())))
fig = go.Figure(go.Histogram(x=np.log10(u["n_samples"].astype(float)), nbinsx=40, marker_color=BLUE,
                             marker_line_color="rgba(255,255,255,0.6)", marker_line_width=1,
                             hovertemplate="10^%{x:.1f}: %{y:,}<extra></extra>"))
fig.update_xaxes(tickvals=[0, 1, 2, 3], ticktext=["1", "10", "100", num(1000)])
layout(fig, t("dq.cov.x", y=yr), t("dq.cov.y"), height=340, legend=False)
chart(fig, t("dq.cov.title"), t("dq.cov.caption"), t("dq.cov.take"))

with st.expander(t("dq.checks.title", n=len(checks))):
    st.dataframe(checks.assign(ok=checks["ok"].map({True: t("dq.checks.pass"), False: t("dq.checks.fail")})),
                 hide_index=True)

# --- Limits -----------------------------------------------------------------------------------------------------
kicker(t("dq.limits.kicker"))
st.header(t("dq.limits.title"))
st.markdown(t("dq.limits.p1"))
st.markdown(t("dq.limits.p2"))

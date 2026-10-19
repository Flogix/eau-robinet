"""Page 5 — France's water map: KPIs, department map, rankings, distribution of scores, trend."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import config
from utils import metrics
from utils.filters import OFFICIAL, dept_mask, get_filters
from utils.io import SOURCE_CAPTION, dep_of_network, departments_geojson, load_table
from utils.viz import GRADE_COLORS, PALETTE, headline, layout, pct, show

f = get_filters()
st.title("🗺️ France's water map")
metrics.render_kpis(f)

# --- Map --------------------------------------------------------------------------------------------
st.subheader("Where are the problems?")
mode = st.segmented_control("Map shows", [f"{f.variable_label} — {f.period_label}", "Current score of communes"],
                            default=f"{f.variable_label} — {f.period_label}", key="map_mode",
                            help="Change the family and the period in the sidebar. The current score uses the last "
                                 "12/36 months whatever the period.")
by_score = mode == "Current score of communes"
if by_score:
    d = metrics.dept_scores(f)
    d = d[d["n_communes"] >= 5]
    d["value"], d["n"] = d["median_score"], d["n_communes"]
    value_label, fmt = "Median commune score (/100)", ".1f"
    colorscale = "Blues"
    hover = "%{customdata[0]} (%{location})<br>median score %{z:.1f}/100<br>%{customdata[1]} communes<extra></extra>"
else:
    d = metrics.dept_variable(f)
    d = d[d["n_networks"] >= 10]
    d["value"], d["n"] = 100 * d["share"], d["n_networks"]
    value_label, fmt = "Networks with ≥ 1 exceedance, per year (%)", ".1f"
    colorscale = "Oranges"
    hover = ("%{customdata[0]} (%{location})<br>%{z:.1f}% of network-years with at least one exceedance"
             "<br>%{customdata[1]:,} network-years measured<extra></extra>")
metro = d[~d["dep"].str.startswith("97")]
overseas = d[d["dep"].str.startswith("97")]

if metro.empty:
    st.info("No department with enough data for this selection.")
else:
    hi = metro.loc[metro["value"].idxmax()]
    lo = metro.loc[metro["value"].idxmin()]
    if by_score:
        headline(f"Median commune score ranges from {lo['value']:.0f}/100 ({lo['dep_nom']}) to {hi['value']:.0f}/100 "
                 f"({hi['dep_nom']}) across mainland departments.")
    else:
        headline(f"{f.variable_label}: from {lo['value']:.1f}% ({lo['dep_nom']}) to {hi['value']:.1f}% "
                 f"({hi['dep_nom']}) of networks with at least one exceedance per year, {f.period_label}.")
    fig = go.Figure(go.Choropleth(
        geojson=departments_geojson(), featureidkey="properties.code", locations=metro["dep"], z=metro["value"],
        colorscale=colorscale, reversescale=by_score, marker_line_color="white", marker_line_width=0.5,
        customdata=metro[["dep_nom", "n"]], hovertemplate=hover,
        colorbar=dict(title=dict(text=value_label.replace(" (", "<br>("), side="right"), thickness=12)))
    fig.update_geos(fitbounds="locations", visible=False, bgcolor="rgba(0,0,0,0)")
    fig.update_layout(height=560, margin=dict(l=0, r=0, t=10, b=0))
    show(fig, f"Choropleth map of mainland departments: {value_label.lower()}"
              f"{'' if by_score else ', ' + f.variable_label + ', ' + f.period_label}; darker = "
              f"{'better score' if by_score else 'more networks affected'}. Departments with too few data are blank.")
    if not overseas.empty:
        st.caption("Overseas departments (not on the map): " + " · ".join(
            f"{r['dep_nom']} {r['value']:{fmt}}" for _, r in overseas.iterrows()))
    if not by_score and f.variable not in OFFICIAL:
        st.caption("Recomputed exceedances: a result above the threshold written on its row. "
                   "Official conformity can differ (temporary derogations, limits changed over time — see Data quality).")

    # --- Rankings -------------------------------------------------------------------------------------
    st.subheader("Rankings of departments")
    n_rank = st.slider("Departments shown at each end", 3, 15, 8, key="rank_n")
    asc = not by_score
    best = d.sort_values("value", ascending=asc).head(n_rank)
    worst = d.sort_values("value", ascending=not asc).head(n_rank)
    r = pd.concat([best.assign(group="Best"), worst.assign(group="Worst")]).drop_duplicates("dep")
    r = r.sort_values("value", ascending=not by_score)
    fig = go.Figure(go.Bar(
        x=r["value"], y=r["dep_nom"] + " (" + r["dep"] + ")", orientation="h",
        marker_color=[PALETTE["green"] if g == "Best" else PALETTE["vermillion"] for g in r["group"]],
        marker_pattern_shape=["" if g == "Best" else "/" for g in r["group"]],
        text=[f"{v:{fmt}}" + ("" if by_score else "%") + f" — {g.lower()}" for v, g in zip(r["value"], r["group"])],
        textposition="outside", customdata=r[["n"]],
        hovertemplate="%{y}: %{x:.1f}<br>based on %{customdata[0]:,} " +
                      ("communes" if by_score else "network-years") + "<extra></extra>"))
    layout(fig, value_label, None, height=max(300, 28 * len(r)), legend=False)
    fig.update_xaxes(range=[0, r["value"].max() * 1.25])
    show(fig, f"Bars: the {n_rank} best and {n_rank} worst departments for {value_label.lower()} (best in green "
              "plain bars, worst in vermillion hatched bars, also written in the label). "
              f"Minimum {'5 communes' if by_score else '10 network-years'} per department.")

# --- Distribution of scores -------------------------------------------------------------------------------
st.subheader("How are the communes' scores distributed?")
sc = metrics.scored_communes(f)
if len(sc):
    share_a = (sc["grade"] == "A").mean()
    headline(f"{share_a:.0%} of the {len(sc):,} communes selected are graded A; "
             f"{sc['grade'].isin(['D', 'E']).mean():.0%} are graded D or E ({f.type_label}, {f.scope_label}).")
    fig = go.Figure(go.Histogram(x=sc["score"], xbins=dict(start=0, end=100.01, size=2.5),
                                 marker_color=PALETTE["blue"], marker_line_color="white", marker_line_width=1,
                                 hovertemplate="score %{x}: %{y:,} communes<extra></extra>"))
    for lo_, hi_, g in ((0, 40, "E"), (40, 60, "D"), (60, 75, "C"), (75, 90, "B"), (90, 100, "A")):
        fig.add_vrect(x0=lo_, x1=hi_, fillcolor=GRADE_COLORS[g], opacity=0.12, line_width=0,
                      annotation_text=f"<b>{g}</b>", annotation_position="top")
    layout(fig, "Commune score (/100)", "Number of communes", height=360, legend=False)
    show(fig, "Histogram: number of communes by current score (bins of 2.5 points), with the grade bands "
              "E, D, C, B, A in the background.")

# --- Trend of the selected family ------------------------------------------------------------------------
st.subheader(f"Trend: {f.variable_label}")
t = metrics.national_variable_by_year(f)
t = t[t["annee"].between(*f.years)]
if len(t):
    fr = t[t["scope"] == "France"].set_index("annee")["share"]
    if len(fr) >= 2:
        headline(f"In France, {pct(fr.iloc[0])} of networks had at least one exceedance of '{f.variable_label}' in "
                 f"{fr.index[0]}, {pct(fr.iloc[-1])} in {fr.index[-1]}"
                 f"{' (partial year)' if fr.index[-1] == config.PARTIAL_YEAR else ''}.")
    fig = go.Figure()
    for i, (scope, s) in enumerate(t.groupby("scope", sort=False)):
        fig.add_trace(go.Scatter(x=s["annee"], y=100 * s["share"], name=scope, mode="lines+markers",
                                 line=dict(width=2, color=[PALETTE["blue"], PALETTE["orange"]][i]),
                                 marker=dict(size=8, symbol=["circle", "square"][i]),
                                 customdata=s[["n_networks_exceed", "n_networks"]],
                                 hovertemplate="%{x}: %{y:.1f}%<br>%{customdata[0]:,} of %{customdata[1]:,} networks"
                                               "<extra>" + scope + "</extra>"))
    if t["annee"].max() == config.PARTIAL_YEAR:
        fig.add_vrect(x0=config.PARTIAL_YEAR - 0.5, x1=config.PARTIAL_YEAR + 0.5, fillcolor="grey", opacity=0.12,
                      line_width=0, annotation_text="2026: Jan–Aug only", annotation_position="top left")
    layout(fig, "Year", "Networks with ≥ 1 exceedance (%)", height=360)
    fig.update_yaxes(rangemode="tozero")
    show(fig, f"Lines: share of distribution networks with at least one exceedance of '{f.variable_label}' each "
              f"year, France{' and ' + f.region_name if f.region else ''}. A partial year has fewer samples, "
              "so fewer chances to detect an exceedance.")

# --- Networks ranking ------------------------------------------------------------------------------------
with st.expander("Lowest-scored networks (at least 12 bacteriological samples in 12 months)"):
    u = load_table("udi_scores")
    names = load_table("dim_udi").set_index("cdreseau")["nomreseau"]
    u = u[u["n_bact"] >= config.MIN_SAMPLES_RANKING].copy()
    u["dep"] = dep_of_network(u["cdreseau"])
    u = u[dept_mask(u, f)]
    u["Network"] = u["cdreseau"].map(names)
    st.dataframe(u.nsmallest(15, "score")[["Network", "cdreseau", "dep", "score", "grade", "micro", "chem", "comfort",
                                          "worst_chem_code", "n_bact"]],
                 hide_index=True, column_config={c: st.column_config.NumberColumn(format="%.1f")
                                                 for c in ("score", "micro", "chem", "comfort")})
    st.caption("Networks with fewer samples are left out of rankings: one incident weighs too much on them.")
st.caption(SOURCE_CAPTION)

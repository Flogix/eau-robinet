"""Page 6 — Deep dives: H3 (what we monitor and how we classify it drives chemical non-compliance), nitrates, PFAS,
bacteria seasonality, hardness, and the what-if weights of the score."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import config
from utils import score as S
from utils.filters import get_filters
from utils.io import SOURCE_CAPTION, departments, dep_of_network, load_table
from utils.viz import PALETTE, event, headline, layout, pct, show, threshold

f = get_filters()
st.title("🔎 Deep dives")
y0, y1 = f.years

py = load_table("param_year")
ny = load_table("national_year")

# ======================================================================================================
st.header("1. What we monitor — and how we classify it — drives chemical non-compliance")
GROUPS = {   # code_merged -> group (the four metabolite groups explain the 2021–2024 rise, see Data quality)
    "CLDZ_D": "Chloridazone metabolites", "CLDZ_MD": "Chloridazone metabolites",
    "MTCESA": "ESA-metolachlor", "MTCNOA": "ESA-metolachlor",
    "471811R": "Chlorothalonil metabolites", "CLTHALS": "Chlorothalonil metabolites",
    "NO3": "Nitrates", "NO2": "Nitrates", "NO3_NO2": "Nitrates",
}
ORDER = ["Chloridazone metabolites", "ESA-metolachlor", "Chlorothalonil metabolites", "Other pesticides",
         "Nitrates", "Other chemistry"]
chem = py[(py["family"] == "chem") & (py["annee"] <= config.YEARS[-1])].copy()
chem["group"] = chem["code_merged"].map(GROUPS)
chem.loc[chem["group"].isna() & (chem["subfamily"] == "pesticides"), "group"] = "Other pesticides"
chem["group"] = chem["group"].fillna("Other chemistry")
# metabolites published under twin codes are in comfort when compared with the 0.9 µg/L value: keep limit rows only
twins = py[py["code"].isin(["ESAMTC", "NOAMTC", "R471811", "471811R", "MTCESA", "MTCNOA"]) & (py["family"] == "comfort")]
twins = twins.assign(group=twins["code_merged"].map(GROUPS))
ex = pd.concat([chem, twins])
by = ex.groupby(["annee", "group"])["n_exceed_limit"].sum().unstack(fill_value=0).reindex(columns=ORDER, fill_value=0)

nc = ny.set_index("annee")["n_chem_nc"]
before = nc.loc[2016:2020].mean()
during = nc.loc[2021:2024].mean()
meta = by.loc[2021:2024, ORDER[:3]].sum().sum() / by.loc[2021:2024].sum().sum()
headline(f"Officially non-compliant chemical samples rose from {before:,.0f} a year (2016–2020) to {during:,.0f} "
         f"(2021–2024), then fell to {nc.loc[2025]:,.0f} in 2025. Three newly monitored or reclassified pesticide "
         f"metabolites account for {meta:.0%} of the limit exceedances of 2021–2024.")
st.markdown(
    "This is our main finding (hypothesis **H3**, confirmed): the rise of chemical non-compliance after 2020 does not "
    "show that the water suddenly got worse. It follows **what laboratories started to look for** (pesticide "
    "metabolites added to the monitoring) and **how these molecules are classified** (Anses reclassified some of them "
    "as *non-relevant*: they are then compared with a 0.9 µg/L indicative value instead of the 0.1 µg/L limit).")

fig = go.Figure()
cols = {"Chloridazone metabolites": PALETTE["vermillion"], "ESA-metolachlor": PALETTE["orange"],
        "Chlorothalonil metabolites": PALETTE["purple"], "Other pesticides": PALETTE["sky"],
        "Nitrates": PALETTE["blue"], "Other chemistry": "#C8C8C8"}
for g in ORDER:
    fig.add_trace(go.Bar(x=by.index, y=by[g], name=g, marker_color=cols[g], marker_line_color="white",
                         marker_line_width=1, hovertemplate="%{x}: %{y:,} exceedances<extra>" + g + "</extra>"))
fig.add_trace(go.Scatter(x=nc.index, y=nc.values, name="Officially non-compliant samples", mode="lines+markers",
                         line=dict(color="#888888", width=2), marker=dict(size=8, symbol="diamond"),
                         hovertemplate="%{x}: %{y:,} non-compliant samples<extra></extra>"))
event(fig, 2020.55, "2021: chloridazone<br>metabolites monitored", 0.99)
event(fig, 2022.75, "30/09/2022: ESA-metolachlor<br>non-relevant (Anses)", 0.80)
event(fig, 2024.33, "29/04/2024: chlorothalonil<br>R471811 non-relevant", 0.99)
event(fig, 2025.55, "01/01/2026: PFAS in<br>routine control", 0.62)
fig.add_vrect(x0=config.PARTIAL_YEAR - 0.5, x1=config.PARTIAL_YEAR + 0.5, fillcolor="grey", opacity=0.10, line_width=0)
fig.update_layout(barmode="stack")
layout(fig, "Year (2026: January–August)", "Number of samples / exceedances", height=520)
show(fig, "Stacked bars: number of limit exceedances per year by group of parameters (one count per sample and "
          "parameter); black line: samples officially declared non-compliant for chemistry. Dotted lines mark the "
          "changes of monitoring and classification.")

c1, c2 = st.columns(2)
with c1:
    n_par = py[py["n_samples"] > 0].groupby("annee")["code"].nunique()
    n_pest = py[(py["n_samples"] > 0) & (py["subfamily"] == "pesticides")].groupby("annee")["code"].nunique()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n_par.index, y=n_par.values, name="All parameters", mode="lines+markers",
                             line=dict(color=PALETTE["blue"], width=2), marker=dict(size=8),
                             hovertemplate="%{x}: %{y} parameters<extra></extra>"))
    fig.add_trace(go.Scatter(x=n_pest.index, y=n_pest.values, name="Pesticides and relevant metabolites",
                             mode="lines+markers", line=dict(color=PALETTE["orange"], width=2),
                             marker=dict(size=8, symbol="square"), hovertemplate="%{x}: %{y} pesticides<extra></extra>"))
    layout(fig, "Year", "Distinct parameters measured", height=360)
    fig.update_yaxes(rangemode="tozero")
    st.markdown(f"**More molecules searched**: {n_par.loc[2016]:,} parameters in 2016, {n_par.loc[2025]:,} in 2025.")
    show(fig, "Lines: number of distinct parameters measured at least once in the year, all parameters and pesticides.")
with c2:
    m = py[py["code_merged"].isin(["MTCESA", "471811R"])].groupby(["annee", "code_merged"])[
        ["n_samples", "n_detected", "n_exceed_limit", "n_exceed_indicative"]].sum().reset_index()
    pick = st.radio("Metabolite", ["ESA-metolachlor", "Chlorothalonil R471811"], horizontal=True, key="h3_meta")
    code = "MTCESA" if pick == "ESA-metolachlor" else "471811R"
    mm = m[m["code_merged"] == code]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=mm["annee"], y=mm["n_exceed_limit"], name="Above the 0.1 µg/L limit",
                         marker_color=PALETTE["vermillion"], hovertemplate="%{x}: %{y:,} samples<extra></extra>"))
    fig.add_trace(go.Bar(x=mm["annee"], y=mm["n_exceed_indicative"], name="Above the 0.9 µg/L indicative value",
                         marker_color=PALETTE["sky"], marker_pattern_shape="/",
                         hovertemplate="%{x}: %{y:,} samples<extra></extra>"))
    fig.add_trace(go.Scatter(x=mm["annee"], y=mm["n_detected"], name="Detected (any level)", mode="lines+markers",
                             line=dict(color="#888888", width=2, dash="dot"), marker=dict(size=8),
                             hovertemplate="%{x}: detected in %{y:,} samples<extra></extra>"))
    event(fig, 2022.75 if code == "MTCESA" else 2024.33, "reclassified non-relevant", 0.99)
    layout(fig, "Year", "Number of samples", height=360)
    st.markdown(f"**Same molecule, new threshold**: {pick} keeps being detected after its reclassification, "
                "but is no longer counted as a limit exceedance.")
    show(fig, f"Bars and line: samples where {pick} was detected, above the 0.1 µg/L limit, and above the 0.9 µg/L "
              "indicative value, per year.")
with st.expander("Sources of the dates and thresholds above"):
    st.markdown(
        "- Anses opinions of 30/09/2022 (ESA and NOA metolachlor non-relevant) and the 0.9 µg/L indicative value "
        "(decree 2022-1720, order of 11/01/2007 as amended): Assemblée nationale, written question no. 2237, answer of "
        "28/03/2023 — https://questions.assemblee-nationale.fr/dyn/16/questions/QANR5L16QE2237.pdf\n"
        "- Chlorothalonil R471811 relevant in 2023, non-relevant since the Anses opinion of 29/04/2024: ARS "
        "Hauts-de-France — https://www.hauts-de-france.ars.sante.fr/les-metabolites-du-chlorothalonil-0 ; ARS "
        "Bourgogne-Franche-Comté — https://bourgogne-franche-comte.ars.sante.fr/media/127554/download\n"
        "- PFAS (sum of 20) in the routine control from 01/01/2026: ARS Nouvelle-Aquitaine — "
        "https://www.nouvelle-aquitaine.ars.sante.fr/surveillance-des-pfas-polluants-chimiques-eternels-dans-leau-en-nouvelle-aquitaine\n"
        "- Selenium and antimony limits raised on 01/01/2023 (directive (EU) 2020/2184, order of 30/12/2022): "
        "https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046849403\n"
        "- Chloridazone metabolites: first year with measurements read from the data (none before 2021).")
st.caption("Caution: an exceedance count depends on how often and where each molecule is searched. These charts show "
           "monitoring and classification effects; they do not measure whether the water got better or worse.")

# ======================================================================================================
st.header("2. Focus by family")
t_nit, t_pfas, t_bact, t_hard = st.tabs(["Nitrates", "PFAS", "Bacteria by season", "Hardness"])
win = load_table("udi_param_window")
with t_nit:
    no3 = win[win["code"] == "NO3"]
    above = (no3["max_value"] > 50).mean()
    headline(f"{(no3['max_value'] <= 25).mean():.0%} of networks stayed below half of the nitrate limit (25 mg/L) in 36 months; "
             f"{above:.1%} exceeded the 50 mg/L limit at least once.")
    fig = go.Figure(go.Histogram(x=no3["max_value"].clip(upper=100), xbins=dict(start=0, end=100.01, size=2.5),
                                 marker_color=PALETTE["blue"], marker_line_color="white", marker_line_width=1,
                                 hovertemplate="max %{x} mg/L: %{y:,} networks<extra></extra>"))
    threshold(fig, 50, "limit 50 mg/L", axis="x", color=PALETTE["vermillion"])
    layout(fig, "Maximum nitrate concentration in 36 months (mg/L, capped at 100)", "Number of networks",
           height=360, legend=False)
    show(fig, "Histogram: networks by their maximum nitrate concentration over the last 36 months, with the "
              "50 mg/L limit as a dashed line. Networks where nitrates were never quantified are not shown.")
with t_pfas:
    pf = py[py["code"] == "SPFAS"].set_index("annee")[["n_samples", "n_exceed_limit"]]
    headline(f"Samples analysed for the sum of 20 PFAS: {pf['n_samples'].get(2022, 0):,} in 2022, "
             f"{pf['n_samples'].get(2025, 0):,} in 2025; {pf['n_exceed_limit'].get(2025, 0):,} were above "
             "0.1 µg/L in 2025.")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=pf.index, y=pf["n_samples"], name="Samples analysed", marker_color=PALETTE["sky"],
                         text=pf["n_samples"], textposition="outside",
                         hovertemplate="%{x}: %{y:,} samples analysed<extra></extra>"))
    fig.add_trace(go.Bar(x=pf.index, y=pf["n_exceed_limit"], name="Above 0.1 µg/L", marker_color=PALETTE["vermillion"],
                         marker_pattern_shape="/", text=pf["n_exceed_limit"], textposition="outside",
                         hovertemplate="%{x}: %{y:,} samples above the limit<extra></extra>"))
    event(fig, 2025.55, "01/01/2026: PFAS in routine control", 0.95)
    layout(fig, "Year (2026: January–August)", "Number of samples", height=360)
    show(fig, "Bars: samples analysed for the sum of 20 PFAS and samples above the 0.1 µg/L limit, per year. "
              "Few measurements before 2025: an absence of measurement is not an absence of PFAS.")
with t_bact:
    nm = load_table("national_month")
    c_last = config.COMPLETE_YEARS[-1]
    m0, m1 = min(y0, c_last), min(y1, c_last)   # complete years only (seasons need all 12 months)
    if (m0, m1) != (y0, y1):
        st.caption(f"Complete years only: {m0}–{m1} (2026 lacks September–December).")
    nm = nm[nm["annee"].between(m0, m1)]
    mo = nm.groupby("month")[["n_bact", "n_bact_nc"]].sum()
    mo["rate"] = mo["n_bact_nc"] / mo["n_bact"]
    names_m = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    hi_m, lo_m = mo["rate"].idxmax(), mo["rate"].idxmin()
    headline(f"Bacteriological non-compliance peaks in {names_m[hi_m - 1]} ({pct(mo.loc[hi_m, 'rate'], 2)}) and is "
             f"lowest in {names_m[lo_m - 1]} ({pct(mo.loc[lo_m, 'rate'], 2)}), France, {m0}–{m1}.")
    fig = go.Figure(go.Bar(x=names_m, y=100 * mo["rate"].values, marker_color=PALETTE["vermillion"],
                           text=[f"{100 * v:.2f}%" for v in mo["rate"]], textposition="outside",
                           customdata=mo[["n_bact_nc", "n_bact"]].values,
                           hovertemplate="%{x}: %{y:.2f}%<br>%{customdata[0]:,} of %{customdata[1]:,} samples"
                                         "<extra></extra>"))
    layout(fig, "Month", "Non-compliant bacteriological samples (%)", height=360, legend=False)
    show(fig, "Bars: share of bacteriological samples officially non-compliant, by month of sampling, over the "
              "complete years of the selected period. A seasonal pattern is a correlation, not an explanation.")
with t_hard:
    th = win[win["code"] == "TH"][["cdreseau", "mean"]].copy()
    th["dep"] = dep_of_network(th["cdreseau"])
    th = th.merge(departments(), on="dep", how="left").dropna(subset=["reg_nom"])
    med = th.groupby("reg_nom")["mean"].median().sort_values()
    headline(f"Median hardness of networks ranges from {med.iloc[0]:.0f} °f ({med.index[0]}) to {med.iloc[-1]:.0f} °f "
             f"({med.index[-1]}) — limescale, not a health issue (hypothesis H4).")
    fig = go.Figure()
    for i, reg in enumerate(med.index):
        fig.add_trace(go.Box(x=th.loc[th["reg_nom"] == reg, "mean"], name=reg, orientation="h", boxpoints=False,
                             marker_color=PALETTE["blue"], hoverinfo="x+name"))
    layout(fig, "Mean hardness of the network in 12 months (°f, French degrees)", None, height=560, legend=False)
    show(fig, "Box plots: hardness of the distribution networks by region, sorted by median. Hardness has no health "
              "limit and never lowers the score.")

# ======================================================================================================
st.header("3. What if the score weighted things differently?")
st.markdown("The default weights (0.4 microbiology, 0.4 chemistry, 0.2 comfort) are a choice. Move them and see how "
            "much the ranking of networks changes.")
u = load_table("udi_scores")
c1, c2, c3 = st.columns(3)
w_micro = c1.slider("Weight of microbiology", 0.0, 1.0, config.WEIGHTS["micro"], 0.05, key="w_micro")
w_chem = c2.slider("Weight of health chemistry", 0.0, 1.0, config.WEIGHTS["chem"], 0.05, key="w_chem")
w_comf = c3.slider("Weight of comfort", 0.0, 1.0, config.WEIGHTS["comfort"], 0.05, key="w_comf")
if w_micro + w_chem + w_comf == 0:
    st.warning("At least one weight must be above 0.")
else:
    tot = w_micro + w_chem + w_comf
    w = {"micro": w_micro / tot, "chem": w_chem / tot, "comfort": w_comf / tot}
    new = S.global_score(u, w)
    elig = u["n_bact"] >= config.MIN_SAMPLES_RANKING
    rho = u.loc[elig, "score"].rank().corr(new[elig].rank())
    g_old = u["grade"]
    g_new = new.map(S.grade)
    changed = (g_old != g_new)[u["score"].notna()].mean()
    headline(f"With these weights (normalised to {w['micro']:.2f} / {w['chem']:.2f} / {w['comfort']:.2f}), "
             f"{changed:.0%} of networks change grade; the ranking stays correlated at ρ = {rho:.3f} with the "
             "default one.")
    dist = pd.DataFrame({"Default weights": g_old.value_counts(normalize=True),
                         "Your weights": g_new.value_counts(normalize=True)}).reindex(list("ABCDE")).fillna(0)
    fig = go.Figure()
    for i, col in enumerate(dist.columns):
        fig.add_trace(go.Bar(x=dist.index, y=100 * dist[col], name=col, marker_color=[PALETTE["grey"], PALETTE["blue"]][i],
                             marker_pattern_shape=["/", ""][i], text=[f"{100 * v:.0f}%" for v in dist[col]],
                             textposition="outside", hovertemplate="grade %{x}: %{y:.1f}% of networks<extra>" + col +
                                                                   "</extra>"))
    layout(fig, "Grade", "Networks (%)", height=340)
    show(fig, "Grouped bars: share of networks in each grade with the default weights (grey, hatched) and with "
              "your weights (blue).")
with st.expander("Sensitivity analysis (14 variants of the method, computed by scripts/05_build_scores.py)"):
    sens = load_table("score_sensitivity")
    st.dataframe(sens[["variant", "spearman_networks", "spearman_communes", "share_grade_changed", "bottom10_overlap",
                       "median_score"]].rename(columns={
        "variant": "Variant", "spearman_networks": "Rank correlation (networks ≥ 12 samples)",
        "spearman_communes": "Rank correlation (communes)", "share_grade_changed": "Networks changing grade",
        "bottom10_overlap": "Same bottom 10%", "median_score": "Median score"}), hide_index=True,
        column_config={"Networks changing grade": st.column_config.NumberColumn(format="percent"),
                       "Same bottom 10%": st.column_config.NumberColumn(format="percent")})
    st.caption("Spearman rank correlation with the default ranking: 1 = identical order. All variants stay above "
               "0.95 except removing comfort entirely (0.86).")
st.caption(SOURCE_CAPTION)

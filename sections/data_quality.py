"""Page 7 — Data quality: missing values, duplicates, validation checks, official vs recomputed, coverage, biases."""
import numpy as np
import plotly.graph_objects as go
import streamlit as st

import config
from utils.filters import get_filters
from utils.io import SOURCE_CAPTION, load_table
from utils.viz import PALETTE, SEQUENTIAL, SERIES, headline, layout, show

f = get_filters()
st.title("🧪 Data quality")

checks = load_table("dq_checks")
n_ok = int(checks["ok"].sum())
rs = load_table("dq_result_status")
headline(f"{n_ok} of {len(checks)} automatic checks pass: no duplicate key left, no result without its sample, "
         f"no join explosion, all {rs['n'].sum() / 1e6:.0f} million results parsed.")

# --- Missing values ----------------------------------------------------------------------------------
st.subheader("Missing values")
mi = load_table("dq_missing")
table = st.segmented_control("File", ["PLV", "RESULT", "COM_UDI"], default="RESULT", key="dq_table",
                             help="PLV = samples, RESULT = analysis results, COM_UDI = commune ↔ network link.")
m = mi[mi["table"] == (table or "RESULT")].pivot(index="column", columns="annee", values="share_missing")
m = m.loc[m.max(axis=1).sort_values(ascending=False).index]
fig = go.Figure(go.Heatmap(z=100 * m.values, x=m.columns, y=m.index, colorscale=SEQUENTIAL, zmin=0, zmax=100,
                           colorbar=dict(title="% missing"),
                           hovertemplate="%{y}, %{x}: %{z:.1f}% missing<extra></extra>"))
layout(fig, "File year", None, height=max(320, 22 * len(m)), legend=False)
show(fig, f"Heatmap: share of empty values per column (rows) and year (columns) in the {table or 'RESULT'} files "
          "as published; darker = more missing.")
st.caption("Fully empty columns (e.g. `libwebparametre`) are not used. Empty values in `limitequal` / `refqual` mean "
           "that the parameter has no threshold.")

# --- Results statuses ------------------------------------------------------------------------------------
st.subheader(f"What the {rs['n'].sum() / 1e6:.0f} million results look like")
labels = {"not_quantified": "Below the quantification limit (< LQ)", "quantified": "Quantified value",
          "qualitative": "Qualitative (e.g. odour)", "not_measured": "Not measured (excluded)",
          "missing": "Empty", "unreadable": "Unreadable", "above": "Above a measurement range (> x)",
          "present": "Presence", "uncountable": "Uncountable bacteria", "other": "Other"}
r = rs.pivot_table(index="annee", columns="status", values="n", aggfunc="sum").fillna(0)
order = r.sum().sort_values(ascending=False).index
nq = r["not_quantified"].sum() / r.values.sum()
headline(f"{nq:.0%} of the results are below the quantification limit: they are counted as 0 when checking "
         "exceedances, and never as a detection.")
fig = go.Figure()
for i, s in enumerate(order[:6]):
    fig.add_trace(go.Bar(x=r.index, y=r[s] / 1e6, name=labels.get(s, s), marker_color=(SERIES + [PALETTE["grey"]])[i],
                         marker_line_color="white", marker_line_width=1,
                         hovertemplate="%{x}: %{y:.2f} million<extra>" + labels.get(s, s) + "</extra>"))
fig.update_layout(barmode="stack")
layout(fig, "Year (2026: January–August)", "Results (millions)", height=380)
show(fig, "Stacked bars: number of analysis results per year by status of the raw value (one row per sample and "
          "parameter, the laboratory measure kept when the field measure also exists).")

# --- Official vs recomputed ---------------------------------------------------------------------------------
st.subheader("Do our recomputed exceedances match the official conclusions?")
cc = load_table("dq_conformity_check")
b_agree = cc["bact_both"].sum() / cc["bact_nc_official"].sum()
headline(f"Bacteriology: {b_agree:.1%} of the official non-compliant samples are also found by our recomputation. "
         "Chemistry differs in 2016–2022 for explained reasons.")
fig = go.Figure()
for col, name, color, dash in (("chem_nc_official", "Chemistry — official", PALETTE["blue"], "solid"),
                               ("chem_nc_recomputed", "Chemistry — recomputed", PALETTE["blue"], "dot"),
                               ("bact_nc_official", "Bacteria — official", PALETTE["vermillion"], "solid"),
                               ("bact_nc_recomputed", "Bacteria — recomputed", PALETTE["vermillion"], "dot")):
    fig.add_trace(go.Scatter(x=cc["annee"], y=cc[col], name=name, mode="lines+markers",
                             line=dict(color=color, dash=dash, width=2), marker=dict(size=8),
                             hovertemplate="%{x}: %{y:,} samples<extra>" + name + "</extra>"))
layout(fig, "Year (2026: January–August)", "Non-compliant samples", height=380)
show(fig, "Lines: samples declared non-compliant by the ARS (solid) and samples where we find a value above the limit "
          "written on the row (dotted), for bacteria and chemistry.")
st.markdown(
    "- **Temporary derogations**: since 2023, most samples above a limit but officially compliant are under a "
    "prefectoral derogation (code *D*).\n"
    "- **Limits that changed**: in 2016–2022, selenium and antimony were judged against their former limits "
    "(10 and 5 µg/L), while the published rows carry the current ones (20 and 10 µg/L, since 01/01/2023, "
    "directive (EU) 2020/2184 transposed by the order of 30/12/2022). Chlorites (2016–2022): 95% of the gap is "
    "≤ 0.7 mg/L, the limit of the dataset code for chlorites when the treatment can generate them.\n"
    "- **Consequence**: the app uses the **official conformity** for history and KPIs, and the recomputation for the "
    "score (windows from September 2023, where both agree) and the families without an official flag.")
with st.expander("Detail of the chemistry gap by parameter"):
    gap = load_table("dq_chem_gap")
    st.dataframe(gap.sort_values(["annee", "n_samples"], ascending=[True, False]), hide_index=True)

# --- Coverage ------------------------------------------------------------------------------------------------
st.subheader("Coverage: big and small networks are not sampled alike")
uy = load_table("udi_year")
yr = min(f.years[1], config.COMPLETE_YEARS[-1])
u = uy[(uy["annee"] == yr) & (uy["n_samples"] > 0)]
med = u["n_samples"].median()
headline(f"In {yr}, half of the {len(u):,} networks had {med:.0f} samples or fewer; the most sampled had "
         f"{u['n_samples'].max():,}.")
fig = go.Figure(go.Histogram(x=np.log10(u["n_samples"]), nbinsx=40, marker_color=PALETTE["blue"],
                             marker_line_color="white", marker_line_width=1,
                             hovertemplate="10^%{x:.1f} samples: %{y:,} networks<extra></extra>"))
fig.update_xaxes(tickvals=[0, 1, 2, 3], ticktext=["1", "10", "100", "1,000"])
layout(fig, f"Samples per network in {yr} (log scale)", "Number of networks", height=340, legend=False)
show(fig, f"Histogram: number of samples taken in each distribution network in {yr}, on a logarithmic axis.")

# --- All checks -----------------------------------------------------------------------------------------------
with st.expander(f"All {len(checks)} automatic checks (scripts/03_build_aggregates.py)"):
    st.dataframe(checks.assign(ok=checks["ok"].map({True: "✅ pass", False: "❌ fail"})), hide_index=True)

st.subheader("Biases and limits to keep in mind")
st.markdown(
    "- **Sampling frequency depends on network size**: a small network sampled 4 times a year has a much more "
    "uncertain rate than a city sampled 300 times — shown by the confidence level of the score.\n"
    "- **Upstream samples**: a sample taken at a plant or a catchment is attached to every network it feeds "
    "(×1.43 on average); national counts use each sample once.\n"
    "- **Population per network is unknown**: population KPIs count a whole commune as soon as one of its networks is "
    "affected — an upper bound.\n"
    "- **2026 is partial** (January–August) and **overseas departments** are completed progressively.\n"
    "- The producer **corrected a publication anomaly** and re-published past years up to 2024; our files match the "
    "online versions (size and SHA-1 checked on 19/10/2026).\n"
    "- **What is not measured is not absent**: PFAS were rarely measured before 2025; there is no microplastics "
    "parameter in the data.\n"
    "- **Mediterranean coast** = Mediterranean departments outside mountain areas: an approximation.")
st.caption(SOURCE_CAPTION)

"""Page 1 — Hook and context: why it matters, how tap water is controlled, KPIs tied to the filters."""
import plotly.graph_objects as go
import streamlit as st

import config
from utils import metrics
from utils.filters import dept_mask, get_filters
from utils.io import SOURCE_CAPTION, load_table, search_communes
from utils.viz import PALETTE, fmt_int, layout, show

f = get_filters()
st.title("💧 Is my tap water good?")

ny = load_table("national_year")
rs = load_table("dq_result_status")
last = config.COMPLETE_YEARS[-1]
n_results = rs[(rs["annee"] == last) & (rs["status"] != "not_measured")]["n"].sum()
n_samples = int(ny.loc[ny["annee"] == last, "n_samples"].iloc[0])

st.markdown(
    f"French tap water is presented by the Ministry of Health as *the most controlled food in France*. "
    f"In {last}, the Regional Health Agencies (ARS) took **{fmt_int(n_samples)} samples** and recorded "
    f"**{n_results / 1e6:.1f} million analysis results**. **But what do they say about *your* water?**"
)

# --- Hook: find your town ------------------------------------------------------------------------
with st.container(border=True):
    st.markdown("**Find your town** — score /100, grade A–E and the report that explains it.")
    q = st.text_input("Town name", placeholder="e.g. Villejuif, Chamonix, Sète…", key="intro_search",
                      label_visibility="collapsed")
    if q:
        hits = search_communes(q, limit=8)
        if hits.empty:
            st.warning("No town found with this name.")
        else:
            cols = st.columns(min(4, len(hits)))
            for i, (_, r) in enumerate(hits.head(4).iterrows()):
                if cols[i].button(r["label"], key=f"go_{r['insee']}"):
                    st.session_state["insee"] = r["insee"]
                    st.switch_page("sections/ma_commune.py")

# --- KPIs tied to the filters ----------------------------------------------------------------------
metrics.render_kpis(f)

# --- Trend chart ------------------------------------------------------------------------------------
dy = load_table("dept_year")

t = dy[dept_mask(dy, f)].groupby("annee")[["n_bact", "n_bact_nc", "n_chem", "n_chem_nc"]].sum().reset_index()
t["bact"] = t["n_bact_nc"] / t["n_bact"]
t["chem"] = t["n_chem_nc"] / t["n_chem"]
t = t[t["annee"].between(*f.years)]
fig = go.Figure()
for col, name, color in (("bact", "Bacteriological", PALETTE["vermillion"]), ("chem", "Chemical", PALETTE["blue"])):
    fig.add_trace(go.Scatter(x=t["annee"], y=100 * t[col], name=name, mode="lines+markers+text",
                             line=dict(color=color, width=2), marker=dict(size=8),
                             text=[f"{v:.1f}%" if a in (t['annee'].min(), t['annee'].max()) else ""
                                   for a, v in zip(t["annee"], 100 * t[col])], textposition="top center",
                             customdata=t[[f"n_{col}_nc", f"n_{col}"]],
                             hovertemplate="%{x}: %{y:.2f}% non-compliant<br>%{customdata[0]:,} of %{customdata[1]:,} "
                                           "samples<extra>" + name + "</extra>"))
if f.years[1] == config.PARTIAL_YEAR:
    fig.add_vrect(x0=config.PARTIAL_YEAR - 0.5, x1=config.PARTIAL_YEAR + 0.5, fillcolor="grey", opacity=0.12,
                  line_width=0, annotation_text="2026: Jan–Aug only", annotation_position="top left")
layout(fig, "Year", "Non-compliant samples (%)")
fig.update_yaxes(rangemode="tozero")
st.subheader("Non-compliant samples per year")
show(fig, f"Line chart: share of samples officially non-compliant with the bacteriological and the chemical limits, "
          f"per year, {f.scope_label}. The chemical share jumps in 2021 — the Deep dives page explains why.")

# --- Context ------------------------------------------------------------------------------------------
st.subheader("How tap water is controlled")
a, b, c = st.columns(3)
a.markdown("**Who?** The Regional Health Agencies (ARS) take samples, from the catchment to the tap, and an "
           "approved laboratory analyses them. The results feed the national SISE-Eaux database.")
b.markdown("**Where?** In each **distribution network (UDI)**: a network in which water quality is homogeneous. "
           "France has more than 25,000; a town can be served by several, and a network can serve several towns.")
c.markdown("**Against what?** **Quality limits** concern health (bacteria, nitrates, pesticides, metals, PFAS…). "
           "**Quality references** are indicators of treatment and comfort (turbidity, colour, iron…).")
st.info("**This app's score is an educational indicator, not a health opinion.** The official opinion on your water "
        "is the one of your ARS, also printed on your water bill. A missing measurement is not an absence of "
        "pollutant; a correlation is not a cause.", icon="ℹ️")

with st.expander("Data, licence and caveats"):
    st.markdown(
        f"- **Data:** {config.DATASET_CITATION} — [{config.DATASET_PAGE}]({config.DATASET_PAGE})\n"
        "- Samples validated by the ARS since 1 January 2016; **2026 is partial (samples up to 31 August 2026)**; "
        "overseas departments are completed progressively.\n"
        "- The producer corrected a publication anomaly and re-published past years up to 2024 (our local files "
        "match the online versions, checked by size and SHA-1).\n"
        "- Small networks are sampled a few times a year, big cities hundreds of times: uncertainty differs, "
        "the app shows a confidence level.\n"
        "- Reference data: geo.api.gouv.fr (communes), INSEE density grid, Cerema (Mountain Act), Etalab contours — "
        "all under Licence Ouverte 2.0. Full list in `docs/sources.md`."
    )
st.caption(SOURCE_CAPTION)

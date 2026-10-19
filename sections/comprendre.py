"""Page 2 — What is measured, which thresholds apply, and how often they are exceeded in France."""
import plotly.graph_objects as go
import streamlit as st

import config
from utils.filters import get_filters
from utils.io import SOURCE_CAPTION, load_table
from utils.score import KEY_LABELS
from utils.viz import FAMILY_COLORS, FAMILY_LABELS, headline, layout, pct, show

f = get_filters()
st.title("🔬 Understand your water")

year = min(f.years[1], config.COMPLETE_YEARS[-1])
py = load_table("param_year")
cat = load_table("params_catalog").set_index("code")
y = py[py["annee"] == year]

# One row per parameter (twin codes merged): samples measured and samples above the applicable threshold
KEYS = {  # code_merged -> (family, threshold kind shown)
    "ECOLI": "micro", "STRF": "micro",
    "NO3": "chem", "PESTOT": "chem", "CLDZ_D": "chem", "ADET": "chem", "SPFAS": "chem", "AS": "chem", "PB": "chem",
    "CLVYL": "chem", "THM4": "chem", "BRATE": "chem",
    "CTF": "comfort", "TURBNFU": "comfort", "FET": "comfort", "MN": "comfort", "ALTMICR": "comfort",
    "471811R": "comfort", "MTCESA": "comfort",
}
g = (y[y["code_merged"].isin(KEYS)].groupby("code_merged")
     .agg(n=("n_samples", "sum"), lim=("n_exceed_limit", "sum"), ind=("n_exceed_indicative", "sum"),
          ref=("n_exceed_reference", "sum"), thr=("typical_threshold", "first"),
          kind=("typical_threshold_kind", "first")).reset_index())
g["n_exceed"] = g["lim"] + g["ind"] + g["ref"]
g["share"] = g["n_exceed"] / g["n"]
g["family"] = g["code_merged"].map(KEYS)
g["label"] = g["code_merged"].map(lambda c: KEY_LABELS.get(c) or cat["label"].get(c, c))
g["label"] = g["label"].replace({"Total pesticides": "Total pesticides (sum)"})
g["label"] = g.apply(lambda r: r["label"] if r["code_merged"] != "CLDZ_D" else "Chloridazone desphenyl (metabolite)", axis=1)
g["label"] = g.apply(lambda r: r["label"] if r["code_merged"] != "ADET" else "Atrazine desethyl (metabolite)", axis=1)
g = g.sort_values("share")

top = g.sort_values("share", ascending=False).iloc[0]
headline(f"In {year}, no single parameter exceeded its threshold in more than {pct(top['share'])} of the samples "
         f"where it was measured — the most frequent is {top['label']}.")

fig = go.Figure()
for fam in ("micro", "chem", "comfort"):
    d = g[g["family"] == fam]
    fig.add_trace(go.Bar(y=d["label"], x=100 * d["share"], orientation="h", name=FAMILY_LABELS[fam],
                         marker_color=FAMILY_COLORS[fam], text=[f"{100 * v:.2f}%" for v in d["share"]],
                         textposition="outside", customdata=d[["n_exceed", "n", "thr", "kind"]],
                         hovertemplate="%{y}<br>%{customdata[0]:,} of %{customdata[1]:,} samples above the "
                                       "%{customdata[3]} (%{customdata[2]})<extra></extra>"))
layout(fig, f"Samples above the threshold in {year} (%)", None, height=560)
fig.update_layout(barmode="overlay", yaxis=dict(categoryorder="array", categoryarray=g["label"].tolist()))
show(fig, f"Horizontal bars: for 19 key parameters, share of the samples analysed in {year} where the value was "
          "above its threshold (health limit, quality reference, or 0.9 µg/L indicative value), coloured by family.")

st.subheader("The four families of parameters")
st.caption("How this app classifies the 1,789 parameters of the dataset (rules in `utils/prep.py`).")
fam_text = {
    "micro": ("🦠 Microbiology — health limits",
              "Bacteria such as *E. coli* and enterococci, counted per 100 mL. **Limit: 0 per 100 mL.** "
              "The score uses the official conformity of each sample over the last 12 months."),
    "chem": ("⚗️ Health-related chemistry — health limits",
             "Nitrates (**50 mg/L**), pesticides and their relevant metabolites (**0.1 µg/L** per substance, "
             "**0.5 µg/L** in total), PFAS (**0.1 µg/L** for the sum of 20, in the routine control since "
             "1 January 2026), metals (lead and arsenic **10 µg/L**), disinfection by-products… "
             "The score uses the last 36 months."),
    "comfort": ("💡 Indicators and comfort — quality references",
                "Turbidity, coliform bacteria, iron, manganese, aluminium, pH, conductivity… They signal a treatment "
                "or network problem rather than a direct health risk. Pesticide metabolites classified **non-relevant** "
                "by Anses are compared with the **0.9 µg/L indicative value** (see Deep dives)."),
    "info": ("ℹ️ Information only — no threshold",
             "Hardness (limescale), calcium, magnesium, temperature… No health limit: hard water is not a health "
             "problem, so it never lowers the score."),
}
cols = st.columns(2)
for i, (fam, (title, text)) in enumerate(fam_text.items()):
    with cols[i % 2].expander(title, expanded=True):
        st.markdown(text)
        n_par = int((cat["family"] == fam).sum())
        st.caption(f"{n_par:,} parameters of the dataset in this family.")

st.markdown("**Limits vs references.** A *quality limit* is a health threshold: above it the sample is "
            "declared non-compliant. A *quality reference* is an indicator value used to "
            "monitor treatment and the network. Thresholds are those written on each result row of the dataset "
            "(the decree of 11 January 2007 as amended).")
with st.expander("Thresholds used in this app (from the dataset rows)"):
    tbl = g[["label", "family", "thr", "kind"]].rename(columns={"label": "Parameter", "family": "Family",
                                                                 "thr": "Threshold", "kind": "Type"})
    tbl["Unit"] = [cat["limit_unit"].get(c) if k == "limit" else cat["ref_unit"].get(c) if k == "reference" else "µg/L"
                   for c, k in zip(g["code_merged"], g["kind"])]
    st.dataframe(tbl.sort_values(["Family", "Parameter"]), hide_index=True)
st.caption(SOURCE_CAPTION)

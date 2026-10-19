"""Page 4 — Compare towns side by side, then groups of communes (mountain vs Mediterranean, urban vs rural, size)."""
from dataclasses import replace

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.filters import commune_mask, get_filters
from utils.io import SOURCE_CAPTION, commune_network_links, communes, load_table, search_communes
from utils.viz import FAMILY_LABELS, SERIES, headline, layout, show

f = get_filters()
st.title("⚖️ Compare")
com = communes().set_index("insee")

# --- Towns side by side --------------------------------------------------------------------------------
st.subheader("Towns side by side")
if "compare" not in st.session_state:
    st.session_state["compare"] = ["75056", "94076"]   # Paris vs Villejuif
c1, c2 = st.columns([1, 2])
q = c1.text_input("Add a town", placeholder="e.g. Chamonix", key="cmp_q")
hits = search_communes(q, limit=15)["insee"].tolist() if q else []
options = list(dict.fromkeys(st.session_state["compare"] + hits))
chosen = c2.multiselect("Towns compared (2 to 4)", options, default=st.session_state["compare"], max_selections=4,
                        format_func=lambda i: com.loc[i, "label"], key="cmp_sel")
st.session_state["compare"] = chosen
sel = com.loc[chosen].reset_index()
sel = sel[sel["score"].notna()]

if len(sel) < 2:
    st.info("Choose at least two towns with a score.")
else:
    best, worst = sel.loc[sel["score"].idxmax()], sel.loc[sel["score"].idxmin()]
    headline(f"{best['nom']} scores {best['score']:.1f}/100 ({best['grade']}), {worst['nom']} "
             f"{worst['score']:.1f}/100 ({worst['grade']}): a gap of {best['score'] - worst['score']:.1f} points.")
    cols = st.columns(len(sel))
    for col, (_, r) in zip(cols, sel.iterrows()):
        col.metric(r["label"], f"{r['score']:.1f}/100", f"grade {r['grade']} · confidence {r['confidence']}",
                   delta_color="off", border=True)

    long = sel.melt(id_vars=["label"], value_vars=["micro", "chem", "comfort"], var_name="family", value_name="v")
    fig = go.Figure()
    for i, (lab, d) in enumerate(long.groupby("label", sort=False)):
        fig.add_trace(go.Bar(x=d["family"].map(FAMILY_LABELS), y=d["v"], name=lab, marker_color=SERIES[i],
                             text=[f"{v:.0f}" if pd.notna(v) else "n/a" for v in d["v"]], textposition="outside",
                             hovertemplate="%{x}: %{y:.1f}/100<extra>" + lab + "</extra>"))
    layout(fig, None, "Sub-score (/100)", height=360)
    fig.update_yaxes(range=[0, 110])
    show(fig, "Grouped bars: microbiology, health-chemistry and comfort sub-scores of each town (out of 100).")

    # key facts per town, from the current windows of all its networks
    links = commune_network_links()
    w = load_table("udi_param_window")
    rows = []
    for _, r in sel.iterrows():
        nets = links.loc[links["insee"] == r["insee"], "cdreseau"]
        p = w[w["cdreseau"].isin(nets)]
        mw = load_table("udi_micro_window")
        m = mw[mw["cdreseau"].isin(nets)]

        def mx(code):
            v = p.loc[p["code"] == code, "max_value"]
            return float(v.max()) if len(v) else np.nan

        th = p.loc[p["code"] == "TH", "mean"]
        rows.append({"Town": r["label"], "Networks": len(nets),
                     "Bacteriological samples (12 m)": int(m["n_bact"].sum()),
                     "Non-compliant (12 m)": int(m["n_bact_nc"].sum()),
                     "Nitrates max (mg/L, 36 m)": mx("NO3"),
                     "Pesticide results above 0.1 µg/L (36 m)": int(p.loc[p["subfamily"] == "pesticides", "n_exceed"].sum()),
                     "PFAS sum max (µg/L)": mx("SPFAS"),
                     "Hardness mean (°f)": float(th.mean()) if len(th) else np.nan})
    st.dataframe(pd.DataFrame(rows), hide_index=True,
                 column_config={k: st.column_config.NumberColumn(format="%.3g") for k in
                                ("Nitrates max (mg/L, 36 m)", "PFAS sum max (µg/L)", "Hardness mean (°f)")})
    st.caption("Table: key facts of each town over the score windows (12 months for bacteria, 36 months for chemistry). "
               "Empty = not measured or not detected. Sums are over all the networks serving the town.")

# --- Groups of communes ----------------------------------------------------------------------------------
st.subheader("Groups of communes")
d = communes()
d = d[d["is_current"] & d["score"].notna()]
d = d[commune_mask(d, replace(f, commune_type="all"))]   # groups ARE commune types: only the region filter applies
size_bins = [0, 500, 2000, 10000, 50000, np.inf]
size_labels = ["< 500", "500–2,000", "2,000–10,000", "10,000–50,000", "> 50,000"]
d["size"] = pd.cut(d["population"], size_bins, labels=size_labels, right=False)
d["territory"] = np.select([d["mountain"].fillna(False).astype(bool), d["mediterranean_coast"].fillna(False).astype(bool)],
                           ["Mountain (loi Montagne)", "Mediterranean coast (approx.)"], "Other communes")
d["density"] = d["density3"].map({1: "Urban — dense", 2: "Urban — intermediate", 3: "Rural"})
group_by = st.segmented_control("Group communes by", ["Territory", "Urban / rural", "Population"], default="Territory",
                                key="cmp_group", help="Mediterranean coast = communes of the Mediterranean coastal "
                                "departments outside mountain areas: an approximation, the national list of coastal "
                                "communes was not available.")
col = {"Territory": "territory", "Urban / rural": "density", "Population": "size"}[group_by or "Territory"]
order = {"territory": ["Mountain (loi Montagne)", "Mediterranean coast (approx.)", "Other communes"],
         "density": ["Urban — dense", "Urban — intermediate", "Rural"], "size": size_labels}[col]
med = d.groupby(col, observed=True)["score"].agg(["median", "size"]).reindex(order).dropna()
de = d.groupby(col, observed=True)["grade"].apply(lambda s: s.isin(["D", "E"]).mean()).reindex(order)
hi, lo = med["median"].idxmax(), med["median"].idxmin()
headline(f"{f.scope_label}: median score {med.loc[hi, 'median']:.1f} for '{hi}' vs {med.loc[lo, 'median']:.1f} "
         f"for '{lo}'; {de.loc[lo]:.0%} of '{lo}' communes are graded D or E vs {de.loc[hi]:.0%} of '{hi}'.")
fig = go.Figure()
for i, g in enumerate(order):
    s = d.loc[d[col] == g, "score"]
    if s.empty:
        continue
    fig.add_trace(go.Box(y=s, name=f"{g}<br>(n = {len(s):,})", marker_color=SERIES[i], boxpoints=False,
                         hoverinfo="y+name"))
layout(fig, None, "Commune score (/100)", height=420, legend=False)
show(fig, f"Box plots: distribution of the current scores of the communes of each group ({f.scope_label}); the line "
          "is the median, the box holds the middle half of the communes.")
st.caption("A difference between groups is not a cause: small rural networks are sampled less often, mountain "
           "water is often very low in minerals, and the Mediterranean group is an approximation.")
st.caption(SOURCE_CAPTION)

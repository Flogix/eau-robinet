"""Page 3 — My town: score /100, grade, confidence, the "why" report per network, and parameter history."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import config
from utils import score as S
from utils.io import (SOURCE_CAPTION, commune_network_links, communes, load_table, network_history,
                      search_communes)
from utils.viz import FAMILY_COLORS, FAMILY_LABELS, GRADE_COLORS, PALETTE, headline, layout, show, threshold

st.title("🏠 My town")

DEFAULT_INSEE = "75056"  # Paris


def pick_commune() -> str:
    """Search box with accent-insensitive matching; the choice is kept in session state and in the URL."""
    current = st.session_state.get("insee") or st.query_params.get("insee") or DEFAULT_INSEE
    com = communes().set_index("insee")
    if current not in com.index:
        current = DEFAULT_INSEE
    c1, c2 = st.columns([1, 2])
    q = c1.text_input("Search a town", placeholder="Type a name, e.g. Villejuif", key="town_q",
                      help="Accents and hyphens are ignored. Homonyms are shown with their department number.")
    if q:
        hits = search_communes(q, limit=30)
        if hits.empty:
            c2.warning("No town found with this name.")
        else:
            options = hits["insee"].tolist()
            choice = c2.selectbox(f"{len(hits)} match(es)", options, format_func=lambda i: com.loc[i, "label"],
                                  key="town_pick")
            current = choice
    st.session_state["insee"] = current
    st.query_params["insee"] = current
    return current


insee = pick_commune()
com = communes().set_index("insee")
c = com.loc[insee]
udi = load_table("udi_scores").set_index("cdreseau")
links = commune_network_links()
nets = links[links["insee"] == insee]
names = load_table("dim_udi").set_index("cdreseau")["nomreseau"]

st.subheader(f"{c['nom']} ({c['dep']} — {c['dep_nom']})")
facts = [f"{int(c['population']):,} inhabitants" if pd.notna(c["population"]) else None, c.get("density7_label"),
         "Mountain Act commune" if c.get("mountain") else None,
         "Mediterranean department outside mountain areas (approximation of the coast)" if c.get("mediterranean_coast") else None,
         f"served by {len(nets)} distribution network(s)"]
st.caption(" · ".join(x for x in facts if x))

if pd.isna(c.get("score")):
    st.warning("No score for this town: none of its networks has samples in the last 12/36 months.")
    st.stop()

# --- Score, grade, confidence ------------------------------------------------------------------------
grade = c["grade"]
headline(f"{c['nom']}: {c['score']:.1f}/100, grade {grade} — confidence {c['confidence']}.")
left, right = st.columns([1, 1.3])
with left:
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=round(float(c["score"]), 1), number=dict(suffix="/100", valueformat=".1f"),
        title=dict(text=f"Grade <b>{grade}</b>"),
        gauge=dict(axis=dict(range=[0, 100], tickvals=[0, 40, 60, 75, 90, 100]),
                   bar=dict(color="#333333", thickness=0.25),
                   steps=[dict(range=[lo, hi], color=GRADE_COLORS[g]) for lo, hi, g in
                          ((0, 40, "E"), (40, 60, "D"), (60, 75, "C"), (75, 90, "B"), (90, 100, "A"))])))
    fig.update_layout(height=260, margin=dict(l=20, r=20, t=50, b=10))
    show(fig, f"Gauge: score {c['score']:.1f} out of 100, in the band of grade {grade} "
              "(E < 40 ≤ D < 60 ≤ C < 75 ≤ B < 90 ≤ A).", source="")
with right:
    subs = pd.DataFrame({"family": ["micro", "chem", "comfort"],
                         "value": [c["micro"], c["chem"], c["comfort"]]})
    subs["label"] = subs["family"].map(FAMILY_LABELS) + " (weight " + subs["family"].map(
        lambda k: f"{config.WEIGHTS[k]:.0%}") + ")"
    fig = go.Figure(go.Bar(x=subs["value"].fillna(0), y=subs["label"], orientation="h",
                           marker_color=[FAMILY_COLORS[k] for k in subs["family"]],
                           text=[f"{v:.0f}" if pd.notna(v) else "not measured" for v in subs["value"]],
                           textposition="outside", hovertemplate="%{y}: %{x:.1f}/100<extra></extra>"))
    layout(fig, "Sub-score (/100)", None, height=260, legend=False)
    fig.update_xaxes(range=[0, 110])
    show(fig, "Bars: the three sub-scores out of 100; the global score is their weighted mean over the measured "
              "families only.", source="")
st.caption(f"**Confidence {c['confidence']}**: high = microbiology, chemistry and comfort measured, ≥ 12 "
           "bacteriological samples in 12 months, nitrates and pesticides analysed in 36 months; low = fewer than 4 "
           "bacteriological samples or a family missing. The score is an educational indicator, not a health opinion.")

# --- Networks and reports ----------------------------------------------------------------------------
st.subheader("Why this score? — network by network")
n = nets.merge(udi.reset_index(), on="cdreseau", how="left")
n["name"] = n["cdreseau"].map(names)
if len(n) > 1:
    tbl = n[["name", "cdreseau", "score", "grade", "confidence", "n_bact", "districts"]].sort_values("score")
    st.dataframe(tbl.rename(columns={"name": "Network", "cdreseau": "Code", "score": "Score", "grade": "Grade",
                                     "confidence": "Confidence", "n_bact": "Bacteriological samples (12 months)",
                                     "districts": "Districts served"}),
                 hide_index=True, column_config={"Score": st.column_config.NumberColumn(format="%.1f")})
    st.caption(f"The town's score is the mean of its {n['score'].notna().sum()} scored networks; the worst is shown first.")

params = load_table("udi_param_window")
fam = load_table("udi_family_window")
p95 = load_table("udi_param_p95")
cat = load_table("params_catalog")
labels = dict(zip(cat["code"], cat["label"]))
ranges = S.reference_ranges(cat)
ordered = n.sort_values("score")
tabs = st.tabs([f"{r['name'] or r['cdreseau']} — {r['score']:.0f} ({r['grade']})" if pd.notna(r["score"])
                else f"{r['name'] or r['cdreseau']} — no data" for _, r in ordered.iterrows()])
for tab, (_, r) in zip(tabs, ordered.iterrows()):
    with tab:
        if pd.isna(r["score"]):
            st.write("No sample in the windows for this network.")
            continue
        row = udi.loc[r["cdreseau"]].copy()
        row["cdreseau"] = r["cdreseau"]
        rep = S.why_report(row, params[params["cdreseau"] == r["cdreseau"]], fam[fam["cdreseau"] == r["cdreseau"]],
                           p95[p95["cdreseau"] == r["cdreseau"]], labels, ranges=ranges)
        for icon, text in rep:
            st.markdown(f"{icon} {text}")
        if isinstance(r.get("districts"), str):
            st.caption(f"Districts served: {r['districts']}")

st.caption("Legend: ✅ strength · ❌ above a health limit · ⚠️ vigilance (above half of a limit, or above a "
           "quality reference) · ℹ️ information · ❔ not measured. Windows: 12 months (bacteria, comfort) and "
           "36 months (chemistry) up to 31 August 2026.")

# --- History of key parameters -------------------------------------------------------------------------
st.subheader("History of a key parameter, 2016–2026")
hist = network_history(tuple(n["cdreseau"]))
if hist.empty:
    st.info("No history for these networks.")
else:
    avail = hist.groupby("code")["n"].sum().sort_values(ascending=False)
    pref = [k for k in ("NO3", "PESTOT", "SPFAS", "ECOLI", "TH", "CLDZ_D", "PB", "AS") if k in avail.index]
    options = pref + [k for k in avail.index if k not in pref]
    code = st.selectbox("Parameter", options, format_func=lambda k: S.KEY_LABELS.get(k) or labels.get(k, k),
                        help="Yearly maximum and mean of the measurements of each network serving the town.")
    h = hist[hist["code"] == code].copy()
    h["name"] = h["cdreseau"].map(names).fillna(h["cdreseau"])
    lab = S.KEY_LABELS.get(code) or labels.get(code, code)
    unit = cat.set_index("code")["unit"].get(code)
    unit = unit if isinstance(unit, str) else ""
    fig = go.Figure()
    colors = [PALETTE[k] for k in ("blue", "orange", "green", "vermillion", "sky", "purple")]
    for i, (net, d) in enumerate(h.groupby("name")):
        col = colors[i % len(colors)]
        fig.add_trace(go.Scatter(x=d["annee"], y=d["max"], name=f"{net} — max", mode="lines+markers",
                                 line=dict(color=col, width=2), marker=dict(size=8),
                                 customdata=d[["n", "n_exceed"]],
                                 hovertemplate="%{x}: max %{y:.3g} " + unit + "<br>%{customdata[0]} measurements, "
                                               "%{customdata[1]} above the threshold<extra>" + net + "</extra>"))
        fig.add_trace(go.Scatter(x=d["annee"], y=d["mean"], name=f"{net} — mean", mode="lines",
                                 line=dict(color=col, width=2, dash="dot"),
                                 hovertemplate="%{x}: mean %{y:.3g} " + unit + "<extra>" + net + "</extra>"))
    thr = h["threshold"].dropna()
    if len(thr):
        kind = h["threshold_kind"].dropna().iloc[-1]
        threshold(fig, float(thr.iloc[-1]), f"{kind} {thr.iloc[-1]:g} {unit}", color=PALETTE["vermillion"])
    if h["annee"].max() == config.PARTIAL_YEAR:
        fig.add_vrect(x0=config.PARTIAL_YEAR - 0.5, x1=config.PARTIAL_YEAR + 0.5, fillcolor="grey", opacity=0.12,
                      line_width=0, annotation_text="2026 partial", annotation_position="top left")
    layout(fig, "Year", f"{lab} ({unit})" if unit else lab, height=400)
    show(fig, f"Lines: yearly maximum (solid) and mean (dotted) of {lab} in each network serving {c['nom']}, "
              "with the threshold as a dashed line when there is one.")
st.caption(SOURCE_CAPTION)

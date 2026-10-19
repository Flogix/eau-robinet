"""Town against town: one searchable multi-select, the marks side by side, key facts, then groups of towns."""
from dataclasses import replace

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import config
from utils import metrics
from utils import score as S
from utils.filters import commune_mask, get_filters
from utils.i18n import lang, num, pct, t, tn
from utils.io import EXAMPLE_TOWNS, commune_network_links, communes, load_table, town_options
from utils.viz import SERIES, chart, headline, kicker, layout, lede, takeaway

f = get_filters()
kicker(t("cmp.kicker"))
st.title(t("cmp.title"))
lede(t("cmp.lede"))
fmt1 = (lambda v: f"{v:.1f}".replace(".", ",")) if lang() == "fr" else (lambda v: f"{v:.1f}")

options, labels = town_options()
if "cmp_sel" not in st.session_state:
    st.session_state["cmp_sel"] = list(EXAMPLE_TOWNS)
chosen = st.multiselect(t("cmp.pick"), options, format_func=labels.get, max_selections=6, key="cmp_sel",
                        help=t("cmp.pick.help"))
com = communes().set_index("insee")
sel = com.loc[chosen].reset_index()
sel = sel[sel["score"].notna()]

if len(sel) < 2:
    st.info(t("cmp.need2"))
else:
    best, worst = sel.loc[sel["score"].idxmax()], sel.loc[sel["score"].idxmin()]
    headline(t("cmp.headline", best=best["nom"], bs=fmt1(best["score"]), bg=best["grade"], worst=worst["nom"],
               ws=fmt1(worst["score"]), wg=worst["grade"], gap=fmt1(best["score"] - worst["score"])))
    cols = st.columns(len(sel))
    for col, (_, r) in zip(cols, sel.iterrows()):
        col.metric(r["label"], f"{fmt1(r['score'])}/100",
                   t("cmp.metric.delta", g=r["grade"], c=t(f"conf.{r['confidence']}")), delta_color="off", border=True)

    fams = ["micro", "chem", "comfort"]
    fig = go.Figure()
    for i, (_, r) in enumerate(sel.iterrows()):
        vals = [r[k] for k in fams]
        fig.add_trace(go.Bar(x=[t(f"fam.{k}") for k in fams], y=[0 if pd.isna(v) else v for v in vals],
                             name=r["label"], marker_color=SERIES[i % len(SERIES)],
                             text=[f"{v:.0f}" if pd.notna(v) else t("cmp.na") for v in vals], textposition="outside",
                             hovertemplate="%{x}: %{y:.1f}/100<extra>" + r["label"] + "</extra>"))
    layout(fig, None, t("cmp.y"), height=380)
    fig.update_yaxes(range=[0, 112])
    spread = {k: sel[k].max() - sel[k].min() for k in fams if sel[k].notna().sum() >= 2}
    fam_gap = max(spread, key=spread.get)
    hi, lo = sel.loc[sel[fam_gap].idxmax()], sel.loc[sel[fam_gap].idxmin()]
    chart(fig, t("cmp.bars.title"), t("cmp.bars.caption"),
          t("cmp.bars.take", fam=t(f"fam.{fam_gap}").lower(), hi=hi["nom"], vhi=f"{hi[fam_gap]:.0f}", lo=lo["nom"],
            vlo=f"{lo[fam_gap]:.0f}"))

    # --- Why the best town does better than the worst one --------------------------------------------------------
    st.markdown(f'<div class="ar-chart-title">{t("cmp.why.title")}</div>', unsafe_allow_html=True)
    cat = load_table("params_catalog")
    cat_labels = dict(zip(cat["code"], cat["label"]))
    if best["score"] - worst["score"] < 1:
        why = t("cmp.why.same", best=best["nom"], worst=worst["nom"], bs=fmt1(best["score"]), ws=fmt1(worst["score"]))
    else:
        gaps = {k: (best[k] - worst[k]) * config.WEIGHTS[k] for k in fams if pd.notna(best[k]) and pd.notna(worst[k])}
        fam_w = max(gaps, key=gaps.get) if gaps else "micro"
        why = t("cmp.why.lead", best=best["nom"], worst=worst["nom"], bs=fmt1(best["score"]), ws=fmt1(worst["score"]),
                fam=t(f"fam.{fam_w}").lower(), vb=f"{best[fam_w]:.0f}", vw=f"{worst[fam_w]:.0f}")
    for town_row in (worst, best):
        causes = metrics.town_causes(town_row["insee"])
        items = []
        k_nc, n_b = causes["micro"]
        if k_nc:
            items.append(tn("cmp.cause.micro", k_nc, k=num(k_nc), n=num(n_b)))
        for k in ("chem", "comfort"):
            if causes[k]:
                items.append(t(f"cmp.cause.{k}", param=S.label(causes[k], cat_labels)))
        why += " " + (t("cmp.why.town", town=town_row["nom"], causes=t("town.why.gen.join").join(items)) if items
                      else t("cmp.why.clean", town=town_row["nom"]))
    if len(sel) > 2:
        why += " " + t("cmp.why.end")
    takeaway(why)

    links = commune_network_links()
    w = load_table("udi_param_window")
    mw = load_table("udi_micro_window")
    rows = []
    for _, r in sel.iterrows():
        nets = links.loc[links["insee"] == r["insee"], "cdreseau"]
        p = w[w["cdreseau"].isin(nets)]
        m = mw[mw["cdreseau"].isin(nets)]

        def mx(code):
            v = p.loc[p["code"] == code, "max_value"]
            return float(v.max()) if len(v) else np.nan

        th = p.loc[p["code"] == "TH", "mean"]
        rows.append({t("cmp.col.town"): r["label"], t("cmp.col.nets"): len(nets),
                     t("cmp.col.nbact"): int(m["n_bact"].sum()), t("cmp.col.nc"): int(m["n_bact_nc"].sum()),
                     t("cmp.col.no3"): mx("NO3"),
                     t("cmp.col.pest"): int(p.loc[p["subfamily"] == "pesticides", "n_exceed"].sum()),
                     t("cmp.col.pfas"): mx("SPFAS"), t("cmp.col.th"): float(th.mean()) if len(th) else np.nan})
    st.markdown(f'<div class="ar-chart-title">{t("cmp.table.title")}</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(rows), hide_index=True,
                 column_config={k: st.column_config.NumberColumn(format="%.3g")
                                for k in (t("cmp.col.no3"), t("cmp.col.pfas"), t("cmp.col.th"))})
    st.caption(t("cmp.table.caption"))

# --- Groups ------------------------------------------------------------------------------------------------
kicker(t("cmp.groups.kicker"))
st.header(t("cmp.groups.title"))
d = communes()
d = d[d["is_current"] & d["score"].notna()]
d = d[commune_mask(d, replace(f, commune_type="all"))]   # groups are kinds of towns: only the region filter applies
size_bins = [0, 500, 2000, 10000, 50000, np.inf]
sep = " " if lang() == "fr" else ","
size_labels = ["< 500", f"500–2{sep}000", f"2{sep}000–10{sep}000", f"10{sep}000–50{sep}000", f"> 50{sep}000"]
d["size"] = pd.cut(d["population"], size_bins, labels=size_labels, right=False)
d["territory"] = np.select([d["mountain"].fillna(False).astype(bool), d["mediterranean_coast"].fillna(False).astype(bool)],
                           [t("cmp.grp.mountain"), t("cmp.grp.med")], t("cmp.grp.other"))
d["density"] = d["density3"].map({1: t("cmp.grp.dense"), 2: t("cmp.grp.inter"), 3: t("cmp.grp.rural")})
choices = {"territory": t("cmp.groups.territory"), "density": t("cmp.groups.density"), "size": t("cmp.groups.size")}
col = st.segmented_control(t("cmp.groups.by"), list(choices), format_func=choices.get, default="territory",
                           key="cmp_group", help=t("cmp.groups.help")) or "territory"
order = {"territory": [t("cmp.grp.mountain"), t("cmp.grp.med"), t("cmp.grp.other")],
         "density": [t("cmp.grp.dense"), t("cmp.grp.inter"), t("cmp.grp.rural")], "size": size_labels}[col]
med = d.groupby(col, observed=True)["score"].median().reindex(order).dropna()
de = d.groupby(col, observed=True)["grade"].apply(lambda s: s.isin(["D", "E"]).mean()).reindex(order)
if len(med) >= 2:
    hi, lo = med.idxmax(), med.idxmin()
    headline(t("cmp.groups.headline", scope=f.scope_label, hi=hi, hi_v=fmt1(med[hi]), lo=lo, lo_v=fmt1(med[lo]),
               de_lo=pct(de[lo], 0), de_hi=pct(de[hi], 0)))
fig = go.Figure()
for i, g in enumerate(order):
    s = d.loc[d[col] == g, "score"]
    if s.empty:
        continue
    fig.add_trace(go.Box(y=s, name=f"{g}<br>{t('cmp.box.n', n=num(len(s)))}", marker_color=SERIES[i],
                         boxpoints=False, hoverinfo="y+name"))
layout(fig, None, t("cmp.box.y"), height=420, legend=False)
chart(fig, t("cmp.box.title"), t("cmp.box.caption"), t("cmp.box.take"))

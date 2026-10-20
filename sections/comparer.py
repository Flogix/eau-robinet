"""Town against town: one searchable multi-select, the marks side by side, key facts, then groups of towns."""
from dataclasses import replace

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import compare_report as CR
from utils.filters import commune_mask, get_filters
from utils.i18n import lang, num, pct, t
from utils.io import EXAMPLE_TOWNS, commune_network_links, communes, load_table, town_options
from utils.town_search import town_search
from utils.viz import SERIES, chart, headline, kicker, layout, lede, takeaway

f = get_filters()
kicker(t("cmp.kicker"))
st.title(t("cmp.title"))
lede(t("cmp.lede"))
fmt1 = (lambda v: f"{v:.1f}".replace(".", ",")) if lang() == "fr" else (lambda v: f"{v:.1f}")

_, labels = town_options()
if "cmp_sel" not in st.session_state:   # first visit: the towns of a shared link (?towns=), else the examples
    from_url = [i for i in str(st.query_params.get("towns", "")).split(",") if i in labels][:6]
    st.session_state["cmp_sel"] = from_url or list(EXAMPLE_TOWNS)
added = st.session_state.pop("_cmp_add", None)          # chosen in the search box below, during the last run
if added and added not in st.session_state["cmp_sel"] and len(st.session_state["cmp_sel"]) < 6:
    st.session_state["cmp_sel"] = st.session_state["cmp_sel"] + [added]
# the multiselect only holds the towns compared (and the examples): no 35,000 options in the browser
small = list(dict.fromkeys(st.session_state["cmp_sel"] + EXAMPLE_TOWNS))
chosen = st.multiselect(t("cmp.pick"), small, format_func=labels.get, max_selections=6, key="cmp_sel",
                        help=t("cmp.pick.help"))
st.query_params["towns"] = ",".join(chosen)   # the comparison can be shared, and survives a reload
full = len(chosen) >= 6
town_search(t("cmp.add"), "cmp_search", lambda i: st.session_state.update(_cmp_add=i), disabled=full,
            placeholder=t("cmp.add.full") if full else None)
com = communes().set_index("insee")
sel = com.loc[chosen].reset_index()
sel = sel[sel["score"].notna()]

if len(sel) < 2:
    st.info(t("cmp.need2"))
else:
    headline(CR.headline_text(sel))
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
    chart(fig, t("cmp.bars.title"), t("cmp.bars.caption"), CR.spread_text(sel) or None)

    # --- Why the best town does better than the worst one --------------------------------------------------------
    st.markdown(f'<div class="ar-chart-title">{t("cmp.why.title")}</div>', unsafe_allow_html=True)
    cat = load_table("params_catalog")
    takeaway(CR.why_text(sel, dict(zip(cat["code"], cat["label"]))))   # same rules as the PDF below

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

    # --- PDF report of the comparison (rule-based text, English or French, identity of the app) -------------------
    st.markdown(f'<div class="ar-chart-title">{t("pdf.cmp.section")}</div>', unsafe_allow_html=True)
    st.markdown(t("pdf.cmp.section.text"))
    compared = list(sel["insee"])
    b1, b2 = st.columns(2)
    for col, code_lang, key in ((b1, "en", "pdf.cmp.button"), (b2, "fr", "pdf.cmp.button.fr")):
        col.download_button(
            t(key), data=lambda lg=code_lang: CR.build_pdf(compared, lg),
            file_name=CR.file_name(list(sel["nom"]), code_lang), mime="application/pdf",
            icon=":material/picture_as_pdf:", on_click="ignore", help=t("pdf.cmp.button.help"), key=f"cmp_pdf_{code_lang}")

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

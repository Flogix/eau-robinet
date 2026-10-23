# Conclusions page: hypothesis verification, analytical synthesis, civic takeaways, and limitations.
"""What it all means: each hypothesis restated, with the numbers, the verdict and what we conclude; one summary chart;
implications for a resident and for local authorities; limits."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import config
from utils.i18n import lang, num, pct, t
from utils.io import departments, load_table
from utils.viz import TEAL, chart, kicker, layout, lede

last = config.COMPLETE_YEARS[-1]
Y = (config.YEARS[0], last)
ny = load_table("national_year").set_index("annee")
dec = (lambda v, k=2: f"{v:.{k}f}".replace(".", ",")) if lang() == "fr" else (lambda v, k=2: f"{v:.{k}f}")

kicker(t("con.kicker"))
st.title(t("con.title"))
lede(t("con.lede", year=last, bact=pct(1 - ny.loc[last, "n_bact_nc"] / ny.loc[last, "n_bact"]),
       chem=pct(1 - ny.loc[last, "n_chem_nc"] / ny.loc[last, "n_chem"])))

# This page comes second in the menu: the summary of the findings, before the pages that prove them.
EVIDENCE = [("sections/comprendre.py", "nav.reading", ":material/science:"),
            ("sections/ma_commune.py", "nav.town", ":material/home_pin:"),
            ("sections/comparer.py", "nav.compare", ":material/compare_arrows:"),
            ("sections/overview.py", "nav.map", ":material/map:"),
            ("sections/deep_dives.py", "nav.monitor", ":material/search_insights:"),
            ("sections/mon_score.py", "nav.myscore", ":material/tune:")]
st.markdown(t("con.preview"))
cols = st.columns(2)
for i, (file, key, icon) in enumerate(EVIDENCE):
    cols[i % 2].page_link(file, label=t(key), icon=icon)

# H1: small networks
uy = load_table("udi_year")
u = uy[uy["annee"].between(*Y) & (uy["n_bact"] > 0)]
u = u.assign(size=pd.cut(u["n_bact"], [0, 6, 12, 52, np.inf], right=False, labels=["s", "m", "l", "xl"]))
h1 = u.groupby("size", observed=True).agg(samples=("n_bact", "sum"), nc=("n_bact_nc", "sum"))
h1["rate"] = h1["nc"] / h1["samples"]
small = h1.loc[["s", "m"]]

# H2: two maps
dy = load_table("dept_year")
d = dy[dy["annee"].between(*Y)].groupby("dep")[["n_bact", "n_bact_nc", "n_chem", "n_chem_nc"]].sum()
d = d[~d.index.str.startswith("97")]
d["b"], d["c"] = d["n_bact_nc"] / d["n_bact"], d["n_chem_nc"] / d["n_chem"]
rho = d["b"].rank().corr(d["c"].rank())
names = departments().set_index("dep")["dep_nom"]

# H3: exceedances with and without the three metabolite families
nc = ny["n_chem_nc"]
py = load_table("param_year")
META = {"CLDZ_D", "CLDZ_MD", "MTCESA", "MTCNOA", "471811R", "CLTHALS"}
rows = py[(py["family"] == "chem") | py["code"].isin(["ESAMTC", "NOAMTC", "R471811", "471811R", "MTCESA", "MTCNOA"])]
rows = rows[rows["annee"] <= last]
allx = rows.groupby("annee")["n_exceed_limit"].sum()
without = rows[~rows["code_merged"].isin(META)].groupby("annee")["n_exceed_limit"].sum()

# H4: hardness, and the robustness of the score
th = load_table("udi_param_window")
th = th.loc[th["code"] == "TH", "mean"]
sens = load_table("score_sensitivity")
sens = sens[sens["variant"] != "default"]

kicker(t("con.found.kicker"))
st.header(t("con.found.title"))
blocks = {
    "h1": dict(share_nc=pct(small["nc"].sum() / h1["nc"].sum(), 0), share_s=pct(small["samples"].sum() / h1["samples"].sum(), 0),
               a=pct(h1.loc["s", "rate"]), b=pct(h1.loc["xl", "rate"], 2), y0=Y[0], y1=Y[1]),
    "h2": dict(rho=dec(rho), top_b=", ".join(names.get(x, x) for x in d["b"].nlargest(3).index),
               top_c=", ".join(names.get(x, x) for x in d["c"].nlargest(3).index)),
    "h3": dict(before=num(nc.loc[2016:2020].mean()), during=num(nc.loc[2021:2024].mean()), y2025=num(nc.loc[2025]),
               w0=num(without.loc[2016]), w1=num(without.loc[last]), a0=num(allx.loc[2016]), a1=num(allx.loc[last])),
    "h4": dict(lo=f"{th.quantile(0.05):.0f}", hi=f"{th.quantile(0.95):.0f}"),
}
PROOF = {"h1": EVIDENCE[3], "h2": EVIDENCE[3], "h3": EVIDENCE[4], "h4": EVIDENCE[4]}   # the page that tests each
for h, kw in blocks.items():
    with st.container(border=True):
        st.subheader(t(f"con.{h}.title"))
        st.markdown(f"**{t('con.lab.hyp')}** {t(f'con.{h}.hyp')}")
        st.markdown(f"**{t('con.lab.data')}** {t(f'con.{h}.data', **kw)}")
        st.markdown(f"**{t('con.lab.verdict')}** {t(f'con.{h}.verdict')}")
        file, key, icon = PROOF[h]
        st.page_link(file, label=t("con.proof", page=t(key)), icon=icon)
st.markdown(t("con.score", k=int((sens["spearman_networks"] >= 0.95).sum()), n=len(sens)))

fig = go.Figure()
fig.add_trace(go.Scatter(x=allx.index, y=allx.values, name=t("con.chart.with"), mode="lines+markers",
                         line=dict(color="#5E5A50", width=2.6), marker=dict(size=8),
                         hovertemplate="%{x}: %{y:,}<extra></extra>"))
fig.add_trace(go.Scatter(x=without.index, y=without.values, name=t("con.chart.without"), mode="lines+markers",
                         line=dict(color=TEAL, width=2.6, dash="dash"), marker=dict(size=8, symbol="square"),
                         hovertemplate="%{x}: %{y:,}<extra></extra>"))
layout(fig, t("common.year"), t("con.chart.y"), height=380)
fig.update_yaxes(rangemode="tozero")
fig.update_xaxes(dtick=1)
chart(fig, t("con.chart.title"), t("con.chart.caption"),
      t("con.chart.take", a0=num(allx.loc[2016]), apeak=num(allx.max()), w0=num(without.loc[2016]),
        w1=num(without.loc[last])))

kicker(t("con.means.kicker"))
st.header(t("con.means.title"))
st.markdown(t("con.resident"))
st.markdown(t("con.authorities"))
kicker(t("con.limits.kicker"))
st.markdown(t("con.limits"))

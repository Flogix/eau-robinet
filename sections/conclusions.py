"""Page 8 — Conclusions: the hypotheses tested, with computed numbers; implications; limits; next steps."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import config
from utils.io import SOURCE_CAPTION, departments, load_table
from utils.viz import PALETTE, headline, layout, pct, show

st.title("✅ Conclusions")
last = config.COMPLETE_YEARS[-1]
Y = (config.YEARS[0], last)

ny = load_table("national_year").set_index("annee")
bact_rate = 1 - ny.loc[last, "n_bact_nc"] / ny.loc[last, "n_bact"]
chem_rate = 1 - ny.loc[last, "n_chem_nc"] / ny.loc[last, "n_chem"]

# H1 — small networks
uy = load_table("udi_year")
u = uy[uy["annee"].between(*Y) & (uy["n_bact"] > 0)].copy()
u["size"] = pd.cut(u["n_bact"], [0, 6, 12, 52, np.inf], right=False,
                   labels=["< 6", "6–11", "12–51", "≥ 52"])
h1 = u.groupby("size", observed=True).agg(samples=("n_bact", "sum"), nc=("n_bact_nc", "sum"))
h1["rate"] = h1["nc"] / h1["samples"]
small = h1.loc[["< 6", "6–11"]]
share_nc_small = small["nc"].sum() / h1["nc"].sum()
share_samples_small = small["samples"].sum() / h1["samples"].sum()

# H2 — geography
dy = load_table("dept_year")
d = dy[dy["annee"].between(*Y)].groupby("dep")[["n_bact", "n_bact_nc", "n_chem", "n_chem_nc"]].sum()
d = d[~d.index.str.startswith("97")]
d["b"], d["c"] = d["n_bact_nc"] / d["n_bact"], d["n_chem_nc"] / d["n_chem"]
rho = d["b"].rank().corr(d["c"].rank())
names = departments().set_index("dep")["dep_nom"]
top_b = ", ".join(names.get(x, x) for x in d["b"].nlargest(3).index)
top_c = ", ".join(names.get(x, x) for x in d["c"].nlargest(3).index)

# H3 — monitoring
nc = ny["n_chem_nc"]
before, during = nc.loc[2016:2020].mean(), nc.loc[2021:2024].mean()

# H4 — hardness
w = load_table("udi_param_window")
th = w.loc[w["code"] == "TH", "mean"]

# score robustness
sens = load_table("score_sensitivity")
sens = sens[sens["variant"] != "default"]
n_robust = int((sens["spearman_networks"] >= 0.95).sum())

headline(f"In {last}, {pct(bact_rate)} of bacteriological samples and {pct(chem_rate)} of chemical samples complied "
         "with the health limits: French tap water is mostly good — the problems are concentrated and explainable.")

st.subheader("What the data says")
st.markdown(f"""
1. **Problems concentrate in small networks (H1, confirmed).** Networks sampled fewer than 12 times a year carry
   **{share_nc_small:.0%} of the bacteriological non-compliances** for **{share_samples_small:.0%} of the samples**
   ({Y[0]}–{Y[1]}). Their non-compliance rate is **{pct(h1.loc['< 6', 'rate'])}** against
   **{pct(h1.loc['≥ 52', 'rate'], 2)}** in the most sampled networks.
2. **Bacteria and chemistry do not share the same map (H2, confirmed).** Across mainland departments, the rank
   correlation between the two non-compliance rates is **ρ = {rho:.2f}**. Bacteria: {top_b}. Chemistry: {top_c}.
3. **Chemical non-compliance follows what we monitor (H3, confirmed — main insight).** From **{before:,.0f}** non-compliant
   samples a year (2016–2020) to **{during:,.0f}** (2021–2024), then **{nc.loc[2025]:,.0f}** in 2025: newly monitored
   pesticide metabolites and their reclassification by Anses explain the rise and the fall (see Deep dives).
4. **Hardness varies a lot, without health stakes (H4, confirmed).** Network hardness ranges from
   **{th.quantile(0.05):.0f} °f** to **{th.quantile(0.95):.0f} °f** (5th–95th percentiles); it never lowers the score.
5. **The score is robust.** Its ranking barely moves when the weights or parameters change (rank correlation ≥ 0.95
   for {n_robust} of {len(sens)} variants), and networks with official non-compliances score clearly lower.
""")

fig = go.Figure(go.Bar(x=h1.index.astype(str), y=100 * h1["rate"], marker_color=PALETTE["vermillion"],
                       text=[f"{100 * v:.2f}%" for v in h1["rate"]], textposition="outside",
                       customdata=h1[["nc", "samples"]].values,
                       hovertemplate="%{x} samples a year: %{y:.2f}% non-compliant<br>%{customdata[0]:,} of "
                                     "%{customdata[1]:,} samples<extra></extra>"))
layout(fig, "Bacteriological samples per network and per year", "Non-compliant samples (%)", height=360, legend=False)
show(fig, f"Bars: share of bacteriological samples officially non-compliant, by size of the network measured by its "
          f"number of samples per year, France {Y[0]}–{Y[1]}. Smaller networks fail far more often.")

st.subheader("What it means")
c1, c2 = st.columns(2)
c1.markdown("""**For a resident**
- Look up your town on *My town*: the score, the grade and, above all, **the report** say what was measured.
- Mind the **confidence**: a small network with few samples can change grade after one incident.
- The **official** opinion is your ARS's (also summarised with your water bill).""")
c2.markdown("""**For a local authority, a journalist, a teacher**
- Small networks are where bacteriological incidents concentrate: they are the priority for monitoring.
- A rise in non-compliance can come from **new molecules searched** or **new thresholds**, not only from pollution:
  read trends together with the monitoring history.
- PFAS are only now measured everywhere (2026): the picture will change.""")

st.subheader("Limits and next steps")
st.markdown("""
- **Limits**: score = educational indicator; recomputed exceedances for some families; population per network
  unknown (upper bounds); 2026 partial; Mediterranean coast approximated; correlations, not causes.
- **Next steps**: yearly scores to follow each town over time; complete 2026 with the PFAS results; population per
  network to weigh KPIs; compare tap water with bottled water (mineral composition only).
""")
st.caption(SOURCE_CAPTION)

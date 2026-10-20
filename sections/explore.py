"""Explore the data: the three files and their keys, real rows, key distributions, rank correlations between
department indicators and a scatter plot of any two of them. Every table is precomputed by
scripts/07_build_explore_tables.py: the page only reads small tables."""
import json
import math

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import config
from utils.i18n import lang, num, pct, t
from utils.io import cached_resource, departments, load_table
from utils.score import label
from utils.texts import TEXTS
from utils.viz import (BLUE, BRICK, FAMILY_COLORS, MONO, OCHRE, TEAL, chart, headline, kicker, layout, lede,
                       partial_year, takeaway)

YEAR = config.COMPLETE_YEARS[-1]
Y0, Y1 = config.COMPLETE_YEARS[0], config.COMPLETE_YEARS[-1]
INDICATORS = ["bact_rate", "chem_rate", "score_median", "small_share", "hardness", "nitrates", "population", "density"]
SHARES = {"bact_rate", "chem_rate", "small_share"}
LOG_AXES = {"population", "density"}
VALUE_CODES = ["NO3", "TH", "PB", "AS", "PESTOT", "SPFAS", "CL", "SO4"]


def dec(v: float, k: int = 2) -> str:
    s = f"{v:.{k}f}".replace("-", "−")
    return s.replace(".", ",") if lang() == "fr" else s


def strength(rho: float) -> str:
    a = abs(rho)
    return ("very_strong" if a >= 0.8 else "strong" if a >= 0.5 else "moderate" if a >= 0.3 else "weak" if a >= 0.15
            else "none")


@cached_resource
def examples() -> dict:
    return json.loads((config.PROCESSED / "explore_examples.json").read_text(encoding="utf-8"))


def param_name(code: str) -> str:
    """English or French name: the app's key labels, then this page's labels, then the catalogue (French)."""
    for key in (f"ex.val.p.{code}", f"ex.p.{code}"):
        if key in TEXTS:
            return t(key)
    return label(code, CATALOG_LABELS)

cat = load_table("params_catalog")
CATALOG_LABELS = dict(zip(cat["code"], cat["label"]))
vol = load_table("explore_volume")
complete = vol[vol["annee"].isin(config.COMPLETE_YEARS)]
last = vol[vol["annee"] == YEAR].iloc[0]
gb = (vol["plv_txt_mb"] + vol["result_txt_mb"] + vol["com_udi_txt_mb"]).sum() / 1000
per = last["result_rows"] / last["samples"]

kicker(t("ex.kicker"))
st.title(t("ex.title"))
lede(t("ex.lede"))
headline(t("ex.headline", y0=int(vol["annee"].min()), y1=int(vol["annee"].max()), samples=num(vol["samples"].sum()),
           results=num(vol["result_rows"].sum()), gb=num(gb), per=num(per)))

# --- 1. The three files and their keys ------------------------------------------------------------------------------
kicker(t("ex.schema.kicker"))
st.header(t("ex.schema.title"))
st.markdown(t("ex.schema.text"))


def _lines(text: str, width: int = 17) -> list[str]:
    out, cur = [], ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > width:
            out.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return out + [cur]


def diagram() -> str:
    """Inline SVG of the three files, their important columns and the two join keys (theme-aware: currentColor)."""
    boxes = [
        ("COM_UDI", t("ex.diag.com_udi"), [("inseecommune", "insee", False), ("quartier", "quartier", False),
                                           ("cdreseau", "cdreseau", True), ("nomreseau", "nomreseau", False)],
         t("ex.diag.rows", n=num(last["com_udi_rows"]))),
        ("PLV", t("ex.diag.plv"), [("referenceprel", "referenceprel", True), ("cdreseau", "cdreseau", True),
                                   ("dateprel", "dateprel", False), ("cdreseauamont", "amont", False),
                                   ("plvconformite…", "conf", False)],
         t("ex.diag.rows_samples", n=num(last["plv_rows"]), s=num(last["samples"]))),
        ("RESULT", t("ex.diag.result"), [("referenceprel", "referenceprel", True),
                                         ("cdparametresiseeaux", "param", False), ("rqana, valtraduite", "value", False),
                                         ("limitequal, refqual", "limits", False)],
         t("ex.diag.rows", n=num(last["result_rows"]))),
    ]
    W, gap, x0, top, head, row = 250, 105, 10, 16, 46, 36
    h = head + 5 * row + 30
    parts = [f'<svg viewBox="0 0 {3 * W + 2 * gap + 2 * x0} {h + top + 8}" role="img" '
             f'aria-label="{t("ex.diag.caption", year=YEAR)}" style="width:100%;min-width:640px;height:auto;'
             f'font-family:IBM Plex Sans, sans-serif">']
    rows_y = {}
    for i, (name, title, fields, foot) in enumerate(boxes):
        x = x0 + i * (W + gap)
        parts.append(f'<rect x="{x}" y="{top}" width="{W}" height="{h}" rx="6" fill="rgba(127,127,127,0.06)" '
                     f'stroke="rgba(127,127,127,0.55)"/>')
        parts.append(f'<rect x="{x}" y="{top}" width="{W}" height="{head}" rx="6" fill="rgba(0,149,163,0.14)"/>')
        parts.append(f'<text x="{x + 12}" y="{top + 20}" font-family="{MONO}" font-size="14" font-weight="600" '
                     f'fill="currentColor">{name}</text>')
        parts.append(f'<text x="{x + 12}" y="{top + 38}" font-size="12.5" fill="currentColor" opacity="0.85">'
                     f'{title}</text>')
        for j, (field, gloss, key) in enumerate(fields):
            y = top + head + 22 + j * row
            rows_y[(name, field)] = y - 4
            color = TEAL if key else "currentColor"
            weight = "600" if key else "400"
            parts.append(f'<text x="{x + 12}" y="{y}" font-family="{MONO}" font-size="12.5" font-weight="{weight}" '
                         f'fill="{color}">{field}{" ●" if key else ""}</text>')
            parts.append(f'<text x="{x + 12}" y="{y + 14}" font-size="11.5" fill="currentColor" opacity="0.72">'
                         f'{t("ex.diag.c." + gloss)}</text>')
        parts.append(f'<text x="{x + 12}" y="{top + h - 12}" font-family="{MONO}" font-size="11.5" '
                     f'fill="currentColor" opacity="0.85">{foot}</text>')
    links = [(("COM_UDI", "cdreseau"), ("PLV", "cdreseau"), "cdreseau", t("ex.diag.nn"), 0),
             (("PLV", "referenceprel"), ("RESULT", "referenceprel"), "referenceprel", t("ex.diag.1n", per=num(per)), 1)]
    for a, b, key, rel, gi in links:
        xa, xb = x0 + gi * (W + gap) + W, x0 + (gi + 1) * (W + gap)
        ya, yb = rows_y[a], rows_y[b]
        xm = (xa + xb) / 2
        parts.append(f'<path d="M{xa} {ya} C{xm} {ya}, {xm} {yb}, {xb} {yb}" fill="none" stroke="{TEAL}" '
                     f'stroke-width="2"/>')
        parts.append(f'<circle cx="{xa}" cy="{ya}" r="3.5" fill="{TEAL}"/><circle cx="{xb}" cy="{yb}" r="3.5" '
                     f'fill="{TEAL}"/>')
        ly = max(ya, yb) + 26
        parts.append(f'<text x="{xm}" y="{ly}" text-anchor="middle" font-family="{MONO}" font-size="11.5" '
                     f'font-weight="600" fill="{TEAL}">{key}</text>')
        for k, line in enumerate(_lines(rel)):
            parts.append(f'<text x="{xm}" y="{ly + 16 + 14 * k}" text-anchor="middle" font-size="11" '
                         f'fill="currentColor" opacity="0.8">{line}</text>')
    parts.append("</svg>")
    return "".join(parts)


st.markdown(f'<div class="ar-chart-title">{t("ex.diag.title", year=YEAR)}</div>', unsafe_allow_html=True)
st.markdown(f'<div style="overflow-x:auto">{diagram()}</div>', unsafe_allow_html=True)
st.caption(f"{t('ex.diag.caption', year=YEAR)} {t('common.source_short')}")
takeaway(t("ex.diag.take"))

# volume per year
fig = go.Figure(go.Bar(
    x=vol["annee"], y=vol["result_rows"] / 1e6, marker_color=BLUE, hoverinfo="text",
    hovertext=[t("ex.vol.hover", year=int(r.annee), res=num(r.result_rows / 1e6, 1), smp=num(r.samples),
                 plv=num(r.plv_rows), mb=num(r.plv_txt_mb + r.result_txt_mb + r.com_udi_txt_mb))
               for r in vol.itertuples()]))
layout(fig, t("ex.vol.x"), t("ex.vol.y"), height=340, legend=False)
fig.update_xaxes(dtick=1)
partial_year(fig, config.PARTIAL_YEAR, t("ex.vol.partial"))
pq_mb = sum(f.stat().st_size for f in (config.INTERIM / "raw_parquet").rglob("*.parquet")) / 1e6 \
    if (config.INTERIM / "raw_parquet").exists() else 428   # measured size of the raw Parquet copy (phase 0)
chart(fig, t("ex.vol.title", lo=num(complete["result_rows"].min() / 1e6, 1), hi=num(complete["result_rows"].max() / 1e6, 1)),
      t("ex.vol.caption"),
      t("ex.vol.take", share=pct(vol["result_txt_mb"].sum() / (gb * 1000), 0), gb=num(gb), pq=num(vol["raw_parquet_mb"].sum())))
with st.expander(t("ex.vol.table")):
    cols = ["annee", "zip_mb", "result_txt_mb", "plv_rows", "samples", "result_rows", "com_udi_rows", "communes",
            "networks_linked"]
    tb = vol[cols].copy()
    for c in ("zip_mb", "result_txt_mb"):
        tb[c] = tb[c].round(0).astype(int)
    st.dataframe(tb.rename(columns={c: t("ex.vol.col." + c) for c in cols}), hide_index=True, width="stretch")

# why the network
kicker(t("ex.net.kicker"))
st.header(t("ex.net.title"))
lk = load_table("explore_links")
town, net = lk[lk["side"] == "town"].set_index("k")["n"], lk[lk["side"] == "network"].set_index("k")["n"]
st.markdown(t("ex.net.text", year=int(lk["annee"].iloc[0]), t1=num(town.get(1, 0)), tn=num(town.sum()),
              t2=num(town.get(2, 0)), t10=num(town[town.index >= 10].sum()), n1=num(net.get(1, 0)),
              nn=num(net.sum()), n20=num(net[net.index >= 20].sum())))
fan = load_table("explore_fanout")
st.markdown(t("ex.net.upstream", year=YEAR, share=pct(fan.loc[fan["n_networks"] > 1, "n_samples"].sum() / fan["n_samples"].sum()),
              n=num(fan["n_samples"].sum()), max=num(fan["n_networks"].max())))

# --- 2. Real rows ------------------------------------------------------------------------------------------------
kicker(t("ex.rows.kicker"))
st.header(t("ex.rows.title"))
ex = examples()
st.markdown(t("ex.rows.text", year=ex["PLV"]["year"]))
tables = ["PLV", "RESULT", "COM_UDI", "udi_year"]
table_labels = {k: t(f"ex.rows.opt.{k}") for k in tables}   # labels computed once per run, as in the sidebar
which = st.segmented_control(t("ex.rows.pick"), tables, default="PLV", key="ex_rows", format_func=table_labels.get,
                             help=t("ex.rows.help")) or "PLV"
e = ex[which]
st.dataframe(pd.DataFrame(e["rows"], columns=e["columns"]), hide_index=True, width="stretch")
st.caption(t("ex.rows.caption", n=len(e["rows"]), table=which, year=e["year"]) + " " + t("common.source_short"))
st.markdown(t(f"ex.rows.{which}"))

# --- 3. Distributions -----------------------------------------------------------------------------------------------
kicker(t("ex.dist.kicker"))
st.header(t("ex.dist.title"))
st.markdown(t("ex.dist.text"))

# samples per network
sh = load_table("explore_samples_hist")
lab = [str(lo) if hi == lo else (t("ex.smp.more", lo=lo) if pd.isna(hi) else f"{lo}–{int(hi)}")
       for lo, hi in zip(sh["lo"], sh["hi"])]
fig = go.Figure(go.Bar(x=lab, y=sh["n_networks"], marker_color=TEAL, text=[num(v) for v in sh["n_networks"]],
                       textposition="outside", hovertemplate=t("ex.smp.hover") + "<extra></extra>"))
layout(fig, t("ex.smp.x"), t("ex.smp.y"), height=360, legend=False)
fig.update_yaxes(range=[0, sh["n_networks"].max() * 1.15])
big = sh.iloc[-2:]
chart(fig, t("ex.smp.title", median=num(sh["median"].iloc[0]), year=YEAR), t("ex.smp.caption", year=YEAR),
      t("ex.smp.take", share=pct(sh["share_below_12"].iloc[0], 0), year=YEAR, big=num(big["n_networks"].sum()),
        lo=int(big["lo"].iloc[0])))

# below the quantification limit
st.markdown(t("ex.lq.text"))
lq = load_table("explore_lq").sort_values("share_not_detected")
names = [t(f"ex.sub.{s}") if f"ex.sub.{s}" in TEXTS else s for s in lq["subfamily"]]
fig = go.Figure(go.Bar(
    x=100 * lq["share_not_detected"], y=names, orientation="h", marker_color=[FAMILY_COLORS[f] for f in lq["family"]],
    text=[f"{pct(v, 1)}  {t('fam.' + f)}" for v, f in zip(lq["share_not_detected"], lq["family"])],
    textposition="outside", hoverinfo="text",
    hovertext=[t("ex.lq.hover", group=g, share=pct(v), n=num(n), k=num(k))
               for g, v, n, k in zip(names, lq["share_not_detected"], lq["n_samples"], lq["n_params"])]))
layout(fig, t("ex.lq.x", year=YEAR), None, height=max(360, 30 * len(lq)), legend=False)
fig.update_xaxes(range=[0, 140], tickvals=[0, 25, 50, 75, 100])
g = lq.set_index("subfamily")["share_not_detected"]
chart(fig, t("ex.lq.title"), t("ex.lq.caption", year=YEAR),
      t("ex.lq.take", pest=pct(g["pesticides"], 0), bact=pct(g["bacteria"], 0), no3=pct(g["nitrates"], 0)))

# most measured parameters
top = load_table("explore_top_params").sort_values("n_results")
pnames = [param_name(c) for c in top["code"]]
fig = go.Figure(go.Bar(
    x=top["n_results"] / 1e6, y=pnames, orientation="h", marker_color=[FAMILY_COLORS[f] for f in top["family"]],
    text=[t("fam." + f) for f in top["family"]], textposition="outside", hoverinfo="text",
    hovertext=[t("ex.top.hover", name=nm, code=c, n=num(n / 1e6, 2), fam=t("fam." + f))
               for nm, c, n, f in zip(pnames, top["code"], top["n_results"], top["family"])]))
layout(fig, t("ex.top.x", y0=int(vol["annee"].min()), y1=int(vol["annee"].max())), None, height=480, legend=False)
fig.update_xaxes(range=[0, top["n_results"].max() / 1e6 * 1.3])
pest = cat[cat["subfamily"] == "pesticides"]
chart(fig, t("ex.top.title", n=len(top)), t("ex.top.caption"),
      t("ex.top.take", no3=num(cat.set_index("code").loc["NO3", "n_results"] / 1e6, 1), pest=num(len(pest)),
        pshare=pct(pest["n_results"].sum() / cat["n_results"].sum(), 0)))

# typical values of key parameters
vals = load_table("explore_values")
value_labels = {c: param_name(c) for c in VALUE_CODES}
code = st.segmented_control(t("ex.val.pick"), VALUE_CODES, default="NO3", key="ex_val", format_func=value_labels.get,
                            help=t("ex.val.help")) or "NO3"
v = vals[vals["code"] == code]
unit = cat.set_index("code").loc[code, "unit"]
first = v.iloc[0]
k = 2 if first["p95"] < 1 else 1 if first["p95"] < 100 else 0
fig = go.Figure(go.Bar(
    x=(v["lo"] + v["hi"]) / 2, y=v["n_networks"], width=(v["hi"] - v["lo"]) * 0.92, marker_color=BLUE,
    hoverinfo="text", hovertext=[t("ex.val.hover", lo=dec(a, k + 1), hi=dec(b, k + 1), unit=unit, n=num(n))
                                 for a, b, n in zip(v["lo"], v["hi"], v["n_networks"])]))
layout(fig, t("ex.val.x", year=YEAR, unit=unit), t("ex.smp.y"), height=360, legend=False)
thr_txt = t("ex.val.nothr")
if not pd.isna(first["threshold"]):
    kind = "reference" if code in ("CL", "SO4") else "limit"
    fig.add_vline(x=first["threshold"], line_dash="dash", line_color=BRICK, line_width=1.5,
                  annotation_text=t(f"ex.val.{kind}", v=dec(first["threshold"], 1).rstrip("0").rstrip(",.") or "0",
                                    unit=unit),
                  annotation_position="top", annotation_font=dict(color=BRICK, size=12))
    thr_txt = t("ex.val.thr", share=pct(first["share_above"]), kind=t(f"ex.val.kind.{kind}"),
                v=dec(first["threshold"], 1).rstrip("0").rstrip(",."), unit=unit)
chart(fig, t("ex.val.title", name=param_name(code), year=YEAR),
      t("ex.val.caption", year=YEAR, top=dec(v["lo"].iloc[-1], k), unit=unit),
      t("ex.val.take", n=num(first["n_total"]), p50=dec(first["p50"], k), p05=dec(first["p05"], k),
        p95=dec(first["p95"], k), unit=unit, zero=pct(first["share_zero"], 0), thr=thr_txt))

# --- 4. Correlations -------------------------------------------------------------------------------------------------
kicker(t("ex.cor.kicker"))
st.header(t("ex.cor.title"))
dept = load_table("explore_dept")
sp = load_table("explore_spearman")
n_dep = len(dept)
st.markdown(t("ex.cor.text", n=n_dep, y0=Y0, y1=Y1, year=YEAR))
m = sp.pivot(index="x", columns="y", values="rho").loc[INDICATORS, INDICATORS]
short = [t(f"ex.ind.{c}") for c in INDICATORS]
fig = go.Figure(go.Heatmap(
    z=m.values, x=short, y=short, zmin=-1, zmax=1, text=[[dec(x) for x in row] for row in m.values],
    colorscale=[[0, BLUE], [0.5, "rgba(127,127,127,0.06)"], [1, OCHRE]],
    colorbar=dict(title=t("ex.cor.cb"), thickness=12, tickvals=[-1, -0.5, 0, 0.5, 1]),
    hovertemplate=t("ex.cor.hover") + "<extra></extra>"))
layout(fig, None, None, height=520, legend=False)
fig.update_yaxes(autorange="reversed", gridcolor="rgba(0,0,0,0)")
for i, a in enumerate(short):          # values written in the cells: theme colour on pale cells, white on strong ones
    for j, b in enumerate(short):
        rho_ij = m.values[i, j]
        fig.add_annotation(x=b, y=a, text=dec(rho_ij), showarrow=False, font=dict(size=12, **(
            {"color": "white"} if abs(rho_ij) >= 0.5 else {})))
fig.update_xaxes(tickangle=-30)
r = lambda a, b: dec(m.loc[a, b])  # noqa: E731
crit = 1.96 / math.sqrt(n_dep - 1)
chart(fig, t("ex.cor.chart"), t("ex.cor.caption"),
      t("ex.cor.take1", h2=r("bact_rate", "chem_rate"), sb=r("small_share", "bact_rate"),
        sp=r("small_share", "population"), bp=r("bact_rate", "population"), ss=r("small_share", "score_median"),
        sn=r("score_median", "nitrates"), hn=r("hardness", "nitrates")))
takeaway(t("ex.cor.take2", n=n_dep, crit=dec(crit)))

# --- 5. Scatter plot of any two indicators ---------------------------------------------------------------------------
kicker(t("ex.sc.kicker"))
st.header(t("ex.sc.title"))
c1, c2 = st.columns(2)
ind_labels = {c: t(f"ex.ind.{c}") for c in INDICATORS}
xv = c1.selectbox(t("ex.sc.x"), INDICATORS, index=INDICATORS.index("small_share"), key="ex_x",
                  format_func=ind_labels.get, help=t("ex.sc.help"))
yv = c2.selectbox(t("ex.sc.y"), INDICATORS, index=INDICATORS.index("bact_rate"), key="ex_y",
                  format_func=ind_labels.get, help=t("ex.sc.help"))


def fmt(c: str, x: float) -> str:
    return pct(x) if c in SHARES else num(x) if c in LOG_AXES else dec(x, 1)


if xv == yv:
    st.info(t("ex.sc.same"))
else:
    d = dept.dropna(subset=[xv, yv]).merge(departments(), on="dep", how="left")
    scale = {c: (100 if c in SHARES else 1) for c in (xv, yv)}
    ext = set(d.nlargest(5, yv)["dep"])
    fig = go.Figure(go.Scatter(
        x=d[xv] * scale[xv], y=d[yv] * scale[yv], mode="markers+text",
        text=[nm if c in ext else "" for nm, c in zip(d["dep_nom"], d["dep"])], textposition="top center",
        textfont=dict(size=10), marker=dict(size=9, color=TEAL, line=dict(color="rgba(127,127,127,0.8)", width=0.6),
                                            opacity=0.85),
        hoverinfo="text", hovertext=[f"{nm} ({c})<br>{t('ex.ind.' + xv)}: {fmt(xv, a)}<br>{t('ex.ind.' + yv)}: "
                                     f"{fmt(yv, b)}" for nm, c, a, b in zip(d["dep_nom"], d["dep"], d[xv], d[yv])]))
    layout(fig, t(f"ex.ax.{xv}", y0=Y0, y1=Y1, year=YEAR), t(f"ex.ax.{yv}", y0=Y0, y1=Y1, year=YEAR), height=540,
           legend=False)
    logs = [c for c in (xv, yv) if c in LOG_AXES]
    if xv in LOG_AXES:
        fig.update_xaxes(type="log")
    if yv in LOG_AXES:
        fig.update_yaxes(type="log")
    rho = float(sp[(sp["x"] == xv) & (sp["y"] == yv)]["rho"].iloc[0])
    n_pair = int(sp[(sp["x"] == xv) & (sp["y"] == yv)]["n"].iloc[0])
    direction = t("ex.sc.up") if rho >= 0.15 else t("ex.sc.down") if rho <= -0.15 else t("ex.sc.flat")
    log_txt = "".join(t("ex.sc.log", var=t(f"ex.ind.{c}").lower()) for c in logs)
    chart(fig, t("ex.sc.chart", x=t(f"ex.ind.{xv}").lower(), y=t(f"ex.ind.{yv}")), t("ex.sc.caption", log=log_txt),
          t("ex.sc.take", rho=dec(rho), n=n_pair, strength=t(f"ex.strength.{strength(rho)}"), direction=direction,
            chance=t("ex.sc.chance") if abs(rho) < 1.96 / math.sqrt(n_pair - 1) else ""))

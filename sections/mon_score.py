"""Build your own score: weights, severities and key thresholds chosen by the reader, against the official settings."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import config
from utils import custom_score as C
from utils import score as S
from utils.i18n import lang, num, pct, t
from utils.io import cached, cached_resource, commune_network_links, communes, load_table, town_options
from utils.town_search import town_search
from utils.viz import BLUE, NEUTRAL, analysis, chart, headline, kicker, layout, lede

kicker(t("my.kicker"))
st.title(t("my.title"))
lede(t("my.lede"))
st.warning(t("my.warning"), icon=":material/info:")

FAMS = list(S.FAMILIES)
W_KEYS = {"micro": "my_w_micro", "chem": "my_w_chem", "comfort": "my_w_comfort"}
DEFAULTS = {**{W_KEYS[k]: config.WEIGHTS[k] for k in FAMS}, "my_k": float(config.MICRO_K),
            **{f"my_sev_{g}": 1.0 for g in C.SEVERITY_GROUPS},
            **{f"my_thr_{k}": v["official"] for k, v in C.THRESHOLDS.items()}}
for key, value in DEFAULTS.items():
    st.session_state.setdefault(key, value)


def _reset():
    for key, value in DEFAULTS.items():
        st.session_state[key] = value


@cached_resource
def _prepared() -> C.Prepared:
    return C.prepare(load_table("udi_micro_window"), load_table("udi_family_window"), load_table("udi_param_window"),
                     load_table("udi_param_p95"), commune_network_links(), S.reference_ranges(load_table("params_catalog")))


@cached
def _personal(weights: tuple, k: float, severity: tuple, thresholds: tuple) -> pd.DataFrame:
    p = _prepared()
    udi = C.recompute(p, C.Personal(weights=weights, micro_k=k, severity=dict(severity), thresholds=dict(thresholds)))
    return C.commune_recompute(p, udi)


def fmt1(v) -> str:
    return num(v, 1)


def rank_txt(r) -> str:
    if pd.isna(r):
        return "?"
    r = int(r)
    return t("my.rank.fmt.one") if r == 1 else (num(r) + ("e" if lang() == "fr" else ""))


# --- Town -----------------------------------------------------------------------------------------------------------
_, labels = town_options()
current = st.session_state.get("insee") or st.query_params.get("insee") or "75056"
if current not in labels:
    current = "75056"
town_search(t("my.pick"), "my_town_search", lambda i: st.session_state.update(insee=i), current=current,
            help=t("my.pick.help"))
insee = current

# --- Settings -------------------------------------------------------------------------------------------------------
st.button(t("my.reset"), on_click=_reset, help=t("my.reset.help"), icon=":material/restart_alt:")
c1, c2, c3 = st.columns(3, gap="large")
with c1:
    st.markdown(f'<div class="ar-chart-title">{t("my.set.weights")}</div>', unsafe_allow_html=True)
    st.caption(t("my.set.weights.text"))
    for k in FAMS:
        st.slider(t(f"mon.w.{k}"), 0.0, 1.0, step=0.05, key=W_KEYS[k], help=t(f"my.w.{k}.help"))
with c2:
    st.markdown(f'<div class="ar-chart-title">{t("my.set.severity")}</div>', unsafe_allow_html=True)
    st.caption(t("my.set.severity.text"))
    for g in C.SEVERITY_GROUPS:
        st.select_slider(t(f"my.sev.{g}"), C.SEVERITY_CHOICES, key=f"my_sev_{g}", help=t("my.sev.help"),
                         format_func=lambda v: f"×{num(v, 1 if v % 1 else 0)}")
    st.select_slider(t("my.k"), C.MICRO_K_CHOICES, key="my_k", help=t("my.k.help"),
                     format_func=lambda v: t(f"my.k.{v:.1f}"))
with c3:
    st.markdown(f'<div class="ar-chart-title">{t("my.set.thr")}</div>', unsafe_allow_html=True)
    st.caption(t("my.set.thr.text"))
    for k, v in C.THRESHOLDS.items():
        digits = 2 if v["step"] < 1 else 0
        hlp = t("my.thr.PEST.help") if k == "PEST" else t("my.thr.help", v=num(v["official"], digits), unit=v["unit"])
        st.slider(t(f"my.thr.{k}"), v["min"], v["max"], step=v["step"], key=f"my_thr_{k}", help=hlp,
                  format=f"%.{digits}f")

weights = tuple(float(st.session_state[W_KEYS[k]]) for k in FAMS)
severity = tuple((g, float(st.session_state[f"my_sev_{g}"])) for g in C.SEVERITY_GROUPS)
thresholds = tuple((k, round(float(st.session_state[f"my_thr_{k}"]), 4)) for k in C.THRESHOLDS)
mine = C.Personal(weights=weights, micro_k=float(st.session_state["my_k"]), severity=dict(severity),
                  thresholds=dict(thresholds))
if sum(weights) == 0:
    st.warning(t("my.w.zero"))
    st.stop()
if mine.is_official:
    st.info(t("my.official_now"))

# --- Results --------------------------------------------------------------------------------------------------------
com = communes().set_index("insee")
off = com.loc[com["score"].notna() & com["is_current"], ["nom", "dep", "population", "score", *FAMS, "grade"]]   # as on the map
per = _personal(weights, mine.micro_k, severity, thresholds)
both = off.join(per, rsuffix="_mine", how="inner")
n_towns = len(both)
both["rank_off"] = both["score"].rank(ascending=False, method="min")
both["rank_mine"] = both["score_mine"].rank(ascending=False, method="min")

kicker(t("my.res.kicker"))
st.header(t("my.res.title"))
town = com.loc[insee, "nom"]
if insee not in both.index:
    st.info(t("my.res.noscore", town=town))
else:
    r = both.loc[insee]
    same_rank = r["rank_mine"] == r["rank_off"]
    headline(t("my.res.headline.same" if same_rank else "my.res.headline", town=town, mine=fmt1(r["score_mine"]), g_mine=r["grade_mine"], off=fmt1(r["score"]),
               g_off=r["grade"], r_mine=rank_txt(r["rank_mine"]), n=num(n_towns), r_off=rank_txt(r["rank_off"])))
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(t("my.m.official"), f"{fmt1(r['score'])} · {r['grade']}")
    m2.metric(t("my.m.mine"), f"{fmt1(r['score_mine'])} · {r['grade_mine']}",
              delta=fmt1(r["score_mine"] - r["score"]) if abs(r["score_mine"] - r["score"]) >= 0.05 else None)
    m3.metric(t("my.m.rank"), rank_txt(r["rank_mine"]), help=t("my.m.rank.help", n=num(n_towns)),
              delta=num(r["rank_off"] - r["rank_mine"]) if r["rank_off"] != r["rank_mine"] else None)
    changed = (both["grade"] != both["grade_mine"]).mean()
    m4.metric(t("my.m.changed"), pct(changed, 0))

    fig = go.Figure()
    labs = [t(f"fam.{k}") for k in FAMS]
    for suffix, name, color, pat in (("", t("my.official"), NEUTRAL, "/"), ("_mine", t("my.yours"), BLUE, "")):
        vals = [r[f"{k}{suffix}"] for k in FAMS]
        fig.add_trace(go.Bar(y=labs, x=[0 if pd.isna(v) else v for v in vals], name=name, orientation="h",
                             marker_color=color, marker_pattern_shape=pat,
                             text=[fmt1(v) if pd.notna(v) else t("town.notmeasured") for v in vals],
                             textposition="outside", hovertemplate="%{y}: %{x:.1f}<extra>" + name + "</extra>"))
    layout(fig, t("town.subs.x"), None, height=300)
    fig.update_xaxes(range=[0, 118])
    fig.update_yaxes(autorange="reversed")
    moves = {k: abs(r[f"{k}_mine"] - r[k]) for k in FAMS if pd.notna(r[k])}
    big = max(moves, key=moves.get) if moves else None
    take = (t("my.subs.take.same", town=town) if not big or moves[big] < 0.05 else
            t("my.subs.take", fam=t(f"fam.{big}").lower(), off=fmt1(r[big]), mine=fmt1(r[f"{big}_mine"]), town=town))
    chart(fig, t("my.subs.title", town=town), t("my.subs.caption"), take)

# grades of all towns
dist = pd.DataFrame({"off": both["grade"].value_counts(normalize=True),
                     "mine": both["grade_mine"].value_counts(normalize=True)}).reindex(list("ABCDE")).fillna(0)
fig = go.Figure()
for col, name, color, pat in (("off", t("my.official"), NEUTRAL, "/"), ("mine", t("my.yours"), BLUE, "")):
    fig.add_trace(go.Bar(x=dist.index, y=100 * dist[col], name=name, marker_color=color, marker_pattern_shape=pat,
                         text=[pct(v, 0) for v in dist[col]], textposition="outside",
                         hovertemplate="%{x}: %{y:.1f}%<extra>" + name + "</extra>"))
layout(fig, t("mon.whatif.x"), t("my.dist.y"), height=340)
rho = both["rank_off"].corr(both["rank_mine"])
rho_txt = num(rho, 3)
take = (t("my.dist.take.same") if mine.is_official else
        t("my.dist.take", changed=pct((both["grade"] != both["grade_mine"]).mean(), 0), rho=rho_txt))
chart(fig, t("my.dist.title"), t("my.dist.caption"), take)

# lowest large towns
big = both[both["population"] > 10_000].copy()
big["rank_off_big"] = big["score"].rank(method="min")
low = big.sort_values("score_mine").head(10)
tbl = pd.DataFrame({t("my.col.town"): low["nom"] + " (" + low["dep"] + ")", t("my.col.mine"): low["score_mine"],
                    t("my.col.g_mine"): low["grade_mine"], t("my.col.off"): low["score"],
                    t("my.col.g_off"): low["grade"], t("my.col.r_off"): low["rank_off_big"].astype(int)})
st.markdown(f'<div class="ar-chart-title">{t("my.low.title")}</div>', unsafe_allow_html=True)
st.dataframe(tbl, hide_index=True, column_config={
    t("my.col.mine"): st.column_config.NumberColumn(format="%.1f"),
    t("my.col.off"): st.column_config.NumberColumn(format="%.1f")})
st.caption(t("my.low.caption") + " " + t("common.source_short"))

# PFAS measured (any result) and found (above the quantification limit) in the scored networks, three-year window
pf = load_table("udi_family_window")
pf = pf[pf["subfamily"] == "pfas"]
scored = load_table("udi_scores")
scored = scored[scored["score"].notna()]
analysis(t("my.analysis.seen"), t("my.analysis.why", pfas=num(pf["cdreseau"].nunique()),
                                  found=num((pf["n_detected"] > 0).sum()), nets=num(len(scored))),
         t("my.analysis.lim"))

# --- Sensitivity (fourteen fixed variants computed by scripts/05_build_scores.py) ------------------------------------
with st.expander(t("mon.sens.title")):
    sens = load_table("score_sensitivity")
    tb = sens[["variant", "spearman_networks", "spearman_communes", "share_grade_changed", "bottom10_overlap",
               "median_score"]].copy()
    tb["variant"] = tb["variant"].map(lambda v: t(f"variant.{v}"))
    tb.columns = [t("mon.sens.variant"), t("mon.sens.rho_n"), t("mon.sens.rho_c"), t("mon.sens.changed"),
                  t("mon.sens.bottom"), t("mon.sens.median")]
    st.dataframe(tb, hide_index=True,
                 column_config={t("mon.sens.changed"): st.column_config.NumberColumn(format="percent"),
                                t("mon.sens.bottom"): st.column_config.NumberColumn(format="percent")})
    st.caption(t("mon.sens.caption"))

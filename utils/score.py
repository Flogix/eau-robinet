"""Score /100 per distribution network (UDI) and per commune, and the rule-based "why" report.

Method (decisions in docs/AVANCEMENT.md, phase 3)
  Unit: network (UDI) over the "current situation" windows ending on config.DATA_END_DATE:
  12 months for microbiology and comfort, 36 months for health-related chemistry.

  micro    S = 100 × (1 − t)^k, t = share of samples officially non-compliant with the bacteriological limits.
  chem     for each parameter with a quality limit, r = value / limit, taken at the maximum, or at the 95th
           percentile when there are >= 10 measurements; any measured exceedance counts at least as r = 1.
           penalty g(r): 0 up to r = 0.5, 0→20 between 0.5 and 1, 20→80 between 1 and 2, 80 beyond.
           S = 100 − worst penalty − 0.25 × sum of the other penalties, bounded to [0, 100].
  comfort  same as chem with references (and the 0.9 µg/L indicative value of non-relevant metabolites),
           penalty capped at 50. For references at 0/100 mL (coliform bacteria, spores) and references that are
           a range (pH 6.5–9, conductivity 200–1100 µS/cm), being close to the bound means nothing: the penalty
           comes from the share t of samples outside the reference: 50 × (1 − (1 − t)^k).
  Nitrates and the "nitrates/50 + nitrites/3" sum describe the same pollution: only the worse one counts.
  global   weighted mean of the MEASURED families only (default 0.4 / 0.4 / 0.2): a family without data is
           never counted as perfect, it is left out and lowers the confidence.
  commune  mean of the networks that serve it (latest year of the commune–network link); worst network kept.

All functions are plain pandas on the small tables of data/processed/, so the app can recompute the
global score with other weights (what-if sliders) without touching the raw data.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace

import numpy as np
import pandas as pd

import config

FAMILIES = ("micro", "chem", "comfort")
# Same pollution published under two codes: one penalty only (the worse). Twin metabolite codes come from config.
SAME_ITEM = {**config.TWIN_CODES, "NO3_NO2": "NO3"}


def reference_ranges(catalog: pd.DataFrame) -> dict:
    """{code: (min, max)} for parameters whose quality reference is a range (pH, conductivity)."""
    r = catalog[catalog["ref_min"].notna() & catalog["family"].isin(["chem", "comfort"])]
    return {c: (lo, hi) for c, lo, hi in zip(r["code"], r["ref_min"], r["ref_max"])}


@dataclass(frozen=True)
class ScoreSettings:
    """Every tunable choice of the score (defaults in config.py); variants feed the sensitivity analysis."""
    weights: dict = field(default_factory=lambda: dict(config.WEIGHTS))
    micro_k: float = config.MICRO_K
    penalty_points: tuple = tuple(config.CHEM_PENALTY_POINTS)
    other_factor: float = config.CHEM_OTHER_PENALTY_FACTOR
    comfort_cap: float = config.COMFORT_PENALTY_CAP
    use_p95: bool = True
    p95_min_n: int = config.P95_MIN_N
    exceedance_floor: float | None = config.EXCEEDANCE_FLOOR_RATIO
    micro_prior_n: float = 0.0   # > 0: t smoothed towards the national rate with this many pseudo-samples

    def with_(self, **kw) -> "ScoreSettings":
        return replace(self, **kw)


DEFAULT = ScoreSettings()


# --- Elementary formulas ---------------------------------------------------------------------------
def micro_subscore(n_samples, n_nonconform, k: float = config.MICRO_K, prior_n: float = 0.0, prior_t: float = 0.0):
    """100 × (1 − t)^k; NaN when there is no sample (not measured ≠ perfect).

    With prior_n > 0, t = (nc + prior_n × prior_t) / (n + prior_n): the observed rate is pulled towards the
    national rate, strongly for a network with 5 samples, hardly for one with 300 (empirical Bayes smoothing)."""
    n = np.asarray(n_samples, dtype=float)
    nc = np.asarray(n_nonconform, dtype=float)
    with np.errstate(invalid="ignore", divide="ignore"):
        t = np.where(n > 0, (nc + prior_n * prior_t) / (n + prior_n), np.nan)
    return 100.0 * (1.0 - t) ** k


def ratio_penalty(r, points=tuple(config.CHEM_PENALTY_POINTS)):
    """Piecewise-linear penalty of a ratio value/threshold: 0 below the first point, flat after the last."""
    xs = np.array([p[0] for p in points], dtype=float)
    ys = np.array([p[1] for p in points], dtype=float)
    r = np.asarray(r, dtype=float)
    out = np.interp(np.nan_to_num(r, nan=0.0), xs, ys, left=0.0, right=ys[-1])
    return np.where(np.isnan(r), np.nan, out)


def frequency_penalty(n, n_exceed, cap: float, k: float = config.MICRO_K):
    """For references at zero (coliforms, spores): cap × (1 − (1 − t)^k), t = share of samples above."""
    n = np.asarray(n, dtype=float)
    t = np.where(n > 0, np.asarray(n_exceed, dtype=float) / np.where(n > 0, n, 1), 0.0)
    return cap * (1.0 - (1.0 - t) ** k)


def combine_penalties(pen: pd.Series, other_factor: float) -> float:
    """100 − worst − other_factor × (sum of the others), bounded to [0, 100]."""
    pen = pen.fillna(0.0)
    if pen.empty:
        return 100.0
    worst = pen.max()
    return float(np.clip(100.0 - worst - other_factor * (pen.sum() - worst), 0.0, 100.0))


def grade(score: float | None) -> str | None:
    """Letter grade A–E from a score /100 (thresholds in config.GRADES), taken on the score rounded to one
    decimal, the value displayed, so that a score shown as 60.0 is never graded D."""
    if score is None or (isinstance(score, float) and np.isnan(score)):
        return None
    score = round(float(score), 1)
    for threshold, letter in config.GRADES:
        if score >= threshold:
            return letter
    return config.GRADES[-1][1]


# --- Parameter penalties ---------------------------------------------------------------------------
def parameter_penalties(params: pd.DataFrame, p95: pd.DataFrame | None, s: ScoreSettings = DEFAULT,
                        ranges: dict | None = None) -> pd.DataFrame:
    """One row per network × parameter (twin codes merged, worst kept) with the effective ratio and penalty.

    params: udi_param_window rows (cdreseau, code, family, n, n_exceed, max_ratio, threshold, ...)
    p95:    udi_param_p95 rows (cdreseau, code, n_ratio, p95_ratio) or None
    ranges: reference_ranges(params_catalog), scored on the share of samples outside the range
    """
    d = params[params["family"].isin(["chem", "comfort"])].copy()
    if p95 is not None and len(p95):
        d = d.merge(p95[["cdreseau", "code", "n_ratio", "p95_ratio"]], on=["cdreseau", "code"], how="left")
    else:
        d["n_ratio"], d["p95_ratio"] = np.nan, np.nan
    use_p95 = s.use_p95 & (d["n_ratio"] >= s.p95_min_n) & d["p95_ratio"].notna()
    d["ratio_basis"] = np.where(use_p95, "p95", "max")
    r = np.where(use_p95, d["p95_ratio"], d["max_ratio"]).astype(float)
    if s.exceedance_floor is not None:
        r = np.where((d["n_exceed"] > 0) & ~np.isnan(r), np.maximum(r, s.exceedance_floor), r)
    d["r_eff"] = r
    pen = ratio_penalty(r, s.penalty_points)
    d["by_share"] = ((np.isnan(r) & (d["threshold"].fillna(-1) == 0).to_numpy())   # coliforms, spores: 0/100 mL
                     | d["code"].isin(list(ranges or {})).to_numpy())              # pH, conductivity: a range
    d.loc[d["by_share"], ["r_eff", "ratio_basis"]] = [np.nan, "share outside"]
    cap = np.where(d["family"] == "comfort", s.comfort_cap, np.inf)
    pen = np.where(d["by_share"], frequency_penalty(d["n"], d["n_exceed"], s.comfort_cap, s.micro_k), pen)
    d["penalty"] = np.minimum(np.nan_to_num(pen, nan=0.0), cap)
    d["code_merged"] = d["code"].map(lambda c: SAME_ITEM.get(c, c))
    d = d.sort_values("penalty", ascending=False).drop_duplicates(["cdreseau", "code_merged"])
    return d.reset_index(drop=True)


# --- Network scores ----------------------------------------------------------------------------------
def udi_scores(micro_win: pd.DataFrame, fam_win: pd.DataFrame, params: pd.DataFrame,
               p95: pd.DataFrame | None, s: ScoreSettings = DEFAULT, ranges: dict | None = None) -> pd.DataFrame:
    """Sub-scores, global score, grade and confidence for every network with data in the windows."""
    nets = pd.Index(sorted(set(micro_win["cdreseau"]) | set(fam_win["cdreseau"])), name="cdreseau")
    out = pd.DataFrame(index=nets)
    m = micro_win.set_index("cdreseau")
    out["n_bact"] = m["n_bact"].reindex(nets).fillna(0).astype(int)
    out["n_bact_nc"] = m["n_bact_nc"].reindex(nets).fillna(0).astype(int)
    out["n_chem_nc_official"] = m["n_chem_nc"].reindex(nets).fillna(0).astype(int)
    national_t = out["n_bact_nc"].sum() / max(out["n_bact"].sum(), 1)
    out["micro"] = micro_subscore(out["n_bact"], out["n_bact_nc"], s.micro_k, s.micro_prior_n, national_t)

    measured = fam_win.groupby(["cdreseau", "family"])["n_samples"].max().unstack()
    for f in ("chem", "comfort"):
        out[f"n_samples_{f}"] = measured[f].reindex(nets).fillna(0).astype(int) if f in measured else 0
    sub = fam_win[fam_win["family"] == "chem"].groupby("cdreseau")["subfamily"].agg(set)
    out["has_nitrates"] = [("nitrates" in sub.get(n, set())) for n in nets]
    out["has_pesticides"] = [("pesticides" in sub.get(n, set())) for n in nets]
    out["has_pfas"] = [("pfas" in sub.get(n, set())) for n in nets]

    pen = parameter_penalties(params, p95, s, ranges)
    for f in ("chem", "comfort"):
        pf = pen[pen["family"] == f]
        sc = pf.groupby("cdreseau")["penalty"].apply(lambda p: combine_penalties(p, s.other_factor))
        # measured with no detected/exceeding parameter -> 100; not measured -> NaN
        out[f] = np.where(out[f"n_samples_{f}"] > 0, sc.reindex(nets).fillna(100.0), np.nan)
        worst = pf.groupby("cdreseau").first()      # sorted by penalty desc
        out[f"worst_{f}_code"] = worst["code"].reindex(nets).where(worst["penalty"].reindex(nets) > 0)
        out[f"worst_{f}_penalty"] = worst["penalty"].reindex(nets).fillna(0.0)
    out["score"] = global_score(out, s.weights)
    out["grade"] = out["score"].map(grade)
    out["n_families"] = out[list(FAMILIES)].notna().sum(axis=1)
    out["confidence"] = confidence(out)
    return out.reset_index()


def global_score(sub: pd.DataFrame, weights: dict) -> pd.Series:
    """Weighted mean of the measured families; NaN when neither microbiology nor chemistry is measured."""
    w = pd.Series(weights, dtype=float)
    vals = sub[list(w.index)]
    wmat = vals.notna() * w
    score = (vals.fillna(0) * w).sum(axis=1) / wmat.sum(axis=1).replace(0, np.nan)
    return score.where(sub["micro"].notna() | sub["chem"].notna())


def confidence(d: pd.DataFrame) -> pd.Series:
    high = ((d["n_families"] == 3) & (d["n_bact"] >= config.CONF_HIGH_MIN_BACT)
            & d["has_nitrates"] & d["has_pesticides"])
    low = d["micro"].isna() | d["chem"].isna() | (d["n_bact"] <= config.CONF_LOW_MAX_BACT)
    conf = pd.Series(np.select([low, high], ["low", "high"], "medium"), index=d.index, dtype=object)
    return conf.where(d["score"].notna(), None)


# --- Commune scores --------------------------------------------------------------------------------
CONF_ORDER = {"low": 0, "medium": 1, "high": 2}


def commune_links(bridge: pd.DataFrame, min_year: int = config.PARTIAL_YEAR - 1) -> pd.DataFrame:
    """Network links of each commune for its latest year (2026, else 2025)."""
    b = bridge[bridge["annee"] >= min_year]
    last = b.groupby("insee")["annee"].transform("max")
    return b[b["annee"] == last][["insee", "cdreseau", "annee", "districts"]]


def commune_scores(udi: pd.DataFrame, links: pd.DataFrame, s: ScoreSettings = DEFAULT) -> pd.DataFrame:
    """Mean of the scored networks of each commune, with the worst network and the lowest confidence."""
    d = links.merge(udi, on="cdreseau", how="left")
    d["conf_rank"] = d["confidence"].map(CONF_ORDER)
    scored = d[d["score"].notna()].sort_values("score")
    g = scored.groupby("insee")
    out = pd.DataFrame({
        "score": g["score"].mean(),
        "micro": g["micro"].mean(), "chem": g["chem"].mean(), "comfort": g["comfort"].mean(),
        "worst_udi": g["cdreseau"].first(), "worst_udi_score": g["score"].min(),
        "conf_rank": g["conf_rank"].min(),
    })
    n = d.groupby("insee").agg(n_udi=("cdreseau", "nunique"), link_year=("annee", "max"))
    out = n.join(out, how="left")
    out["n_udi_scored"] = scored.groupby("insee")["cdreseau"].nunique().reindex(out.index).fillna(0).astype(int)
    out["grade"] = out["score"].map(grade)
    inv = {v: k for k, v in CONF_ORDER.items()}
    out["confidence"] = out["conf_rank"].map(inv)
    out.loc[(out["n_udi_scored"] < out["n_udi"]) & (out["confidence"] == "high"), "confidence"] = "medium"
    return out.drop(columns="conf_rank").reset_index()


# --- "Why" report (rules, no AI) ---------------------------------------------------------------------
# Labels of the key parameters; in French the catalogue labels (French) are used for the others.
KEY_LABELS = {
    "en": {"NO3": "Nitrates", "NO2": "Nitrites", "NO3_NO2": "Nitrates/50 + nitrites/3", "SPFAS": "PFAS (sum of 20)",
           "PESTOT": "Total pesticides", "AS": "Arsenic", "PB": "Lead", "SE": "Selenium", "SB": "Antimony",
           "CLVYL": "Vinyl chloride", "THM4": "Trihalomethanes", "BRATE": "Bromates", "CLITE_T": "Chlorites",
           "CLATE_T": "Chlorates", "CLATE": "Chlorates", "ECOLI": "E. coli", "STRF": "Enterococci",
           "CTF": "Coliform bacteria", "BSIR": "Sulphite-reducing spores", "TURBNFU": "Turbidity", "FET": "Iron",
           "MN": "Manganese", "ALTMICR": "Aluminium", "NH4": "Ammonium", "COT": "Total organic carbon", "PH": "pH",
           "CDT25": "Conductivity", "TH": "Hardness", "MTCESA": "ESA-metolachlor", "ESAMTC": "ESA-metolachlor",
           "MTCNOA": "NOA-metolachlor", "NOAMTC": "NOA-metolachlor", "471811R": "Chlorothalonil R471811",
           "R471811": "Chlorothalonil R471811", "CLDZ_D": "Chloridazon-desphenyl",
           "CLDZ_MD": "Chloridazon-methyl-desphenyl", "ADET": "Atrazine-desethyl", "CLTHALS": "Chlorothalonil R417888"},
    "fr": {"NO3": "Nitrates", "NO2": "Nitrites", "NO3_NO2": "Nitrates/50 + nitrites/3", "SPFAS": "PFAS (somme de 20)",
           "PESTOT": "Total des pesticides", "AS": "Arsenic", "PB": "Plomb", "SE": "Sélénium", "SB": "Antimoine",
           "CLVYL": "Chlorure de vinyle", "THM4": "Trihalométhanes", "BRATE": "Bromates", "CLITE_T": "Chlorites",
           "CLATE_T": "Chlorates", "CLATE": "Chlorates", "ECOLI": "E. coli", "STRF": "Entérocoques",
           "CTF": "Bactéries coliformes", "BSIR": "Spores sulfito-réductrices", "TURBNFU": "Turbidité", "FET": "Fer",
           "MN": "Manganèse", "ALTMICR": "Aluminium", "NH4": "Ammonium", "COT": "Carbone organique total", "PH": "pH",
           "CDT25": "Conductivité", "TH": "Dureté", "MTCESA": "ESA-métolachlore", "ESAMTC": "ESA-métolachlore",
           "MTCNOA": "NOA-métolachlore", "NOAMTC": "NOA-métolachlore", "471811R": "Chlorothalonil R471811",
           "R471811": "Chlorothalonil R471811", "CLDZ_D": "Chloridazone desphényl",
           "CLDZ_MD": "Chloridazone méthyl desphényl", "ADET": "Atrazine déséthyl", "CLTHALS": "Chlorothalonil R417888"},
}
REPORT_KINDS = ("ok", "limit", "watch", "info", "unknown")
REPORT_LABELS_EN = {"ok": "Good", "limit": "Above limit", "watch": "Watch", "info": "Note", "unknown": "Not tested"}


def _tr(key: str, **kw) -> str:
    from utils.i18n import t
    return t(key, **kw)


def _trn(key: str, count, **kw) -> str:
    """Translated sentence with singular agreement when count == 1."""
    from utils.i18n import tn
    return tn(key, count, **kw)


def _lang() -> str:
    from utils.i18n import lang
    return lang()


def _fmt(v: float) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "?"
    if v == 0:
        return "0"
    a = abs(v)
    s = f"{v:.0f}" if a >= 100 else f"{v:.1f}" if a >= 10 else f"{v:.2f}" if a >= 0.1 else f"{v:.3g}"
    s = s.rstrip("0").rstrip(".") if "." in s else s
    return s.replace(".", ",") if _lang() == "fr" else s


def _date(d) -> str:
    from utils.i18n import date_fr_en
    try:
        return date_fr_en(d)
    except (ValueError, TypeError):
        return str(d)


def _pct1(x: float) -> str:
    s = f"{100 * x:.1f}"
    return f"{s.replace('.', ',')} %" if _lang() == "fr" else f"{s}%"


def label(code: str, catalog_labels: dict | None = None) -> str:
    return KEY_LABELS[_lang()].get(code) or (catalog_labels or {}).get(code) or code


def why_report(udi_row: pd.Series, params: pd.DataFrame, fam: pd.DataFrame, p95: pd.DataFrame | None = None,
               catalog_labels: dict | None = None, s: ScoreSettings = DEFAULT, ranges: dict | None = None,
               max_items: int = 6) -> list[tuple[str, str]]:
    """Rule-based explanation of one network's score: list of (kind, sentence) in the current language.

    kind: ok (strength), limit (above a health limit), watch (close to a limit, or above a comfort reference),
    info (good to know), unknown (not measured). The app shows each kind as a labelled badge.
    """
    out: list[tuple[str, str]] = []
    net = udi_row["cdreseau"]
    p = params[params["cdreseau"] == net]
    pen = parameter_penalties(p, None if p95 is None else p95[p95["cdreseau"] == net], s, ranges)
    f = fam[fam["cdreseau"] == net]

    def unit_of(r):
        u = r.get("unit")
        return u if isinstance(u, str) else ""

    # bacteria (official conformity, 12 months)
    n, nc = int(udi_row["n_bact"]), int(udi_row["n_bact_nc"])
    if n == 0:
        out.append(("unknown", _tr("rep.bact_none")))
    elif nc == 0:
        out.append(("ok", _trn("rep.bact_ok", n, n=n)))
    else:
        bugs = p[(p["family"] == "micro") & (p["n_exceed"] > 0)]
        which = ", ".join(label(c, catalog_labels) for c in bugs["code"]) or _tr("rep.bacteria")
        out.append(("limit", _trn("rep.bact_nc", nc, nc=nc, n=n, pct=_pct1(nc / n), which=which)))

    # health chemistry (36 months)
    chem = pen[pen["family"] == "chem"]
    issues = chem[chem["penalty"] > 0]
    for _, r in issues.head(max_items).iterrows():
        lab, unit = label(r["code"], catalog_labels), unit_of(r)
        date = _tr("rep.on_date", date=_date(r["date_max"])) if pd.notna(r.get("date_max")) else ""
        if r["n_exceed"] > 0:
            out.append(("limit", _trn("rep.chem_exceed", r["n_exceed"], lab=lab, k=int(r["n_exceed"]), n=int(r["n"]),
                                     thr=_fmt(r["threshold"]), unit=unit, max=_fmt(r["max_value"]), date=date)))
        else:
            key = "rep.chem_close_p95" if r["ratio_basis"] == "p95" else "rep.chem_close"
            out.append(("watch", _tr(key, lab=lab, max=_fmt(r["max_value"]), unit=unit, date=date,
                                     thr=_fmt(r["threshold"]))))
    if udi_row.get("n_samples_chem", 0) > 0 and issues.empty:
        out.append(("ok", _tr("rep.chem_ok")))
    nit = chem[chem["code"] == "NO3"]
    if len(nit) and nit["penalty"].iloc[0] == 0:
        r = nit.iloc[0]
        out.append(("ok", _tr("rep.nitrates_ok", max=_fmt(r["max_value"]), unit=unit_of(r), thr=_fmt(r["threshold"]))))
    pest_sub = f[(f["family"] == "chem") & (f["subfamily"] == "pesticides")]
    if len(pest_sub) and int(pest_sub["n_exceed"].sum()) == 0:
        out.append(("ok", _tr("rep.pest_ok", n=int(pest_sub["n_samples"].max()), k=int(pest_sub["n_params"].max()))))

    # comfort and indicators (12 months)
    comf = pen[(pen["family"] == "comfort") & (pen["penalty"] > 0)]
    for _, r in comf.head(max_items).iterrows():
        lab, unit = label(r["code"], catalog_labels), unit_of(r)
        kind = _tr("rep.kind_indicative") if r["threshold_kind"] == "indicative" else _tr("rep.kind_reference")
        if r["code"] in (ranges or {}):
            lo, hi = ranges[r["code"]]
            out.append(("watch", _trn("rep.comf_range", r["n_exceed"], lab=lab, k=int(r["n_exceed"]), n=int(r["n"]), lo=_fmt(lo),
                                     hi=_fmt(hi), unit=unit)))
        elif r["n_exceed"] > 0 and r["threshold_kind"] == "indicative":
            out.append(("watch", _trn("rep.indicative_exceed", r["n_exceed"], lab=lab, k=int(r["n_exceed"]), n=int(r["n"]))))
        elif r["n_exceed"] > 0:
            out.append(("watch", _trn("rep.comf_exceed", r["n_exceed"], lab=lab, k=int(r["n_exceed"]), n=int(r["n"]), kind=kind,
                                     thr=_fmt(r["threshold"]), unit=unit)))
        else:
            out.append(("info", _tr("rep.comf_close", lab=lab, max=_fmt(r["max_value"]), unit=unit, kind=kind,
                                    thr=_fmt(r["threshold"]))))
    nonrel = p[(p["subfamily"] == "pesticide_metabolite_non_relevant") & (p["n_detected"] > 0) & (p["n_exceed"] == 0)]
    for _, r in nonrel.drop_duplicates("code").iterrows():
        if r["code"] not in set(comf["code"]):
            out.append(("info", _tr("rep.nonrel", lab=label(r["code"], catalog_labels), max=_fmt(r["max_value"]))))
    th = p[p["code"] == "TH"]
    if len(th):
        out.append(("info", _tr("rep.hardness", v=_fmt(float(th["mean"].iloc[0])))))

    # not measured
    if udi_row.get("n_samples_chem", 0) == 0:
        out.append(("unknown", _tr("rep.no_chem")))
    else:
        if not udi_row.get("has_nitrates", False):
            out.append(("unknown", _tr("rep.no_nitrates")))
        if not udi_row.get("has_pesticides", False):
            out.append(("unknown", _tr("rep.no_pesticides")))
        if not udi_row.get("has_pfas", False):
            out.append(("unknown", _tr("rep.no_pfas")))
    if udi_row.get("n_samples_comfort", 0) == 0:
        out.append(("unknown", _tr("rep.no_comfort")))
    return out

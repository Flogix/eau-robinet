"""Personal score: the official method of utils/score.py, recomputed with the reader's own settings.

The reader can change three kinds of choices on the page "Build your score":
  weights     how much bacteria, health chemistry and comfort count in the global score;
  severity    a multiplier on the penalties of one group of substances (pesticides x 2, metals x 3, ...),
              and how hard a bacterial incident counts (the exponent k of the microbiology mark);
  thresholds  the value a key substance is compared with (nitrates, lead, arsenic, PFAS, each pesticide).

utils/score.udi_scores takes about 6 seconds for the 23,000 networks: too slow for a slider. Everything that does not
depend on the reader's settings is computed once (prepare), and recompute() only redoes the arithmetic on numpy
arrays. With the official settings, recompute() gives exactly the published scores (tests/test_custom_score.py).

Changing a threshold rescales the ratio value / threshold of the rows concerned: r_new = r x old / new. An exceedance
is then "the highest value is above the new threshold", which is the published rule with the new value.
These settings are personal choices to explore the method. They change nothing to the regulatory limits.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

import config
from utils import score as S

# Groups of health-chemistry substances whose penalties the reader can make heavier or lighter.
SEVERITY_GROUPS = ("pesticides", "nitrates", "metals", "pfas", "disinfection_byproducts")
SEVERITY_CHOICES = (0.5, 1.0, 2.0, 3.0)
MICRO_K_CHOICES = (2.5, 5.0, 10.0, 20.0)

# Key thresholds the reader can move: official value, slider range and step, unit, and the rows they apply to.
# The official values are those written on the result rows (checked in tests/test_custom_score.py).
THRESHOLDS = {
    "NO3": {"official": 50.0, "min": 10.0, "max": 100.0, "step": 5.0, "unit": "mg/L"},
    "PB": {"official": 10.0, "min": 1.0, "max": 25.0, "step": 1.0, "unit": "µg/L"},
    "AS": {"official": 10.0, "min": 1.0, "max": 25.0, "step": 1.0, "unit": "µg/L"},
    "SPFAS": {"official": 0.1, "min": 0.02, "max": 0.5, "step": 0.02, "unit": "µg/L"},
    "PEST": {"official": 0.1, "min": 0.02, "max": 0.5, "step": 0.02, "unit": "µg/L"},   # each pesticide
}


@dataclass(frozen=True)
class Personal:
    weights: tuple = (config.WEIGHTS["micro"], config.WEIGHTS["chem"], config.WEIGHTS["comfort"])
    micro_k: float = config.MICRO_K
    severity: dict = field(default_factory=dict)      # group -> multiplier (missing = 1)
    thresholds: dict = field(default_factory=dict)    # key of THRESHOLDS -> value (missing = official)

    @property
    def is_official(self) -> bool:
        w = np.array(self.weights, dtype=float)
        w_off = np.array([config.WEIGHTS[k] for k in S.FAMILIES])
        return (w.sum() > 0 and np.allclose(w / w.sum(), w_off) and self.micro_k == config.MICRO_K
                and all(v == 1 for v in self.severity.values())
                and all(v == THRESHOLDS[k]["official"] for k, v in self.thresholds.items()))


@dataclass
class Prepared:
    """Everything that does not depend on the reader's settings, as aligned numpy arrays."""
    nets: pd.Index              # network codes, in the order of the network arrays
    n_bact: np.ndarray
    n_bact_nc: np.ndarray
    measured_chem: np.ndarray   # bool per network: health chemistry measured in the window
    measured_comfort: np.ndarray
    # one entry per network x parameter row (chem and comfort families)
    row_net: np.ndarray         # index into nets
    row_chem: np.ndarray        # bool: chem (True) or comfort (False)
    row_item: np.ndarray        # index of (network, merged code): twin codes count once, the worse one
    row_group: np.ndarray       # index of the severity group of the row in SEVERITY_GROUPS, -1 if none (int8)
    row_key: np.ndarray         # index of the threshold key of the row in THRESHOLDS, -1 if none (int8)
    ratio: np.ndarray           # P95 or max ratio value / threshold (official choice), NaN for "share outside" rows
    max_ratio: np.ndarray
    exceeded: np.ndarray        # bool: at least one measurement above the official threshold
    share_pen: np.ndarray       # penalty of the "share outside the reference" rows (pH, coliforms, ...), NaN elsewhere
    n_items: int
    # commune links
    link_insee: np.ndarray
    link_net: np.ndarray        # index into nets, -1 if the network has no score data


def threshold_key(code: str, subfamily: str, threshold: float) -> str:
    """Which reader's threshold applies to a row. "Each pesticide" covers the individual substances (limit 0.1 µg/L,
    0.03 for a few old ones), not the 0.5 µg/L limits on sums (total pesticides, atrazine and its metabolites...)."""
    if code in THRESHOLDS:
        return code
    if subfamily == "pesticides" and threshold <= THRESHOLDS["PEST"]["official"] + 1e-6:
        return "PEST"
    return ""


def prepare(micro_win: pd.DataFrame, fam_win: pd.DataFrame, params: pd.DataFrame, p95: pd.DataFrame | None,
            links: pd.DataFrame, ranges: dict | None = None, s: S.ScoreSettings = S.DEFAULT) -> Prepared:
    nets = pd.Index(sorted(set(micro_win["cdreseau"]) | set(fam_win["cdreseau"])), name="cdreseau")
    m = micro_win.set_index("cdreseau")
    measured = fam_win.groupby(["cdreseau", "family"], observed=True)["n_samples"].max().unstack()

    def has(f):
        return (measured[f].reindex(nets).fillna(0) > 0).to_numpy() if f in measured else np.zeros(len(nets), bool)

    d = params[params["family"].isin(["chem", "comfort"])].copy()
    for c in ("cdreseau", "code", "family", "subfamily"):
        d[c] = d[c].astype(str)
    if p95 is not None and len(p95):
        q = p95[["cdreseau", "code", "n_ratio", "p95_ratio"]].copy()
        q["cdreseau"], q["code"] = q["cdreseau"].astype(str), q["code"].astype(str)
        d = d.merge(q, on=["cdreseau", "code"], how="left")
    else:
        d["n_ratio"], d["p95_ratio"] = np.nan, np.nan
    use_p95 = (s.use_p95 & (d["n_ratio"] >= s.p95_min_n) & d["p95_ratio"].notna()).to_numpy()
    ratio = np.where(use_p95, d["p95_ratio"], d["max_ratio"]).astype(float)
    by_share = ((np.isnan(ratio) & (d["threshold"].fillna(-1) == 0).to_numpy())
                | d["code"].isin(list(ranges or {})).to_numpy())
    share_pen = np.where(by_share, S.frequency_penalty(d["n"], d["n_exceed"], s.comfort_cap, s.micro_k), np.nan)
    ratio[by_share] = np.nan
    merged = d["code"].map(lambda c: S.SAME_ITEM.get(c, c))
    item = pd.factorize(d["cdreseau"] + "|" + merged)[0]
    groups = np.where(d["family"].to_numpy() == "chem", d["subfamily"].to_numpy(), "")
    keys = [threshold_key(c, sf, thr) for c, sf, thr in zip(d["code"], d["subfamily"], d["threshold"].fillna(np.inf))]
    lk = links[["insee", "cdreseau"]].astype(str)
    return Prepared(
        nets=nets,
        n_bact=m["n_bact"].reindex(nets).fillna(0).to_numpy(float),
        n_bact_nc=m["n_bact_nc"].reindex(nets).fillna(0).to_numpy(float),
        measured_chem=has("chem"), measured_comfort=has("comfort"),
        row_net=nets.get_indexer(d["cdreseau"]), row_chem=(d["family"] == "chem").to_numpy(),
        row_item=item.astype(np.int32), row_group=_index_of(groups, SEVERITY_GROUPS),
        row_key=_index_of(keys, list(THRESHOLDS)),
        ratio=ratio, max_ratio=d["max_ratio"].to_numpy(float), exceeded=(d["n_exceed"] > 0).to_numpy(),
        share_pen=share_pen, n_items=int(item.max()) + 1 if len(item) else 0,
        link_insee=lk["insee"].to_numpy(), link_net=nets.get_indexer(lk["cdreseau"]))


def _index_of(values, choices) -> np.ndarray:
    pos = {v: i for i, v in enumerate(choices)}
    return np.array([pos.get(v, -1) for v in values], dtype=np.int8)


def _combine(pen: np.ndarray, net: np.ndarray, n_nets: int, other_factor: float) -> np.ndarray:
    """100 − worst − other_factor × (sum of the others) per network, bounded to [0, 100]."""
    worst = np.zeros(n_nets)
    np.maximum.at(worst, net, pen)
    total = np.bincount(net, weights=pen, minlength=n_nets)
    return np.clip(100.0 - worst - other_factor * (total - worst), 0.0, 100.0)


def recompute(p: Prepared, mine: Personal, s: S.ScoreSettings = S.DEFAULT) -> pd.DataFrame:
    """Sub-scores, score and grade of every network with the reader's settings (index = network code)."""
    factor = np.ones(len(p.ratio))
    for key, value in mine.thresholds.items():
        factor[p.row_key == list(THRESHOLDS).index(key)] = THRESHOLDS[key]["official"] / float(value)
    changed = factor != 1.0
    r = p.ratio * factor
    exceeded = np.where(changed, p.max_ratio * factor > 1.0, p.exceeded)
    if s.exceedance_floor is not None:
        r = np.where(exceeded & ~np.isnan(r), np.maximum(r, s.exceedance_floor), r)
    pen = np.nan_to_num(S.ratio_penalty(r, s.penalty_points), nan=0.0)
    pen = np.where(np.isnan(p.share_pen), pen, p.share_pen)
    pen = np.where(p.row_chem, pen, np.minimum(pen, s.comfort_cap))
    for group, mult in mine.severity.items():
        pen = np.where(p.row_group == SEVERITY_GROUPS.index(group), np.minimum(pen * float(mult), 100.0), pen)

    # twin codes: keep the worse row of each (network, merged code), with its family
    order = np.lexsort((-pen, p.row_item))
    first = order[np.r_[True, p.row_item[order][1:] != p.row_item[order][:-1]]] if len(order) else order
    n = len(p.nets)
    out = pd.DataFrame(index=p.nets)
    out["micro"] = S.micro_subscore(p.n_bact, p.n_bact_nc, mine.micro_k)
    for fam, is_chem, measured in (("chem", True, p.measured_chem), ("comfort", False, p.measured_comfort)):
        rows = first[p.row_chem[first] == is_chem]
        sc = _combine(pen[rows], p.row_net[rows], n, s.other_factor)
        out[fam] = np.where(measured, sc, np.nan)
    w = np.array(mine.weights, dtype=float)
    out["score"] = S.global_score(out, dict(zip(S.FAMILIES, w / w.sum()))) if w.sum() > 0 else np.nan
    out["grade"] = out["score"].map(S.grade)
    return out


def commune_recompute(p: Prepared, udi: pd.DataFrame) -> pd.DataFrame:
    """Mean of the scored networks of each commune (same rule as utils/score.commune_scores)."""
    ok = p.link_net >= 0
    d = pd.DataFrame({"insee": p.link_insee[ok], "score": udi["score"].to_numpy()[p.link_net[ok]]})
    for f in S.FAMILIES:
        d[f] = udi[f].to_numpy()[p.link_net[ok]]
    d = d[d["score"].notna()]
    out = d.groupby("insee")[["score", *S.FAMILIES]].mean()
    out["grade"] = out["score"].map(S.grade)
    return out

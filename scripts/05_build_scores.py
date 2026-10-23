# Pipeline stage 05: computes network and commune scores, validations, and sensitivity metrics.
"""05: scores /100 (networks and communes), validation against official conformity, sensitivity analysis.

Reads only data/processed/ (small tables): no DuckDB, no raw data, a few seconds of pandas.
Outputs (data/processed/)
  udi_scores           one row per network: sub-scores, score, grade, confidence, worst parameters
  commune_scores       one row per commune (latest commune–network link): mean of its networks, worst network
  score_validation     scores of networks with / without official non-conformities (12 months)
  score_sensitivity    rank correlation (Spearman) between the default ranking and each variant
  score_witnesses.md   (docs/) the 5 witness communes with their "why" report

Usage: python scripts/05_build_scores.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config  # noqa: E402
from utils import score as S  # noqa: E402
from utils.io import read_processed  # noqa: E402

P = config.PROCESSED
WITNESSES = {   # role -> INSEE code (the rural commune is drawn at random, see pick_rural)
    "Paris": "75056",
    "Villejuif": "94076",
    "Mountain (loi Montagne)": "74056",          # Chamonix-Mont-Blanc
    "Mediterranean coast (approximation)": "34301",   # Sète
}

VARIANTS = {   # name -> changes to the default settings
    "weights equal (1/3 each)": dict(weights={"micro": 1 / 3, "chem": 1 / 3, "comfort": 1 / 3}),
    "weights micro-heavy (0.6/0.3/0.1)": dict(weights={"micro": 0.6, "chem": 0.3, "comfort": 0.1}),
    "weights chem-heavy (0.3/0.6/0.1)": dict(weights={"micro": 0.3, "chem": 0.6, "comfort": 0.1}),
    "no comfort (0.5/0.5/0)": dict(weights={"micro": 0.5, "chem": 0.5, "comfort": 0.0}),
    "micro k = 10 (first proposal)": dict(micro_k=10),
    "micro k = 20": dict(micro_k=20),
    "micro smoothed (12 pseudo-samples at the national rate)": dict(micro_prior_n=12),
    "max instead of P95": dict(use_p95=False),
    "no exceedance floor": dict(exceedance_floor=None),
    "other penalties x 0": dict(other_factor=0.0),
    "other penalties x 0.5": dict(other_factor=0.5),
    "comfort cap 30": dict(comfort_cap=30),
    "comfort cap 80": dict(comfort_cap=80),
    "steeper curve (20 -> 40 at r = 1)": dict(penalty_points=((0.5, 0), (1.0, 40), (2.0, 80))),
}


def load():
    """Load required processed tables into a dictionary of DataFrames."""
    t = {name: read_processed(name) for name in
         ("udi_micro_window", "udi_family_window", "udi_param_window", "udi_param_p95", "bridge_commune_udi",
          "dim_communes", "dim_udi", "params_catalog")}
    t["ranges"] = S.reference_ranges(t["params_catalog"])   # pH, conductivity: scored on the share outside
    return t


def auc_lower(scores_bad: pd.Series, scores_good: pd.Series) -> float:
    """Probability that a network with an official non-conformity scores lower than one without (ties = 1/2)."""
    a, b = scores_bad.dropna().to_numpy(), scores_good.dropna().to_numpy()
    if len(a) == 0 or len(b) == 0:
        return float("nan")
    ranks = pd.Series(np.concatenate([a, b])).rank().to_numpy()
    u_bad = ranks[: len(a)].sum() - len(a) * (len(a) + 1) / 2     # Mann–Whitney U of the "bad" group
    return float(1 - u_bad / (len(a) * len(b)))


def spearman(x: pd.Series, y: pd.Series) -> float:
    """Spearman rank correlation = Pearson correlation of the ranks (average ranks for ties); no scipy needed."""
    d = pd.DataFrame({"x": x, "y": y}).dropna()
    return float(d["x"].rank().corr(d["y"].rank()))


def validation(udi: pd.DataFrame) -> pd.DataFrame:
    """Compare calculated scores across networks with and without official non-conformities."""
    rows = []
    for label, flag, col in (("bacteriology", "n_bact_nc", "micro"), ("bacteriology", "n_bact_nc", "score"),
                             ("chemistry", "n_chem_nc_official", "chem"), ("chemistry", "n_chem_nc_official", "score")):
        d = udi[udi["score"].notna()]
        bad, good = d[d[flag] > 0][col], d[d[flag] == 0][col]
        rows.append({"official_nonconformity": label, "score_column": col,
                     "n_networks_with": int(bad.notna().sum()), "n_networks_without": int(good.notna().sum()),
                     "median_with": float(bad.median()), "median_without": float(good.median()),
                     "mean_with": float(bad.mean()), "mean_without": float(good.mean()),
                     "share_with_below_100": float((bad < 100).mean()),
                     "share_without_below_100": float((good < 100).mean()),
                     "auc_lower": auc_lower(bad, good)})
    return pd.DataFrame(rows)


def sensitivity(t, base_udi: pd.DataFrame, base_com: pd.DataFrame, links: pd.DataFrame) -> pd.DataFrame:
    """Compute rank correlations and stability metrics across score formula variants."""
    eligible = base_udi[(base_udi["n_bact"] >= config.MIN_SAMPLES_RANKING) & base_udi["score"].notna()]["cdreseau"]
    b = base_udi.set_index("cdreseau")
    bc = base_com.set_index("insee")
    rows = []
    for name, changes in {"default": {}, **VARIANTS}.items():
        s = S.DEFAULT.with_(**changes)
        if changes:
            v = S.udi_scores(t["udi_micro_window"], t["udi_family_window"], t["udi_param_window"],
                             t["udi_param_p95"], s, t["ranges"])
            vc = S.commune_scores(v, links, s).set_index("insee")
        else:
            v, vc = base_udi, bc
        v = v.set_index("cdreseau")
        e = eligible[eligible.isin(v.index)]
        x, y = b.loc[e, "score"], v.loc[e, "score"]
        bottom = int(round(0.1 * len(e)))
        bot_base = set(x.sort_values(kind="stable").index[:bottom])
        bot_var = set(y.sort_values(kind="stable").index[:bottom])
        cx, cy = bc["score"].dropna(), vc["score"].reindex(bc["score"].dropna().index)
        grades = v["grade"].value_counts(normalize=True)
        rows.append({"variant": name, "n_networks": len(e),
                     # ranking networks (>= 12 bacteriological samples), as in the top/bottom rankings of the app
                     "spearman_networks": spearman(x, y),
                     "spearman_all_networks": spearman(b["score"], v["score"].reindex(b.index)),
                     "spearman_communes": spearman(cx, cy),
                     "bottom10_overlap": len(bot_base & bot_var) / max(bottom, 1),
                     "share_grade_changed": float((b.loc[e, "grade"] != v.loc[e, "grade"]).mean()),
                     "median_abs_change": float((y - x).abs().median()),
                     "median_score": float(y.median()),
                     **{f"share_{g}_all": float(grades.get(g, 0.0)) for g in "ABCDE"}})
    return pd.DataFrame(rows)


def pick_rural(com: pd.DataFrame, dim: pd.DataFrame) -> str:
    """A small rural commune drawn at random (seed config.SEED) among scored communes of mainland France
    with fewer than 500 inhabitants, 'rural à habitat dispersé' or 'très dispersé' (INSEE grid, 7 levels)."""
    d = dim[dim["is_current"] & (dim["population"] < 500) & (dim["density7"] >= 6) & ~dim["dep"].str.startswith("97")]
    cand = com[com["insee"].isin(d["insee"]) & com["score"].notna()].sort_values("insee")
    return cand.sample(1, random_state=config.SEED)["insee"].iloc[0]


def witnesses_md(t, udi: pd.DataFrame, com: pd.DataFrame, links: pd.DataFrame) -> str:
    """Generate Markdown documentation detailing scores and diagnostic reports for witness communes."""
    dim = t["dim_communes"].set_index("insee")
    names = t["dim_udi"].set_index("cdreseau")["nomreseau"]
    labels = dict(zip(t["params_catalog"]["code"], t["params_catalog"]["label"]))
    picks = dict(WITNESSES)
    picks["Small rural commune (random, seed 42)"] = pick_rural(com, t["dim_communes"])
    u = udi.set_index("cdreseau")
    c = com.set_index("insee")
    lines = ["# Score: 5 witness communes", "",
             f"Generated by `scripts/05_build_scores.py`. Windows: microbiology and comfort 12 months, chemistry "
             f"36 months, ending on {config.DATA_END_DATE:%d/%m/%Y}. Score = teaching indicator, not a health opinion "
             "(the official opinion is the ARS one).", ""]
    for role, insee in picks.items():
        info, cs = dim.loc[insee], c.loc[insee]
        lines += [f"## {role}: {info['nom']} ({info['dep']}, INSEE {insee})", "",
                  f"Population {int(info['population']):,} · {info['density7_label']} · mountain: "
                  f"{'yes' if info['mountain'] else 'no'} · Mediterranean dept. outside mountain: "
                  f"{'yes' if info['mediterranean_coast'] else 'no'}", "",
                  f"**Score {cs['score']:.1f}/100, grade {cs['grade']}, confidence {cs['confidence']}** "
                  f"(micro {cs['micro']:.1f} · chem {cs['chem']:.1f} · comfort "
                  f"{'n/a' if pd.isna(cs['comfort']) else f'{cs['comfort']:.1f}'}), "
                  f"{int(cs['n_udi_scored'])}/{int(cs['n_udi'])} network(s) scored", ""]
        for net in links[links["insee"] == insee]["cdreseau"]:
            if net not in u.index or pd.isna(u.loc[net, "score"]):
                lines += [f"### Network {net} {names.get(net, '')}: no score (no data in the windows)", ""]
                continue
            r = u.loc[net]
            lines += [f"### Network {net}, {names.get(net, '')}: {r['score']:.1f}/100, grade {r['grade']}, "
                      f"confidence {r['confidence']} (micro {r['micro']:.1f} · chem {r['chem']:.1f} · comfort "
                      f"{'n/a' if pd.isna(r['comfort']) else f'{r['comfort']:.1f}'}; {r['n_bact']} bacteriological "
                      f"samples)", ""]
            rep = S.why_report(r.rename(net).to_frame().T.reset_index(names="cdreseau").iloc[0],
                               t["udi_param_window"], t["udi_family_window"], t["udi_param_p95"], labels,
                               ranges=t["ranges"])
            lines += [f"- **{S.REPORT_LABELS_EN[kind]}.** {text}" for kind, text in rep] + [""]
    return "\n".join(lines)


def main() -> int:
    """Execute score calculations, validation benchmarks, and sensitivity analysis exports."""
    t0 = time.time()
    t = load()
    links = S.commune_links(t["bridge_commune_udi"])
    udi = S.udi_scores(t["udi_micro_window"], t["udi_family_window"], t["udi_param_window"], t["udi_param_p95"],
                       ranges=t["ranges"])
    com = S.commune_scores(udi, links)
    float_cols = ["micro", "chem", "comfort", "score", "worst_chem_penalty", "worst_comfort_penalty"]
    udi[float_cols] = udi[float_cols].astype("float32")
    udi.to_parquet(P / "udi_scores.parquet", index=False)
    com.to_parquet(P / "commune_scores.parquet", index=False)
    print(f"udi_scores: {len(udi):,} networks, {udi['score'].notna().sum():,} scored")
    print(f"commune_scores: {len(com):,} communes, {com['score'].notna().sum():,} scored")
    print(udi["grade"].value_counts().sort_index().to_string())
    print(udi["confidence"].value_counts(dropna=False).to_string())

    val = validation(udi)
    val.to_parquet(P / "score_validation.parquet", index=False)
    print(val.to_string())

    sens = sensitivity(t, udi, com, links)
    sens.to_parquet(P / "score_sensitivity.parquet", index=False)
    print(sens.to_string())

    (config.ROOT / "docs" / "score_witnesses.md").write_text(witnesses_md(t, udi, com, links), encoding="utf-8")
    print(f"docs/score_witnesses.md written in {time.time() - t0:.0f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())

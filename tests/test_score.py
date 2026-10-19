"""Score on synthetic data: every rule of utils/score.py, with hand-computed expectations."""
import numpy as np
import pandas as pd
import pytest

import config
from utils import score as S


def micro(net="U1", n=24, nc=0, chem_nc=0):
    return pd.DataFrame([{"cdreseau": net, "n_bact": n, "n_bact_nc": nc, "n_chem_nc": chem_nc}])


def fam(net="U1", families=(("chem", "nitrates"), ("chem", "pesticides"), ("chem", "pfas"), ("comfort", "indicators")),
        n_samples=12, n_exceed=0):
    return pd.DataFrame([{"cdreseau": net, "family": f, "subfamily": sf, "n_samples": n_samples, "n_params": 5,
                          "n_exceed": n_exceed} for f, sf in families])


def param(net="U1", code="NO3", family="chem", subfamily="nitrates", n=12, n_exceed=0, max_ratio=0.2,
          threshold=50.0, max_value=None, kind="limit", n_detected=None):
    return {"cdreseau": net, "code": code, "family": family, "subfamily": subfamily, "win": "36m", "n": n,
            "n_detected": n if n_detected is None else n_detected, "max_value": max_value if max_value is not None
            else (max_ratio or 0) * threshold, "date_max": "2026-01-15", "mean": 1.0, "n_exceed": n_exceed,
            "max_ratio": max_ratio, "threshold": threshold, "threshold_kind": kind, "unit": "mg/L"}


def run(params_rows, m=None, f=None, p95=None, s=S.DEFAULT):
    params = pd.DataFrame(params_rows) if params_rows else pd.DataFrame(columns=list(param().keys()))
    return S.udi_scores(micro() if m is None else m, fam() if f is None else f, params, p95, s).iloc[0]


# --- elementary formulas ----------------------------------------------------------------------------
def test_micro_formula_matches_spec_examples():
    assert S.micro_subscore(200, 1)[()] == pytest.approx(95.1, abs=0.1)    # 0.5 % non-compliant -> ≈ 95
    assert S.micro_subscore(100, 5)[()] == pytest.approx(59.9, abs=0.1)    # 5 % -> ≈ 60
    assert S.micro_subscore(10, 0)[()] == 100
    assert np.isnan(S.micro_subscore(0, 0)[()])                           # no sample = not measured


def test_micro_smoothing_helps_small_networks_more_than_large_ones():
    small = S.micro_subscore(5, 1, prior_n=12, prior_t=0.01)[()]
    large = S.micro_subscore(300, 6, prior_n=12, prior_t=0.01)[()]
    assert small > S.micro_subscore(5, 1)[()]                         # 1/5 alone -> ≈ 11
    assert large == pytest.approx(S.micro_subscore(300, 6)[()], rel=0.02)
    assert S.micro_subscore(50, 0, prior_n=12, prior_t=0.0)[()] == 100


@pytest.mark.parametrize("r, expected", [(0, 0), (0.5, 0), (0.75, 10), (1.0, 20), (1.5, 50), (2.0, 80), (5.0, 80)])
def test_ratio_penalty_piecewise(r, expected):
    assert S.ratio_penalty([r])[0] == pytest.approx(expected)


def test_combine_penalties():
    assert S.combine_penalties(pd.Series([], dtype=float), 0.25) == 100
    assert S.combine_penalties(pd.Series([20.0, 10.0, 10.0]), 0.25) == pytest.approx(75)
    assert S.combine_penalties(pd.Series([80.0, 80.0, 80.0, 80.0, 80.0]), 0.25) == 0   # bounded at 0


@pytest.mark.parametrize("score, letter", [(100, "A"), (90, "A"), (89.9, "B"), (75, "B"), (60, "C"), (40, "D"), (39.9, "E"), (0, "E")])
def test_grades(score, letter):
    assert S.grade(score) == letter


def test_grade_none():
    assert S.grade(None) is None and S.grade(float("nan")) is None


# --- network score ------------------------------------------------------------------------------------
def test_perfect_network_scores_100_with_high_confidence():
    r = run([param(max_ratio=0.1)])
    assert r["micro"] == 100 and r["chem"] == 100 and r["comfort"] == 100
    assert r["score"] == 100 and r["grade"] == "A" and r["confidence"] == "high"


def test_nitrate_exceedance_lowers_chemistry():
    ok = run([param(max_ratio=0.4)])
    bad = run([param(max_ratio=1.5, n_exceed=1, n=8)])
    assert ok["chem"] == 100
    assert bad["chem"] == pytest.approx(50)              # g(1.5) = 50
    assert bad["score"] < ok["score"]
    assert bad["worst_chem_code"] == "NO3"


def test_missing_family_is_excluded_not_perfect():
    f = fam(families=(("chem", "nitrates"), ("chem", "pesticides")))   # no comfort
    r = run([param(max_ratio=1.5, n_exceed=1, n=8)], f=f)
    assert np.isnan(r["comfort"])
    # weighted mean of micro (100, w 0.4) and chem (50, w 0.4) only: 75, not (40+20+20)/1 = 80
    assert r["score"] == pytest.approx(75)
    assert r["n_families"] == 2 and r["confidence"] == "medium"


def test_no_micro_no_chem_gives_no_score():
    m = micro(n=0)
    f = fam(families=(("comfort", "indicators"),))
    r = run([], m=m, f=f)
    assert np.isnan(r["score"]) and r["grade"] is None and r["confidence"] is None


def test_few_bacteriological_samples_lower_confidence():
    assert run([param()], m=micro(n=3))["confidence"] == "low"
    assert run([param()], m=micro(n=8))["confidence"] == "medium"


def test_p95_used_with_10_measurements_but_exceedance_never_hidden():
    rows = [param(n=40, max_ratio=1.8, n_exceed=1)]
    p95 = pd.DataFrame([{"cdreseau": "U1", "code": "NO3", "n_ratio": 40, "p95_ratio": 0.3}])
    with_p95 = run(rows, p95=p95)
    assert with_p95["chem"] == pytest.approx(80)             # P95 0.3 -> floored at ratio 1 -> penalty 20
    with_max = run(rows, p95=p95, s=S.DEFAULT.with_(use_p95=False))
    assert with_max["chem"] == pytest.approx(100 - S.ratio_penalty([1.8])[0])
    no_floor = run(rows, p95=p95, s=S.DEFAULT.with_(exceedance_floor=None))
    assert no_floor["chem"] == 100


def test_p95_ignored_below_10_measurements():
    rows = [param(n=9, max_ratio=0.9)]
    p95 = pd.DataFrame([{"cdreseau": "U1", "code": "NO3", "n_ratio": 9, "p95_ratio": 0.2}])
    assert run(rows, p95=p95)["chem"] == pytest.approx(100 - S.ratio_penalty([0.9])[0])


def test_comfort_penalty_is_capped():
    rows = [param(code="FET", family="comfort", subfamily="indicators", max_ratio=10, n_exceed=3, kind="reference")]
    assert run(rows)["comfort"] == pytest.approx(100 - config.COMFORT_PENALTY_CAP)


def test_zero_reference_uses_share_of_samples():
    rows = [param(code="CTF", family="comfort", subfamily="bacteria_indicators", max_ratio=None, threshold=0.0,
                  n=10, n_exceed=1, kind="reference")]
    expected = 100 - config.COMFORT_PENALTY_CAP * (1 - 0.9 ** config.MICRO_K)
    assert run(rows)["comfort"] == pytest.approx(expected)


def test_range_reference_uses_share_outside_not_closeness_to_max():
    ranges = {"PH": (6.5, 9.0)}
    near_max = [param(code="PH", family="comfort", subfamily="indicators", max_ratio=0.95, threshold=9.0,
                      n=20, n_exceed=0, kind="reference")]
    params = pd.DataFrame(near_max)
    assert S.udi_scores(micro(), fam(), params, None, ranges=ranges).iloc[0]["comfort"] == 100
    outside = [dict(near_max[0], n_exceed=2, max_ratio=0.9)]       # 2 of 20 below 6.5
    r = S.udi_scores(micro(), fam(), pd.DataFrame(outside), None, ranges=ranges).iloc[0]
    assert r["comfort"] == pytest.approx(100 - config.COMFORT_PENALTY_CAP * (1 - 0.9 ** config.MICRO_K))
    rep = S.why_report(r, pd.DataFrame(outside), fam(), ranges=ranges)
    assert any("outside the quality reference range (6.5–9" in t for _, t in rep)


def test_nitrates_and_nitrate_nitrite_sum_counted_once():
    rows = [param(max_ratio=0.9), param(code="NO3_NO2", max_ratio=0.9, threshold=1.0)]
    assert run(rows)["chem"] == pytest.approx(100 - S.ratio_penalty([0.9])[0])


def test_twin_codes_counted_once():
    rows = [param(code="MTCESA", family="comfort", subfamily="pesticide_metabolite_non_relevant", max_ratio=1.2,
                  n_exceed=1, threshold=0.9, kind="indicative"),
            param(code="ESAMTC", family="comfort", subfamily="pesticide_metabolite_non_relevant", max_ratio=1.2,
                  n_exceed=1, threshold=0.9, kind="indicative")]
    assert run(rows)["comfort"] == pytest.approx(100 - S.ratio_penalty([1.2])[0])


def test_weights_change_the_global_score():
    rows = [param(max_ratio=1.5, n_exceed=1, n=8)]
    a = run(rows)
    b = run(rows, s=S.DEFAULT.with_(weights={"micro": 0.2, "chem": 0.6, "comfort": 0.2}))
    assert b["score"] < a["score"]


# --- commune -------------------------------------------------------------------------------------------
def test_commune_is_mean_of_networks_with_worst_kept():
    m = pd.concat([micro("U1"), micro("U2", nc=12)])
    f = pd.concat([fam("U1"), fam("U2")])
    udi = S.udi_scores(m, f, pd.DataFrame([param("U1"), param("U2")]), None)
    links = pd.DataFrame({"insee": ["X", "X", "Y"], "cdreseau": ["U1", "U2", "U3"], "annee": [2026] * 3,
                          "districts": [None] * 3})
    c = S.commune_scores(udi, links).set_index("insee")
    u = udi.set_index("cdreseau")["score"]
    assert c.loc["X", "score"] == pytest.approx((u["U1"] + u["U2"]) / 2)
    assert c.loc["X", "worst_udi"] == "U2" and c.loc["X", "n_udi"] == 2
    assert np.isnan(c.loc["Y", "score"]) and c.loc["Y", "n_udi_scored"] == 0


def test_commune_links_keep_latest_year():
    b = pd.DataFrame({"annee": [2025, 2026, 2025], "insee": ["X", "X", "Y"], "cdreseau": ["OLD", "NEW", "U9"],
                      "districts": [None] * 3})
    links = S.commune_links(b)
    assert set(zip(links["insee"], links["cdreseau"])) == {("X", "NEW"), ("Y", "U9")}


# --- report --------------------------------------------------------------------------------------------
def test_why_report_mentions_strengths_issues_and_unmeasured():
    f = fam(families=(("chem", "nitrates"), ("chem", "pesticides"), ("comfort", "indicators")))
    params = pd.DataFrame([param(max_ratio=0.76, max_value=38.0)])
    udi = S.udi_scores(micro(n=48), f, params, None).iloc[0]
    rep = S.why_report(udi, params, f)
    text = " ".join(t for _, t in rep)
    assert ("✅", "100% of the 48 bacteriological samples compliant (12 months).") in rep
    assert "Nitrates: max 38 mg/L" in text and "limit of 50 mg/L" in text
    assert any(i == "❔" and "PFAS" in t for i, t in rep)
    assert all(t for _, t in rep)

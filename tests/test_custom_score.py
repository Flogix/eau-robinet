"""Personal score (page "Build your own score"): the fast engine must give exactly the published scores with the
official settings, and move in the expected direction when a setting changes."""
import numpy as np
import pandas as pd
import pytest

import config
from utils import custom_score as C
from utils import score as S
from utils.io import read_processed


@pytest.fixture(scope="module")
def prepared():
    links = S.commune_links(read_processed("bridge_commune_udi"))
    return C.prepare(read_processed("udi_micro_window"), read_processed("udi_family_window"),
                     read_processed("udi_param_window"), read_processed("udi_param_p95"), links,
                     S.reference_ranges(read_processed("params_catalog")))


@pytest.fixture(scope="module")
def official(prepared):
    return C.recompute(prepared, C.Personal())


def test_official_settings_reproduce_published_network_scores(official):
    pub = read_processed("udi_scores").set_index("cdreseau").reindex(official.index)
    for col in ("micro", "chem", "comfort", "score"):
        assert (official[col].isna() == pub[col].isna()).all(), col
        assert np.nanmax(np.abs(official[col] - pub[col])) < 1e-3, col
    assert (official["grade"].fillna("") == pub["grade"].fillna("")).all()


def test_official_settings_reproduce_published_town_scores(prepared, official):
    towns = C.commune_recompute(prepared, official)
    pub = read_processed("commune_scores").set_index("insee")
    pub = pub[pub["score"].notna()]
    assert set(towns.index) == set(pub.index)
    assert np.abs(towns["score"] - pub["score"].reindex(towns.index)).max() < 1e-3


def test_official_values_of_thresholds_match_the_data():
    w = read_processed("udi_param_window")
    for code in ("NO3", "PB", "AS", "SPFAS"):
        assert w.loc[w["code"] == code, "threshold"].astype(float).round(4).unique().tolist() == [C.THRESHOLDS[code]["official"]]
    pest = w[(w["subfamily"] == "pesticides")]
    keys = {C.threshold_key(c, "pesticides", thr) for c, thr in zip(pest["code"], pest["threshold"])}
    assert keys == {"PEST", ""}
    sums = pest[[C.threshold_key(c, "pesticides", thr) == "" for c, thr in zip(pest["code"], pest["threshold"])]]
    assert set(sums["code"]) <= {"PESTOT", "ATRZMET", "TBZMETA"}   # the 0.5 µg/L sums stay untouched


def test_is_official():
    assert C.Personal().is_official
    assert C.Personal(weights=(2, 2, 1)).is_official            # same weights once rescaled
    assert not C.Personal(weights=(1, 1, 1)).is_official
    assert not C.Personal(severity={"pesticides": 2.0}).is_official
    assert not C.Personal(thresholds={"NO3": 25.0}).is_official
    assert not C.Personal(micro_k=10).is_official


def test_stricter_settings_never_raise_a_score(prepared, official):
    strict = C.recompute(prepared, C.Personal(micro_k=10, severity={g: 2.0 for g in C.SEVERITY_GROUPS},
                                              thresholds={"NO3": 25.0, "PB": 5.0, "AS": 5.0, "PEST": 0.05}))
    for col in ("micro", "chem"):
        diff = (strict[col] - official[col]).dropna()
        assert (diff <= 1e-9).all(), col
        assert (diff < -0.05).any(), col                         # and some scores do drop


def test_lower_nitrate_threshold_hits_networks_with_nitrates(prepared, official):
    """A network whose nitrates reached 30 mg/L is untouched at 50 mg/L (ratio 0.6 is barely penalised) but
    exceeds a 25 mg/L threshold: its chemistry mark must drop by at least the 20-point exceedance penalty."""
    w = read_processed("udi_param_window")
    no3 = w[(w["code"] == "NO3") & (w["max_value"].between(30, 32))]
    nets = set(no3["cdreseau"]) & set(official.index[official["chem"] == 100])
    if not nets:
        pytest.skip("no network with nitrates at 30 mg/L and a perfect chemistry mark")
    mine = C.recompute(prepared, C.Personal(thresholds={"NO3": 25.0}))
    net = sorted(nets)[0]
    assert mine.loc[net, "chem"] <= official.loc[net, "chem"] - 20 + 1e-6


def test_severity_multiplies_the_penalty_of_one_group_only():
    """Synthetic network: one pesticide at the limit (penalty 20) and nitrates at the limit (penalty 20)."""
    micro = pd.DataFrame([{"cdreseau": "U1", "n_bact": 24, "n_bact_nc": 0, "n_chem_nc": 0}])
    fam = pd.DataFrame([{"cdreseau": "U1", "family": "chem", "subfamily": sf, "n_samples": 12, "n_params": 1,
                         "n_exceed": 0} for sf in ("pesticides", "nitrates")])
    rows = [{"cdreseau": "U1", "code": code, "family": "chem", "subfamily": sf, "win": "36m", "n": 5,
             "n_detected": 5, "max_value": thr, "date_max": "2026-01-01", "mean": thr, "n_exceed": 0,
             "max_ratio": 1.0, "threshold": thr, "threshold_kind": "limit", "unit": "µg/L"}
            for code, sf, thr in (("ATRZ", "pesticides", 0.1), ("NO3", "nitrates", 50.0))]
    links = pd.DataFrame({"insee": ["00001"], "cdreseau": ["U1"]})
    p = C.prepare(micro, fam, pd.DataFrame(rows), None, links)
    base = C.recompute(p, C.Personal()).loc["U1", "chem"]
    assert base == pytest.approx(100 - 20 - 0.25 * 20)
    double = C.recompute(p, C.Personal(severity={"pesticides": 2.0})).loc["U1", "chem"]
    assert double == pytest.approx(100 - 40 - 0.25 * 20)
    # halving the nitrate threshold: ratio 2 -> penalty 80, the pesticide becomes the "other"
    strict = C.recompute(p, C.Personal(thresholds={"NO3": 25.0})).loc["U1", "chem"]
    assert strict == pytest.approx(100 - 80 - 0.25 * 20)
    # town score = network score
    town = C.commune_recompute(p, C.recompute(p, C.Personal()))
    assert town.loc["00001", "score"] == pytest.approx(C.recompute(p, C.Personal()).loc["U1", "score"])


def test_weights_change_global_score_only(prepared, official):
    mine = C.recompute(prepared, C.Personal(weights=(1.0, 0.0, 0.0)))
    both = mine.dropna(subset=["micro"])
    assert np.allclose(both["score"], both["micro"])
    assert np.allclose(mine["chem"].fillna(-1), official["chem"].fillna(-1))


def test_recompute_is_fast_enough_for_a_slider(prepared):
    import time
    t0 = time.perf_counter()
    C.recompute(prepared, C.Personal(weights=(0.2, 0.5, 0.3), severity={"metals": 3.0}))
    assert time.perf_counter() - t0 < 2.0


def test_defaults_come_from_config():
    assert C.Personal().weights == tuple(config.WEIGHTS[k] for k in S.FAMILIES)
    assert C.Personal().micro_k == config.MICRO_K
    assert config.MICRO_K in C.MICRO_K_CHOICES and 1.0 in C.SEVERITY_CHOICES

"""Integrity of the committed tables in data/processed/ (runs from a clean clone, no raw data needed)."""
import json

import pandas as pd
import pytest

import config
from utils.io import read_processed

TABLES_KEYS = {
    "params_catalog": ["code"],
    "national_year": ["annee"],
    "national_month": ["annee", "month"],
    "dept_year": ["annee", "dep"],
    "udi_year": ["annee", "cdreseau"],
    "dim_udi": ["cdreseau"],
    "bridge_commune_udi": ["annee", "insee", "cdreseau"],
    "commune_year": ["annee", "insee"],
    "param_year": ["annee", "code"],
    "udi_family_year": ["annee", "cdreseau", "family", "subfamily"],
    "udi_param_year": ["annee", "cdreseau", "code"],
    "udi_micro_window": ["cdreseau"],
    "udi_family_window": ["cdreseau", "family", "subfamily"],
    "udi_param_window": ["cdreseau", "code"],
    "dim_communes": ["insee"],
    "dim_departements": ["dep"],
    "dq_checks": ["check", "year"],
    "dq_conformity_check": ["annee"],
}


@pytest.mark.parametrize("name, keys", TABLES_KEYS.items())
def test_table_exists_with_unique_key(name, keys):
    df = read_processed(name)
    assert len(df) > 0
    assert not df.duplicated(keys).any(), f"{name}: duplicated key {keys}"


def test_all_years_present():
    ny = read_processed("national_year")
    assert ny["annee"].tolist() == config.YEARS


def test_conformity_counts_are_consistent():
    ny = read_processed("national_year")
    assert (ny["n_bact_nc"] <= ny["n_bact"]).all()
    assert (ny["n_chem_nc"] + ny["n_chem_derog"] <= ny["n_chem"]).all()
    assert (ny["n_bact"] <= ny["n_samples"]).all()


def test_department_totals_match_national():
    ny = read_processed("national_year").set_index("annee")
    dy = read_processed("dept_year").groupby("annee")[["n_samples", "n_bact_nc", "n_chem_nc"]].sum()
    pd.testing.assert_frame_equal(dy, ny[["n_samples", "n_bact_nc", "n_chem_nc"]], check_dtype=False, check_index_type=False)


def test_every_family_known():
    cat = read_processed("params_catalog")
    assert set(cat["family"]) <= {"micro", "chem", "comfort", "info"}
    nonrel = cat[cat["code"].isin(config.NON_RELEVANT_METABOLITES)]
    assert (nonrel["family"] == "comfort").all()


def test_automatic_checks_all_passed():
    dq = read_processed("dq_checks")
    failed = dq[~dq["ok"]]
    assert failed.empty, failed.to_string()


def test_processed_size_budget():
    total = sum(f.stat().st_size for f in config.PROCESSED.iterdir()) / 1e6
    assert total < 150
    for f in config.PROCESSED.iterdir():
        assert f.stat().st_size / 1e6 < 50, f.name


def test_source_manifest():
    m = json.loads((config.PROCESSED / "source_manifest.json").read_text(encoding="utf-8"))
    assert [f["file"] for f in m["files"]] == [f"dis-{y}.zip" for y in config.YEARS]

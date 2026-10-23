# Integrity and consistency tests for committed processed Parquet tables.
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
    "udi_param_p95": ["cdreseau", "code"],
    "udi_scores": ["cdreseau"],
    "commune_scores": ["insee"],
    "score_sensitivity": ["variant"],
    "dept_family_year": ["annee", "dep", "variable"],
    "dim_communes": ["insee"],
    "dim_departements": ["dep"],
    "dq_checks": ["check", "year"],
    "dq_conformity_check": ["annee"],
}


@pytest.mark.parametrize("name, keys", TABLES_KEYS.items())
def test_table_exists_with_unique_key(name, keys):
    """Verify that each processed Parquet table exists and possesses unique primary keys."""
    df = read_processed(name)
    assert len(df) > 0
    assert not df.duplicated(keys).any(), f"{name}: duplicated key {keys}"


def test_all_years_present():
    """Verify that national annual table contains all study years (2016-2026)."""
    ny = read_processed("national_year")
    assert ny["annee"].tolist() == config.YEARS


def test_conformity_counts_are_consistent():
    """Verify arithmetic consistency of national compliance counts."""
    ny = read_processed("national_year")
    assert (ny["n_bact_nc"] <= ny["n_bact"]).all()
    assert (ny["n_chem_nc"] + ny["n_chem_derog"] <= ny["n_chem"]).all()
    assert (ny["n_bact"] <= ny["n_samples"]).all()


def test_department_totals_match_national():
    """Verify that departmental sample and non-compliance sums equal national totals."""
    ny = read_processed("national_year").set_index("annee")
    dy = read_processed("dept_year").groupby("annee")[["n_samples", "n_bact_nc", "n_chem_nc"]].sum()
    pd.testing.assert_frame_equal(dy, ny[["n_samples", "n_bact_nc", "n_chem_nc"]], check_dtype=False, check_index_type=False)


def test_every_family_known():
    """Verify that all parameter codes in catalog map to known classification families."""
    cat = read_processed("params_catalog")
    assert set(cat["family"]) <= {"micro", "chem", "comfort", "info"}
    nonrel = cat[cat["code"].isin(config.NON_RELEVANT_METABOLITES)]
    assert (nonrel["family"] == "comfort").all()


def test_automatic_checks_all_passed():
    """Verify that all automated data quality assertions in dq_checks passed successfully."""
    dq = read_processed("dq_checks")
    failed = dq[~dq["ok"]]
    assert failed.empty, failed.to_string()


def test_processed_size_budget():
    """Verify that committed data/processed tables stay within overall file size budget."""
    total = sum(f.stat().st_size for f in config.PROCESSED.iterdir()) / 1e6
    assert total < 150
    for f in config.PROCESSED.iterdir():
        assert f.stat().st_size / 1e6 < 50, f.name


def test_source_manifest():
    """Verify structure and metadata integrity of source_manifest.json."""
    m = json.loads((config.PROCESSED / "source_manifest.json").read_text(encoding="utf-8"))
    assert [f["file"] for f in m["files"]] == [f"dis-{y}.zip" for y in config.YEARS]


def test_build_processed_zip_valid_and_complete():
    """Verify that build_processed_zip archive contains all processed tables and valid metadata."""
    import zipfile
    from utils.io import build_processed_zip, generate_data_readme, get_processed_data_size_mb

    assert get_processed_data_size_mb() > 40
    buf = build_processed_zip()
    assert buf.getbuffer().nbytes > 40 * 1024 * 1024

    with zipfile.ZipFile(buf, "r") as zf:
        assert zf.testzip() is None
        names = set(zf.namelist())

        # Check every file in data/processed/ is included
        for f in config.PROCESSED.glob("*"):
            if f.is_file():
                assert f"data/processed/{f.name}" in names, f"Missing {f.name} in export zip"

        # Check documentation files
        assert "docs/data_dictionary.md" in names
        assert "DATASET.md" in names
        assert "DATA_README.txt" in names

        # Check no raw or interim files are included
        assert not any("data/raw" in name or "data/interim" in name for name in names)

        # Check DATA_README.txt contents
        readme = zf.read("DATA_README.txt").decode("utf-8")
        assert config.DATASET_PAGE in readme
        assert config.DATASET_UPDATED in readme
        assert "Licence Ouverte" in readme
        assert "DERIVED" in readme
        assert "make data" in readme

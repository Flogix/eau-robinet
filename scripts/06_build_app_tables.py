"""06 — Small tables shaped for the app's map and trend charts (pandas only, a few seconds).

dept_family_year: department × year × variable -> networks measured / networks with at least one exceedance.
  bact_official, chem_official  official conformity of the samples (plvconformitebacterio / plvconformitechimique)
  nitrates, pesticides, pfas, metals, disinfection_byproducts, comfort
                                recomputed exceedances (value above the threshold written on the result row)
A network is counted in the department of its code (first 3 characters), so department and national totals never
count a network twice.

Usage: python scripts/06_build_app_tables.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config  # noqa: E402
from utils.io import dep_of_network, read_processed  # noqa: E402

SUBFAMILIES = ["nitrates", "pesticides", "pfas", "metals", "disinfection_byproducts"]


def main() -> int:
    uy = read_processed("udi_year")
    rows = []
    for var, n_col, nc_col in (("bact_official", "n_bact", "n_bact_nc"), ("chem_official", "n_chem", "n_chem_nc")):
        d = uy[uy[n_col] > 0].assign(variable=var, exceed=lambda x: x[nc_col] > 0)
        rows.append(d[["annee", "cdreseau", "variable", "exceed"]])
    uf = pd.read_parquet(config.PROCESSED / "udi_family_year.parquet",
                         columns=["annee", "cdreseau", "family", "subfamily", "n_exceed"])
    sub = uf[uf["subfamily"].isin(SUBFAMILIES)].rename(columns={"subfamily": "variable"})
    sub = sub.groupby(["annee", "cdreseau", "variable"], as_index=False)["n_exceed"].sum()
    com = uf[uf["family"] == "comfort"].groupby(["annee", "cdreseau"], as_index=False)["n_exceed"].sum()
    for d in (sub, com.assign(variable="comfort")):
        rows.append(d.assign(exceed=d["n_exceed"] > 0)[["annee", "cdreseau", "variable", "exceed"]])
    allr = pd.concat(rows, ignore_index=True)
    allr["dep"] = dep_of_network(allr["cdreseau"])
    out = (allr.groupby(["annee", "dep", "variable"], as_index=False)
           .agg(n_networks=("cdreseau", "size"), n_networks_exceed=("exceed", "sum")))
    out["annee"] = out["annee"].astype("int16")
    out = out.sort_values(["variable", "annee", "dep"]).reset_index(drop=True)
    out.to_parquet(config.PROCESSED / "dept_family_year.parquet", index=False)
    print(f"dept_family_year: {len(out):,} rows, variables {sorted(out['variable'].unique())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""04: Reference tables: communes (population, centre, department, region), typologies, department contours.

Downloads (cached in data/raw/ref/, never overwritten):
  * geo.api.gouv.fr (API Découpage administratif): current communes with population and centre,
    delegated/associated communes (to map old codes to their current commune), departments, regions;
  * Etalab administrative contours 2025, departments simplified at 1 km (GeoJSON);
  * INSEE density grid (geography at 01/01/2026): urban / intermediate / rural;
  * Cerema: communes subject to the Mountain Act (loi Montagne), geography 2019.
The national list of "loi Littoral" communes is no longer downloadable (dead link): documented fallback
(docs/sources.md, source 16) -> "Mediterranean coast" = communes of the coastal Mediterranean departments
(06, 11, 13, 30, 34, 66, 83, 2A, 2B) that are not classified as mountain.

Outputs (data/processed/): dim_communes.parquet, dim_departements.parquet, departements.geojson
Usage: python scripts/04_referentiels.py
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config  # noqa: E402
from utils.io import connect_duckdb  # noqa: E402

SOURCES = {
    "geo_communes.json": "https://geo.api.gouv.fr/communes?fields=code,nom,codeDepartement,codeRegion,population,centre&format=json",
    "geo_communes_associees_deleguees.json": "https://geo.api.gouv.fr/communes_associees_deleguees?fields=code,nom,chefLieu,type",
    "geo_departements.json": "https://geo.api.gouv.fr/departements?fields=code,nom,codeRegion",
    "geo_regions.json": "https://geo.api.gouv.fr/regions?fields=code,nom",
    "departements-1000m.geojson": "https://etalab-datasets.geo.data.gouv.fr/contours-administratifs/2025/geojson/departements-1000m.geojson",
    "insee_grille_densite_2026.xlsx": "https://www.insee.fr/fr/statistiques/fichier/8571524/fichier_diffusion_2026.xlsx",
    "loi_montagne_communes_2019.csv": "https://static.data.gouv.fr/resources/application-des-dispositions-durbanisme-de-la-loi-montagne-en-france-metropolitaine/20241112-091136/l-commune-loimontagne85-000-2019-.csv",
}
MEDITERRANEAN_DEPTS = {"06", "11", "13", "30", "34", "66", "83", "2A", "2B"}


def looks_valid(name: str, content: bytes) -> bool:
    """Content check (an HTML error/redirect page must not be cached as data)."""
    if name.endswith((".json", ".geojson")):
        try:
            json.loads(content)
            return True
        except ValueError:
            return False
    if name.endswith(".xlsx"):
        return content[:2] == b"PK"
    if name.endswith(".csv"):
        return b"insee" in content[:300].lower()
    return True


def fetch(name: str) -> Path:
    path = config.RAW_REF / name
    if path.exists():
        if looks_valid(name, path.read_bytes()):
            return path
        # never delete or overwrite raw files: stop and let a human look at it
        raise RuntimeError(f"{path} exists but is not valid data; please check it by hand")
    print(f"[download] {name}", flush=True)
    r = requests.get(SOURCES[name], timeout=120)
    r.raise_for_status()
    if not looks_valid(name, r.content):
        raise RuntimeError(f"{name}: downloaded content is not valid data ({len(r.content)} bytes)")
    path.write_bytes(r.content)
    return path


def dept_of(insee: str) -> str:
    return insee[:3] if insee.startswith("97") else insee[:2]


def main() -> int:
    config.RAW_REF.mkdir(parents=True, exist_ok=True)
    config.PROCESSED.mkdir(parents=True, exist_ok=True)
    paths = {name: fetch(name) for name in SOURCES}

    # --- geo.api ----------------------------------------------------------------------------
    geo = pd.DataFrame(json.loads(paths["geo_communes.json"].read_text(encoding="utf-8")))
    geo["lon"] = geo["centre"].map(lambda c: c["coordinates"][0] if isinstance(c, dict) else None)
    geo["lat"] = geo["centre"].map(lambda c: c["coordinates"][1] if isinstance(c, dict) else None)
    geo = geo.drop(columns="centre").rename(columns={"code": "insee", "nom": "nom_geo"})
    old = pd.DataFrame(json.loads(paths["geo_communes_associees_deleguees.json"].read_text(encoding="utf-8")))
    old_to_current = dict(zip(old["code"], old["chefLieu"]))
    depts = pd.DataFrame(json.loads(paths["geo_departements.json"].read_text(encoding="utf-8")))
    regions = pd.DataFrame(json.loads(paths["geo_regions.json"].read_text(encoding="utf-8")))
    depts = depts.rename(columns={"code": "dep", "nom": "dep_nom", "codeRegion": "reg"}).merge(
        regions.rename(columns={"code": "reg", "nom": "reg_nom"}), on="reg", how="left")

    # --- Typologies -------------------------------------------------------------------------
    grid = pd.read_excel(paths["insee_grille_densite_2026.xlsx"], sheet_name=0, header=4, dtype={"CODGEO": str})
    grid = grid[["CODGEO", "DENS", "LIBDENS", "DENS7", "LIBDENS7"]].rename(columns={
        "CODGEO": "insee", "DENS": "density3", "LIBDENS": "density3_label", "DENS7": "density7", "LIBDENS7": "density7_label"})
    mountain = pd.read_csv(paths["loi_montagne_communes_2019.csv"], dtype=str, encoding="utf-8")
    mountain = mountain[["insee_2019", "classement_2019"]].rename(columns={"insee_2019": "insee_2019_code"})
    # 2019 codes merged since then -> their current commune (a commune is "mountain" if one of its parts is)
    mountain["insee"] = mountain["insee_2019_code"].map(lambda c: old_to_current.get(c, c))
    mountain_set = set(mountain["insee"])

    # --- Communes present in the water dataset (all years) -------------------------------------
    con = connect_duckdb()
    ds = con.execute(f"""
        SELECT inseecommune AS insee, arg_max(nomcommune, annee) AS nom_dataset,
               min(annee) AS first_year, max(annee) AS last_year
        FROM read_parquet('{(config.CLEAN / "com_udi").as_posix()}/*.parquet') GROUP BY 1""").df()

    dim = ds.copy()
    dim["insee_current"] = dim["insee"].where(dim["insee"].isin(geo["insee"]), dim["insee"].map(old_to_current))
    dim = dim.merge(geo, left_on="insee_current", right_on="insee", how="left", suffixes=("", "_g")).drop(columns="insee_g")
    dim["dep"] = dim["insee"].map(dept_of)
    dim = dim.merge(depts[["dep", "dep_nom", "reg", "reg_nom"]], on="dep", how="left")
    dim = dim.merge(grid, left_on="insee_current", right_on="insee", how="left", suffixes=("", "_grid")).drop(columns="insee_grid")
    dim["is_current"] = dim["insee"].isin(geo["insee"])
    # an old (merged) code must not carry the population of its current commune: no double counting
    dim.loc[~dim["is_current"], "population"] = None
    dim["mountain"] = dim["insee_current"].isin(mountain_set)
    dim["mediterranean_coast"] = dim["dep"].isin(MEDITERRANEAN_DEPTS) & ~dim["mountain"]
    dim["territory_group"] = "Other"
    dim.loc[dim["mountain"], "territory_group"] = "Mountain (loi Montagne)"
    dim.loc[dim["mediterranean_coast"], "territory_group"] = "Mediterranean coastal departments"
    dim["nom"] = dim["nom_geo"].fillna(dim["nom_dataset"].str.title())
    cols = ["insee", "nom", "nom_dataset", "dep", "dep_nom", "reg", "reg_nom", "population", "lat", "lon",
            "insee_current", "is_current", "first_year", "last_year", "density3", "density3_label",
            "density7", "density7_label", "mountain", "mediterranean_coast", "territory_group"]
    dim = dim[cols].sort_values("insee").reset_index(drop=True)
    dim.to_parquet(config.PROCESSED / "dim_communes.parquet", index=False)
    depts.to_parquet(config.PROCESSED / "dim_departements.parquet", index=False)
    shutil.copyfile(paths["departements-1000m.geojson"], config.PROCESSED / "departements.geojson")

    # --- Report -----------------------------------------------------------------------------
    latest = dim[dim["last_year"] == config.YEARS[-1]]
    report = {
        "communes_in_dataset_all_years": len(dim),
        "communes_in_2026": len(latest),
        "codes_not_in_current_geography": int((~dim["is_current"]).sum()),
        "codes_mapped_to_current_commune": int((~dim["is_current"] & dim["insee_current"].notna()).sum()),
        "2026_communes_without_population": int(latest["population"].isna().sum()),
        "2026_communes_without_density": int(latest["density3"].isna().sum()),
        "2026_mountain_communes": int(latest["mountain"].sum()),
        "2026_mediterranean_coast_communes": int(latest["mediterranean_coast"].sum()),
        "mountain_2019_codes": len(mountain), "mountain_codes_found_in_dataset": int(dim["mountain"].sum()),
    }
    (config.INTERIM / "referentiels_report.json").write_text(json.dumps(report, indent=1))
    print(json.dumps(report, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

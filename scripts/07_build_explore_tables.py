"""07: Small tables for the page "Explore the data" (everything heavy is computed here, the page only reads).

explore_volume        per year: size of the zip, of each text file in it and of its raw Parquet copy, number of
                      parameter codes (all, and those with a text result such as odour or aspect), rows of PLV / RESULT / COM_UDI, distinct samples,
                      networks and towns (needs data/raw/dis/*.zip, only listed, and data/interim/raw_parquet/)
explore_fanout        2025: number of networks each sample is attached to (a sample taken upstream is copied
                      for each network it feeds)
explore_param_changes parameter codes that appeared or disappeared between the first and the last complete year, by group
                      (pesticides and metabolites, PFAS, cyanobacteria, other): rules on the catalogue, see param_group()
explore_links         last year of the town-network links: towns by number of networks, networks by number of towns
explore_examples      the 10 example rows per raw file of docs/data_dictionary.md section 12 (already public in the
                      repository, drawn with seed 42 during phase 0) and 6 rows of the processed table udi_year
                      drawn with config.SEED: no new raw row is added to the repository
explore_lq            2025: share of results below the quantification limit, by group of parameters
explore_top_params    the 15 parameters with the most results, 2016 to 2026
explore_values        2025: distribution of the yearly mean of each network for 8 key parameters (bins + quantiles)
explore_dept          one row per department of mainland France: 9 indicators for the correlation matrix
explore_spearman      Spearman rank correlation between every pair of these indicators (and the number of departments)

Usage: python scripts/07_build_explore_tables.py   (a few seconds; the volume part takes about 20 s)
"""
from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config  # noqa: E402
from utils.io import connect_duckdb, dep_of_network, read_processed  # noqa: E402

OUT = config.PROCESSED
RAW_PARQUET = config.INTERIM / "raw_parquet"
YEAR = config.COMPLETE_YEARS[-1]                        # last complete year
PERIOD = (config.COMPLETE_YEARS[0], config.COMPLETE_YEARS[-1])
VALUE_PARAMS = {"NO3": 50.0, "TH": None, "PB": 10.0, "AS": 10.0, "PESTOT": 0.5, "SPFAS": 0.1, "CL": 250.0, "SO4": 250.0}
SMALL_NETWORK = 12                                      # bacteriological samples a year, as in H1
MIN_TOWNS = 5                                           # scored towns needed for a department median (as on the map)


def save(d: pd.DataFrame, name: str) -> None:
    d.to_parquet(OUT / f"{name}.parquet", index=False)
    print(f"{name}: {len(d):,} rows")


# --- volume (raw files) ---------------------------------------------------------------------------------------------
def volume() -> None:
    zips = sorted((config.RAW / "dis").glob("dis-20??.zip"))
    if not zips or not RAW_PARQUET.exists():
        print("explore_volume, explore_fanout: raw files not found, existing tables kept")
        return
    con = connect_duckdb()
    rows = []
    for z in zips:
        year = int(z.stem[-4:])
        with zipfile.ZipFile(z) as zf:        # only the listing is read, nothing is extracted
            sizes = {re.sub(r"^DIS_|_\d{4}\.txt$", "", i.filename.split("/")[-1]): i.file_size for i in zf.infolist()}
        p = lambda kind: (RAW_PARQUET / kind / f"{kind.lower()}_{year}.parquet").as_posix()  # noqa: E731
        plv = con.sql(f"""SELECT count(*) AS plv_rows, count(DISTINCT referenceprel) AS samples,
                          count(DISTINCT cdreseau) AS networks FROM read_parquet('{p("PLV")}')""").fetchone()
        res, n_params, n_text = con.sql(f"""SELECT count(*), count(DISTINCT cdparametresiseeaux),
                count(DISTINCT cdparametresiseeaux) FILTER (WHERE qualitparam = 'O')
                FROM read_parquet('{p('RESULT')}')""").fetchone()
        cu = con.sql(f"""SELECT count(*), count(DISTINCT inseecommune), count(DISTINCT cdreseau)
                         FROM read_parquet('{p("COM_UDI")}')""").fetchone()
        rows.append({"annee": year, "zip_mb": z.stat().st_size / 1e6,
                     "plv_txt_mb": sizes.get("PLV", 0) / 1e6, "result_txt_mb": sizes.get("RESULT", 0) / 1e6,
                     "com_udi_txt_mb": sizes.get("COM_UDI", 0) / 1e6,
                     "plv_rows": plv[0], "samples": plv[1], "networks_sampled": plv[2], "result_rows": res,
                     "com_udi_rows": cu[0], "communes": cu[1], "networks_linked": cu[2],
                     "n_params": n_params, "n_params_text": n_text,
                     "raw_parquet_mb": sum(Path(p(k)).stat().st_size for k in ("PLV", "RESULT", "COM_UDI")) / 1e6})
    save(pd.DataFrame(rows), "explore_volume")
    fan = con.sql(f"""SELECT n_networks, count(*) AS n_samples FROM (
                        SELECT referenceprel, count(DISTINCT cdreseau) AS n_networks
                        FROM read_parquet('{(RAW_PARQUET / "PLV" / f"plv_{YEAR}.parquet").as_posix()}') GROUP BY 1)
                      GROUP BY 1 ORDER BY 1""").df()
    save(fan.astype({"n_networks": "int32", "n_samples": "int64"}), "explore_fanout")


# --- parameters that appeared or disappeared ------------------------------------------------------------------------
def param_group(row) -> str:
    """Pesticides and their metabolites (with or without a limit: catalogue subfamily, or a metabolite code of the
    usual pesticide families), PFAS (subfamily or 'perfluoro' in the name), cyanobacteria (counts of cells or volumes),
    other."""
    label, unit, sub = str(row["label"]).lower(), str(row["unit"]), str(row["subfamily"])
    if sub in ("pesticides", "pesticide_metabolite_non_relevant") or any(
            k in label for k in (" esa", " oxa", "cga ", "ampa", "desméthyl", "desethyl", "déséthyl", "desphényl")):
        return "pesticides"
    if sub == "pfas" or "perfluoro" in label or "pfas" in label:
        return "pfas"
    if unit in ("mm3/L", "n(cellules)/mL") or "cyano" in label:
        return "cyanobacteria"
    return "other"


def param_changes() -> None:
    if not RAW_PARQUET.exists():
        print("explore_param_changes: raw files not found, existing table kept")
        return
    con = connect_duckdb()
    y0, y1 = PERIOD
    codes = {y: set(con.sql(f"""SELECT DISTINCT cdparametresiseeaux FROM
                read_parquet('{(RAW_PARQUET / "RESULT" / f"result_{y}.parquet").as_posix()}')""").df().iloc[:, 0])
             for y in (y0, y1)}
    cat = read_processed("params_catalog").set_index("code")
    rows = []
    for change, s in (("new", codes[y1] - codes[y0]), ("gone", codes[y0] - codes[y1])):
        d = cat.reindex(sorted(s)).reset_index()
        d["group"] = d.apply(param_group, axis=1)
        for g, n in d.groupby("group").size().items():
            rows.append({"change": change, "group": g, "n": int(n), "y0": y0, "y1": y1})
    save(pd.DataFrame(rows), "explore_param_changes")


# --- town <-> network links ---------------------------------------------------------------------------------------
def links() -> None:
    b = read_processed("bridge_commune_udi")
    last = int(b["annee"].max())
    b = b.loc[b["annee"] == last, ["insee", "cdreseau"]].drop_duplicates()
    per_town = b.groupby("insee").size().value_counts().rename_axis("k").reset_index(name="n").assign(side="town")
    per_net = b.groupby("cdreseau").size().value_counts().rename_axis("k").reset_index(name="n").assign(side="network")
    out = pd.concat([per_town, per_net], ignore_index=True).assign(annee=last).sort_values(["side", "k"])
    save(out.astype({"k": "int32", "n": "int32"}), "explore_links")


# --- example rows -------------------------------------------------------------------------------------------------
def examples() -> None:
    md = (config.ROOT / "docs" / "data_dictionary.md").read_text(encoding="utf-8")
    section = md.split("## 12.", 1)[1]
    blocks = re.findall(r"\*\*(PLV|RESULT|COM_UDI)\*\* \((\d{4})\)\s+```csv\n(.*?)```", section, flags=re.S)
    out = {}
    for kind, year, csv in blocks:
        from io import StringIO
        d = pd.read_csv(StringIO(csv), dtype=str, keep_default_na=False)
        out[kind] = {"year": int(year), "columns": list(d.columns), "rows": d.values.tolist()}
    assert set(out) == {"PLV", "RESULT", "COM_UDI"}, f"example blocks not found in the data dictionary: {set(out)}"
    uy = read_processed("udi_year")
    uy = uy[uy["annee"] == YEAR].sample(6, random_state=config.SEED).sort_values("cdreseau")
    out["udi_year"] = {"year": YEAR, "columns": list(uy.columns),
                       "rows": uy.astype(object).where(uy.notna(), "").astype(str).values.tolist()}
    (OUT / "explore_examples.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8",
                                               newline="\n")
    print("explore_examples.json:", {k: len(v["rows"]) for k, v in out.items()})


# --- distributions ------------------------------------------------------------------------------------------------
def distributions() -> None:
    py = read_processed("param_year")
    p = py[(py["annee"] == YEAR) & (py["family"] != "info")]
    g = p.groupby(["family", "subfamily"], as_index=False)[["n_samples", "n_detected"]].sum()
    g["share_not_detected"] = 1 - g["n_detected"] / g["n_samples"]
    g["n_params"] = p.groupby(["family", "subfamily"]).size().values
    save(g[g["n_samples"] >= 1000].sort_values("share_not_detected", ascending=False), "explore_lq")

    cat = read_processed("params_catalog")
    top = cat.nlargest(15, "n_results")[["code", "label", "family", "subfamily", "unit", "n_results", "n_detected",
                                         "n_years"]]
    save(top, "explore_top_params")

    upy = pd.read_parquet(OUT / "udi_param_year.parquet", filters=[("annee", "==", YEAR)],
                          columns=["cdreseau", "code", "n", "mean"])
    rows = []
    for code, thr in VALUE_PARAMS.items():
        v = upy.loc[upy["code"] == code, "mean"].dropna().astype(float)
        q = v.quantile([0.05, 0.25, 0.5, 0.75, 0.95])
        top_edge = max(float(v.quantile(0.99)), (thr or 0) * 1.2)
        bins = np.linspace(0, top_edge, 31)
        counts, _ = np.histogram(v.clip(upper=top_edge), bins=bins)
        for lo, hi, c in zip(bins[:-1], bins[1:], counts):
            rows.append({"code": code, "lo": lo, "hi": hi, "n_networks": int(c), "threshold": thr,
                         "n_total": len(v), "p05": q[0.05], "p25": q[0.25], "p50": q[0.5], "p75": q[0.75],
                         "p95": q[0.95], "share_above": float((v > thr).mean()) if thr else None,
                         "share_zero": float((v == 0).mean())})
    save(pd.DataFrame(rows), "explore_values")


# --- department indicators and their rank correlations --------------------------------------------------------------
def polygon_area_km2(coords) -> float:
    """Area of a lon/lat ring on the sphere (equal-area sinusoidal projection around the ring's mean latitude)."""
    r = 6371.0088
    lon, lat = np.radians(np.asarray(coords)[:, 0]), np.radians(np.asarray(coords)[:, 1])
    x, y = r * lon * np.cos(lat), r * lat
    return abs(float(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))) / 2


def dept_area() -> pd.Series:
    geo = json.loads((OUT / "departements.geojson").read_text(encoding="utf-8"))
    out = {}
    for f in geo["features"]:
        g = f["geometry"]
        polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
        out[f["properties"]["code"]] = sum(polygon_area_km2(p[0]) - sum(polygon_area_km2(h) for h in p[1:])
                                           for p in polys)
    return pd.Series(out, name="area_km2")


def departments() -> None:
    dy = read_processed("dept_year")
    d = dy[dy["annee"].between(*PERIOD)].groupby("dep")[["n_bact", "n_bact_nc", "n_chem", "n_chem_nc"]].sum()
    ind = pd.DataFrame({"bact_rate": d["n_bact_nc"] / d["n_bact"], "chem_rate": d["n_chem_nc"] / d["n_chem"]})
    com = read_processed("dim_communes")
    com = com[com["is_current"]]
    sc = read_processed("commune_scores").merge(com[["insee", "dep"]], on="insee")
    g = sc.dropna(subset=["score"]).groupby("dep")["score"]
    ind["score_median"] = g.median().where(g.size() >= MIN_TOWNS)   # same rule as the map: no median of 1 to 4 towns
    uy = read_processed("udi_year")
    u = uy[uy["annee"].between(*PERIOD) & (uy["n_bact"] > 0)]
    ind["small_share"] = (u["n_bact"] < SMALL_NETWORK).groupby(dep_of_network(u["cdreseau"].astype(str))).mean()
    upy = pd.read_parquet(OUT / "udi_param_year.parquet", filters=[("annee", "==", YEAR)],
                          columns=["cdreseau", "code", "mean"])
    for code, col in (("TH", "hardness"), ("NO3", "nitrates")):
        v = upy[upy["code"] == code]
        ind[col] = v.groupby(dep_of_network(v["cdreseau"].astype(str)))["mean"].median()
    ind["population"] = com.groupby("dep")["population"].sum()
    ind["density"] = ind["population"] / dept_area().reindex(ind.index)
    ind = ind[~ind.index.str.startswith("97")]
    ind.index.name = "dep"
    ind = ind.reset_index()
    save(ind, "explore_dept")
    cols = [c for c in ind.columns if c != "dep"]
    rows = []
    for x in cols:
        for y in cols:
            both = ind[[x] if x == y else [x, y]].dropna()   # pairwise: a department missing one indicator is left out
            rows.append({"x": x, "y": y, "rho": spearman(both[x], both[y]), "n": len(both)})
    save(pd.DataFrame(rows), "explore_spearman")


def spearman(a: pd.Series, b: pd.Series) -> float:
    """Spearman rank correlation = Pearson correlation of the ranks (average ranks for ties); no scipy needed."""
    return float(a.rank().corr(b.rank()))


def main() -> int:
    volume()
    param_changes()
    links()
    examples()
    distributions()
    departments()
    return 0


if __name__ == "__main__":
    sys.exit(main())

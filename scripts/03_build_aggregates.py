"""03: Small tables for the app (data/processed/) + automatic data-quality checks.

Steps
  1. parameter catalogue (labels, units, typical thresholds, family) -> params_catalog
  2. per year, join clean results with samples (network, date) and attach the applicable threshold
     (data/interim/joined/): this is the only place where "exceedance" is defined:
       limit       the quality limit written on the row (value > limit)
       indicative  0.9 µg/L for metabolites classified non-relevant by Anses, when the row has no limit
       reference   the quality reference written on the row (value > max, or < min for intervals like pH)
  3. aggregates: national/department/commune/network × year, parameter × year, network × family × year,
     key parameters × network × year, "current situation" windows (12 / 36 months to 31/08/2026)
  4. data quality: missing values, duplicates, integrity, validity, coverage, official vs recomputed
     conformity (and the explanation of the chemistry gap), metabolite rule checks
  5. automatic checks (row counts, unique keys, no join explosion, file sizes) -> fail loudly

Usage: python scripts/03_build_aggregates.py [--rebuild-joined]
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config  # noqa: E402
from utils.io import connect_duckdb  # noqa: E402
from utils.prep import MICRO_UNITS, classify_parameter, register_macros  # noqa: E402

P = config.PROCESSED
JOINED = config.INTERIM / "joined"
CLEAN = config.CLEAN.as_posix()
RAW = config.RAW_PARQUET.as_posix()
END = config.DATA_END_DATE
START_12 = date(END.year - 1, END.month + 1, 1) if END.month < 12 else date(END.year, 1, 1)   # 2025-09-01
START_36 = date(START_12.year - 2, START_12.month, 1)                                          # 2023-09-01
KEY_PARAMS = ["ECOLI", "STRF", "CTF", "NO3", "NO2", "PESTOT", "SPFAS", "AS", "PB", "CLVYL", "THM4", "BRATE",
              "TURBNFU", "FET", "MN", "ALTMICR", "COT", "NH4", "TH", "CA", "MG", "CL", "SO4",
              "FMG", "MTCESA", "MTCNOA", "471811R", "CLDZ_D", "CLDZ_MD", "CLTHALS", "ATRZ", "ADET"]
MAX_FILE_MB, MAX_TOTAL_MB = 50, 150
CHECKS: list[dict] = []
STAMPS = config.INTERIM / "stamps"   # resumability: one stamp per output = hash of the query that built it
PREP_SOURCE = (Path(config.ROOT) / "utils" / "prep.py").read_text(encoding="utf-8")


def _key(*parts) -> str:
    return hashlib.sha1("\x1f".join(map(str, parts)).encode("utf-8")).hexdigest()


def _newest(paths) -> float:
    return max((q.stat().st_mtime for q in paths if q.exists()), default=0.0)


def is_fresh(out: Path, key: str, inputs) -> bool:
    """True if `out` was built by the same query (stamp) after its inputs were last modified."""
    stamp = STAMPS / f"{out.parent.name}__{out.name}.txt"
    return (out.exists() and stamp.exists() and stamp.read_text() == key
            and out.stat().st_mtime >= _newest(inputs))


def write_stamp(out: Path, key: str) -> None:
    STAMPS.mkdir(parents=True, exist_ok=True)
    (STAMPS / f"{out.parent.name}__{out.name}.txt").write_text(key)


def all_inputs():
    return list(Path(config.CLEAN).glob("*/*.parquet")) + list(JOINED.glob("*.parquet")) + [P / "params_catalog.parquet"]


def sql_list(values) -> str:
    return ", ".join(f"'{v}'" for v in values)


def check(name: str, ok: bool, value, expected, year=None, detail: str = "") -> None:
    CHECKS.append({"check": name, "year": year, "value": str(value), "expected": str(expected),
                   "ok": bool(ok), "detail": detail})
    flag = "OK " if ok else "FAIL"
    print(f"  [{flag}] {name}{'' if year is None else f' ({year})'}: {value} (expected {expected}) {detail}")


def copy(con, sql: str, name: str, inputs=None) -> int:
    """Write a processed table, unless it is already up to date (same query, inputs unchanged)."""
    path = P / f"{name}.parquet"
    key = _key(sql, PREP_SOURCE)
    if not is_fresh(path, key, all_inputs() if inputs is None else inputs):
        con.execute(f"COPY ({sql}) TO '{path.as_posix()}' (FORMAT parquet, COMPRESSION zstd)")
        write_stamp(path, key)
        status = ""
    else:
        status = " (cache)"
    n = con.execute(f"SELECT count(*) FROM '{path.as_posix()}'").fetchone()[0]
    print(f"  {name}: {n:,} rows, {path.stat().st_size / 1e6:.1f} MB{status}", flush=True)
    return n


def copy_by_year(con, template: str, name: str, order: str) -> int:
    """Run `template` (which reads {J}) on one year of joined data at a time, then concatenate.
    Bounded memory: DISTINCT counts on 190 million rows do not spill to disk."""
    parts = build_parts(con, template, name)
    return copy(con, f"SELECT * FROM read_parquet('{parts.as_posix()}/*.parquet') ORDER BY {order}", name,
                inputs=list(parts.glob("*.parquet")))


def build_parts(con, template: str, name: str) -> Path:
    """One file per year in data/interim/parts/<name>/; a year already built with the same query is skipped."""
    parts = config.INTERIM / "parts" / name
    parts.mkdir(parents=True, exist_ok=True)
    for y in config.YEARS:
        joined = JOINED / f"joined_{y}.parquet"
        out = parts / f"{y}.parquet"
        key = _key(template, y, PREP_SOURCE)
        if is_fresh(out, key, [joined]):
            continue
        src = f"read_parquet('{joined.as_posix()}')"
        con.execute(f"COPY ({template.replace('{J}', src)}) TO '{out.as_posix()}' (FORMAT parquet)")
        write_stamp(out, key)
    return parts


# --- 1. Parameter catalogue ------------------------------------------------------------------
def build_catalog(con) -> pd.DataFrame:
    print("1. parameter catalogue", flush=True)
    out = P / "params_catalog.parquet"
    key = _key("catalog", PREP_SOURCE, sorted(config.NON_RELEVANT_METABOLITES), sorted(config.TWIN_CODES.items()))
    if is_fresh(out, key, list(Path(config.CLEAN).glob("result/*.parquet"))):
        cat = pd.read_parquet(out)
        print(f"  params_catalog: {len(cat):,} parameters (cache)")
        return cat
    labels = con.execute(f"""
        SELECT cdparametresiseeaux AS code, mode(libminparametre) AS label, mode(cdparametre) AS sandre,
               mode(casparam) AS cas
        FROM read_parquet('{RAW}/RESULT/*.parquet') GROUP BY 1""").df()
    stats = con.execute(f"""
        SELECT code, mode(unit_n) AS unit, count(lim_max) > 0 AS has_limit, mode(lim_max) AS limit_max,
               mode(lim_unit_n) AS limit_unit, count(ref_max) + count(ref_min) > 0 AS has_ref,
               mode(ref_min) AS ref_min, mode(ref_max) AS ref_max, mode(ref_unit_n) AS ref_unit,
               mode(qualit) AS qualit,
               count(value) AS n_results,
               count(*) FILTER (WHERE is_detected(status, value)) AS n_detected,
               min(annee) AS first_year, max(annee) AS last_year, count(DISTINCT annee) AS n_years
        FROM read_parquet('{CLEAN}/result/*.parquet') GROUP BY 1""").df()
    cat = stats.merge(labels, on="code", how="left")
    fam = cat.apply(lambda r: classify_parameter(
        r["code"], r["unit"], bool(r["has_limit"]), bool(r["has_ref"]),
        None if pd.isna(r["limit_max"]) else float(r["limit_max"]),
        None if pd.isna(r["limit_unit"]) else r["limit_unit"]), axis=1, result_type="expand")
    cat["family"], cat["subfamily"] = fam[0], fam[1]
    cat.loc[cat["qualit"] == "O", ["family", "subfamily"]] = ["info", "qualitative"]
    cat["code_merged"] = cat["code"].map(lambda c: config.TWIN_CODES.get(c, c))
    cat["non_relevant_metabolite"] = cat["code"].isin(config.NON_RELEVANT_METABOLITES)
    cat = cat.sort_values("n_results", ascending=False).reset_index(drop=True)
    cat.to_parquet(out, index=False)
    write_stamp(out, key)
    print(f"  params_catalog: {len(cat):,} parameters")
    print(cat.groupby(["family", "subfamily"]).size().to_string())
    return cat


# --- 2. Joined results × samples ----------------------------------------------------------------
def build_joined(con, rebuild: bool) -> None:
    print("2. results × samples with thresholds")
    JOINED.mkdir(parents=True, exist_ok=True)
    nonrel = sql_list(config.NON_RELEVANT_METABOLITES)
    micro_units = sql_list(MICRO_UNITS)
    for y in config.YEARS:
        out = JOINED / f"joined_{y}.parquet"
        src = Path(config.CLEAN) / "result" / f"result_{y}.parquet"
        plv = Path(config.CLEAN) / "plv" / f"plv_{y}.parquet"
        if not rebuild and out.exists() and out.stat().st_mtime > _newest([src, plv, P / "params_catalog.parquet"]):
            continue
        t0 = time.time()
        con.execute(f"""
            COPY (
              WITH r AS (
                SELECT r.*, c.family, c.subfamily, c.code_merged,
                       thr_kind(r.lim_max, r.code IN ({nonrel}), r.ref_min, r.ref_max) AS thr_kind
                FROM '{src.as_posix()}' r JOIN cat c USING (code)
                WHERE r.status <> 'qualitative'
              ), t AS (
                SELECT *,
                  CASE thr_kind WHEN 'limit' THEN lim_max WHEN 'indicative' THEN {config.NON_RELEVANT_INDICATIVE_UGL}
                                WHEN 'reference' THEN ref_max END AS thr_max,
                  CASE thr_kind WHEN 'reference' THEN ref_min END AS thr_min,
                  CASE thr_kind WHEN 'limit' THEN lim_unit_n WHEN 'indicative' THEN 'µg/L'
                                WHEN 'reference' THEN ref_unit_n END AS thr_unit,
                  is_detected(status, value) AS detected,
                  unit_n IN ({micro_units}) AS micro_unit
                FROM r
              )
              SELECT p.cdreseau, p.dateprel, p.cddept, p.upstream, t.*,
                is_exceed(status, value, thr_kind, thr_max, thr_min) AS exceed,
                CASE WHEN thr_max > 0 AND value IS NOT NULL THEN value / thr_max END AS ratio,
                thr_unit IS NULL OR thr_unit = unit_n AS unit_ok
              FROM t JOIN '{CLEAN}/plv/plv_{y}.parquet' p USING (referenceprel)
            ) TO '{out.as_posix()}' (FORMAT parquet, COMPRESSION zstd, ROW_GROUP_SIZE 500000)""")
        n = con.execute(f"SELECT count(*) FROM '{out.as_posix()}'").fetchone()[0]
        print(f"  joined_{y}: {n:,} rows ({time.time() - t0:.0f}s)")


# --- 3. Aggregates --------------------------------------------------------------------------------
def build_aggregates(con) -> None:
    print("3. aggregates")
    J = f"read_parquet('{JOINED.as_posix()}/*.parquet')"
    PLV = f"read_parquet('{CLEAN}/plv/*.parquet')"
    CU = f"read_parquet('{CLEAN}/com_udi/*.parquet')"
    # sample-level conformity (one row per sample and year; identical across the networks of a sample)
    con.execute(f"""CREATE OR REPLACE TEMP TABLE s AS
        SELECT annee, referenceprel, any_value(cddept) AS cddept, any_value(dateprel) AS dateprel,
               any_value(conf_bact) AS conf_bact, any_value(conf_chem) AS conf_chem,
               any_value(conf_ref_bact) AS conf_ref_bact, any_value(conf_ref_chem) AS conf_ref_chem,
               count(*) AS n_networks, bool_or(upstream) AS upstream
        FROM {PLV} GROUP BY 1, 2""")
    conf_cols = """
        count(*) AS n_samples,
        count(*) FILTER (WHERE conf_bact IN ('C', 'N')) AS n_bact,
        count(*) FILTER (WHERE conf_bact = 'N') AS n_bact_nc,
        count(*) FILTER (WHERE conf_chem IN ('C', 'N', 'D')) AS n_chem,
        count(*) FILTER (WHERE conf_chem = 'N') AS n_chem_nc,
        count(*) FILTER (WHERE conf_chem = 'D') AS n_chem_derog,
        count(*) FILTER (WHERE conf_ref_bact = 'N') AS n_ref_bact_nc,
        count(*) FILTER (WHERE conf_ref_chem = 'N') AS n_ref_chem_nc"""
    copy(con, f"SELECT annee, {conf_cols}, count(*) FILTER (WHERE upstream) AS n_upstream FROM s GROUP BY 1 ORDER BY 1", "national_year")
    copy(con, f"SELECT annee, month(dateprel)::TINYINT AS month, {conf_cols} FROM s GROUP BY 1, 2 ORDER BY 1, 2", "national_month")
    copy(con, f"""SELECT annee, CASE WHEN cddept LIKE '97%' THEN cddept WHEN cddept LIKE '0%' THEN substr(cddept, 2) ELSE cddept END AS dep,
                         {conf_cols} FROM s GROUP BY 1, 2 ORDER BY 1, 2""", "dept_year")

    # networks
    copy(con, f"""SELECT annee, cdreseau, {conf_cols},
                         count(*) FILTER (WHERE upstream) AS n_upstream
                  FROM {PLV} GROUP BY 1, 2 ORDER BY 1, 2""", "udi_year")
    copy(con, f"""SELECT cdreseau, arg_max(nomreseau, annee) AS nomreseau, max(annee) AS last_year,
                         count(DISTINCT inseecommune) FILTER (WHERE annee = {config.YEARS[-1]}) AS n_communes_last_year
                  FROM {CU} GROUP BY 1 ORDER BY 1""", "dim_udi")
    copy(con, f"""SELECT annee, inseecommune AS insee, cdreseau, count(*) AS n_districts,
                         string_agg(quartier, ' | ' ORDER BY quartier) FILTER (WHERE quartier <> '-') AS districts
                  FROM {CU} GROUP BY 1, 2, 3 ORDER BY 1, 2, 3""", "bridge_commune_udi")
    # communes: sum over the networks that serve them (a sample of a shared network counts for each commune)
    copy(con, f"""
        WITH b AS (SELECT DISTINCT annee, inseecommune AS insee, cdreseau FROM {CU}),
             u AS (SELECT annee, cdreseau, {conf_cols} FROM {PLV} GROUP BY 1, 2)
        SELECT b.annee, b.insee, count(*) AS n_udi, count(u.cdreseau) AS n_udi_sampled,
               coalesce(sum(n_samples), 0)::INT AS n_samples, coalesce(sum(n_bact), 0)::INT AS n_bact,
               coalesce(sum(n_bact_nc), 0)::INT AS n_bact_nc, coalesce(sum(n_chem), 0)::INT AS n_chem,
               coalesce(sum(n_chem_nc), 0)::INT AS n_chem_nc, coalesce(sum(n_chem_derog), 0)::INT AS n_chem_derog,
               coalesce(sum(n_ref_bact_nc), 0)::INT AS n_ref_bact_nc, coalesce(sum(n_ref_chem_nc), 0)::INT AS n_ref_chem_nc
        FROM b LEFT JOIN u USING (annee, cdreseau) GROUP BY 1, 2 ORDER BY 1, 2""", "commune_year")

    # parameters × year (national, one count per sample and parameter)
    copy_by_year(con, """
        SELECT annee, code, any_value(code_merged) AS code_merged, any_value(family) AS family,
               any_value(subfamily) AS subfamily,
               count(DISTINCT referenceprel) AS n_samples,
               count(DISTINCT referenceprel) FILTER (WHERE detected) AS n_detected,
               count(DISTINCT referenceprel) FILTER (WHERE exceed AND thr_kind = 'limit') AS n_exceed_limit,
               count(DISTINCT referenceprel) FILTER (WHERE exceed AND thr_kind = 'indicative') AS n_exceed_indicative,
               count(DISTINCT referenceprel) FILTER (WHERE exceed AND thr_kind = 'reference') AS n_exceed_reference,
               max(value) AS max_value, mode(thr_max) AS typical_threshold, mode(thr_kind) AS typical_threshold_kind
        FROM {J} GROUP BY 1, 2""", "param_year", "annee, code")

    # networks × family × year, two-stage aggregation (per sample, then per network) instead of DISTINCT
    copy_by_year(con, """
        WITH a AS (
          SELECT annee, cdreseau, family, subfamily, referenceprel, count(*) AS n_res,
                 count(*) FILTER (WHERE detected) AS n_det, count(*) FILTER (WHERE exceed) AS n_exc, max(ratio) AS mr
          FROM {J} WHERE family <> 'info' GROUP BY 1, 2, 3, 4, 5),
        b AS (
          SELECT annee, cdreseau, family, subfamily, count(*) AS n_samples, sum(n_res)::INT AS n_results,
                 sum(n_det)::INT AS n_detected, sum(n_exc)::INT AS n_exceed, max(mr)::FLOAT AS max_ratio
          FROM a GROUP BY 1, 2, 3, 4),
        c AS (
          SELECT annee, cdreseau, family, subfamily, count(*) AS n_params
          FROM (SELECT annee, cdreseau, family, subfamily, code FROM {J} WHERE family <> 'info' GROUP BY ALL)
          GROUP BY 1, 2, 3, 4)
        SELECT b.annee, b.cdreseau, b.family, b.subfamily, n_samples, n_results, n_params, n_detected, n_exceed, max_ratio
        FROM b JOIN c USING (annee, cdreseau, family, subfamily)""", "udi_family_year", "annee, cdreseau, family, subfamily")

    # key parameters × network × year (twin codes merged)
    copy_by_year(con, f"""
        SELECT annee, cdreseau, code_merged AS code, count(*) AS n, count(*) FILTER (WHERE detected) AS n_detected,
               avg(value)::FLOAT AS mean, max(value)::FLOAT AS max,
               count(*) FILTER (WHERE exceed) AS n_exceed,
               arg_max(thr_max, dateprel)::FLOAT AS threshold, arg_max(thr_kind, dateprel) AS threshold_kind
        FROM {{J}} WHERE code_merged IN ({sql_list(KEY_PARAMS)}) AND value IS NOT NULL
        GROUP BY 1, 2, 3""", "udi_param_year", "annee, cdreseau, code")

    # "current situation" windows: 12 months (micro, comfort) / 36 months (chem) ending on DATA_END_DATE
    win = f"""(family IN ('micro', 'comfort', 'info') AND dateprel >= DATE '{START_12}')
              OR (family = 'chem' AND dateprel >= DATE '{START_36}')"""
    con.execute(f"""CREATE OR REPLACE TEMP VIEW jw AS
        SELECT *, CASE WHEN family = 'chem' THEN '36m' ELSE '12m' END AS win
        FROM read_parquet([{', '.join(repr((JOINED / f'joined_{y}.parquet').as_posix()) for y in range(START_36.year, END.year + 1))}])
        WHERE dateprel <= DATE '{END}' AND ({win})""")
    copy(con, f"""
        SELECT cdreseau, {conf_cols}, max(dateprel) AS last_sample
        FROM {PLV} WHERE dateprel BETWEEN DATE '{START_12}' AND DATE '{END}' GROUP BY 1 ORDER BY 1""", "udi_micro_window")
    copy(con, """
        WITH a AS (
          SELECT cdreseau, family, subfamily, win, referenceprel, count(*) AS n_res,
                 count(*) FILTER (WHERE detected) AS n_det, count(*) FILTER (WHERE exceed) AS n_exc, max(ratio) AS mr
          FROM jw WHERE family <> 'info' GROUP BY 1, 2, 3, 4, 5),
        b AS (
          SELECT cdreseau, family, subfamily, win, count(*) AS n_samples, sum(n_res)::INT AS n_results,
                 sum(n_det)::INT AS n_detected, sum(n_exc)::INT AS n_exceed, max(mr)::FLOAT AS max_ratio
          FROM a GROUP BY 1, 2, 3, 4),
        c AS (
          SELECT cdreseau, family, subfamily, win, count(*) AS n_params
          FROM (SELECT cdreseau, family, subfamily, win, code FROM jw WHERE family <> 'info' GROUP BY ALL)
          GROUP BY 1, 2, 3, 4)
        SELECT b.*, c.n_params FROM b JOIN c USING (cdreseau, family, subfamily, win)
        ORDER BY 1, 2, 3""", "udi_family_window")
    copy(con, f"""
        SELECT cdreseau, code, any_value(family) AS family, any_value(subfamily) AS subfamily, any_value(win) AS win,
               count(*) AS n, count(*) FILTER (WHERE detected) AS n_detected, max(value)::FLOAT AS max_value,
               arg_max(dateprel, value) AS date_max, avg(value)::FLOAT AS mean,
               count(*) FILTER (WHERE exceed) AS n_exceed, max(ratio)::FLOAT AS max_ratio,
               arg_max(thr_max, coalesce(ratio, value))::FLOAT AS threshold,
               arg_max(thr_kind, coalesce(ratio, value)) AS threshold_kind,
               arg_max(thr_unit, coalesce(ratio, value)) AS unit
        FROM jw WHERE thr_kind IS NOT NULL OR code IN ({sql_list(KEY_PARAMS)})
        GROUP BY 1, 2 HAVING count(*) FILTER (WHERE detected) > 0 OR count(*) FILTER (WHERE exceed) > 0
        ORDER BY 1, 2""", "udi_param_window")
    build_p95(con)


P95_MIN_N = config.P95_MIN_N   # P95 only when a network has at least 10 measurements of a parameter in the window
P95_BUCKETS = 8  # networks split into 8 groups processed one after the other (exact quantiles stay in memory)


def build_p95(con) -> None:
    """95th percentile of value/threshold per network × parameter (chem 36 months, comfort 12 months).
    Used by the score instead of the maximum when n >= 10 (fair to large networks that sample a lot)."""
    parts = config.INTERIM / "parts" / "udi_param_p95"
    parts.mkdir(parents=True, exist_ok=True)
    window_files = [JOINED / f"joined_{y}.parquet" for y in range(START_36.year, END.year + 1)]
    for b in range(P95_BUCKETS):
        out = parts / f"bucket_{b}.parquet"
        sql = f"""
            SELECT cdreseau, code, count(ratio)::INT AS n_ratio, quantile_cont(ratio, 0.95)::FLOAT AS p95_ratio
            FROM jw WHERE family IN ('chem', 'comfort') AND ratio IS NOT NULL
                      AND hash(cdreseau) % {P95_BUCKETS} = {b}
            GROUP BY 1, 2 HAVING count(ratio) >= {P95_MIN_N}"""
        key = _key(sql, PREP_SOURCE, START_12, START_36, END)
        if is_fresh(out, key, window_files):
            continue
        t0 = time.time()
        con.execute(f"COPY ({sql}) TO '{out.as_posix()}' (FORMAT parquet)")
        write_stamp(out, key)
        print(f"  udi_param_p95 bucket {b}: {time.time() - t0:.0f}s", flush=True)
    copy(con, f"SELECT * FROM read_parquet('{parts.as_posix()}/*.parquet') ORDER BY 1, 2", "udi_param_p95",
         inputs=list(parts.glob("*.parquet")))


# --- 4. Data quality ------------------------------------------------------------------------------------
def build_data_quality(con) -> None:
    print("4. data quality")
    # missing values per column and year, on the raw files (as published)
    out = P / "dq_missing.parquet"
    raw_files = list(Path(RAW).glob("*/*.parquet"))
    rows = []
    for typ in ("PLV", "RESULT", "COM_UDI") if not is_fresh(out, _key("dq_missing"), raw_files) else ():
        cols = [c for c in con.execute(f"DESCRIBE SELECT * FROM read_parquet('{RAW}/{typ}/*.parquet')").df()["column_name"]
                if c != "annee_fichier"]
        expr = ", ".join(f"avg((\"{c}\" IS NULL)::INT) AS \"{c}\"" for c in cols)
        df = con.execute(f"SELECT annee_fichier AS annee, {expr} FROM read_parquet('{RAW}/{typ}/*.parquet') GROUP BY 1").df()
        df = df.melt(id_vars="annee", var_name="column", value_name="share_missing")
        df.insert(0, "table", typ)
        rows.append(df)
    if rows:
        pd.concat(rows).sort_values(["table", "column", "annee"]).to_parquet(out, index=False)
        write_stamp(out, _key("dq_missing"))
    print(f"  dq_missing{'' if rows else ' (cache)'}", flush=True)

    # result statuses (after keeping one row per sample and parameter)
    copy(con, f"""SELECT annee, status, count(*) AS n, count(*) FILTER (WHERE n_raw_rows > 1) AS n_collapsed
                  FROM read_parquet('{CLEAN}/result/*.parquet') GROUP BY 1, 2 ORDER BY 1, 2""", "dq_result_status")

    # official vs recomputed conformity per sample, and the explanation of the chemistry gap
    J = f"read_parquet('{JOINED.as_posix()}/*.parquet')"
    rec_sql = """
        SELECT annee, referenceprel,
               bool_or(exceed AND thr_kind = 'limit' AND micro_unit) AS rec_bact,
               bool_or(exceed AND thr_kind = 'limit' AND NOT micro_unit) AS rec_chem,
               arg_max(code, ratio) FILTER (WHERE thr_kind = 'limit' AND NOT micro_unit) AS top_code,
               max(ratio) FILTER (WHERE thr_kind = 'limit' AND NOT micro_unit) AS top_ratio,
               bool_or(thr_kind = 'limit' AND NOT micro_unit AND value IS NOT NULL AND value = thr_max) AS at_limit,
               bool_or(thr_kind = 'limit' AND NOT micro_unit AND NOT unit_ok) AS unit_mismatch
        FROM {J} GROUP BY 1, 2"""
    rec_parts = build_parts(con, rec_sql, "dq_recomputed")  # year by year (bounded memory), resumable
    con.execute(f"CREATE OR REPLACE TEMP TABLE rec AS SELECT * FROM read_parquet('{rec_parts.as_posix()}/*.parquet')")
    copy(con, """
        SELECT s.annee,
          count(*) FILTER (WHERE conf_bact = 'N') AS bact_nc_official,
          count(*) FILTER (WHERE rec_bact) AS bact_nc_recomputed,
          count(*) FILTER (WHERE conf_bact = 'N' AND rec_bact) AS bact_both,
          count(*) FILTER (WHERE conf_chem = 'N') AS chem_nc_official,
          count(*) FILTER (WHERE rec_chem) AS chem_nc_recomputed,
          count(*) FILTER (WHERE conf_chem = 'N' AND rec_chem) AS chem_both,
          count(*) FILTER (WHERE conf_chem = 'N' AND NOT coalesce(rec_chem, false)) AS chem_official_only,
          count(*) FILTER (WHERE conf_chem <> 'N' AND rec_chem) AS chem_recomputed_only,
          count(*) FILTER (WHERE conf_chem = 'D' AND rec_chem) AS chem_recomputed_only_derogation
        FROM s LEFT JOIN rec USING (annee, referenceprel) GROUP BY 1 ORDER BY 1""", "dq_conformity_check")
    # gap detail: which parameters explain the samples where official and recomputed chemistry disagree
    copy(con, """
        SELECT s.annee,
          CASE WHEN conf_chem = 'N' THEN 'official non-conform, no exceedance recomputed'
               ELSE 'exceedance recomputed, officially ' || coalesce(conf_chem, 'blank') END AS gap_type,
          coalesce(r.top_code, '(no limit row)') AS top_code,
          count(*) AS n_samples, median(r.top_ratio) AS median_top_ratio,
          count(*) FILTER (WHERE r.at_limit) AS n_value_equal_limit,
          count(*) FILTER (WHERE r.unit_mismatch) AS n_unit_mismatch
        FROM s LEFT JOIN rec r USING (annee, referenceprel)
        WHERE (conf_chem = 'N' AND NOT coalesce(r.rec_chem, false)) OR (conf_chem <> 'N' AND r.rec_chem)
        GROUP BY ALL ORDER BY 1, 2, 4 DESC""", "dq_chem_gap")

    # metabolite rule: rows of non-relevant metabolites by year, with/without a limit, before/after the Anses opinion
    cases = " ".join(f"WHEN '{c}' THEN DATE '{d}'" for c, (_, d) in config.NON_RELEVANT_METABOLITES.items())
    copy(con, f"""
        SELECT annee, code, thr_kind, dateprel >= (CASE code {cases} END) AS after_opinion,
               count(*) AS n, count(*) FILTER (WHERE detected) AS n_detected, count(*) FILTER (WHERE exceed) AS n_exceed,
               count(*) FILTER (WHERE value > {config.NON_RELEVANT_INDICATIVE_UGL}) AS n_above_0_9
        FROM {J} WHERE code IN ({sql_list(config.NON_RELEVANT_METABOLITES)}) GROUP BY ALL ORDER BY 1, 2, 3, 4""",
         "dq_metabolites")

    # unit concordance between result and threshold
    copy(con, f"""SELECT annee, thr_kind, unit_n AS result_unit, thr_unit, count(*) AS n
                  FROM {J} WHERE NOT unit_ok GROUP BY ALL ORDER BY n DESC""", "dq_unit_mismatch")


# --- 5. Automatic checks ------------------------------------------------------------------------------
def run_checks(con) -> None:
    print("5. automatic checks")
    log = [json.loads(l) for l in (config.INTERIM / "build_log.jsonl").read_text().splitlines()]
    last = {}
    for rec in log:  # last build of each year
        last[rec["year"]] = rec
    for y in config.YEARS:
        rec = last.get(y)
        check("raw rows read = data lines in the text file", rec is not None, "checked in 02" if rec else "missing", "build log", y)

    plv = f"read_parquet('{CLEAN}/plv/*.parquet')"
    res = f"read_parquet('{CLEAN}/result/*.parquet')"
    cu = f"read_parquet('{CLEAN}/com_udi/*.parquet')"
    raw_plv = f"read_parquet('{RAW}/PLV/*.parquet')"
    raw_res = f"read_parquet('{RAW}/RESULT/*.parquet')"
    for y, n_raw, n_clean, n_keys in con.execute(f"""
            SELECT annee_fichier, count(*), (SELECT count(*) FROM {plv} c WHERE c.annee = r.annee_fichier),
                   count(DISTINCT (referenceprel, cdreseau)) FROM {raw_plv} r GROUP BY 1 ORDER BY 1""").fetchall():
        check("PLV clean rows = distinct (sample, network)", n_clean == n_keys, n_clean, n_keys, y,
              f"{n_raw - n_clean} duplicate row(s) removed")
    for y, n_clean, n_keys in con.execute(f"""
            SELECT annee_fichier, (SELECT count(*) FROM {res} c WHERE c.annee = r.annee_fichier),
                   count(DISTINCT (referenceprel, cdparametresiseeaux)) FROM {raw_res} r GROUP BY 1 ORDER BY 1""").fetchall():
        check("RESULT clean rows = distinct (sample, parameter)", n_clean == n_keys, n_clean, n_keys, y)
    for y, n, n_keys in con.execute(f"""SELECT annee, count(*), count(DISTINCT (inseecommune, cdreseau, quartier))
                                       FROM {cu} GROUP BY 1 ORDER BY 1""").fetchall():
        check("COM_UDI key unique", n == n_keys, n, n_keys, y)
    # join explosion: joined rows = clean results × number of networks of each sample
    for y in config.YEARS:
        joined = con.execute(f"SELECT count(*) FROM '{(JOINED / f'joined_{y}.parquet').as_posix()}'").fetchone()[0]
        expected = con.execute(f"""
            SELECT sum(p.n_net * r.n_res) FROM
              (SELECT referenceprel, count(*) AS n_net FROM '{CLEAN}/plv/plv_{y}.parquet' GROUP BY 1) p
            JOIN (SELECT referenceprel, count(*) AS n_res FROM '{CLEAN}/result/result_{y}.parquet'
                  WHERE status <> 'qualitative' GROUP BY 1) r USING (referenceprel)""").fetchone()[0]
        check("no join explosion (results × networks of each sample)", joined == expected, joined, expected, y)
    orphans = con.execute(f"SELECT count(*) FROM {res} r ANTI JOIN {plv} p USING (annee, referenceprel)").fetchone()[0]
    check("results without sample", orphans == 0, orphans, 0)
    # every network that serves a commune exists; every sampled network is linked to a commune
    no_commune = con.execute(f"SELECT count(DISTINCT (annee, cdreseau)) FROM {plv} p ANTI JOIN {cu} c USING (annee, cdreseau)").fetchone()[0]
    check("sampled networks without commune", no_commune == 0, no_commune, 0)
    # national totals reproduce phase-0 numbers
    tot = con.execute(f"SELECT count(DISTINCT referenceprel) FROM {plv}").fetchone()[0]
    check("distinct samples 2016–2026 (phase 0)", tot == 2_991_181, tot, 2_991_181)
    # value parsing: 'quantified' values agree with the raw text
    bad = con.execute(f"""SELECT count(*) FROM {res} WHERE status = 'quantified' AND value IS NULL""").fetchone()[0]
    check("quantified results with a numeric value", bad == 0, bad, 0)
    neg = con.execute(f"""SELECT count(*) FROM {res} WHERE value < 0 AND code IN ('NO3', 'NO2', 'NO3_NO2', 'NH4')""").fetchone()[0]
    check("negative nitrate/nitrite/ammonium values (impossible, kept as published)", True, neg, "few, reported")
    dates = con.execute(f"SELECT count(*) FROM {plv} WHERE year(dateprel) <> annee OR dateprel > DATE '{END}'").fetchone()[0]
    check("sample dates inside the file year and before the data end date", dates == 0, dates, 0)
    # processed sizes
    total = 0.0
    for f in sorted(P.iterdir()):
        mb = f.stat().st_size / 1e6
        total += mb
        check(f"file size {f.name}", mb < MAX_FILE_MB, f"{mb:.1f} MB", f"< {MAX_FILE_MB} MB")
    check("data/processed total size", total < MAX_TOTAL_MB, f"{total:.1f} MB", f"< {MAX_TOTAL_MB} MB")
    pd.DataFrame(CHECKS).to_parquet(P / "dq_checks.parquet", index=False)


def main() -> int:
    t0 = time.time()
    P.mkdir(parents=True, exist_ok=True)
    con = connect_duckdb()   # memory_limit and threads from config.py (3 GB, 4 threads)
    register_macros(con)
    cat = build_catalog(con)
    con.register("cat_df", cat)
    con.execute("CREATE OR REPLACE TEMP TABLE cat AS SELECT code, family, subfamily, code_merged FROM cat_df")
    build_joined(con, "--rebuild-joined" in sys.argv)
    build_aggregates(con)
    build_data_quality(con)
    run_checks(con)
    failed = [c for c in CHECKS if not c["ok"]]
    print(f"\n{len(CHECKS) - len(failed)}/{len(CHECKS)} checks OK, {time.time() - t0:.0f}s")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

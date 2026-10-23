# Pipeline stage 02: unpacks yearly text archives and compiles validated clean Parquet partitions.
"""02: From the yearly zips to clean, typed Parquet files (one year at a time).

For each year:
  1. extract the 3 text files to data/interim/extract/<year>/ (never inside data/raw/);
  2. read them with DuckDB as text (all_varchar) and write a raw Parquet copy (data/interim/raw_parquet/),
     checking that every line was read (rows == newlines - header); delete the extracted text;
  3. build the clean tables (data/interim/clean/):
       plv_<year>     one row per (sample, network): typed dates, upstream flag, conformity codes
       result_<year>  one row per (sample, parameter): parsed value / LQ / status / thresholds,
                      laboratory measure kept when a parameter was measured twice (field + lab)
       com_udi_<year> commune <-> network links, duplicates removed (latest supply start kept)
Cache: a year is skipped when its outputs exist and the zip (size, mtime) has not changed.

Usage: python scripts/02_build_parquet.py [year ...] [--force]
"""
from __future__ import annotations

import json
import shutil
import sys
import time
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config  # noqa: E402
from utils.io import connect_duckdb  # noqa: E402
from utils.prep import EXCLUDED_THRESHOLD_UNITS, register_macros  # noqa: E402

FILES = {"PLV": "DIS_PLV_{y}.txt", "RESULT": "DIS_RESULT_{y}.txt", "COM_UDI": "DIS_COM_UDI_{y}.txt"}
EXTRACT = config.INTERIM / "extract"
LOG = config.INTERIM / "build_log.jsonl"


def count_newlines(path: Path) -> int:
    """Count newline characters in binary file to verify complete record ingestion."""
    n = 0
    with open(path, "rb") as f:
        while chunk := f.read(1 << 24):
            n += chunk.count(b"\n")
    return n


def zip_signature(zp: Path) -> str:
    """Generate cache key from zip file size and modification timestamp."""
    st = zp.stat()
    return f"{st.st_size}|{st.st_mtime_ns}"


def build_raw(con, y: int, zp: Path) -> list[dict]:
    """Steps 1–2: extract, read as text, write raw Parquet, check line counts."""
    out = EXTRACT / str(y)
    out.mkdir(parents=True, exist_ok=True)
    records = []
    for typ, pattern in FILES.items():
        name = pattern.format(y=y)
        txt = out / name
        with zipfile.ZipFile(zp) as z, z.open(name) as src, open(txt, "wb") as dst:
            shutil.copyfileobj(src, dst, 1 << 24)
        newlines = count_newlines(txt)
        header = txt.open(encoding="utf-8").readline().strip().split(",")
        cols = "{" + ", ".join(f"'{c}': 'VARCHAR'" for c in header) + "}"
        dest = config.RAW_PARQUET / typ
        dest.mkdir(parents=True, exist_ok=True)
        pq = dest / f"{typ.lower()}_{y}.parquet"
        con.execute(f"""
            COPY (SELECT *, {y} AS annee_fichier
                  FROM read_csv('{txt.as_posix()}', header=true, all_varchar=true, delim=',', quote='"',
                                escape='"', auto_detect=false, columns={cols}))
            TO '{pq.as_posix()}' (FORMAT parquet, COMPRESSION zstd, ROW_GROUP_SIZE 500000)""")
        rows = con.execute(f"SELECT count(*) FROM '{pq.as_posix()}'").fetchone()[0]
        if rows != newlines - 1:
            raise RuntimeError(f"{name}: {rows} rows read but {newlines - 1} data lines in the file")
        records.append({"year": y, "file": typ, "rows": rows, "text_bytes": txt.stat().st_size})
        txt.unlink()
    out.rmdir()
    return records


def build_clean(con, y: int) -> dict:
    """Step 3: typed and cleaned tables for one year."""
    raw = config.RAW_PARQUET
    clean = config.CLEAN
    for d in ("plv", "result", "com_udi"):
        (clean / d).mkdir(parents=True, exist_ok=True)
    excluded_units = ", ".join(f"'{u}'" for u in EXCLUDED_THRESHOLD_UNITS)

    # PLV: (referenceprel, cdreseau) is the key; 1–2 rows per year are recorded both on-site and as their own
    # upstream installation -> keep the on-site row.
    con.execute(f"""
        COPY (
          SELECT DISTINCT ON (referenceprel, cdreseau)
            {y}::SMALLINT AS annee, referenceprel, cdreseau, cddept, inseecommuneprinc,
            CAST(dateprel AS DATE) AS dateprel,
            cdreseauamont IS NOT NULL AS upstream, cdreseauamont,
            try_cast(regexp_extract(pourcentdebit, '([0-9]+)', 1) AS SMALLINT) AS pct_debit,
            plvconformitebacterio AS conf_bact, plvconformitechimique AS conf_chem,
            plvconformitereferencebact AS conf_ref_bact, plvconformitereferencechim AS conf_ref_chem,
            trim(conclusionprel, ' ' || chr(9)) AS conclusion
          FROM '{(raw / "PLV" / f"plv_{y}.parquet").as_posix()}'
          ORDER BY referenceprel, cdreseau, (cdreseauamont IS NULL) DESC
        ) TO '{(clean / "plv" / f"plv_{y}.parquet").as_posix()}' (FORMAT parquet, COMPRESSION zstd)""")

    # RESULT: parse values and thresholds; one row per (sample, parameter), laboratory measure first.
    con.execute(f"""
        COPY (
          WITH r AS (
            SELECT referenceprel, cdparametresiseeaux AS code, insituana AS insitu, qualitparam AS qualit,
                   rq_status(rqana, qualitparam) AS status,
                   rq_value(rqana, qualitparam, valtraduite) AS value,
                   rq_lq(rqana, qualitparam) AS lq,
                   cdunitereferencesiseeaux AS unit,
                   unit_norm(cdunitereferencesiseeaux) AS unit_n,
                   CASE WHEN thr_unit(limitequal) NOT IN ({excluded_units}) THEN thr_max(limitequal) END AS lim_max,
                   unit_norm(thr_unit(limitequal)) AS lim_unit_n,
                   thr_min(refqual) AS ref_min, thr_max(refqual) AS ref_max,
                   unit_norm(thr_unit(refqual)) AS ref_unit_n,
                   CASE WHEN qualitparam = 'O' THEN rqana END AS qualitative_text,
                   count(*) OVER (PARTITION BY referenceprel, cdparametresiseeaux) AS n_raw_rows
            FROM '{(raw / "RESULT" / f"result_{y}.parquet").as_posix()}'
          )
          SELECT {y}::SMALLINT AS annee, * FROM r
          QUALIFY row_number() OVER (
            PARTITION BY referenceprel, code
            ORDER BY (value IS NOT NULL) DESC, (insitu = 'L') DESC, value DESC NULLS LAST) = 1
        ) TO '{(clean / "result" / f"result_{y}.parquet").as_posix()}' (FORMAT parquet, COMPRESSION zstd)""")

    # COM_UDI: (commune, network, district) duplicates differ only by the supply start date -> keep the latest.
    con.execute(f"""
        COPY (
          SELECT DISTINCT ON (inseecommune, cdreseau, quartier)
            {y}::SMALLINT AS annee, inseecommune, nomcommune, quartier, cdreseau, nomreseau,
            try_cast(debutalim AS DATE) AS debutalim
          FROM '{(raw / "COM_UDI" / f"com_udi_{y}.parquet").as_posix()}'
          ORDER BY inseecommune, cdreseau, quartier, debutalim DESC
        ) TO '{(clean / "com_udi" / f"com_udi_{y}.parquet").as_posix()}' (FORMAT parquet, COMPRESSION zstd)""")

    counts = {}
    for d in ("plv", "result", "com_udi"):
        counts[d] = con.execute(f"SELECT count(*) FROM '{(clean / d / f'{d}_{y}.parquet').as_posix()}'").fetchone()[0]
    return counts


def main() -> int:
    """Execute yearly Parquet extraction and cleaning pipeline with incremental caching."""
    force = "--force" in sys.argv
    years = [int(a) for a in sys.argv[1:] if a.isdigit()] or config.YEARS
    con = connect_duckdb()
    register_macros(con)
    state_file = config.INTERIM / "build_state.json"
    state = json.loads(state_file.read_text()) if state_file.exists() else {}
    for y in years:
        zp = config.RAW_DIS / f"dis-{y}.zip"
        if not zp.exists():
            print(f"{y}: {zp.name} missing, run scripts/01_download.py first")
            return 1
        sig = zip_signature(zp)
        outputs = [config.CLEAN / d / f"{d}_{y}.parquet" for d in ("plv", "result", "com_udi")]
        if not force and state.get(str(y)) == sig and all(p.exists() for p in outputs):
            print(f"{y}: up to date (cache)")
            continue
        t0 = time.time()
        raw_records = build_raw(con, y, zp)
        counts = build_clean(con, y)
        rec = {"year": y, "raw": raw_records, "clean": counts, "seconds": round(time.time() - t0, 1)}
        print(json.dumps(rec), flush=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
        state[str(y)] = sig
        state_file.write_text(json.dumps(state, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Exploratory benchmark: extracts raw archives and counts line breaks versus DuckDB rows.
"""Phase 0, reconnaissance (lecture seule de data/raw/).

Pour chaque année : extrait les 3 fichiers texte du zip dans data/interim/extract/<année>/,
les relit avec DuckDB en texte brut (all_varchar, aucune conversion), écrit une copie Parquet
« brute » dans data/interim/raw_parquet/, compte les lignes de deux façons (DuckDB vs nombre de
fins de ligne) pour détecter des lignes rejetées ou des retours à la ligne dans les champs,
puis supprime le texte extrait. data/raw/ n'est jamais modifié.

Usage : python -I scripts/explore/p0_extract_to_parquet.py <racine_projet> [année ...]
"""
import json
import shutil
import sys
import time
import zipfile
from pathlib import Path

import duckdb

ROOT = Path(sys.argv[1]).resolve()
YEARS = [int(y) for y in sys.argv[2:]] or list(range(2016, 2027))
RAW = ROOT / "data" / "raw" / "dis"
INTERIM = ROOT / "data" / "interim"
EXTRACT = INTERIM / "extract"
PARQ = INTERIM / "raw_parquet"
TMP = INTERIM / "duckdb_tmp"
LOG = INTERIM / "p0_counts.jsonl"

TYPES = {"PLV": "DIS_PLV_{y}.txt", "RESULT": "DIS_RESULT_{y}.txt", "COM_UDI": "DIS_COM_UDI_{y}.txt"}

for d in (EXTRACT, PARQ, TMP):
    d.mkdir(parents=True, exist_ok=True)

con = duckdb.connect()
con.execute("SET memory_limit='4GB'")
con.execute("SET threads=8")
con.execute(f"SET temp_directory='{TMP.as_posix()}'")
con.execute("SET preserve_insertion_order=false")


def count_newlines(path: Path) -> int:
    """Count total newline characters in binary file."""
    n = 0
    with open(path, "rb") as f:
        while chunk := f.read(1 << 24):
            n += chunk.count(b"\n")
    return n


for y in YEARS:
    zp = RAW / f"dis-{y}.zip"
    out_dir = EXTRACT / str(y)
    out_dir.mkdir(exist_ok=True)
    for typ, pattern in TYPES.items():
        name = pattern.format(y=y)
        t0 = time.time()
        txt = out_dir / name
        with zipfile.ZipFile(zp) as z, z.open(name) as src, open(txt, "wb") as dst:
            shutil.copyfileobj(src, dst, 1 << 24)
        nl = count_newlines(txt)
        dest = PARQ / typ
        dest.mkdir(exist_ok=True)
        pq = dest / f"{typ.lower()}_{y}.parquet"
        con.execute(
            f"""
            COPY (
              SELECT *, {y} AS annee_fichier
              FROM read_csv('{txt.as_posix()}', header=true, all_varchar=true,
                            delim=',', quote='"', escape='"', auto_detect=false,
                            columns=$cols)
            ) TO '{pq.as_posix()}' (FORMAT parquet, COMPRESSION zstd, ROW_GROUP_SIZE 500000)
            """.replace("$cols", "{" + ", ".join(
                f"'{c}': 'VARCHAR'" for c in open(txt, encoding="utf-8").readline().strip().split(",")
            ) + "}")
        )
        n = con.execute(f"SELECT count(*) FROM '{pq.as_posix()}'").fetchone()[0]
        rec = {"annee": y, "type": typ, "lignes_duckdb": n, "fins_de_ligne": nl,
               "octets_txt": txt.stat().st_size, "octets_parquet": pq.stat().st_size,
               "secondes": round(time.time() - t0, 1)}
        print(json.dumps(rec), flush=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
        txt.unlink()  # texte extrait supprimé (data/interim/, jamais data/raw/)
    out_dir.rmdir()

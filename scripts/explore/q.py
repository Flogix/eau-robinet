# Exploratory utility: executes DuckDB SQL script files over raw Parquet partitions.
"""Petit utilitaire d'exploration : exécute des requêtes SQL DuckDB (séparées par ';;')
sur les Parquet bruts de data/interim/raw_parquet/ et affiche les résultats.

Vues disponibles : plv, result, com_udi (toutes années, colonne annee_fichier).
Usage : python -I scripts/explore/q.py <racine_projet> <fichier.sql> [année]
"""
import sys
from pathlib import Path

import duckdb

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(sys.argv[1]).resolve()
P = (ROOT / "data" / "interim" / "raw_parquet").as_posix()

con = duckdb.connect()
con.execute("SET memory_limit='4GB'; SET threads=8")
con.execute(f"SET temp_directory='{(ROOT / 'data' / 'interim' / 'duckdb_tmp').as_posix()}'")
YEAR = sys.argv[3] if len(sys.argv) > 3 else "*"  # optionnel : limiter à une année
for v in ("plv", "result", "com_udi"):
    con.execute(f"CREATE VIEW {v} AS SELECT * FROM read_parquet('{P}/{v.upper()}/{v}_{YEAR}.parquet')")

sql = Path(sys.argv[2]).read_text(encoding="utf-8")
for q in [s.strip() for s in sql.split(";;") if s.strip()]:
    title = q.splitlines()[0] if q.startswith("--") else q[:80]
    print(f"\n### {title}")
    rel = con.sql(q)
    print(rel.df().to_string(max_rows=200, max_colwidth=70, index=False))

"""Phase 0 — 10 lignes d'exemple par type de fichier (2025, échantillon reproductible, graine 42),
au format CSV brut tel que lu, pour docs/data_dictionary.md.

Usage : python -I scripts/explore/p0_samples.py <racine_projet> <fichier_sortie.md>
"""
import sys
from pathlib import Path

import duckdb

ROOT = Path(sys.argv[1]).resolve()
P = (ROOT / "data" / "interim" / "raw_parquet").as_posix()
out = []
con = duckdb.connect()
for typ, excl in (("PLV", ""), ("RESULT", ""), ("COM_UDI", "")):
    rel = con.sql(
        f"SELECT * EXCLUDE (annee_fichier) FROM read_parquet('{P}/{typ}/{typ.lower()}_2025.parquet') "
        "USING SAMPLE 10 ROWS (reservoir, 42)"
    )
    out.append(f"**{typ}** (2025)\n\n```csv\n" + ",".join(rel.columns))
    for row in rel.fetchall():
        out.append(",".join("" if v is None else f'"{v}"' for v in row))
    out.append("```\n")
Path(sys.argv[2]).write_text("\n".join(out), encoding="utf-8")

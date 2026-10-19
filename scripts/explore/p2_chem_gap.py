"""Phase 2 — explain the gap between the official chemical conformity and our recomputation.

Reads data/interim (joined results, clean samples) with the project DuckDB settings (3 GB, 4 threads).
Usage: python -I scripts/explore/p2_chem_gap.py <project_root>
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import config  # noqa: E402
from utils.io import connect_duckdb  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
con = connect_duckdb()
J = f"read_parquet('{(config.INTERIM / 'joined').as_posix()}/*.parquet')"
PLV = f"read_parquet('{config.CLEAN.as_posix()}/plv/*.parquet')"
REC = f"read_parquet('{(config.INTERIM / 'parts' / 'dq_recomputed').as_posix()}/*.parquet')"
con.execute(f"""CREATE TEMP TABLE s AS SELECT annee, referenceprel, any_value(conf_chem) AS conf_chem,
                any_value(conclusion) AS conclusion FROM {PLV} GROUP BY 1, 2""")
con.execute(f"CREATE TEMP TABLE g AS SELECT s.*, r.* EXCLUDE (annee, referenceprel) FROM s JOIN {REC} r USING (annee, referenceprel)")


def show(title, sql):
    print(f"\n### {title}")
    print(con.sql(sql).df().to_string(index=False, max_colwidth=110))


# A. exceedance recomputed but officially conform: chlorites (limit 0.25 mg/L; 0.7 mg/L "if the treatment can generate them")
show("A1. Recomputed-only (officially C) by year and top parameter", """
    SELECT annee, top_code, count(*) n FROM g WHERE conf_chem = 'C' AND rec_chem GROUP BY annee, top_code
    QUALIFY row_number() OVER (PARTITION BY annee ORDER BY count(*) DESC) <= 2 ORDER BY 1, 3 DESC""")
show("A2. Chlorite (CLITEMG) values in those samples", f"""
    WITH x AS (SELECT referenceprel, annee FROM g WHERE conf_chem = 'C' AND rec_chem AND top_code = 'CLITEMG')
    SELECT count(DISTINCT j.referenceprel) n_samples, min(value) vmin, median(value) vmed, max(value) vmax,
           count(DISTINCT j.referenceprel) FILTER (WHERE value <= 0.7) n_le_0_7
    FROM {J} j JOIN x USING (annee, referenceprel) WHERE j.code = 'CLITEMG'""")
show("A3. Limit written on CLITEMG rows, by year", f"""
    SELECT annee, lim_max, count(*) n FROM {J} WHERE code = 'CLITEMG' GROUP BY ALL ORDER BY 1, 2""")

# B. officially non-conform without any recomputed exceedance
show("B1. Official-only N by year", """
    SELECT annee, count(*) n, count(*) FILTER (WHERE top_code IN ('SE', 'SB')) n_se_sb FROM g
    WHERE conf_chem = 'N' AND NOT coalesce(rec_chem, false) GROUP BY 1 ORDER BY 1""")
show("B2. What the ARS conclusion text says (official-only N, keywords)", """
    SELECT CASE WHEN conclusion ILIKE '%sélénium%' OR conclusion ILIKE '%selenium%' THEN 'mentions selenium'
                WHEN conclusion ILIKE '%antimoine%' THEN 'mentions antimony'
                WHEN conclusion ILIKE '%nitrate%' THEN 'mentions nitrates'
                WHEN conclusion ILIKE '%pesticide%' OR conclusion ILIKE '%métabolite%' THEN 'mentions pesticides'
                WHEN conclusion ILIKE '%non conforme%' OR conclusion ILIKE '%non-conforme%' THEN 'non-conform, parameter not named'
                ELSE 'other' END AS conclusion_says,
           count(*) n, any_value(left(conclusion, 160)) example
    FROM g WHERE conf_chem = 'N' AND NOT coalesce(rec_chem, false) GROUP BY 1 ORDER BY 2 DESC""")
show("B3. Selenium in official-only N samples: value vs limit on the row", f"""
    WITH x AS (SELECT annee, referenceprel FROM g WHERE conf_chem = 'N' AND NOT coalesce(rec_chem, false) AND top_code = 'SE')
    SELECT j.annee, count(*) n, median(value) vmed, max(value) vmax, mode(lim_max) lim
    FROM {J} j JOIN x USING (annee, referenceprel) WHERE j.code = 'SE' GROUP BY 1 ORDER BY 1""")
show("B4. Selenium limits written in the data, by year", f"""
    SELECT annee, code, lim_max, count(*) n FROM {J} WHERE code IN ('SE', 'SECL') GROUP BY ALL ORDER BY 1, 2, 3""")

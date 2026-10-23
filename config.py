# Central configuration: filesystem paths, analysis windows, score thresholds, and data sources.
# Serves as the single source of truth imported by the pipeline scripts, web app, and tests.
"""Project-wide constants: paths, periods, score parameters, sources.

Every threshold used by the score lives here so that it is documented in one place
and can be changed (what-if sliders reuse the defaults below).
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

# --- Paths -------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RAW = DATA / "raw"            # read-only, never committed
RAW_DIS = RAW / "dis"         # national yearly zips dis-YYYY.zip
RAW_REF = RAW / "ref"         # downloaded reference files (communes, contours, typologies)
INTERIM = DATA / "interim"    # extracted text, raw/clean Parquet, DuckDB temp (never committed)
RAW_PARQUET = INTERIM / "raw_parquet"
CLEAN = INTERIM / "clean"
DUCKDB_TMP = INTERIM / "duckdb_tmp"
PROCESSED = DATA / "processed"  # small tables read by the app (committed)

# --- Reproducibility -----------------------------------------------------------
SEED = 42

# --- Periods -------------------------------------------------------------------
YEARS = list(range(2016, 2027))
COMPLETE_YEARS = list(range(2016, 2026))   # 2026 is partial
PARTIAL_YEAR = 2026
DATA_END_DATE = date(2026, 8, 31)          # last sampling date in the 2026 file (measured in phase 0)
WINDOW_MONTHS_SHORT = 12   # microbiology and comfort ("current situation")
WINDOW_MONTHS_LONG = 36    # health-related chemistry (full analyses are rarer in small networks)

# --- DuckDB --------------------------------------------------------------------
DUCKDB_MEMORY_LIMIT = "3GB"   # ~4 GB free RAM on the dev machine: keep room for the OS and the app
DUCKDB_THREADS = 4

# --- Source dataset --------------------------------------------------------------
DATASET_SLUG = "resultats-du-controle-sanitaire-de-leau-distribuee-commune-par-commune"
DATASET_PAGE = f"https://www.data.gouv.fr/datasets/{DATASET_SLUG}"
AUTHOR_LINKEDIN = "https://www.linkedin.com/in/florian-giraud-67883a291/"
REPO_URL = "https://github.com/Flogix/eau-robinet"
DATASET_API = f"https://www.data.gouv.fr/api/1/datasets/{DATASET_SLUG}/"
DATASET_UPDATED = "2026-10-05"
DATASET_CITATION = (
    "Ministère des Solidarités et de la Santé, « Résultats du contrôle sanitaire de l'eau distribuée "
    "commune par commune », data.gouv.fr, Licence Ouverte 2.0, last updated 5 October 2026."
)

# --- Pesticide metabolites classified "non-relevant" by Anses -------------------
# Rule (decided 19/10/2026): if a result row carries a quality limit, that limit applies;
# otherwise these codes are compared with the 0.9 µg/L indicative value (comfort/vigilance family).
# Sources: docs/sources.md (Anses opinions of 30/09/2022 and 29/04/2024).
NON_RELEVANT_INDICATIVE_UGL = 0.9
NON_RELEVANT_METABOLITES = {
    # code: (substance, date of the Anses opinion)
    "MTCESA": ("ESA-metolachlor", date(2022, 9, 30)),
    "ESAMTC": ("ESA-metolachlor", date(2022, 9, 30)),
    "MTCNOA": ("NOA-metolachlor", date(2022, 9, 30)),
    "NOAMTC": ("NOA-metolachlor", date(2022, 9, 30)),
    "471811R": ("Chlorothalonil R471811", date(2024, 4, 29)),
    "R471811": ("Chlorothalonil R471811", date(2024, 4, 29)),
}
# Same substance published under two codes (one with a limit, one without): merged for time series.
TWIN_CODES = {"ESAMTC": "MTCESA", "NOAMTC": "MTCNOA", "R471811": "471811R", "OXAMTC": "MTCOXA"}

# --- Score (method: utils/score.py, decisions: docs/AVANCEMENT.md phase 3) ----------
# These are project choices (a teaching indicator), not regulatory values; the sensitivity analysis
# (scripts/05_build_scores.py -> score_sensitivity) shows how much the ranking depends on them.
WEIGHTS = {"micro": 0.4, "chem": 0.4, "comfort": 0.2}
MICRO_K = 5                       # S = 100 * (1 - t) ** k, t = share of non-compliant bacteriological samples
                                  # (k = 10 in the first proposal; 5 chosen at the phase-3 review so that 1 incident in 5 samples
                                  # of a small network does not sink it to grade D, see docs/AVANCEMENT.md phase 3)
CHEM_PENALTY_POINTS = [(0.5, 0), (1.0, 20), (2.0, 80)]   # ratio value/threshold -> penalty, capped at 80
CHEM_OTHER_PENALTY_FACTOR = 0.25  # S = 100 - worst penalty - 0.25 x sum of the other penalties
COMFORT_PENALTY_CAP = 50
P95_MIN_N = 10                    # ratio = P95 instead of max when >= 10 measurements (same value in script 03)
EXCEEDANCE_FLOOR_RATIO = 1.0      # any measured exceedance counts at least as ratio 1 (penalty 20): never hidden by P95
GRADES = [(90, "A"), (75, "B"), (60, "C"), (40, "D"), (0, "E")]
MIN_SAMPLES_RANKING = 12          # minimum samples for a network to appear in top/bottom rankings
# Confidence: high = 3 families measured, >= 12 bacteriological samples in 12 months (about monthly),
# nitrates and pesticides measured in 36 months; low = fewer than 4 bacteriological samples, or no microbiology
# or no health-related chemistry in the windows; medium otherwise
CONF_HIGH_MIN_BACT = 12
CONF_LOW_MAX_BACT = 3

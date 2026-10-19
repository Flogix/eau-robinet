# Is my tap water good? 💧

*EFREI 2026 individual project — Streamlit data-storytelling dashboard — Florian GIRAUD (20230851, DAI).*

A Streamlit app that tells the story of French tap-water quality from 2016 to 2026, built on the official results of the
sanitary control carried out by the Regional Health Agencies (ARS): ~3 million water samples and 133 million analyses.

> **Status: work in progress** (phase 3 — score). Sections marked *TODO* are filled in later phases.

## Question and audience
- **Main audience:** a resident who wonders whether the water from their tap is good.
- **Secondary audience:** elected officials, journalists, teachers looking for where the problems are in France.
- **Questions:** Is my water good (score /100, grade A–E, explained)? What is in the water and what is serious?
  Where are the problems? Big city vs small town, mountain vs Mediterranean coast? Is it getting better since 2016?

The score is an **educational indicator, not a health opinion**: the official opinion is the one of the ARS.

## Data
- **Dataset:** Ministère des Solidarités et de la Santé, « Résultats du contrôle sanitaire de l'eau distribuée commune par commune »,
  data.gouv.fr, Licence Ouverte / Open Licence 2.0, last updated 5 October 2026 —
  https://www.data.gouv.fr/datasets/resultats-du-controle-sanitaire-de-leau-distribuee-commune-par-commune
- Coverage: samples validated since 1 January 2016; **2026 is partial (samples up to 31 August 2026)**.
- Data dictionary: [docs/data_dictionary.md](docs/data_dictionary.md). All sources: [docs/sources.md](docs/sources.md).
- Raw files (~3 GB of zips, ~22 GB of text) are **not** in the repository: `make data` downloads them (with cache) and rebuilds
  the small tables of `data/processed/`, which are committed so the app runs from a clean clone.

## Method

### Data pipeline (`make data`)
| Step | What it does | Time on the dev machine* |
|---|---|---|
| `01_download.py` | Lists the yearly national zips on the data.gouv.fr API, checks size + SHA1, downloads only what is missing (never overwrites) | ~10 s when up to date |
| `02_build_parquet.py` | One year at a time: extract → raw Parquet (row-count check) → clean tables: values parsed (`<LQ`, decimal commas, codes), thresholds parsed, one row per sample × parameter (lab measure kept), duplicates removed | ~10 min (11 years) |
| `03_build_aggregates.py` | Parameter families; results × samples with the applicable threshold (quality limit, 0.9 µg/L indicative value for non-relevant pesticide metabolites, quality reference); small tables for the app; data-quality tables; P95 per network × parameter; 88 automatic checks | ~12 min first run, ~1 min when cached |
| `04_referentiels.py` | Communes (population, centre), INSEE density grid, Mountain Act communes, department contours | < 1 min |

\* Windows laptop, DuckDB limited to 3 GB of RAM and 4 threads. Every step is resumable: an interrupted run restarts
where it stopped. Long steps can run in the background with a log: `.\scripts\run_logged.ps1 03_build_aggregates`.

| `05_build_scores.py` | Scores of networks and communes, validation against official conformity, sensitivity analysis, witness communes ([docs/score_witnesses.md](docs/score_witnesses.md)) | ~3 min (pandas only) |

### Score /100 (`utils/score.py`, settings in `config.py`)
The score is computed per **distribution network (UDI)** over the "current situation" windows ending on 31/08/2026:
12 months for microbiology and comfort, 36 months for health-related chemistry (full analyses are rare in small networks).
1. **Microbiology** — `100 × (1 − t)^10`, `t` = share of samples officially non-compliant with the bacteriological limits.
2. **Health-related chemistry** — for each parameter with a quality limit, `r = value / limit` at the maximum (or at the 95th
   percentile with ≥ 10 measurements, to be fair to big networks that sample a lot); any measured exceedance counts at least
   as `r = 1`. Penalty: 0 up to `r = 0.5`, 0→20 up to `r = 1`, 20→80 up to `r = 2`, 80 beyond.
   Sub-score = `100 − worst penalty − 0.25 × sum of the other penalties`.
3. **Comfort / indicators** — same rule with quality references and the 0.9 µg/L indicative value, penalty capped at 50;
   ranges (pH, conductivity) and zero references (coliform bacteria) are scored on the share of samples outside.
4. **Global** = weighted mean (0.4 / 0.4 / 0.2) of the **measured** families only: a family without data is never counted as
   perfect. Grade A ≥ 90 · B ≥ 75 · C ≥ 60 · D ≥ 40 · E. Confidence high / medium / low from the number of samples and families.
5. **Commune** = mean of the networks serving it (worst network shown). A rule-based report explains each score.

**Validation** (23,733 networks): networks with an official bacteriological non-conformity in the last 12 months have a median
score of 52 vs 90 for the others; with an official chemical non-conformity, a median chemistry sub-score of 19 vs 100
(probability that such a network scores lower than a compliant one: 0.95 for bacteriology, 0.85 for chemistry, on the global score).
**Sensitivity**: across 14 variants (weights, `k`, P95 vs max, penalty curve, caps), the Spearman rank correlation with the
default ranking stays between 0.85 (comfort removed) and 0.998 — the ranking depends little on these choices.

## Key insights
*TODO (phase 5).*

## Limitations
*TODO (phase 5).*

## How to run

With `make` (Linux/macOS, or Windows with make installed):

```bash
make setup   # virtual environment + pinned dependencies
make run     # streamlit run app.py (uses data/processed/, no raw data needed)
make test    # pytest
make data    # optional: download raw data and rebuild data/processed/ (duration: see Method)
```

On Windows PowerShell without `make`:

```powershell
.\make.ps1 setup
.\make.ps1 run
.\make.ps1 test
.\make.ps1 data
```

Requires Python ≥ 3.11 (developed with 3.12.9).

## Project structure

```
app.py                  page config, navigation, global sidebar
config.py               paths, periods, thresholds, score weights, SEED
sections/               one page per file, in the order of the story
utils/                  io.py (loading, DuckDB), prep.py (parsing, families), score.py, viz.py (chart style)
scripts/                01_download → 02_build_parquet → 03_build_aggregates → 04_referentiels
scripts/explore/        phase-0 reconnaissance queries (reproducible numbers of the data dictionary)
data/processed/         small tables read by the app (committed)
tests/                  pytest
docs/                   brief, specification, progress log, data dictionary, sources, storyboard, video script
```

## Tools
*TODO: AI assistant usage statement (Claude Code was used as a coding assistant).*

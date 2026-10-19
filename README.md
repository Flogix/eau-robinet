# Is my tap water good? 💧

*EFREI 2026 individual project — Streamlit data-storytelling dashboard — Florian GIRAUD (20230851, DAI).*

A Streamlit app that tells the story of French tap-water quality from 2016 to 2026, built on the official results of the
sanitary control carried out by the Regional Health Agencies (ARS): ~3 million water samples and 133 million analyses.

> **Status: work in progress** (phase 1 — setup). Sections marked *TODO* are filled in later phases.

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
*TODO (phases 2–3): pipeline, cleaning choices, score method, validation.*

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

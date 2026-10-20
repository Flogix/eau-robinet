# Is my tap water good?

*Au robinet. EFREI Paris 2026 individual project, Streamlit data-storytelling dashboard.
Florian GIRAUD, student number 20230851, group DAI.*

**Live app: https://eau-robinet.streamlit.app/** · Code and processed data: https://github.com/Flogix/eau-robinet

Every day, people in France fill a glass at the tap without a second thought. This app checks, town by town, whether that
trust is deserved. It is built on ten years of official results of the sanitary control of tap water carried out by the
regional health agencies (ARS): about 3 million water samples and 133 million analysis results, from January 2016 to
August 2026. It gives every French town a score out of 100 with a plain-language report on why, lets readers compare
towns and regions, shows where the problems are on a map, follows the main substances over time, and lets anyone rebuild
the score with their own rules or take a PDF report home.

This README is also the project report: question, data, method, findings, limits, and how to run everything.

## 1. The question and the audience

The main reader is **a resident who wonders whether the water from their tap is good**. They do not know what a
"distribution network" or a "quality reference" is, so the app explains every technical word the first time it appears.
The second audience is **elected officials, journalists and teachers** who want to see where the problems are in France
and whether they are getting better or worse.

The app answers five questions, one page or more each:

| Question | Where it is answered |
|---|---|
| Is the water of my town good, and why? | *The water of my town* (score, grade, report per network, PDF) |
| What is in the water, and what is serious? | *How to read a water test* (20 sourced fact sheets, search over 1,789 parameters) |
| Big city or village, mountain or Mediterranean coast? | *Town against town* |
| Where are the problems in France? | *The map of France* |
| Is it getting better since 2016, and can we trust the curves? | *What we look for, what we find*, *Behind the numbers* |
| What do the raw data look like, and which indicators go together? | *Explore the data* (files and keys, real rows, distributions, rank correlations) |

The story follows the arc asked by the brief. The **hook** is the home page: water that makes people ill is not a thing
of the past (WHO and Santé publique France figures, sourced). The **context** is how the control works and how to read a
test. The **insights** are four hypotheses, H1 to H4, tested on the data. The **implications** page says what this means
for a resident and for local authorities, and what the data cannot say. It comes second in the menu, right after the hook:
the reader gets the findings first, and every page after it is the evidence, each hypothesis linking to the page that tests
it.

The score is a **teaching indicator, not a health opinion**. The official opinion on a town's water is the one of its
regional health agency. This warning is in the sidebar of every page, in the PDF report and on the personal score page.

## 2. The data

**Dataset.** Ministère des Solidarités et de la Santé, « Résultats du contrôle sanitaire de l'eau distribuée commune par
commune », data.gouv.fr, Licence Ouverte / Open Licence 2.0, last updated on 5 October 2026.
https://www.data.gouv.fr/datasets/resultats-du-controle-sanitaire-de-leau-distribuee-commune-par-commune

The yearly national files `dis-2016.zip` to `dis-2026.zip` were checked against the data.gouv.fr API (same size, same SHA1)
on 19 October 2026. Each year holds three tables: the samples (PLV), the analysis results (RESULT) and the link between towns
and distribution networks (UDI_COM). A **distribution network** (UDI) is a set of pipes fed by the same source or plant,
inside which the water has the same quality; the agencies test networks, not towns, and a town can be served by several
networks while a network can serve several towns.

| Measured in phase 0 | Value |
|---|---|
| Years | 2016 to 2026, **2026 partial: samples up to 31 August 2026** |
| Distinct samples | 2,991,181 |
| Analysis results | 133,474,398 |
| Parameters (codes) | 1,789 |
| Town codes / network codes | 34,945 / 24,461 |
| Raw size | about 3 GB of zips, 22 GB of text |

The raw files are **not** in the repository. `make data` downloads them (with a cache that never overwrites a file) and
rebuilds the small tables of `data/processed/` (31 files, 53 MB, largest 24 MB), which are committed so that the app runs
from a clean clone without the raw data. Other sources (town referentials, INSEE density grid, Mountain Act towns,
department contours, and 39 health and regulatory sources used in the texts) are listed with their URLs in
[docs/sources.md](docs/sources.md). The columns and their formats are described in
[docs/data_dictionary.md](docs/data_dictionary.md).

## 3. Method

### 3.1 Pipeline (`make data`)

The raw text is far too big for pandas, so the heavy work is done with **DuckDB out of memory** and stored as **Parquet**,
one year at a time, with a 3 GB memory limit (the development laptop had about 4 GB of free RAM).

| Step | What it does | Time on the dev machine |
|---|---|---|
| `01_download.py` | Lists the yearly zips on the data.gouv.fr API, checks size and SHA1, downloads only what is missing | about 10 s when up to date |
| `02_build_parquet.py` | Extracts each year into `data/interim/`, converts to raw Parquet (row count checked against the file), then builds clean tables | about 10 min |
| `03_build_aggregates.py` | Parameter families, the threshold that applies to every result, small tables for the app, data-quality tables, 95th percentiles, 88 automatic checks | about 12 min the first time, 1 min when cached |
| `04_referentiels.py` | Towns (population, centre, department, region), former towns merged into current ones, density grid, Mountain Act, contours | under 1 min |
| `05_build_scores.py` | Scores of networks and towns, validation, sensitivity analysis, witness towns | about 3 min (pandas only) |
| `06_build_app_tables.py` | Department × family × year table for the map | seconds |
| `07_build_explore_tables.py` | Small tables of *Explore the data*: volume per year, town-network links, distributions, department indicators and their rank correlations | about 3 s |

Every step can be interrupted and restarted where it stopped (state files and stamps in `data/interim/`).

### 3.2 Cleaning

The cleaning rules come from what the files actually contain (all measured in phase 0, see the data dictionary):

- **Values.** The text value mixes numbers, decimal commas and qualifiers such as `<0,05`. Each result is parsed into a
  status (quantified, below the quantification limit, qualitative, not measured), a number and a quantification limit.
  Results below the quantification limit count as zero when thresholds are checked, never as a detection. The 0.93 million
  "not measured" rows are excluded.
- **Thresholds.** Limits and references are parsed into a bound (or a range for pH and conductivity) with a normalised unit.
  The threshold **written on each row** is used, because one parameter can have several limits (nitrites 0.5 or 0.1 mg/L).
- **Duplicates.** A sample taken upstream is copied for every network downstream (x1.43 on average): national counts use
  distinct samples, network counts use the pair (sample, network). When a parameter is measured both on site and in the
  laboratory, the laboratory value is kept.
- **Twin codes.** The same pesticide metabolite is sometimes published under two codes, one with a limit and one without
  (for example `ESAMTC` and `MTCESA`); they are merged in time series and counted once in the score.
- **Non-relevant metabolites.** Three metabolites classified "non-relevant" by Anses are compared with a 0.9 µg/L indicative
  value when their row carries no limit (sources 5 to 7 and 20 to 21).
- **Families.** Every parameter is put in one family: microbiology, health chemistry (nitrates, pesticides, metals, PFAS,
  disinfection by-products...), comfort and indicators (taste, colour, treatment), or information only (hardness, temperature).

### 3.3 The score out of 100 (`utils/score.py`, settings in `config.py`)

The score is computed for each **network** over the "current situation" windows ending on 31 August 2026: twelve months for
bacteria and comfort, three years for health chemistry, because full chemical analyses are rare in small networks.

1. **Bacteria**: `S = 100 × (1 − t)^5`, where `t` is the share of samples officially non-compliant with the bacteriological
   limits. One failed sample out of 100 gives 95, five out of 100 give 77. The exponent 5 (rather than 10 in the first
   proposal) avoids sinking a small network sampled five times a year to grade D after a single incident.
2. **Health chemistry**: for each substance with a limit, `r = value / limit`, taken at the maximum, or at the 95th percentile
   when there are ten measurements or more, so that big networks that sample a lot are not punished for one peak. Any measured
   exceedance still counts at least as `r = 1`. The penalty is 0 up to half of the limit, 20 at the limit, 80 at twice the
   limit and stays there. The mark is `100 − worst penalty − 0.25 × sum of the other penalties`.
3. **Comfort**: the same rule with quality references and the 0.9 µg/L indicative value, penalties capped at 50. For ranges
   (pH, conductivity) and references at zero (coliform bacteria), the penalty depends on the share of samples outside.
4. **Global score**: weighted mean, 40% bacteria, 40% chemistry, 20% comfort, of the **measured** families only. A family that
   was not measured is never counted as perfect: it is left out and lowers the confidence.
5. **Grade** A from 90, B from 75, C from 60, D from 40, E below, on the score rounded to one decimal (the value displayed).
   **Confidence** is high when the three families were measured with at least twelve bacterial samples in the year and
   nitrates and pesticides in three years, low with three bacterial samples or fewer.
6. **Town** = mean of the scores of the networks that serve it. A rule-based report explains each network in sentences.

The same formulas are shown in the app (LaTeX, each followed by a sentence) and in the PDF report.

### 3.4 Validation

The score was checked against the official verdicts it does not use directly. Over 23,733 networks, those with an official
bacteriological non-conformity in the last twelve months have a median score of 61, against 90 for the others. Those with
an official chemical non-conformity have a median chemistry mark of 19, against 100. The probability that a non-compliant
network scores lower than a compliant one is 0.91 for bacteria and 0.88 for chemistry. Five witness towns are documented in
[docs/score_witnesses.md](docs/score_witnesses.md): Paris 84.1 (B), Villejuif 81.1 (B), Chamonix 83.1 (B), Sète 100 (A),
and a small rural town drawn at random with seed 42, Fouchères (Yonne) 95.0 (A).

For bacteria, our recomputation of non-conformity from the raw values finds 100% of the samples declared non-compliant by
the agencies. For chemistry, the two differ before 2023 for reasons we traced and sourced: prefectoral derogations, chlorites
judged against a 0.7 mg/L limit, and the selenium and antimony limits that changed on 1 January 2023 (sources 8 to 10). This
is why the historical indicators use the official verdicts, and the score uses the recent windows where both agree.

### 3.5 Sensitivity, and the reader's own score

Weights and curves are choices, so the score was recomputed with 14 variants of the method (equal weights, bacteria or
chemistry heavier, no comfort, `k` = 10 or 20, smoothing towards the national rate, maximum instead of 95th percentile, no
minimum penalty, other caps and curves). The rank correlation with the default ranking stays between 0.95 and 0.998, and
0.86 when comfort is removed: the ranking depends little on these choices, only the letters move.

The page *Build your own score* goes further: the reader changes the weights, makes a group of substances more severe
(pesticides x2, metals x3...), changes how hard a bacterial failure counts, and moves the key thresholds (nitrates, lead,
arsenic, PFAS, each pesticide). The official score and the personal score of a town are shown side by side, with its rank,
the grades of all towns and the ten lowest large towns. A fast engine (`utils/custom_score.py`) recomputes the 23,000
networks in about 0.1 s and gives exactly the published scores with the official settings (tested). A clear warning says
that these settings are personal and change nothing to the regulatory limits.

### 3.6 Reports in PDF: one town, or a comparison

From the town page, a report can be downloaded in English or in French: score, grade, the three marks, the networks, the
substances in question, ten years of a key substance, the position against the national and departmental medians, the
formulas, the sources, the date of the data and the warning. Every sentence comes from fixed rules applied to the data, the
same rules as in the app, so no number can be invented; no AI writes or changes any text. The PDF is drawn with **fpdf2**
(pure Python, installs on Streamlit Community Cloud without system packages) with the app's fonts embedded (IBM Plex and
Fraunces, SIL Open Font License, in `assets/fonts/`), so accents and symbols such as µ, ≤ and × are drawn correctly. Charts
are drawn directly with fpdf2 shapes, which avoids a headless browser on the server.

The page *Town against town* offers the same kind of report for the towns compared (2 to 6), in English or in French
(`utils/compare_report.py`): each town with its score, grade, confidence and three marks, bars that put the score and the
marks side by side (town name on the left of each bar, value on the right, so colour is never needed), why the best town
does better than the weakest (family and substances in question), the position of each town against the national median,
then the formulas, the sources, the date of the data and the warning. The paragraph on the gap is the same function on
the page and in the PDF; a town without score is named and set aside. Both reports share one layout class
(`town_report._Doc`).

## 4. What we found

**The big picture.** Over 2016 to 2025, 98.0% of bacteriological samples and 97.0% of chemical samples met the health
limits; in 2025, 98.3% and 97.0%. French tap water is good in the vast majority of places. 47% of the towns are graded A
and 13% D or E. The median town score ranges from 57/100 in Aisne to 99/100 in Bouches-du-Rhône.

**H1. Problems concentrate in small networks. Confirmed.** Networks tested fewer than twelve times a year carry 73% of the
bacterial failures for only 26% of the samples (2016 to 2025). Their failure rate is 5.1%, against 0.16% in the most tested
networks. This is also where a score rests on the fewest samples, which is why each score comes with a confidence level.

**H2. Bacteria and chemistry do not hit the same places. Confirmed.** Between mainland departments, the rank correlation of
the two failure rates is ρ = 0.05, close to zero. The departments most affected by bacteria are Lozère, Haute-Corse and
Corse-du-Sud; by chemistry, Aisne, Aube and Marne. A single national ranking hides more than it shows. The map says where,
not why: the causes are not in the data.

**H3. Part of the recent rise in chemical non-compliance comes from what laboratories look for. Confirmed, and the main
finding.** Officially non-compliant samples went from 6,219 a year (2016 to 2020) to 11,412 (2021 to 2024), then 8,742 in
2025. Three families of pesticide metabolites, newly searched or reclassified by Anses, account for 58% of the limit
exceedances of 2021 to 2024. Without them, exceedances would have gone from 6,177 in 2016 to 7,592 in 2025; with them, from
6,676 to 15,917. Exceedances still grow a little without them, which deserves attention, but nothing like the official curve
suggests. The number of different parameters searched each year grows too, and PFAS show the same pattern in the making:
122 samples analysed for the sum of 20 PFAS in 2022, 16,475 in 2025, of which 386 were above 0.1 µg/L. PFAS are part of the
routine control only since 1 January 2026 (source 11).

**H4. Hardness varies a lot, without health stakes. Confirmed.** Network hardness ranges from 1 °f to 36 °f between the 5th
and the 95th percentile, and the regional medians from 2 °f in Guyane to 33 °f in Hauts-de-France. Health agencies state
that hard water has no effect on health (source 37), so hardness never lowers the score.

**Other findings.** 74% of networks stayed below half of the nitrate limit (25 mg/L) over three years, and 3.2% went above
the 50 mg/L limit at least once. Bacterial failures follow the seasons: 3.05% of samples in October against 0.80% in April
(2016 to 2025).

**Implications.** For a resident: read the report rather than the grade alone, watch the confidence level, and remember that
lead comes mostly from the pipes of old buildings (let the cold water run, source 26). For local authorities: protection of
catchments and treatment in small networks bring the most (source 33), a rise in non-compliance must be read with the
history of the monitoring, and two deadlines are coming, PFAS in the routine control since 2026 and the lead limit dropping
from 10 to 5 µg/L in 2036 (source 26).

## 5. Limits and biases

- **A teaching indicator.** The score is our construction: weights, curves and windows are choices. The sensitivity analysis
  and the personal score page show how much they matter, but the score is never a health verdict.
- **Absence of measurement is not absence of pollutant.** Small networks are tested a few times a year, and many substances
  (PFAS before 2026, some metabolites) were not searched everywhere. A missing family lowers the confidence instead of being
  counted as perfect.
- **Monitoring changes the curves.** New molecules, reclassifications and limit changes move the national curves on their
  own (H3). Every chart that crosses such a date carries an annotation.
- **Two sources of truth for chemistry.** Official verdicts and our recomputation differ before 2023 (derogations, old
  limits). The app shows both and explains the gap on *Behind the numbers*.
- **No population per network.** The population served by each network is not in the data, so the number of people behind a
  town with a non-conformity is an upper bound, and towns are not weighted by the people each network serves.
- **2026 is partial** (January to August) and is always marked as such. The overseas departments are completed progressively
  by the producer.
- **The Mediterranean coast is approximated** by the coastal Mediterranean departments outside mountain areas, because the
  national list of coastal towns could not be downloaded (dead link). The app says so wherever the group appears.
- **Correlation is not causation.** The maps and correlations say where and how much, never why.
- **Producer warning.** The producer corrected a publication anomaly, with past years re-published up to 2024. The local files
  are identical to the online versions (size and SHA1 checked on 19 October 2026).

## 6. How to run

The app reads only `data/processed/`, which is in the repository: no raw data is needed to run it.

With `make` (Linux, macOS, or Windows with make installed):

```bash
make setup   # virtual environment + pinned dependencies
make run     # streamlit run app.py
make test    # pytest
make data    # optional: download the raw data and rebuild data/processed/ (about 25 minutes the first time)
```

On Windows PowerShell without `make`:

```powershell
.\make.ps1 setup
.\make.ps1 run
.\make.ps1 test
.\make.ps1 data
```

Or by hand, on any system:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt        # Windows: .venv\Scripts\pip install -r requirements.txt
.venv/bin/streamlit run app.py                   # Windows: .venv\Scripts\streamlit run app.py
```

Requires Python 3.11 or later (developed and deployed with 3.12). Dependencies are pinned in `requirements.txt`; the random
draw of a witness town uses the constant `SEED = 42` in `config.py`. Long pipeline steps can run in the background with a log:
`.\scripts\run_logged.ps1 03_build_aggregates`.

The test suite (`make test`, 271 tests) covers the parsing rules, the score formulas on synthetic data, the integrity
of the committed tables, the personal score engine against the published scores, the PDF report in both languages, and
opens every page in English and in French, with extreme filters (Mayotte with PFAS and 2026 alone, Corse in 2016...).

**Performance.** `scripts/perf_audit.py` drives a real browser (Playwright with the installed Chrome, tools in
`requirements-dev.txt`) and measures every page load and interaction, both the time until the app is usable again and the
time the browser was frozen. It found that Streamlit's selectbox, given the 34,812 towns, froze the page for 4 to 25 seconds
when its field was emptied: the browser drew every option. The town search now runs on the server
(`utils/town_search.py`, built on `streamlit-searchbox`): the browser only receives the five examples or the 20 best
matches, the box lives in a fragment so that typing does not rerun the page, and the report of each network is cached.
`tests/test_performance.py` fails if a widget sends more than 2,000 options to the browser, if a key interaction takes more
than 3 seconds on the server, or if emptying the town field freezes a real browser for more than 1 second. The page *Explore the data* reads only small precomputed tables, and its three controls live in fragments, so
that changing one redraws one chart: `tests/test_explore.py` fails if any of its controls takes more than 1.5 seconds
on the server (measured 0.1 to 0.3 s; 0.2 to 0.4 s in Chrome).

## 7. Project structure

```
app.py                  page config, language, menu (order of the story) under the author block, sidebar, footer
config.py               paths, periods, thresholds, score weights, SEED
sections/               one page per file, in the order of the story
  intro.py              What's in my glass? (hook, context, KPIs tied to the filters)
  conclusions.py        What it all means, second in the menu (H1 to H4 with links to the evidence, implications, limits)
  comprendre.py         How to read a water test (fact sheets, parameter search)
  ma_commune.py         The water of my town (score, report per network, formulas, history, PDF)
  comparer.py           Town against town (2 to 6 towns, groups of towns)
  overview.py           The map of France (choropleth, rankings, H1, H2, distribution, trend)
  deep_dives.py         What we look for, what we find (H3, nitrates, PFAS, seasons, hardness H4)
  mon_score.py          Build your own score (weights, severities, thresholds)
  explore.py            Explore the data (the three files and their keys, real rows, distributions, Spearman matrix,
                        scatter plot of any two department indicators)
  data_quality.py       Behind the numbers (missing values, checks, official vs recomputed, coverage, biases)
  about.py              Credits, licences, how it was built
utils/
  io.py                 cached loading of data/processed/, DuckDB connections, town search
  prep.py               parsing macros, thresholds, parameter families
  score.py              score, sub-scores, grade, confidence, rule-based report
  custom_score.py       fast recomputation of the score with the reader's settings
  town_report.py        generated explanation and the PDF report of a town (fpdf2)
  compare_report.py     texts of the comparison and its PDF report (same rules on the page and in the PDF)
  town_search.py        town search box shared by the pages (server-side matches, see section 6)
  filters.py, metrics.py, viz.py, i18n.py, texts/   sidebar, KPIs, chart style, translation (English and French)
scripts/                01_download -> 02_build_parquet -> 03_build_aggregates -> 04_referentiels -> 05_build_scores
                        -> 06_build_app_tables -> 07_build_explore_tables; explore/ holds the phase-0 queries behind
                        the data dictionary;
                        perf_audit.py measures page loads and interactions in a real browser (Playwright)
assets/fonts/           IBM Plex and Fraunces (SIL Open Font License) for the PDF report
assets/efrei-logo-*.png EFREI logo of the sidebar, black (light theme) and white (dark theme), 400 px, 16 colours,
                        transparent background (5 and 7 KB); the original PNGs stay out of git
data/processed/         small tables read by the app (committed); data/raw and data/interim are never committed
tests/                  pytest
docs/                   progress log, data dictionary, sources, storyboard, witness towns
LICENSE                 MIT licence of the code (the data stays under Licence Ouverte 2.0)
DATASET.md              citation and links of the dataset (the raw files are downloaded by make data)
```

## 8. Credits

Made by Florian Giraud ([LinkedIn](https://www.linkedin.com/in/florian-giraud-67883a291/)), EFREI Paris, Data & AI track, 2026. Data: French Ministry of Health, Licence Ouverte 2.0 (citation
above). Health and regulatory sources: WHO, Santé publique France, Anses, the regional health agencies, EUR-Lex and
Légifrance, all listed in [docs/sources.md](docs/sources.md). Geography: geo.api.gouv.fr and Etalab contours (Licence
Ouverte 2.0), INSEE density grid, Cerema list of Mountain Act towns. Fonts: Fraunces, IBM Plex Sans and IBM Plex Mono (SIL
Open Font License 1.1). Built with Streamlit, pandas, DuckDB, PyArrow, Plotly, fpdf2 and streamlit-searchbox.

**Licences.** The code of this project is released under the MIT licence ([LICENSE](LICENSE), Florian Giraud, 2026). The data
is not covered by it: the source dataset and the tables derived from it in `data/processed/` remain under the Licence Ouverte
2.0 of their producer, which allows reuse provided the source and the date of update are cited. The fonts in `assets/fonts/`
keep their SIL Open Font License.

## 9. Tools

This project was built with the help of an AI coding assistant, **Claude Code** (Anthropic). I framed the question, chose
the dataset, the audience, the hypotheses and every method decision (score formula, windows, treatment of small networks,
non-relevant metabolites, visual identity, writing rules), and I reviewed the results at the end of each phase. The assistant
wrote most of the code under these instructions, ran the pipeline and the tests, drafted the texts in English and French,
and searched for official sources, which I checked. Two rules framed its work: no number is shown without being computed
from the data or cited with its source in `docs/sources.md`, and every text of the app and of the PDF report is generated by
fixed rules from the data, not by an AI at run time. The decisions and their reasons are logged in
[docs/AVANCEMENT.md](docs/AVANCEMENT.md) (in French).

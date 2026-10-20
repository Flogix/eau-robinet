# Storyboard: Is my tap water good?

The app is read like an investigation, in the order of the sidebar. It opens on a hook (water that makes people ill is not a
thing of the past), gives the reader the tools to read a water test, answers their personal question (my town), widens the
view (other towns, the map), digs into what the curves really mean, lets the reader question our own method, and ends on
what it all means. Two pages stand apart, "Behind the numbers" and "About", for readers who want the method and the credits.

Every page opens with a sentence that states its insight, computed from the data. Every chart has a title that says what it
shows, a caption that describes it (also used as alternative text), the source, and a short paragraph that says what to take
away. All numbers below come from the current version of the app (data up to 31 August 2026).

The sidebar holds the language switch (English, official, or French), and three filters: period, region and kind of town.
On the map page, it also holds the variable selection: what the map shows.
A filter that does nothing on the open page is greyed out, and a short note says why, so that no control is decorative.

---

## 1. What's in my glass? (`sections/intro.py`)

**Question.** Why should I care about the water from my tap, and how good is it in France overall?

**Visuals.** Four indicators (KPIs) tied to the filters: the share of bacteriological and of chemical samples that met the
health limits, with the change against the previous year, the number of towns with at least one non-compliance, and the
median score. A line chart shows the share of samples that failed a health limit, year by year, with the partial year 2026
shaded. A town search box sends the reader straight to their town.

**Insight.** "Over 2016 to 2025 in all of France, 98.0% of bacteriological samples and 97.0% of chemical samples met the
health limits." The hook comes first: the WHO and Santé publique France figures show that waterborne outbreaks still happen,
and the page says honestly that there is no official count of deaths in France. Then the page states the four hypotheses
the app will test.

**Interactions.** Period, region and kind of town change the KPIs and the curve. The search box opens the town page.

## 2. How to read a water test (`sections/comprendre.py`)

**Question.** What does a water test say, and what is serious?

**Visuals.** A search over the 1,789 parameters of the dataset, with 20 sourced fact sheets (what it is, where it comes from,
possible health effects, the threshold and why, what happens when it is exceeded) and, for each one, what the data says. The
four families of parameters (bacteria, health chemistry, comfort, information) are explained. A bar chart shows the share of
samples above the threshold for nineteen key parameters, and a table lists the thresholds as written in the data.

**Insight.** "In 2025, the parameter most often above its threshold was chloridazon-desphenyl, a pesticide metabolite: 20.0%
of the samples where it was searched." A limit (health) is not a reference (comfort), and a value below the quantification
limit is not a detection.

**Interactions.** Search as you type; the period filter changes the year of the chart.

## 3. The water of my town (`sections/ma_commune.py`)

**Question.** Is the water of my town good, and why?

**Visuals.** A gauge places the score on the A to E scale; horizontal bars give the three marks (bacteria, health chemistry,
comfort) with their weights. A generated paragraph says how many points the town loses, in which family and because of which
substance, and places it against the national and departmental medians. A table lists the distribution networks of the town
and one tab per network holds a rule-based report, each sentence labelled Good, Above limit, Watch, Note or Not tested (a
word, never a colour alone). The six formulas of the score are shown in LaTeX, each followed by a sentence. A line chart
follows one substance over ten years, per network, with the regulatory threshold as a dashed line.

**Insight.** Example of Paris: "84.1/100, grade B, confidence high"; it loses 11.7 points in health chemistry, mainly because
of one lead measurement above the limit, and sits 5.1 points below the national median.

**Interactions.** Town search (accents ignored, homonyms told apart by their department); the substance followed in the
history; a shareable link (`?insee=`); two buttons download the **PDF report** of the town, in English or in French, with the
same content and the visual identity of the app.

## 4. Town against town (`sections/comparer.py`)

**Question.** Is a big city better than a village, a mountain town better than a seaside town?

**Visuals.** Grouped bars give the three marks of two to six towns side by side; a generated paragraph explains the gap
between the best and the weakest; a table gives key facts. Then box plots show how the scores of whole groups of towns spread
(mountain against Mediterranean coast, urban against rural, size of the town), so that distributions are compared, not
averages.

**Insight.** "Marseille scores 98.7 (A) and Lille 57.4 (D): a gap of 41.3 points." For groups: "the median score is 95.8 for
the Mediterranean coast (approximation) and 88.7 for mountain towns; 6% of mountain towns are graded D or E, against 2%."

**Interactions.** Choice of towns, choice of grouping, region filter.

## 5. The map of France (`sections/overview.py`)

**Question.** Where are the problems?

**Visuals.** KPIs, a choropleth map of the departments (score, bacteria, chemistry, comfort, or one family over the period),
a computed paragraph "what the map says" with prudent, sourced hypotheses, a ranking of the best and worst departments, a
scatter plot of the departments by bacterial and chemical failure rates (H2), the failure rate by size of network (H1), the
histogram of town scores, and the trend of the chosen family.

**Insight.** "The median score of the towns ranges from 57/100 in Aisne to 99/100 in Bouches-du-Rhône." H2: "the rank
correlation between the two failure rates is ρ = 0.05: almost none." H1: "networks tested fewer than 12 times a year carry 73%
of the bacterial failures for 26% of the samples."

**Interactions.** In the sidebar, under the filters, the variable shown by the map ("What the map shows": score, one of
the three marks, or one family over the period), then period, region and kind of town; on the page, the number of
departments at each end of the ranking;
hover on every department.

## 6. What we look for, what we find (`sections/deep_dives.py`)

**Question.** Chemical non-compliance nearly doubled in 2021: did the water get worse?

**Visuals.** Told as three clues. Clue 1, a line chart of the number of different parameters measured each year. Clue 2,
stacked bars of limit exceedances by group of substances with the official non-compliant samples as a line, and annotations
for each monitoring change (new metabolites, Anses reclassifications, PFAS in the routine control from 2026). Clue 3, one
metabolite at a time, samples where it was found and above each threshold. Then four tabs: nitrates (histogram with the
50 mg/L limit), PFAS, the seasons of bacterial failures, hardness by region (H4). A link leads to the personal score page.

**Insight.** "Chemically non-compliant samples went from 6,219 a year (2016 to 2020) to 11,412 (2021 to 2024), then fell to
8,742 in 2025. Three families of pesticide metabolites, newly searched or reclassified, account for 58% of the limit
exceedances of 2021 to 2024." What we look for changes what we find.

**Interactions.** Choice of molecule in clue 3; tabs; period filter for the seasons.

## 7. Build your own score (`sections/mon_score.py`)

**Question.** Our score rests on choices. What if I made them differently?

**Visuals.** Three groups of settings: the weights of the three families; the severity of five groups of substances
(pesticides, nitrates, metals, PFAS, disinfection by-products, from x0.5 to x3) and how hard a bacterial failure counts; the
thresholds of nitrates, lead, arsenic, PFAS and each pesticide. Then the official and personal score of a town with its rank
and the share of towns that change grade, grouped bars of the three marks of the town (official against personal), grouped
bars of the grades of all French towns (official against personal) with the rank correlation, the ten lowest-scoring large
towns with the reader's settings, and the sensitivity table of fourteen fixed variants.

**Insight.** Most settings move the letters more than the order: the towns at the bottom stay at the bottom. A clear warning
says that these settings are personal and change nothing to the regulatory limits; only the health agency can judge a water.

**Interactions.** Every slider recomputes the 23,000 networks and 35,000 towns in about a tenth of a second; a button goes
back to the official settings; the town is shared with the town page.

## 8. What it all means (`sections/conclusions.py`)

**Question.** So, is my tap water good, and what should we do?

**Visuals.** Each hypothesis restated in a box (hypothesis, what the data says, verdict), one summary chart of limit
exceedances with and without the three metabolite families, then implications and limits.

**Insight.** "In 2025, 98.3% of bacterial samples and 97.0% of chemical samples met the health limits. French tap water is
good in the vast majority of places; the problems exist, but they are concentrated and, for a large part, explainable." H1,
H2, H3 and H4 are confirmed, with their numbers. For a resident: read the report, not only the grade, and watch the
confidence. For local authorities: small networks first, read curves with the history of the monitoring, prepare for PFAS
and the lower lead limit.

**Interactions.** None on purpose: this page concludes.

## 9. Behind the numbers (`sections/data_quality.py`)

**Question.** Can we trust the data and our processing?

**Visuals.** A heatmap of empty cells column by column and year by year, results by kind of value, official verdict against
our recomputation, a histogram of samples per network, and the list of biases and limits.

**Insight.** "88 of the 88 automatic checks pass." "66% of the results are below the quantification limit." "For bacteria,
our recomputation finds 100.0% of the samples declared non-compliant; for chemistry the two differ in 2016 to 2022, for
reasons we could trace" (derogations, old selenium and antimony limits).

**Interactions.** Choice of file for the heatmap; period filter.

## 10. About this project (`sections/about.py`)

Credits, licences, links to the code and to the sources, and how the app was built.

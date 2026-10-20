"""Page "Behind the numbers": data quality, checks, official vs recomputed verdicts, coverage, biases."""

T = {
    "dq.kicker": {"en": "Transparency", "fr": "Transparence"},
    "dq.title": {"en": "Behind the numbers", "fr": "Les coulisses des chiffres"},
    "dq.lede": {
        "en": "An investigation is only as good as its data. This page shows what the raw files look like, what we "
              "checked, where our recomputation differs from the official verdicts, and what the data cannot tell.",
        "fr": "Une enquête ne vaut que par ses données. Cette page montre à quoi ressemblent les fichiers bruts, ce que "
              "nous avons vérifié, où notre recalcul diffère des verdicts officiels, et ce que les données ne peuvent "
              "pas dire."},
    "dq.headline": {
        "en": "{ok} of the {n} automatic checks pass: no duplicate left, no result without its sample, no row multiplied "
              "by a join, and all {m} million results read.",
        "fr": "{ok} des {n} contrôles automatiques passent : plus aucun doublon, aucun résultat sans son prélèvement, "
              "aucune ligne multipliée par une jointure, et les {m} millions de résultats lus."},
    "dq.pipeline": {
        "en": "The raw files weigh about 22 GB of text for eleven years. A pipeline of six scripts turns them into small "
              "tables: it extracts one year at a time, reads every value as text, then converts decimal commas, values "
              "written as \"<0.05\" and dates, keeps one result per sample and parameter, and attaches to each result the "
              "threshold written next to it. A **join** is the operation that links two tables, here the results to "
              "their samples and the samples to the towns; a careless join can multiply rows, which is why it is checked.",
        "fr": "Les fichiers bruts pèsent environ 22 Go de texte pour onze ans. Une chaîne de six scripts les transforme "
              "en petites tables : elle extrait une année à la fois, lit chaque valeur comme du texte, puis convertit "
              "les virgules décimales, les valeurs écrites « <0,05 » et les dates, garde un résultat par prélèvement et "
              "par paramètre, et rattache à chaque résultat le seuil écrit à côté de lui. Une **jointure** est "
              "l'opération qui relie deux tables, ici les résultats à leurs prélèvements et les prélèvements aux "
              "communes ; une jointure mal faite peut multiplier les lignes, c'est pourquoi elle est contrôlée."},

    "dq.missing.kicker": {"en": "Missing values", "fr": "Valeurs manquantes"},
    "dq.missing.file": {"en": "File", "fr": "Fichier"},
    "dq.missing.help": {"en": "PLV holds the samples, RESULT the analysis results, COM_UDI the link between towns and "
                              "networks.",
                        "fr": "PLV contient les prélèvements, RESULT les résultats d'analyse, COM_UDI le lien entre "
                              "communes et réseaux."},
    "dq.missing.title": {"en": "Share of empty cells, column by column and year by year, in the {file} files",
                         "fr": "Part de cases vides, colonne par colonne et année par année, dans les fichiers {file}"},
    "dq.missing.headline": {
        "en": "In the {file} files, {k} of the {n} columns are complete every year; the emptiest is {col} (up to {share} "
              "empty).",
        "fr": "Dans les fichiers {file}, {k} des {n} colonnes sont complètes chaque année ; la plus vide est {col} "
              "(jusqu'à {share} de cases vides)."},
    "dq.missing.headline.none": {
        "en": "In the {file} files, 0% of the cells are empty, in all {n} columns and every year: the heatmap is uniform "
              "because nothing is missing.",
        "fr": "Dans les fichiers {file}, 0 % de cases vides, dans les {n} colonnes et chaque année : la carte est uniforme "
              "parce que rien ne manque."},
    "dq.missing.caption.none": {
        "en": "Here, 0% of empty cells in every column: each cell shows 0%.",
        "fr": "Ici, 0 % de cases vides dans toutes les colonnes : chaque case affiche 0 %."},
    "dq.missing.x": {"en": "Year of the file", "fr": "Année du fichier"},
    "dq.missing.cb": {"en": "% empty", "fr": "% vide"},
    "dq.missing.hover": {"en": "%{y}, %{x}: %{z:.1f}% empty", "fr": "%{y}, %{x} : %{z:.1f} % vide"},
    "dq.missing.caption": {
        "en": "Heatmap: one row per column of the file, one column per year; the darker the cell, the more empty values.",
        "fr": "Carte de chaleur : une ligne par colonne du fichier, une colonne par année ; plus la case est foncée, plus "
              "il y a de valeurs vides."},

    "dq.status.kicker": {"en": "What a result looks like", "fr": "À quoi ressemble un résultat"},
    "dq.status.headline": {
        "en": "{share} of the results are below the quantification limit: they count as zero when thresholds are checked, "
              "and never as a detection.",
        "fr": "{share} des résultats sont inférieurs à la limite de quantification : ils comptent pour zéro quand on "
              "vérifie les seuils, et jamais comme une détection."},
    "dq.status.title": {"en": "Analysis results per year, by kind of value", "fr": "Résultats d'analyse par année, selon le type de valeur"},
    "dq.status.y": {"en": "Results (millions)", "fr": "Résultats (millions)"},
    "dq.status.hover": {"en": "{y}: {v} million", "fr": "{y} : {v} millions"},
    "dq.status.caption": {
        "en": "Stacked bars: number of results per year, split by the kind of raw value; one row per sample and parameter, "
              "the laboratory measurement being kept when a field measurement also exists.",
        "fr": "Barres empilées : nombre de résultats par année, selon le type de valeur brute ; une ligne par prélèvement "
              "et par paramètre, la mesure de laboratoire étant gardée quand une mesure de terrain existe aussi."},
    "st.not_quantified": {"en": "Below the quantification limit", "fr": "Sous la limite de quantification"},
    "st.quantified": {"en": "Quantified value", "fr": "Valeur quantifiée"},
    "st.qualitative": {"en": "Qualitative (odour, taste…)", "fr": "Qualitatif (odeur, saveur…)"},
    "st.not_measured": {"en": "Not measured (left out)", "fr": "Non mesuré (écarté)"},
    "st.missing": {"en": "Empty", "fr": "Vide"},
    "st.unreadable": {"en": "Unreadable", "fr": "Illisible"},
    "st.above": {"en": "Above a measuring range", "fr": "Au-dessus d'une gamme de mesure"},
    "st.present": {"en": "Presence", "fr": "Présence"},
    "st.uncountable": {"en": "Too many bacteria to count", "fr": "Bactéries trop nombreuses pour être comptées"},
    "st.other": {"en": "Other", "fr": "Autre"},

    "dq.verdict.kicker": {"en": "Official verdict against our recomputation", "fr": "Verdict officiel contre notre recalcul"},
    "dq.verdict.headline": {
        "en": "For bacteria, our recomputation finds {agree} of the samples that the health agencies declared "
              "non-compliant. For chemistry the two differ in 2016 to 2022, for reasons we could trace.",
        "fr": "Pour les bactéries, notre recalcul retrouve {agree} des prélèvements que les agences de santé ont déclarés "
              "non conformes. Pour la chimie, les deux diffèrent de 2016 à 2022, pour des raisons que nous avons "
              "retrouvées."},
    "dq.verdict.title": {"en": "Non-compliant samples per year: official verdict and our recomputation",
                         "fr": "Prélèvements non conformes par année : verdict officiel et notre recalcul"},
    "dq.verdict.chem_off": {"en": "Chemistry, official", "fr": "Chimie, officiel"},
    "dq.verdict.chem_rec": {"en": "Chemistry, recomputed", "fr": "Chimie, recalculé"},
    "dq.verdict.bact_off": {"en": "Bacteria, official", "fr": "Bactéries, officiel"},
    "dq.verdict.bact_rec": {"en": "Bacteria, recomputed", "fr": "Bactéries, recalculé"},
    "dq.verdict.y": {"en": "Non-compliant samples", "fr": "Prélèvements non conformes"},
    "dq.verdict.caption": {
        "en": "Lines: samples declared non-compliant by the health agencies (solid) and samples where we find a value above "
              "the limit written next to it (dotted), for bacteria (brick) and chemistry (blue).",
        "fr": "Courbes : prélèvements déclarés non conformes par les agences de santé (trait plein) et prélèvements où nous "
              "trouvons une valeur au-dessus de la limite écrite à côté (pointillé), pour les bactéries (brique) et la "
              "chimie (bleu)."},
    "dq.verdict.sources": {"en": "Selenium and antimony limits: directives 98/83/EC and (EU) 2020/2184, order of "
                                 "30 December 2022 (docs/sources.md, sources 8 to 10).",
                           "fr": "Limites du sélénium et de l'antimoine : directives 98/83/CE et (UE) 2020/2184, arrêté du "
                                 "30 décembre 2022 (docs/sources.md, sources 8 à 10)."},
    "dq.gap.title": {"en": "Detail of the chemical gap, by parameter", "fr": "Détail de l'écart chimique, par paramètre"},

    "dq.cov.kicker": {"en": "Coverage", "fr": "Couverture"},
    "dq.cov.headline": {"en": "In {y}, half of the {n} networks had {med} samples or fewer; the most tested had {max}.",
                        "fr": "En {y}, la moitié des {n} réseaux a eu {med} prélèvements ou moins ; le plus contrôlé en a eu {max}."},
    "dq.cov.title": {"en": "How many samples each network gets in a year", "fr": "Combien de prélèvements chaque réseau reçoit dans l'année"},
    "dq.cov.x": {"en": "Samples per network in {y} (logarithmic scale)", "fr": "Prélèvements par réseau en {y} (échelle logarithmique)"},
    "dq.cov.y": {"en": "Number of networks", "fr": "Nombre de réseaux"},
    "dq.cov.caption": {
        "en": "Histogram on a logarithmic axis, where each step multiplies by ten (1, 10, 100, 1,000 samples): number of "
              "networks according to how many samples they got in the year.",
        "fr": "Histogramme sur un axe logarithmique, où chaque graduation multiplie par dix (1, 10, 100, 1 000 "
              "prélèvements) : nombre de réseaux selon le nombre de prélèvements reçus dans l'année."},
    "dq.checks.title": {"en": "All {n} automatic checks", "fr": "Les {n} contrôles automatiques"},
    "dq.checks.pass": {"en": "pass", "fr": "réussi"},
    "dq.checks.fail": {"en": "fail", "fr": "échec"},

    "dq.limits.kicker": {"en": "What the data cannot tell", "fr": "Ce que les données ne disent pas"},
    "dq.limits.title": {"en": "Biases and limits to keep in mind", "fr": "Biais et limites à garder en tête"},
    "dq.limits.p1": {
        "en": "Testing frequency depends on the size of the network, so small networks have much more uncertain results. "
              "A sample taken at a treatment plant or a source is attached to every network it feeds, 1.43 networks on "
              "average; national counts use each sample only once. The population served by each network is not in the "
              "data, so population figures count a whole town as soon as one of its networks is affected: they are upper "
              "bounds.",
        "fr": "La fréquence des contrôles dépend de la taille du réseau, si bien que les petits réseaux ont des résultats "
              "bien plus incertains. Un prélèvement fait à l'usine ou au captage est rattaché à chaque réseau qu'il "
              "alimente, 1,43 réseau en moyenne ; les comptes nationaux n'utilisent chaque prélèvement qu'une fois. La "
              "population desservie par chaque réseau n'est pas dans les données : les chiffres de population comptent "
              "une commune entière dès qu'un de ses réseaux est touché, ce sont des bornes hautes."},
    "dq.limits.p2": {
        "en": "2026 stops at 31 August, and overseas departments are completed progressively by the producer, who also "
              "corrected a publication error and republished the years up to 2024; our files match the online versions, "
              "checked by size and fingerprint on 19 October 2026. What is not measured is not absent: PFAS were rarely "
              "measured before 2025, and there is no microplastics parameter in the data. Finally, the Mediterranean "
              "coast is an approximation, built from the coastal departments outside mountain areas.",
        "fr": "2026 s'arrête au 31 août, et les départements d'outre-mer sont complétés progressivement par le producteur, "
              "qui a aussi corrigé une erreur de diffusion et republié les années jusqu'en 2024 ; nos fichiers "
              "correspondent aux versions en ligne, vérifiés par taille et empreinte le 19 octobre 2026. Ce qui n'est pas "
              "mesuré n'est pas absent : les PFAS étaient rarement mesurés avant 2025, et les données ne contiennent aucun "
              "paramètre « microplastiques ». Enfin, le littoral méditerranéen est une approximation, construite à partir "
              "des départements côtiers hors zones de montagne."},
}

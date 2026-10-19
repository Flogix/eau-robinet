"""Page "What we look for, what we find": H3 as a story, focus by family (H4), what-if weights."""

T = {
    "mon.kicker": {"en": "The main finding", "fr": "Le résultat principal"},
    "mon.title": {"en": "What we look for, what we find", "fr": "Ce qu'on cherche, ce qu'on trouve"},
    "mon.lede": {
        "en": "Between 2020 and 2021, the number of chemically non-compliant samples in France nearly doubled. Did the "
              "water suddenly get worse? The data says something else.",
        "fr": "Entre 2020 et 2021, le nombre de prélèvements non conformes en chimie a presque doublé en France. L'eau "
              "s'est-elle soudain dégradée ? Les données disent autre chose."},
    "mon.headline": {
        "en": "Chemically non-compliant samples went from {before} a year (2016 to 2020) to {during} (2021 to 2024), then "
              "fell to {y2025} in 2025. Three families of pesticide metabolites, newly searched or reclassified, account "
              "for {meta} of the limit exceedances of 2021 to 2024.",
        "fr": "Les prélèvements non conformes en chimie sont passés de {before} par an (2016 à 2020) à {during} (2021 à "
              "2024), puis sont retombés à {y2025} en 2025. Trois familles de métabolites de pesticides, nouvellement "
              "cherchés ou reclassés, expliquent {meta} des dépassements de limite de 2021 à 2024."},

    "mon.s1.kicker": {"en": "Clue 1", "fr": "Indice 1"},
    "mon.s1.title": {"en": "Laboratories search for more and more molecules", "fr": "Les laboratoires cherchent de plus en plus de molécules"},
    "mon.s1.text": {
        "en": "A substance can only be found if someone looks for it. The list of parameters measured in France grew "
              "from {a} in 2016 to {b} in 2025, and most of the new ones are pesticides and their **metabolites**, the "
              "molecules a pesticide turns into as it breaks down in soil and water.",
        "fr": "On ne trouve une substance que si on la cherche. La liste des paramètres mesurés en France est passée de "
              "{a} en 2016 à {b} en 2025, et la plupart des nouveaux sont des pesticides et leurs **métabolites**, les "
              "molécules que devient un pesticide en se dégradant dans le sol et l'eau."},
    "mon.s1.chart": {"en": "Number of different parameters measured at least once in the year",
                     "fr": "Nombre de paramètres différents mesurés au moins une fois dans l'année"},
    "mon.s1.all": {"en": "All parameters", "fr": "Tous les paramètres"},
    "mon.s1.pest": {"en": "Pesticides and their metabolites with a limit", "fr": "Pesticides et métabolites avec une limite"},
    "mon.s1.y": {"en": "Different parameters measured", "fr": "Paramètres différents mesurés"},
    "mon.s1.hover": {"en": "{y}: {v} parameters", "fr": "{y} : {v} paramètres"},
    "mon.s1.caption": {
        "en": "Two lines: all parameters (teal) and pesticides with their metabolites that carry a limit (ochre), per year.",
        "fr": "Deux courbes : tous les paramètres (bleu-vert) et les pesticides avec leurs métabolites qui ont une limite "
              "(ocre), par année."},
    "mon.s1.take": {
        "en": "The growth is steady rather than sudden, so it cannot by itself explain a jump in 2021. The next clue is "
              "which molecules entered the list, and when.",
        "fr": "La hausse est régulière plutôt que brutale : elle ne peut pas expliquer à elle seule un saut en 2021. "
              "L'indice suivant, c'est quelles molécules sont entrées dans la liste, et quand."},

    "mon.s2.kicker": {"en": "Clue 2", "fr": "Indice 2"},
    "mon.s2.title": {"en": "Three molecules make the curve", "fr": "Trois molécules font la courbe"},
    "mon.s2.text": {
        "en": 'When we split the limit exceedances by substance, three families stand out, all of them metabolites of pesticides. The metabolites of **chloridazon** enter the data in 2021 and immediately account for thousands of exceedances. **ESA-metolachlor** grows until 2021, then disappears from the exceedances in 2023. **Chlorothalonil R471811** appears in 2023 and vanishes in 2025.',
        "fr": "Quand on répartit les dépassements de limite par substance, trois familles ressortent, toutes des métabolites de pesticides. Les métabolites de la **chloridazone** entrent dans les données en 2021 et comptent aussitôt des milliers de dépassements. L'**ESA-métolachlore** augmente jusqu'en 2021, puis disparaît des dépassements en 2023. Le **chlorothalonil R471811** apparaît en 2023 et s'efface en 2025."},
    "mon.s2.chart": {"en": "Limit exceedances per year by group of substances, and officially non-compliant samples",
                     "fr": "Dépassements de limite par année et par groupe de substances, et prélèvements officiellement non conformes"},
    "mon.grp.cldz": {"en": "Chloridazon metabolites", "fr": "Métabolites de la chloridazone"},
    "mon.grp.esa": {"en": "ESA-metolachlor", "fr": "ESA-métolachlore"},
    "mon.grp.chlo": {"en": "Chlorothalonil metabolites", "fr": "Métabolites du chlorothalonil"},
    "mon.grp.pest": {"en": "Other pesticides", "fr": "Autres pesticides"},
    "mon.grp.no3": {"en": "Nitrates", "fr": "Nitrates"},
    "mon.grp.other": {"en": "Other chemistry", "fr": "Autre chimie"},
    "mon.s2.official": {"en": "Officially non-compliant samples", "fr": "Prélèvements officiellement non conformes"},
    "mon.s2.y": {"en": "Number of samples or exceedances", "fr": "Nombre de prélèvements ou de dépassements"},
    "mon.s2.x": {"en": "Year (2026: January to August)", "fr": "Année (2026 : janvier à août)"},
    "mon.s2.hover": {"en": "{y}: {v} exceedances", "fr": "{y} : {v} dépassements"},
    "mon.s2.hover.off": {"en": "{y}: {v} non-compliant samples", "fr": "{y} : {v} prélèvements non conformes"},
    "mon.ev.cldz": {"en": "2021: chloridazon<br>metabolites searched", "fr": "2021 : métabolites<br>de la chloridazone cherchés"},
    "mon.ev.esa": {"en": "30/09/2022: ESA-metolachlor<br>judged non-relevant", "fr": "30/09/2022 : ESA-métolachlore<br>jugé non pertinent"},
    "mon.ev.chlo": {"en": "29/04/2024: chlorothalonil<br>R471811 non-relevant", "fr": "29/04/2024 : chlorothalonil<br>R471811 non pertinent"},
    "mon.ev.pfas": {"en": "01/01/2026: PFAS in<br>the routine control", "fr": "01/01/2026 : PFAS dans<br>le contrôle courant"},
    "mon.s2.caption": {
        "en": "Stacked bars: limit exceedances per year, one count per sample and substance, coloured by group; the "
              "dark grey line with diamonds is the number of samples officially declared non-compliant. Dotted "
              "vertical lines mark the changes in what was searched and how it was classified.",
        "fr": "Barres empilées : dépassements de limite par année, un compte par prélèvement et par substance, colorés "
              "par groupe ; la ligne gris foncé à losanges est le nombre de prélèvements officiellement déclarés non "
              "conformes. Les lignes verticales en pointillé marquent les changements dans ce qui était cherché et dans "
              "la façon de le classer."},
    "mon.s2.take": {
        "en": "The official line follows the coloured blocks. It rises when the chloridazon metabolites enter the "
              "monitoring and falls when ESA-metolachlor, then chlorothalonil, stop counting as exceedances. The water "
              "did not change overnight; what changed is what was searched and the threshold used to judge it.",
        "fr": "La ligne officielle suit les blocs colorés. Elle monte quand les métabolites de la chloridazone entrent "
              "dans le contrôle et redescend quand l'ESA-métolachlore, puis le chlorothalonil, cessent de compter comme "
              "dépassements. L'eau n'a pas changé du jour au lendemain ; ce qui a changé, c'est ce qu'on cherchait et le "
              "seuil utilisé pour le juger."},

    "mon.s3.kicker": {"en": "Clue 3", "fr": "Indice 3"},
    "mon.s3.title": {"en": "Same molecule, new threshold", "fr": "Même molécule, nouveau seuil"},
    "mon.s3.text": {
        "en": 'Why do some exceedances vanish? Because the national health safety agency, Anses, reviewed these metabolites and classified them as **non-relevant**, a term of the regulation. From then on they are no longer compared with the limit of 0.1 µg/L but with an **indicative value** of 0.9 µg/L, nine times higher. According to the health authorities, going above it does not prevent drinking the water, but the supplier must set up an action plan.',
        "fr": "Pourquoi certains dépassements disparaissent-ils ? Parce que l'Anses, l'agence nationale de sécurité sanitaire, a réexaminé ces métabolites et les a classés **non pertinents**, un terme de la réglementation. Dès lors, ils ne sont plus comparés à la limite de 0,1 µg/L, mais à une **valeur indicative** de 0,9 µg/L, neuf fois plus haute. Selon les autorités sanitaires, la dépasser n'empêche pas de boire l'eau, mais le distributeur doit mettre en place un plan d'actions."},
    "mon.s3.pick": {"en": "Molecule", "fr": "Molécule"},
    "mon.s3.chart": {"en": "{mol}: samples where it was found, and above each threshold, year by year",
                     "fr": "{mol} : prélèvements où il a été trouvé, et au-dessus de chaque seuil, année par année"},
    "mon.s3.limit": {"en": "Above the 0.1 µg/L limit", "fr": "Au-dessus de la limite de 0,1 µg/L"},
    "mon.s3.ind": {"en": "Above the 0.9 µg/L indicative value", "fr": "Au-dessus de la valeur indicative de 0,9 µg/L"},
    "mon.s3.det": {"en": "Found, at any level", "fr": "Trouvé, à n'importe quel niveau"},
    "mon.s3.y": {"en": "Number of samples", "fr": "Nombre de prélèvements"},
    "mon.s3.ev": {"en": "judged non-relevant", "fr": "jugé non pertinent"},
    "mon.s3.caption": {
        "en": "Brick bars: samples above the 0.1 µg/L limit; teal hatched bars: above the 0.9 µg/L indicative value; "
              "dotted line: samples where the molecule was found at any level.",
        "fr": "Barres brique : prélèvements au-dessus de la limite de 0,1 µg/L ; barres bleu-vert hachurées : au-dessus "
              "de la valeur indicative de 0,9 µg/L ; ligne pointillée : prélèvements où la molécule a été trouvée, quel "
              "que soit le niveau."},
    "mon.s3.take": {
        "en": "The dotted line does not collapse after the reclassification: in 2025 the molecule was still found in {n} "
              "samples. Only the verdict changed. A drop in non-compliance can therefore come from a new rule rather than "
              "from cleaner water, and a rise can come from a new search rather than from dirtier water.",
        "fr": "La ligne pointillée ne s'effondre pas après le reclassement : en 2025, la molécule était encore trouvée dans "
              "{n} prélèvements. Seul le verdict a changé. Une baisse des non-conformités peut donc venir d'une nouvelle "
              "règle plutôt que d'une eau plus propre, et une hausse d'une nouvelle recherche plutôt que d'une eau plus sale."},
    "mon.sources": {
        "en": "Sources of the dates and thresholds: Anses opinions of 30/09/2022 and the 0.9 µg/L indicative value, "
              "Assemblée nationale written question 2237 (answer of 28/03/2023); chlorothalonil R471811, ARS "
              "Hauts-de-France and ARS Bourgogne-Franche-Comté; PFAS from 01/01/2026, ARS Nouvelle-Aquitaine. The first "
              "year of the chloridazon metabolites is read from the data. Full references in docs/sources.md "
              "(sources 5 to 11).",
        "fr": "Sources des dates et des seuils : avis de l'Anses du 30/09/2022 et valeur indicative de 0,9 µg/L, question "
              "écrite 2237 de l'Assemblée nationale (réponse du 28/03/2023) ; chlorothalonil R471811, ARS Hauts-de-France "
              "et ARS Bourgogne-Franche-Comté ; PFAS au 01/01/2026, ARS Nouvelle-Aquitaine. La première année des "
              "métabolites de la chloridazone est lue dans les données. Références complètes dans docs/sources.md "
              "(sources 5 à 11)."},
    "mon.verdict": {
        "en": "**Verdict on H3: confirmed.** Most of the rise and fall of chemical non-compliance between 2021 and 2025 "
              "follows changes in what is searched and how it is classified. This does not prove that the water is "
              "fine, nor that it is worse: it means that a trend in non-compliance must always be read together with "
              "the history of the monitoring.",
        "fr": "**Verdict sur H3 : confirmée.** L'essentiel de la hausse puis de la baisse des non-conformités chimiques "
              "entre 2021 et 2025 suit les changements dans ce qu'on cherche et dans la façon de le classer. Cela ne "
              "prouve ni que l'eau va bien, ni qu'elle va plus mal : cela veut dire qu'une tendance des non-conformités "
              "doit toujours se lire avec l'histoire du contrôle."},

    "mon.focus.kicker": {"en": "Other things we looked at", "fr": "Ce que nous avons aussi regardé"},
    "mon.focus.title": {"en": "Nitrates, PFAS, seasons and limescale", "fr": "Nitrates, PFAS, saisons et calcaire"},
    "mon.tab.no3": {"en": "Nitrates", "fr": "Nitrates"},
    "mon.tab.pfas": {"en": "PFAS", "fr": "PFAS"},
    "mon.tab.season": {"en": "Bacteria by season", "fr": "Bactéries et saisons"},
    "mon.tab.hard": {"en": "Hardness (H4)", "fr": "Dureté (H4)"},
    "mon.no3.headline": {
        "en": "{low} of networks stayed below half of the nitrate limit (25 mg/L) over three years; {above} went above "
              "the 50 mg/L limit at least once.",
        "fr": "{low} des réseaux sont restés sous la moitié de la limite des nitrates (25 mg/L) sur trois ans ; {above} "
              "ont dépassé la limite de 50 mg/L au moins une fois."},
    "mon.no3.chart": {"en": "Networks by their highest nitrate level over the last three years",
                      "fr": "Les réseaux selon leur niveau de nitrates le plus haut sur trois ans"},
    "mon.no3.x": {"en": "Highest nitrate level over three years (mg/L, capped at 100)",
                  "fr": "Niveau de nitrates le plus haut sur trois ans (mg/L, plafonné à 100)"},
    "mon.no3.y": {"en": "Number of networks", "fr": "Nombre de réseaux"},
    "mon.no3.thr": {"en": "limit 50 mg/L", "fr": "limite 50 mg/L"},
    "mon.no3.hover": {"en": "highest %{x} mg/L: %{y:,} networks", "fr": "maximum %{x} mg/L : %{y:,} réseaux"},
    "mon.no3.caption": {
        "en": "Histogram: number of networks in each band of 2.5 mg/L of their highest nitrate value, with the 50 mg/L "
              "limit as a dashed brick line. Networks where nitrates were never quantified are not shown.",
        "fr": "Histogramme : nombre de réseaux par tranche de 2,5 mg/L de leur valeur de nitrates la plus haute, avec la "
              "limite de 50 mg/L en tirets brique. Les réseaux où les nitrates n'ont jamais été quantifiés ne sont pas "
              "montrés."},
    "mon.no3.take": {
        "en": 'The bulk of networks sit far from the nitrate limit. The few that cross it form a thin tail on the right of the chart, and their report says so.',
        "fr": "L'essentiel des réseaux est loin de la limite des nitrates. Les quelques réseaux qui la franchissent forment une fine traîne à droite du graphique, et leur rapport le dit."},
    "mon.pfas.headline": {
        "en": "Samples analysed for the sum of twenty PFAS: {a} in 2022, {b} in 2025; {c} of them were above 0.1 µg/L in "
              "2025.",
        "fr": "Prélèvements analysés pour la somme de vingt PFAS : {a} en 2022, {b} en 2025 ; {c} étaient au-dessus de "
              "0,1 µg/L en 2025."},
    "mon.pfas.chart": {"en": "PFAS: samples analysed and samples above the limit, year by year",
                       "fr": "PFAS : prélèvements analysés et prélèvements au-dessus de la limite, année par année"},
    "mon.pfas.n": {"en": "Samples analysed", "fr": "Prélèvements analysés"},
    "mon.pfas.k": {"en": "Above 0.1 µg/L", "fr": "Au-dessus de 0,1 µg/L"},
    "mon.pfas.y": {"en": "Number of samples", "fr": "Nombre de prélèvements"},
    "mon.pfas.caption": {
        "en": "Bars per year: samples analysed for the sum of 20 PFAS (teal) and samples above the 0.1 µg/L limit (brick, "
              "hatched), values written on top.",
        "fr": "Barres par année : prélèvements analysés pour la somme de 20 PFAS (bleu-vert) et prélèvements au-dessus de "
              "la limite de 0,1 µg/L (brique, hachurés), valeurs écrites au-dessus."},
    "mon.pfas.take": {
        "en": 'PFAS, called forever chemicals by the health agencies, were almost never measured before 2025. The lesson of the pesticides applies here too: the first wave of results will look like a sudden problem, while it is mostly a new search. An absence of measurement was never an absence of PFAS.',
        "fr": "Les PFAS, appelés polluants éternels par les agences de santé, n'étaient presque jamais mesurés avant 2025. La leçon des pesticides vaut ici aussi : la première vague de résultats ressemblera à un problème soudain, alors qu'il s'agit surtout d'une nouvelle recherche. Une absence de mesure n'a jamais été une absence de PFAS."},
    "mon.season.note": {"en": "Complete years only: {a} to {b} (2026 lacks September to December).",
                        "fr": "Années complètes seulement : {a} à {b} (il manque septembre à décembre 2026)."},
    "mon.season.headline": {
        "en": "Bacterial non-compliance peaks in {hi} ({hv}) and is lowest in {lo} ({lv}), France, {a} to {b}.",
        "fr": "La non-conformité bactériologique culmine en {hi} ({hv}) et est la plus basse en {lo} ({lv}), France, "
              "{a} à {b}."},
    "mon.season.chart": {"en": "Share of bacterial samples that failed, by month", "fr": "Part des prélèvements bactériologiques non conformes, par mois"},
    "mon.season.y": {"en": "Non-compliant samples (%)", "fr": "Prélèvements non conformes (%)"},
    "mon.season.x": {"en": "Month of sampling", "fr": "Mois du prélèvement"},
    "mon.season.hover": {"en": "{m}: {v}<br>{k} of {n} samples", "fr": "{m} : {v}<br>{k} sur {n} prélèvements"},
    "mon.season.caption": {
        "en": "Bars, one per month: share of bacterial samples officially non-compliant, over the complete years of the "
              "chosen period; the value is written on each bar.",
        "fr": "Barres, une par mois : part des prélèvements bactériologiques officiellement non conformes, sur les années "
              "complètes de la période choisie ; la valeur est écrite sur chaque barre."},
    "mon.season.take": {
        "en": "Failures are about {ratio} times more frequent in the worst month than in the best one. This seasonal "
              "pattern is a correlation: the data does not say what causes it, only when to be more careful.",
        "fr": "Les échecs sont environ {ratio} fois plus fréquents le pire mois que le meilleur. Ce rythme saisonnier est "
              "une corrélation : les données ne disent pas ce qui le cause, seulement quand être plus vigilant."},
    "mon.hard.headline": {
        "en": "The median hardness of networks ranges from {lo_v} °f in {lo} to {hi_v} °f in {hi}. H4 is confirmed: "
              "limescale varies a lot, without any health limit.",
        "fr": "La dureté médiane des réseaux va de {lo_v} °f en {lo} à {hi_v} °f en {hi}. H4 est confirmée : le calcaire "
              "varie beaucoup, sans aucune limite sanitaire."},
    "mon.hard.text": {
        "en": "**Hardness** measures the calcium and magnesium dissolved in the water, which leave limescale in kettles "
              "and pipes. It is expressed in French degrees (°f).",
        "fr": "La **dureté** mesure le calcium et le magnésium dissous dans l'eau, qui laissent du calcaire dans les "
              "bouilloires et les canalisations. Elle s'exprime en degrés français (°f)."},
    "mon.hard.chart": {"en": "Hardness of the networks, region by region", "fr": "La dureté des réseaux, région par région"},
    "mon.hard.x": {"en": "Average hardness of the network over twelve months (°f)",
                   "fr": "Dureté moyenne du réseau sur douze mois (°f)"},
    "mon.hard.caption": {
        "en": "Box plots, one per region, sorted by median: the line in each box is the median network, the box holds "
              "the middle half of the networks.",
        "fr": "Boîtes à moustaches, une par région, triées par médiane : le trait dans chaque boîte est le réseau médian, "
              "la boîte contient la moitié centrale des réseaux."},
    "mon.hard.take": {
        "en": "This is the difference people notice most in their daily life, and it is the one that matters least for "
              "health. That is why hardness is shown in the reports as information and never lowers the score.",
        "fr": "C'est la différence que l'on remarque le plus au quotidien, et c'est celle qui compte le moins pour la "
              "santé. C'est pourquoi la dureté apparaît dans les rapports comme une information et ne fait jamais "
              "baisser le score."},

    "mon.whatif.kicker": {"en": "What if", "fr": "Et si"},
    "mon.whatif.title": {"en": "What if the score weighted things differently?", "fr": "Et si le score pesait les choses autrement ?"},
    "mon.whatif.text": {
        "en": "The default weights, 40% bacteria, 40% health chemistry and 20% comfort, are a choice, not a law. Move "
              "them and see how much the ranking of the networks changes. The weights are rescaled so that they add up "
              "to 100%.",
        "fr": "Les poids par défaut, 40 % bactéries, 40 % chimie sanitaire et 20 % confort, sont un choix, pas une loi. "
              "Déplacez-les et regardez à quel point le classement des réseaux change. Les poids sont remis à l'échelle "
              "pour que leur somme fasse 100 %."},
    "mon.w.micro": {"en": "Weight of bacteria", "fr": "Poids des bactéries"},
    "mon.w.chem": {"en": "Weight of health chemistry", "fr": "Poids de la chimie sanitaire"},
    "mon.w.comfort": {"en": "Weight of comfort", "fr": "Poids du confort"},
    "mon.w.zero": {"en": "At least one weight must be above zero.", "fr": "Au moins un poids doit être supérieur à zéro."},
    "mon.whatif.headline": {
        "en": "With these weights ({w}), {changed} of networks change grade, and the ranking keeps a rank correlation "
              "of ρ = {rho} with the default one (1 would mean the same order).",
        "fr": "Avec ces poids ({w}), {changed} des réseaux changent de note, et le classement garde une corrélation de "
              "rang ρ = {rho} avec celui par défaut (1 voudrait dire le même ordre)."},
    "mon.whatif.chart": {"en": "Share of networks in each grade, default weights against yours",
                         "fr": "Part des réseaux dans chaque note, poids par défaut contre les vôtres"},
    "mon.whatif.default": {"en": "Default weights", "fr": "Poids par défaut"},
    "mon.whatif.yours": {"en": "Your weights", "fr": "Vos poids"},
    "mon.whatif.x": {"en": "Grade", "fr": "Note"},
    "mon.whatif.y": {"en": "Networks (%)", "fr": "Réseaux (%)"},
    "mon.whatif.caption": {
        "en": "Grouped bars: share of networks in each grade with the default weights (grey, hatched) and with yours "
              "(blue), values written on top.",
        "fr": "Barres groupées : part des réseaux dans chaque note avec les poids par défaut (gris, hachuré) et avec les "
              "vôtres (bleu), valeurs écrites au-dessus."},
    "mon.whatif.take": {
        "en": "Grades move, but the order of the networks hardly does: the networks at the bottom stay at the bottom. "
              "That is what makes the score usable despite its arbitrary weights.",
        "fr": "Les notes bougent, mais l'ordre des réseaux presque pas : les réseaux du bas restent en bas. C'est ce qui "
              "rend le score utilisable malgré des poids arbitraires."},
    "mon.sens.title": {"en": "Sensitivity analysis: fourteen variants of the method",
                       "fr": "Analyse de sensibilité : quatorze variantes de la méthode"},
    "mon.sens.caption": {
        "en": "Each row recomputes all the scores with one change to the method. A rank correlation of 1 means the same "
              "order of networks as the default; all variants stay above 0.95, except removing comfort entirely.",
        "fr": "Chaque ligne recalcule tous les scores avec un seul changement de méthode. Une corrélation de rang de 1 "
              "veut dire le même ordre des réseaux que par défaut ; toutes les variantes restent au-dessus de 0,95, sauf "
              "la suppression complète du confort."},
    "mon.sens.variant": {"en": "Variant", "fr": "Variante"},
    "mon.sens.rho_n": {"en": "Rank correlation, networks", "fr": "Corrélation de rang, réseaux"},
    "mon.sens.rho_c": {"en": "Rank correlation, towns", "fr": "Corrélation de rang, communes"},
    "mon.sens.changed": {"en": "Networks changing grade", "fr": "Réseaux changeant de note"},
    "mon.sens.bottom": {"en": "Same bottom 10%", "fr": "Mêmes 10 % du bas"},
    "mon.sens.median": {"en": "Median score", "fr": "Score médian"},
    'variant.default': {"en": 'Default method', "fr": 'Méthode par défaut'},
    'variant.weights equal (1/3 each)': {"en": 'Equal weights (one third each)', "fr": 'Poids égaux (un tiers chacun)'},
    'variant.weights micro-heavy (0.6/0.3/0.1)': {"en": 'Bacteria weighted more (60/30/10)', "fr": 'Bactéries plus lourdes (60/30/10)'},
    'variant.weights chem-heavy (0.3/0.6/0.1)': {"en": 'Chemistry weighted more (30/60/10)', "fr": 'Chimie plus lourde (30/60/10)'},
    'variant.no comfort (0.5/0.5/0)': {"en": 'Comfort removed (50/50/0)', "fr": 'Confort retiré (50/50/0)'},
    'variant.micro k = 10 (first proposal)': {"en": 'Bacteria stricter, k = 10 (first proposal)', "fr": 'Bactéries plus sévères, k = 10 (première proposition)'},
    'variant.micro k = 20': {"en": 'Bacteria much stricter, k = 20', "fr": 'Bactéries beaucoup plus sévères, k = 20'},
    'variant.micro smoothed (12 pseudo-samples at the national rate)': {"en": 'Bacteria smoothed towards the national rate', "fr": 'Bactéries lissées vers le taux national'},
    'variant.max instead of P95': {"en": 'Highest value instead of the 95th percentile', "fr": 'Valeur maximale au lieu du 95e centile'},
    'variant.no exceedance floor': {"en": 'No minimum penalty for an exceedance', "fr": 'Pas de pénalité minimale pour un dépassement'},
    'variant.other penalties x 0': {"en": 'Only the worst substance counts', "fr": 'Seule la pire substance compte'},
    'variant.other penalties x 0.5': {"en": 'Other substances count for half', "fr": 'Les autres substances comptent pour moitié'},
    'variant.comfort cap 30': {"en": 'Comfort penalty capped at 30', "fr": 'Pénalité de confort plafonnée à 30'},
    'variant.comfort cap 80': {"en": 'Comfort penalty capped at 80', "fr": 'Pénalité de confort plafonnée à 80'},
    'variant.steeper curve (20 -> 40 at r = 1)': {"en": 'Steeper penalty at the limit (40 instead of 20)', "fr": 'Pénalité plus raide à la limite (40 au lieu de 20)'},
}

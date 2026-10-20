"""Interpretations under the charts of "What we look for, what we find" and "Behind the numbers":
what we see (computed placeholders), why it is probably so (with the source numbers of docs/sources.md), and limits."""

T = {
    # --- What we look for: clue 1, parameters measured -------------------------------------------------------------
    "an.mon.s1.seen": {
        "en": "The number of parameters in the yearly file went from {a} in 2016 to {b} in 2025, and pesticides with their "
              "metabolites follow the same slow climb.",
        "fr": "Le nombre de paramètres du fichier annuel est passé de {a} en 2016 à {b} en 2025, et les pesticides avec "
              "leurs métabolites suivent la même lente montée."},
    "an.mon.s1.why": {
        "en": "Each regional health agency sets its own list of molecules to search, according to the pesticides sold and "
              "used locally and to past detections (ARS Grand Est, source 20), and the national campaigns of Anses recommend "
              "adding the metabolites they find, such as those of chlorothalonil (sources 6 and 21).",
        "fr": "Chaque agence régionale de santé fixe sa propre liste de molécules à chercher, selon les pesticides vendus et "
              "utilisés localement et les détections passées (ARS Grand Est, source 20), et les campagnes nationales de "
              "l'Anses recommandent d'ajouter les métabolites qu'elles trouvent, comme ceux du chlorothalonil (sources 6 et "
              "21)."},
    "an.mon.s1.lim": {
        "en": "A parameter counts as soon as it is measured once in the year, anywhere in France, and a molecule published "
              "under two codes counts twice. The curve shows the breadth of the search, not how often each molecule is "
              "searched.",
        "fr": "Un paramètre compte dès qu'il est mesuré une fois dans l'année, n'importe où en France, et une molécule "
              "publiée sous deux codes compte deux fois. La courbe montre l'étendue de la recherche, pas la fréquence à "
              "laquelle chaque molécule est cherchée."},

    # --- clue 2, exceedances by group -------------------------------------------------------------------------------
    "an.mon.s2.seen": {
        "en": "The official count of chemically non-compliant samples jumps in 2021, stays high until 2024 and falls in "
              "2025. The coloured blocks that appear and disappear at the same dates are the three metabolite families; "
              "nitrates and the other substances barely move.",
        "fr": "Le compte officiel des prélèvements non conformes en chimie bondit en 2021, reste haut jusqu'en 2024 et baisse "
              "en 2025. Les blocs colorés qui apparaissent et disparaissent aux mêmes dates sont les trois familles de "
              "métabolites ; les nitrates et les autres substances bougent à peine."},
    "an.mon.s2.why": {
        "en": "The chloridazon metabolites were classified relevant by Anses in April 2020 (source 19) and searched from "
              "2021. ESA-metolachlor stopped counting as an exceedance when Anses judged it non-relevant on "
              "30 September 2022 (source 5), and chlorothalonil R471811 when it was reclassified on 29 April 2024 "
              "(source 6). Each date matches a break in the curve.",
        "fr": "Les métabolites de la chloridazone ont été classés pertinents par l'Anses en avril 2020 (source 19) et "
              "cherchés à partir de 2021. L'ESA-métolachlore a cessé de compter comme dépassement quand l'Anses l'a jugé non "
              "pertinent le 30 septembre 2022 (source 5), et le chlorothalonil R471811 lors de son reclassement le "
              "29 avril 2024 (source 6). Chaque date correspond à une cassure de la courbe."},
    "an.mon.s2.lim": {
        "en": "The bars count one exceedance per sample and substance, so a sample with two molecules above their limit "
              "counts twice: bars and the official line are not the same unit. Regions did not add the new molecules at the "
              "same time, which spreads the jumps over several years.",
        "fr": "Les barres comptent un dépassement par prélèvement et par substance : un prélèvement avec deux molécules "
              "au-dessus de leur limite compte deux fois, si bien que barres et ligne officielle ne sont pas dans la même "
              "unité. Les régions n'ont pas ajouté les nouvelles molécules en même temps, ce qui étale les sauts sur "
              "plusieurs années."},

    # --- clue 3, same molecule, new threshold ------------------------------------------------------------------------
    "an.mon.s3.seen": {
        "en": "After the reclassification, the bars of limit exceedances drop to almost nothing while the dotted line of "
              "detections stays high: in 2025 the molecule was still found in {n} samples.",
        "fr": "Après le reclassement, les barres de dépassements de limite tombent presque à rien alors que la ligne "
              "pointillée des détections reste haute : en 2025, la molécule était encore trouvée dans {n} prélèvements."},
    "an.mon.s3.why": {
        "en": "Only the threshold changed: a non-relevant metabolite is compared with an indicative value of 0.9 µg/L "
              "instead of the limit of 0.1 µg/L (sources 5 and 6). The water that reaches the tap did not change on the day "
              "of the decision.",
        "fr": "Seul le seuil a changé : un métabolite non pertinent est comparé à une valeur indicative de 0,9 µg/L au lieu "
              "de la limite de 0,1 µg/L (sources 5 et 6). L'eau qui arrive au robinet n'a pas changé le jour de la décision."},
    "an.mon.s3.lim": {
        "en": "Found means quantified, that is above the smallest amount the laboratory can measure, and that amount differs "
              "between laboratories and years. The number of detections also depends on how many samples were analysed for "
              "the molecule each year.",
        "fr": "Trouvé veut dire quantifié, c'est-à-dire au-dessus de la plus petite quantité que le laboratoire sait mesurer, "
              "et cette quantité varie selon les laboratoires et les années. Le nombre de détections dépend aussi du nombre "
              "de prélèvements analysés pour la molécule chaque année."},

    # --- nitrates --------------------------------------------------------------------------------------------------
    "an.mon.no3.seen": {
        "en": "Most networks pile up far below the limit, with {low} of them under half of it; a thin tail of {above} crosses "
              "50 mg/L at least once in three years.",
        "fr": "La plupart des réseaux s'entassent loin sous la limite, dont {low} sous la moitié ; une fine traîne de "
              "{above} franchit 50 mg/L au moins une fois en trois ans."},
    "an.mon.no3.why": {
        "en": "Nitrates come mostly from agriculture, fertilisers and manure, and from wastewater (WHO, source 23): the "
              "networks of the tail are likely fed by resources exposed to these inputs.",
        "fr": "Les nitrates viennent surtout de l'agriculture, engrais et fumier, et des eaux usées (OMS, source 23) : les "
              "réseaux de la traîne sont probablement alimentés par des ressources exposées à ces apports."},
    "an.mon.no3.lim": {
        "en": "The chart uses the highest value of each network over three years: a single high measurement is enough to "
              "place a network on the right. Networks where nitrates were never quantified are not shown.",
        "fr": "Le graphique utilise la valeur la plus haute de chaque réseau sur trois ans : une seule mesure élevée suffit à "
              "placer un réseau à droite. Les réseaux où les nitrates n'ont jamais été quantifiés ne sont pas montrés."},

    # --- PFAS ------------------------------------------------------------------------------------------------------
    "an.mon.pfas.seen": {
        "en": "The number of samples analysed for the sum of twenty PFAS went from {a} in 2022 to {b} in 2025, and {c} of "
              "them were above 0.1 µg/L in 2025.",
        "fr": "Le nombre de prélèvements analysés pour la somme de vingt PFAS est passé de {a} en 2022 à {b} en 2025, et {c} "
              "étaient au-dessus de 0,1 µg/L en 2025."},
    "an.mon.pfas.why": {
        "en": "The sum of twenty PFAS became part of the routine control on 1 January 2026 (source 11); before that, "
              "measurements were campaigns and local investigations, some of them near industrial sites (source 39).",
        "fr": "La somme de vingt PFAS est entrée dans le contrôle courant le 1er janvier 2026 (source 11) ; avant, les mesures "
              "relevaient de campagnes et d'enquêtes locales, certaines près de sites industriels (source 39)."},
    "an.mon.pfas.lim": {
        "en": "When early measurements are targeted at suspected places, the share of results above the limit can look "
              "higher than in the country as a whole; 2026 is incomplete. Comparing years is not yet meaningful.",
        "fr": "Quand les premières mesures visent des lieux suspects, la part de résultats au-dessus de la limite peut "
              "paraître plus élevée que dans l'ensemble du pays ; 2026 est incomplète. Comparer les années n'a pas encore "
              "de sens."},

    # --- bacteria by season ---------------------------------------------------------------------------------------
    "an.mon.season.seen": {
        "en": "Bacterial failures are {ratio} times more frequent in the worst month than in the best one: {hi} against "
              "{lo}.",
        "fr": "Les échecs bactériologiques sont {ratio} fois plus fréquents le pire mois que le meilleur : {hi} "
              "contre {lo}."},
    "an.mon.season.why": {
        "en": "Health agencies list weather among the causes of bacterial contamination, heavy rain, storms and droughts, "
              "next to poorly protected catchments (ARS Occitanie, source 33). A seasonal rhythm is compatible with this, "
              "but the data does not record the weather, so it remains a hypothesis.",
        "fr": "Les agences de santé citent la météo parmi les causes de contamination bactérienne, fortes pluies, orages et "
              "sécheresses, à côté des captages mal protégés (ARS Occitanie, source 33). Un rythme saisonnier est compatible "
              "avec cela, mais les données n'enregistrent pas la météo : cela reste une hypothèse."},
    "an.mon.season.lim": {
        "en": "The months are added up over all of France and all the complete years of the period; the number of samples "
              "taken can also differ from one month to another.",
        "fr": "Les mois sont additionnés sur toute la France et toutes les années complètes de la période ; le nombre de "
              "prélèvements peut aussi varier d'un mois à l'autre."},

    # --- hardness -------------------------------------------------------------------------------------------------
    "an.mon.hard.seen": {
        "en": "The median hardness goes from {lo_v} °f in {lo} to {hi_v} °f in {hi}, and each region spreads widely around "
              "its median.",
        "fr": "La dureté médiane va de {lo_v} °f en {lo} à {hi_v} °f en {hi}, et chaque région s'étale largement autour de "
              "sa médiane."},
    "an.mon.hard.why": {
        "en": "Hardness is the calcium and magnesium dissolved in the water (source 37): it follows the ground the water "
              "flows through, which changes from one network to the next, more than administrative borders.",
        "fr": "La dureté est le calcium et le magnésium dissous dans l'eau (source 37) : elle suit les terrains que traverse "
              "l'eau, qui changent d'un réseau à l'autre, plus que les frontières administratives."},
    "an.mon.hard.lim": {
        "en": "Each network is represented by its average over twelve months, whatever the number of people it serves. And "
              "hard water has no effect on health according to the health agencies (source 37): this chart is about "
              "comfort.",
        "fr": "Chaque réseau est représenté par sa moyenne sur douze mois, quel que soit le nombre de personnes desservies. "
              "Et une eau dure n'a pas d'effet sur la santé selon les agences de santé (source 37) : ce graphique parle de "
              "confort."},

    # --- what if ---------------------------------------------------------------------------------------------------
    "an.mon.whatif.seen": {
        "en": "With your weights, {changed} of the networks change grade, but the order of the networks keeps a rank "
              "correlation of {rho} with the default one.",
        "fr": "Avec vos poids, {changed} des réseaux changent de note, mais l'ordre des réseaux garde une corrélation de rang "
              "de {rho} avec celui par défaut."},
    "an.mon.whatif.why": {
        "en": "A network that fails in one family loses many points in that family, and the weights only change how many "
              "count: the networks at the bottom stay at the bottom, only the letters move.",
        "fr": "Un réseau qui échoue dans une famille y perd beaucoup de points, et les poids ne changent que la part qui "
              "compte : les réseaux du bas restent en bas, seules les lettres bougent."},
    "an.mon.whatif.lim": {
        "en": "Weights are a choice, not a scientific result. The sensitivity table below tests fourteen other variants of "
              "the method, not only the weights.",
        "fr": "Les poids sont un choix, pas un résultat scientifique. Le tableau de sensibilité ci-dessous teste quatorze "
              "autres variantes de la méthode, pas seulement les poids."},

    # --- Behind the numbers ---------------------------------------------------------------------------------------
    "an.dq.missing.seen": {
        "en": "Most columns are complete every year; a few rows are dark from top to bottom.",
        "fr": "La plupart des colonnes sont complètes chaque année ; quelques lignes sont foncées de haut en bas."},
    "an.dq.missing.seen.none": {
        "en": "Not a single cell is empty in this file, in any column or year: the town-network link is always filled in.",
        "fr": "Aucune case n'est vide dans ce fichier, quelles que soient la colonne et l'année : le lien entre communes et "
              "réseaux est toujours renseigné."},
    "an.dq.missing.why": {
        "en": "Some columns are left empty by the producer, and an empty limit or reference simply means that the parameter "
              "has no threshold (producer documentation, source 2).",
        "fr": "Certaines colonnes sont laissées vides par le producteur, et une limite ou une référence vide veut simplement "
              "dire que le paramètre n'a pas de seuil (documentation du producteur, source 2)."},
    "an.dq.missing.lim": {
        "en": "Missing values are measured on the files as published, before any cleaning; a complete cell can still hold "
              "a code such as \"not measured\", which is counted in the next chart.",
        "fr": "Les valeurs manquantes sont mesurées sur les fichiers tels que publiés, avant tout nettoyage ; une case "
              "remplie peut quand même contenir un code comme « non mesuré », compté dans le graphique suivant."},
    "an.dq.status.seen": {
        "en": "{share} of the results are below the quantification limit, and quantified values are a minority every year.",
        "fr": "{share} des résultats sont sous la limite de quantification, et les valeurs quantifiées sont minoritaires "
              "chaque année."},
    "an.dq.status.why": {
        "en": "Laboratories search for hundreds of substances in each full analysis, and in drinking water most of them are "
              "absent or too rare to be measured: \"below the quantification limit\" is the normal result of a clean sample.",
        "fr": "Les laboratoires cherchent des centaines de substances dans chaque analyse complète, et dans l'eau potable la "
              "plupart sont absentes ou trop rares pour être mesurées : « sous la limite de quantification » est le résultat "
              "normal d'un prélèvement propre."},
    "an.dq.status.lim": {
        "en": "The quantification limit is not the same for every laboratory and every year, so a substance can become "
              "\"visible\" only because measurement improved.",
        "fr": "La limite de quantification n'est pas la même pour tous les laboratoires et toutes les années : une substance "
              "peut devenir « visible » seulement parce que la mesure s'est améliorée."},
    "an.dq.verdict.seen": {
        "en": "The bacterial lines lie on top of each other; the chemical lines part ways between 2016 and 2022, then come "
              "back together.",
        "fr": "Les courbes bactériologiques se superposent ; les courbes chimiques se séparent entre 2016 et 2022, puis se "
              "rejoignent."},
    "an.dq.verdict.why": {
        "en": "Three traced causes: temporary exemptions granted by the prefect, under which a sample above a limit stays "
              "officially compliant; the limits of selenium and antimony raised on 1 January 2023 (sources 8 to 10), while "
              "the published rows show today's limits; and a higher limit for chlorites when the treatment can produce them.",
        "fr": "Trois causes retrouvées : les dérogations temporaires accordées par le préfet, sous lesquelles un prélèvement "
              "au-dessus d'une limite reste officiellement conforme ; les limites du sélénium et de l'antimoine relevées le "
              "1er janvier 2023 (sources 8 à 10), alors que les lignes publiées affichent les limites actuelles ; et une "
              "limite plus haute pour les chlorites quand le traitement peut en produire."},
    "an.dq.verdict.lim": {
        "en": "Our recomputation can only use the threshold written next to each result; this is why the app relies on the "
              "official verdict for history, and on the recomputation only for the score, whose windows start in "
              "September 2023.",
        "fr": "Notre recalcul ne peut utiliser que le seuil écrit à côté de chaque résultat ; c'est pourquoi l'application "
              "s'appuie sur le verdict officiel pour l'historique, et sur le recalcul seulement pour le score, dont les "
              "fenêtres commencent en septembre 2023."},
    "an.dq.cov.seen": {
        "en": "Half of the networks had {med} samples or fewer in {y}, while the most tested had {max}: a gap of several "
              "orders of magnitude.",
        "fr": "La moitié des réseaux a eu {med} prélèvements ou moins en {y}, alors que le plus contrôlé en a eu {max} : un "
              "écart de plusieurs ordres de grandeur."},
    "an.dq.cov.why": {
        "en": "The number of samples required depends on the size of the network, measured by the population served and "
              "the volume distributed (as recalled by ARS Guadeloupe, source 32): a city network is tested far more "
              "often than a hamlet's.",
        "fr": "Le nombre de prélèvements exigé dépend de la taille du réseau, mesurée par la population desservie et le "
              "volume distribué (comme le rappelle l'ARS Guadeloupe, source 32) : le réseau d'une ville est "
              "contrôlé bien plus souvent que celui d'un hameau."},
    "an.dq.cov.lim": {
        "en": "A sample taken at a plant or a source is attached to every network it feeds, so the counts per network add "
              "up to more than the number of samples. Rates computed on a handful of samples are uncertain, hence the "
              "confidence level of each score.",
        "fr": "Un prélèvement fait à l'usine ou au captage est rattaché à chaque réseau qu'il alimente : les comptes par "
              "réseau dépassent donc le nombre de prélèvements. Les taux calculés sur quelques prélèvements sont "
              "incertains, d'où le niveau de confiance de chaque score."},
}

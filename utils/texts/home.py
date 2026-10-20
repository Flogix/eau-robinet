"""Home page: the problem, why water is tested, the method and hypotheses, the national indicators."""

T = {
    "home.kicker": {"en": "An investigation", "fr": "Une enquête"},
    "home.title": {"en": "What's in my glass?", "fr": "Qu'y a-t-il dans mon verre ?"},
    "home.lede": {
        "en": "Every day, people in France fill a glass at the tap without a second thought. This app uses ten years "
              "of official test results to check, town by town, whether that trust is deserved.",
        "fr": "Chaque jour, en France, on remplit un verre au robinet sans y penser. Cette application reprend dix ans "
              "de résultats officiels pour vérifier, commune par commune, si cette confiance est méritée."},

    "home.why.kicker": {"en": "Why it matters", "fr": "Pourquoi c'est important"},
    "home.why.title": {"en": "Water that makes people ill is not a thing of the past",
                       "fr": "L'eau qui rend malade n'appartient pas au passé"},
    "home.why.world": {
        "en": "Worldwide, at least **1.7 billion people** drank from a source contaminated with faeces in 2022. "
              "The World Health Organization estimates that this contaminated water causes about **505,000 deaths "
              "from diarrhoea every year**, and that it can also carry cholera, dysentery, typhoid and polio.",
        "fr": "Dans le monde, au moins **1,7 milliard de personnes** buvaient en 2022 une eau contaminée par des "
              "matières fécales. L'Organisation mondiale de la santé estime que cette eau contaminée cause environ "
              "**505 000 décès par diarrhée chaque année**, et qu'elle peut aussi transmettre le choléra, la "
              "dysenterie, la typhoïde et la poliomyélite."},
    "home.why.france": {
        "en": "France is far from that situation, but it is not immune. Between 2010 and 2022, Santé publique France, "
              "the national public health agency, confirmed **145 outbreaks of gastroenteritis caused by tap water**, "
              "on networks serving more than **790,000 people**. The largest, in Grasse in 2019, made 717 people ill. "
              "The authors themselves warn that the real number is strongly underestimated, because many episodes are "
              "never linked to the water.",
        "fr": "La France est loin de cette situation, mais elle n'en est pas à l'abri. Entre 2010 et 2022, Santé "
              "publique France a confirmé **145 épidémies de gastro-entérite dues à l'eau du robinet**, sur des réseaux "
              "desservant plus de **790 000 habitants**. La plus importante, à Grasse en 2019, a rendu malades 717 "
              "personnes. Les auteurs préviennent eux-mêmes que le vrai nombre est fortement sous-estimé, car beaucoup "
              "d'épisodes ne sont jamais reliés à l'eau."},
    "home.why.nodeaths": {
        "en": "How many people fall ill or die because of tap water in France each year? We looked for an official "
              "national figure and did not find one, so this app does not give one.",
        "fr": "Combien de personnes tombent malades ou meurent chaque année en France à cause de l'eau du robinet ? "
              "Nous avons cherché un chiffre national officiel et n'en avons pas trouvé : cette application n'en "
              "donne donc pas."},
    "home.why.control": {
        "en": "This is why tap water is tested so often. The **regional health agencies (ARS)** take samples at the "
              "source, at the treatment plant and at the tap, and approved laboratories analyse them. In {year} they "
              "took **{samples} samples** and recorded **{results} million results**, one result being one substance "
              "measured in one sample. The Ministry of Health calls tap water *the most controlled food in France*.",
        "fr": "C'est pour cela que l'eau du robinet est contrôlée si souvent. Les **agences régionales de santé (ARS)** "
              "font des prélèvements au captage, à l'usine de traitement et au robinet, puis des laboratoires agréés "
              "les analysent. En {year}, elles ont fait **{samples} prélèvements** et enregistré **{results} millions "
              "de résultats**, un résultat étant une substance mesurée dans un prélèvement. Le ministère de la Santé "
              "présente l'eau du robinet comme *l'aliment le plus contrôlé en France*."},
    "home.why.sources": {
        "en": "Sources: WHO, Drinking-water fact sheet, 13 September 2023; Santé publique France, Bulletin "
              "épidémiologique hebdomadaire no. 15, 10 September 2024; Ministry of Health, dataset documentation. "
              "Full references in docs/sources.md (sources 1 to 4).",
        "fr": "Sources : OMS, fiche « Drinking-water », 13 septembre 2023 ; Santé publique France, Bulletin "
              "épidémiologique hebdomadaire n° 15, 10 septembre 2024 ; ministère de la Santé, documentation du jeu "
              "de données. Références complètes dans docs/sources.md (sources 1 à 4)."},

    "home.find.title": {"en": "Look up your town", "fr": "Cherchez votre commune"},
    "home.find.text": {
        "en": "Type the first letters of your town: you get a score out of 100, a grade from A to E, and a plain-language "
              "report of what was found in your water.",
        "fr": "Tapez les premières lettres de votre commune : vous obtenez un score sur 100, une note de A à E et un "
              "rapport en langage clair sur ce qui a été trouvé dans votre eau."},
    "home.find.placeholder": {"en": "Start typing a town name", "fr": "Commencez à taper un nom de commune"},
    "home.find.score": {"en": "{score}/100, grade {grade}, confidence {conf}",
                        "fr": "{score}/100, note {grade}, confiance {conf}"},
    "home.find.report": {"en": "See the full report", "fr": "Voir le rapport complet"},

    "home.method.kicker": {"en": "How we worked", "fr": "Notre méthode"},
    "home.method.title": {"en": "Ten years of tests, four questions to settle",
                          "fr": "Dix ans de contrôles, quatre questions à trancher"},
    "home.method.p1": {
        "en": "The data is the national file of the sanitary control, published by the Ministry of Health: about "
              "**{samples} million samples** and **{results} million results** from January 2016 to August 2026. Water "
              "reaches homes through **distribution networks**: a network is a set of pipes in which the water has the "
              "same quality; {nets} of them were sampled in {year}, and {codes} different networks appear in the files "
              "since 2016. A town can be served by several networks, and one network can serve several towns.",
        "fr": "Les données sont le fichier national du contrôle sanitaire, publié par le ministère de la Santé : environ "
              "**{samples} millions de prélèvements** et **{results} millions de résultats**, de janvier 2016 à août 2026. "
              "L'eau arrive chez nous par des **réseaux de distribution** : un réseau est un ensemble de canalisations "
              "dans lequel l'eau a la même qualité ; {nets} d'entre eux ont été prélevés en {year}, et {codes} réseaux "
              "différents apparaissent dans les fichiers depuis 2016. Une commune peut être desservie par plusieurs "
              "réseaux, et un réseau peut desservir plusieurs communes."},
    "home.method.p2": {
        "en": "Each result is compared with a threshold. A **limit** is a health threshold: above it, the sample is "
              "declared non-compliant. A **reference** is a softer signal that the treatment or the pipes need "
              "attention, such as cloudy water or too much iron. From these comparisons we built a score out of 100 "
              "for every network, then for every town. It is a teaching tool, not a health opinion: the official "
              "opinion is the one of the health agency.",
        "fr": "Chaque résultat est comparé à un seuil. Une **limite** est un seuil sanitaire : au-dessus, le prélèvement "
              "est déclaré non conforme. Une **référence** est un signal plus doux, qui indique que le traitement ou les "
              "canalisations demandent de l'attention, comme une eau trouble ou trop de fer. À partir de ces "
              "comparaisons, nous avons construit un score sur 100 pour chaque réseau, puis pour chaque commune. C'est un "
              "outil pédagogique, pas un avis sanitaire : l'avis officiel est celui de l'agence de santé."},
    "home.method.p3": {
        "en": "Before looking at the results, we wrote down four hypotheses. Each one is tested later in the app with "
              "the data, and any of them could have turned out wrong.",
        "fr": "Avant de regarder les résultats, nous avons écrit quatre hypothèses. Chacune est testée plus loin avec "
              "les données, et chacune aurait pu se révéler fausse."},
    "home.h1": {
        "en": "**H1. Problems concentrate in small networks.** A village network is tested a few times a year, a city "
              "network hundreds of times. If small networks fail more often, it says something about their means, not "
              "only about their water. Tested on the map page and in the conclusions.",
        "fr": "**H1. Les problèmes se concentrent dans les petits réseaux.** Le réseau d'un village est contrôlé quelques "
              "fois par an, celui d'une ville des centaines de fois. Si les petits réseaux échouent plus souvent, cela "
              "parle de leurs moyens, pas seulement de leur eau. Testée sur la carte et dans les conclusions."},
    "home.h2": {
        "en": "**H2. Bacteria and chemistry do not hit the same places.** If both kinds of "
              "problems had the same causes, they would draw the same map. We expect two different maps. Tested on the map page and in the conclusions.",
        "fr": "**H2. Bactéries et chimie ne touchent pas les mêmes endroits.** Si les deux types de "
              "problèmes avaient les mêmes causes, ils dessineraient la même carte. Nous attendons deux cartes différentes. Testée sur la carte et dans les conclusions."},
    "home.h3": {
        "en": "**H3. Part of the \"new\" chemical problems comes from what we look for, not from worse water.** "
              "Laboratories have added new pesticide residues to their lists, and some of them were later reclassified. "
              "This is the main thread of the investigation, on the page *What we look for, what we find*.",
        "fr": "**H3. Une partie des « nouveaux » problèmes chimiques vient de ce qu'on cherche, pas d'une eau plus "
              "mauvaise.** Les laboratoires ont ajouté de nouveaux résidus de pesticides à leurs listes, et certains ont "
              "ensuite été reclassés. C'est le fil principal de l'enquête, sur la page *Ce qu'on cherche, ce qu'on trouve*."},
    "home.h4": {
        "en": "**H4. Hardness varies a lot across France, without health stakes.** Limescale is what people notice "
              "first in their kettle, yet it has no health limit. Tested on the page *What we look for, what we find*.",
        "fr": "**H4. La dureté varie énormément selon les territoires, sans enjeu sanitaire.** Le calcaire est ce qu'on "
              "remarque en premier dans sa bouilloire, mais il n'a pas de limite sanitaire. Testée sur la page *Ce "
              "qu'on cherche, ce qu'on trouve*."},

    "home.kpi.kicker": {"en": "The national picture", "fr": "Le tableau national"},
    "home.kpi.title": {"en": "Four numbers to start with", "fr": "Quatre chiffres pour commencer"},
    "kpi.headline": {
        "en": "Over {period} in {scope}, {bact} of bacteriological samples and {chem} of chemical samples met the health "
              "limits.",
        "fr": "Sur {period}, pour {scope}, {bact} des prélèvements bactériologiques et {chem} des prélèvements "
              "chimiques respectaient les limites sanitaires."},
    "kpi.bact": {"en": "Bacteria: samples OK", "fr": "Bactéries : prélèvements OK"},
    "kpi.chem": {"en": "Chemistry: samples OK", "fr": "Chimie : prélèvements OK"},
    "kpi.hit": {"en": "Towns with a bacterial alert", "fr": "Communes avec alerte bactérienne"},
    "kpi.score": {"en": "Median town score today", "fr": "Score médian des communes"},
    "kpi.delta": {"en": "{d} vs {y}", "fr": "{d} par rapport à {y}"},
    "kpi.hit.delta": {"en": "{share} of {n} towns", "fr": "{share} de {n} communes"},
    "kpi.score.delta": {"en": "{share} graded D or E", "fr": "{share} notées D ou E"},
    "kpi.bact.help": {"en": "Share of the {n} samples that the health agency declared compliant with the bacterial "
                            "limits. Filters: period and region.",
                      "fr": "Part des {n} prélèvements déclarés conformes aux limites bactériologiques par l'agence de "
                            "santé. Filtres : période et région."},
    "kpi.chem.help": {"en": "Share of the {n} samples declared compliant with the chemical limits. Filters: period and "
                            "region.",
                      "fr": "Part des {n} prélèvements déclarés conformes aux limites chimiques. Filtres : période et "
                            "région."},
    "kpi.hit.help": {"en": "Towns where at least one sample failed the bacterial limits over the period. Filters: "
                           "period, region, kind of town.",
                     "fr": "Communes où au moins un prélèvement n'a pas respecté les limites bactériologiques sur la "
                           "période. Filtres : période, région, type de commune."},
    "kpi.score.help": {"en": "Score of the last 12 to 36 months, whatever the period. Filters: region, kind of town.",
                       "fr": "Score des 12 à 36 derniers mois, quelle que soit la période. Filtres : région, type de "
                             "commune."},
    "kpi.read.bact": {
        "en": "**Bacteria.** Each sample gets an official verdict from the health agency: compliant or not with the "
              "bacterial limits (no *E. coli* and no enterococci per 100 mL). The "
              "first number is the share of compliant samples over the chosen period. The small number below compares "
              "the last year of the period with the year before, in percentage points: a positive value means a "
              "larger share of good samples.",
        "fr": "**Bactéries.** Chaque prélèvement reçoit un verdict officiel de l'agence de santé : conforme ou non aux "
              "limites bactériologiques (ni *E. coli* ni entérocoques "
              "dans 100 mL). Le premier chiffre est la part de prélèvements conformes sur la période choisie. Le petit "
              "chiffre en dessous compare la dernière année de la période à l'année précédente, en points de "
              "pourcentage : une valeur positive veut dire une plus grande part de bons prélèvements."},
    "kpi.read.chem": {
        "en": "**Chemistry.** Same reading for the chemical limits (nitrates, pesticides, metals and others). A sample "
              "above a limit but covered by a temporary exemption granted by the prefect counts as compliant, as in "
              "the official verdict.",
        "fr": "**Chimie.** Même lecture pour les limites chimiques (nitrates, pesticides, métaux et autres). Un "
              "prélèvement au-dessus d'une limite mais couvert par une dérogation temporaire accordée par le préfet "
              "compte comme conforme, comme dans le verdict officiel."},
    "kpi.read.hit": {
        "en": "**Towns with a bacterial alert** counts the towns where at least one sample failed over the period. "
              "These towns have {pop} million inhabitants, but this is an upper bound: a whole town is counted even "
              "when only one district or one of its networks was affected.",
        "fr": "**Communes avec alerte bactérienne** compte les communes où au moins un prélèvement a échoué sur la "
              "période. Elles comptent {pop} millions d'habitants, mais c'est une borne haute : une commune entière est "
              "comptée même quand un seul quartier ou un seul de ses réseaux a été touché."},
    "kpi.read.score": {
        "en": "**The median score** is the score of the town in the middle when all towns are sorted: half do better, "
              "half do worse. It describes today's water, over the last twelve months for bacteria and the last three "
              "years for chemistry.",
        "fr": "**Le score médian** est celui de la commune du milieu quand on les range toutes : la moitié fait mieux, "
              "l'autre moitié moins bien. Il décrit l'eau d'aujourd'hui, sur les douze derniers mois pour les bactéries "
              "et les trois dernières années pour la chimie."},
    "kpi.trend.better_bact": {
        "en": "**Is it getting better?** For bacteria, yes: the share of non-compliant samples went from {a} in {y0} "
              "to {b} in {y1}.",
        "fr": "**Est-ce que ça s'améliore ?** Pour les bactéries, oui : la part de prélèvements non conformes est passée "
              "de {a} en {y0} à {b} en {y1}."},
    "kpi.trend.worse_bact": {
        "en": "**Is it getting better?** For bacteria, not over this period: the share of non-compliant samples went "
              "from {a} in {y0} to {b} in {y1}.",
        "fr": "**Est-ce que ça s'améliore ?** Pour les bactéries, pas sur cette période : la part de prélèvements non "
              "conformes est passée de {a} en {y0} à {b} en {y1}."},
    "kpi.trend.chem_up": {
        "en": "For chemistry, the share rose from {a} to {b}. Read this with care: laboratories now look for more "
              "substances than in {y0}, and the page *What we look for, what we find* shows that this explains most of "
              "the rise.",
        "fr": "Pour la chimie, la part est passée de {a} à {b}. À lire avec prudence : les laboratoires cherchent "
              "aujourd'hui plus de substances qu'en {y0}, et la page *Ce qu'on cherche, ce qu'on trouve* montre que cela "
              "explique l'essentiel de la hausse."},
    "kpi.trend.chem_down": {
        "en": "For chemistry, the share went from {a} to {b}.",
        "fr": "Pour la chimie, la part est passée de {a} à {b}."},
    "kpi.trend.short": {"en": "Choose a period of at least two years to see a trend.",
                        "fr": "Choisissez une période d'au moins deux ans pour voir une tendance."},

    "home.trend.title": {"en": "Share of samples that failed a health limit, year by year",
                         "fr": "Part des prélèvements hors limite sanitaire, année par année"},
    "home.trend.caption": {
        "en": "Line chart: share of samples officially non-compliant with the bacterial limits (brick) and with the "
              "chemical limits (blue), per year, {scope}. Hover a point for the counts.",
        "fr": "Courbes : part des prélèvements officiellement non conformes aux limites bactériologiques (brique) et "
              "chimiques (bleu), par année, {scope}. Survolez un point pour voir les effectifs."},
    "home.trend.take": {
        "en": "The two lines tell different stories. Bacterial failures slowly decline over the years. The "
              "chemical line jumps in 2021 and drops again in 2025, two "
              "moves that are hard to explain by the water alone: this chart is the starting point of the investigation on "
              "the page *What we look for, what we find*.",
        "fr": "Les deux courbes racontent deux histoires. Les échecs bactériologiques baissent lentement au fil des "
              "années. La courbe chimique bondit en 2021 "
              "puis retombe en 2025, deux mouvements que l'eau seule explique mal : ce graphique est le point de "
              "départ de l'enquête de la page *Ce qu'on cherche, ce qu'on trouve*."},
    "home.trend.y": {"en": "Non-compliant samples (%)", "fr": "Prélèvements non conformes (%)"},
    "home.trend.bact": {"en": "Bacteria", "fr": "Bactéries"},
    "home.trend.chem": {"en": "Chemistry", "fr": "Chimie"},
    "home.trend.hover": {"en": "{y}: {v} non-compliant<br>{k} of {n} samples",
                         "fr": "{y} : {v} non conformes<br>{k} sur {n} prélèvements"},
    "home.caveat": {
        "en": "A few precautions before going further. 2026 is incomplete (samples up to 31 August). Overseas "
              "departments are added progressively by the producer. A substance that was not measured is not absent: it "
              "was simply not searched. And when two things go together on a chart, that does not prove that one "
              "causes the other.",
        "fr": "Quelques précautions avant d'aller plus loin. 2026 est incomplète (prélèvements jusqu'au 31 août). Les "
              "départements d'outre-mer sont complétés progressivement par le producteur. Une substance non mesurée "
              "n'est pas absente : elle n'a simplement pas été cherchée. Et quand deux choses vont ensemble sur un "
              "graphique, cela ne prouve pas que l'une cause l'autre."},
}

"""Page "How to read a water test": samples, results, thresholds, families, and how often each is exceeded."""

T = {
    "read.kicker": {"en": "The basics", "fr": "Les bases"},
    "read.title": {"en": "How to read a water test", "fr": "Lire une analyse d'eau"},
    "read.lede": {
        "en": "Before judging a town, it helps to know what a test actually says. A water test is not one number: it is "
              "a list of substances, each compared with its own threshold.",
        "fr": "Avant de juger une commune, il faut savoir ce que dit vraiment une analyse. Une analyse d'eau n'est pas "
              "un chiffre unique : c'est une liste de substances, chacune comparée à son propre seuil."},
    "read.p1": {
        "en": "A **sample** is a bottle of water taken on a given day at a given place: the source, the treatment plant "
              "or a tap in town. The laboratory then measures dozens or hundreds of **parameters** in it, a parameter "
              "being anything that can be measured, from a bacterium to a pesticide or the temperature. Each measurement "
              "is one **result**.",
        "fr": "Un **prélèvement** est un flacon d'eau pris un jour donné à un endroit donné : le captage, l'usine de "
              "traitement ou un robinet en ville. Le laboratoire y mesure ensuite des dizaines ou des centaines de "
              "**paramètres**, un paramètre étant tout ce qui se mesure, d'une bactérie à un pesticide ou à la "
              "température. Chaque mesure est un **résultat**."},
    "read.p2": {
        "en": "Most results say *below the quantification limit*: the substance was searched but, if present, it was "
              "below the smallest amount the laboratory can measure reliably. In this app such a result counts as zero "
              "when we check thresholds, and never as a detection. In the data, {share} of the results are of this kind.",
        "fr": "La plupart des résultats indiquent *inférieur à la limite de quantification* : la substance a été "
              "cherchée mais, si elle était là, c'était sous la plus petite quantité que le laboratoire sait mesurer de "
              "façon fiable. Dans cette application, un tel résultat compte pour zéro quand on vérifie les seuils, et "
              "jamais comme une détection. Dans les données, {share} des résultats sont de ce type."},
    "read.p3": {
        "en": "Thresholds come in two kinds. A **limit** protects health: above it the sample is declared non-compliant. "
              "A **reference** is a warning light for the people who run the network, for instance cloudy water, too "
              "much iron or an unusual acidity. Being above a reference is not, in itself, a health problem.",
        "fr": "Les seuils sont de deux sortes. Une **limite** protège la santé : au-dessus, le prélèvement est déclaré "
              "non conforme. Une **référence** est un voyant pour ceux qui gèrent le réseau, par exemple une eau trouble, "
              "trop de fer ou une acidité inhabituelle. Dépasser une référence n'est pas, en soi, un problème de santé."},

    "read.families.kicker": {"en": "Four families", "fr": "Quatre familles"},
    "read.families.title": {"en": "What is searched in the water", "fr": "Ce qu'on cherche dans l'eau"},
    "read.fam.micro": {
        "en": "**Bacteria.** The laboratory counts *E. coli* and enterococci in 100 mL of water. The limit is zero: a "
              "single one makes the sample non-compliant. In the score we use the official verdict on each sample over "
              "the last twelve months.",
        "fr": "**Bactéries.** Le laboratoire compte les *E. coli* et les entérocoques dans 100 mL d'eau. La limite est "
              "zéro : une seule suffit à rendre le prélèvement non conforme. Dans le score, nous utilisons le verdict "
              "officiel de chaque prélèvement sur les douze derniers mois."},
    "read.fam.chem": {
        "en": "**Health chemistry.** Nitrates (limit 50 mg/L), pesticides (0.1 µg/L per substance and 0.5 µg/L in "
              "total), their **metabolites**, which are the molecules a pesticide turns into as it breaks down, PFAS "
              "(0.1 µg/L for the sum of twenty of these very persistent compounds, in the routine control since "
              "1 January 2026), metals such as lead and arsenic (10 µg/L each) and the by-products of disinfection. "
              "The score looks at the last three years, because small networks are fully analysed only once in a while.",
        "fr": "**Chimie sanitaire.** Les nitrates (limite 50 mg/L), les pesticides (0,1 µg/L par substance et 0,5 µg/L au "
              "total), leurs **métabolites**, c'est-à-dire les molécules que devient un pesticide en se dégradant, les "
              "PFAS (0,1 µg/L pour la somme de vingt de ces composés très persistants, dans le contrôle courant depuis le "
              "1er janvier 2026), les métaux comme le plomb et l'arsenic (10 µg/L chacun) et les sous-produits de la "
              "désinfection. Le score regarde les trois dernières années, car les petits réseaux ne sont analysés "
              "complètement que de temps en temps."},
    "read.fam.comfort": {
        "en": "**Comfort and indicators.** Cloudiness (turbidity), coliform bacteria, iron, manganese, aluminium, acidity "
              "(pH) and mineral content (conductivity). They tell whether treatment and pipes work well. Some pesticide "
              "metabolites judged *non-relevant* by the national health safety agency, Anses, are compared with an "
              "**indicative value** of 0.9 µg/L instead of a limit: above it, the water can still be drunk but the "
              "supplier must act.",
        "fr": "**Confort et indicateurs.** La turbidité (eau trouble), les bactéries coliformes, le fer, le manganèse, "
              "l'aluminium, l'acidité (pH) et la minéralisation (conductivité). Ils disent si le traitement et les "
              "canalisations fonctionnent bien. Certains métabolites de pesticides jugés *non pertinents* par l'Anses, "
              "l'agence nationale de sécurité sanitaire, sont comparés à une **valeur indicative** de 0,9 µg/L au lieu "
              "d'une limite : au-dessus, l'eau reste buvable mais le distributeur doit agir."},
    "read.fam.info": {
        "en": "**Information only.** Hardness, which says how much limescale the water carries, calcium, magnesium and "
              "temperature. They have no health threshold and never lower the score.",
        "fr": "**Simple information.** La dureté, qui dit combien de calcaire l'eau transporte, le calcium, le magnésium "
              "et la température. Ils n'ont pas de seuil sanitaire et ne font jamais baisser le score."},
    "read.fam.count": {"en": "{n} of the {total} parameters of the dataset fall in this family.",
                       "fr": "{n} des {total} paramètres du jeu de données sont dans cette famille."},
    "read.fam.sources": {
        "en": "Thresholds are those written next to each result in the dataset (decree of 11 January 2007 as amended). "
              "Non-relevant metabolites and the 0.9 µg/L value: Assemblée nationale written question 2237 and ARS "
              "Hauts-de-France (docs/sources.md, sources 5 and 6). PFAS: ARS Nouvelle-Aquitaine (source 11).",
        "fr": "Les seuils sont ceux écrits à côté de chaque résultat dans le jeu de données (arrêté du 11 janvier 2007 "
              "modifié). Métabolites non pertinents et valeur de 0,9 µg/L : question écrite 2237 de l'Assemblée "
              "nationale et ARS Hauts-de-France (docs/sources.md, sources 5 et 6). PFAS : ARS Nouvelle-Aquitaine "
              "(source 11)."},

    "read.chart.kicker": {"en": "How often thresholds are crossed", "fr": "À quelle fréquence les seuils sont dépassés"},
    "read.chart.headline": {
        "en": "In {year}, the parameter most often above its threshold was {label}: {share} of the samples where it was "
              "searched. {k} of the {n} parameters shown stay below 1%.",
        "fr": "En {year}, le paramètre le plus souvent au-dessus de son seuil était {label} : {share} des prélèvements "
              "où il a été cherché. {k} des {n} paramètres montrés restent sous 1 %."},
    "read.chart.title": {"en": "Share of samples above the threshold, for nineteen key parameters, in {year}",
                         "fr": "Part des prélèvements au-dessus du seuil, pour dix-neuf paramètres clés, en {year}"},
    "read.chart.x": {"en": "Samples above the threshold (%)", "fr": "Prélèvements au-dessus du seuil (%)"},
    "read.chart.caption": {
        "en": "Horizontal bars, one per parameter, coloured by family (brick for bacteria, blue for health chemistry, "
              "ochre for comfort); the value is written at the end of each bar. Hover a bar for the counts and the "
              "threshold.",
        "fr": "Barres horizontales, une par paramètre, colorées par famille (brique pour les bactéries, bleu pour la "
              "chimie sanitaire, ocre pour le confort) ; la valeur est écrite au bout de chaque barre. Survolez une "
              "barre pour voir les effectifs et le seuil."},
    "read.chart.take": {
        "en": "Two lessons. First, exceedances are rare: for most parameters, fewer than one sample in a hundred. "
              "Second, the top of the list is not where one would expect it. A pesticide metabolite searched only "
              "since 2021 comes before nitrates and bacteria. That is the first clue of the main finding of this "
              "investigation: what we find depends on what we look for.",
        "fr": "Deux leçons. D'abord, les dépassements sont rares : pour la plupart des paramètres, moins d'un "
              "prélèvement sur cent. Ensuite, le haut de la liste n'est pas là où on l'attendrait. Un métabolite de "
              "pesticide cherché seulement depuis 2021 passe devant les nitrates et les bactéries. C'est le premier "
              "indice du résultat principal de cette enquête : ce qu'on trouve dépend de ce qu'on cherche."},
    "read.chart.hover": {"en": "{label}<br>{k} of {n} samples above the {kind} ({thr})",
                         "fr": "{label}<br>{k} prélèvements sur {n} au-dessus de la {kind} ({thr})"},
    "read.kind.limit": {"en": "limit", "fr": "limite"},
    "read.kind.reference": {"en": "reference", "fr": "référence"},
    "read.kind.indicative": {"en": "indicative value", "fr": "valeur indicative"},
    "read.table.title": {"en": "The thresholds used, as written in the data", "fr": "Les seuils utilisés, tels qu'écrits dans les données"},
    "read.col.param": {"en": "Parameter", "fr": "Paramètre"},
    "read.col.family": {"en": "Family", "fr": "Famille"},
    "read.col.thr": {"en": "Threshold", "fr": "Seuil"},
    "read.col.kind": {"en": "Kind", "fr": "Type"},
    "read.col.unit": {"en": "Unit", "fr": "Unité"},

    # search engine of parameters
    "read.search.kicker": {"en": "Search the water", "fr": "Chercher dans l'eau"},
    "read.search.title": {"en": "Look up a substance or a parameter", "fr": "Chercher une substance ou un paramètre"},
    "read.search.text": {
        "en": "Type a name in the box: the list holds the {n} parameters of the dataset, with the twenty that matter most for "
              "the story at the top. Each of these twenty has a fact sheet written from official sources (Anses, World "
              "Health Organization, regional health agencies); for the others, the app shows what the data contains.",
        "fr": "Tapez un nom dans le champ : la liste contient les {n} paramètres du jeu de données, avec en tête les vingt "
              "qui comptent le plus pour le récit. Chacun de ces vingt a une fiche rédigée à partir de sources officielles "
              "(Anses, Organisation mondiale de la santé, agences régionales de santé) ; pour les autres, l'application "
              "montre ce que contiennent les données."},
    "read.search.box": {"en": "Substance or parameter", "fr": "Substance ou paramètre"},
    "read.search.help": {"en": "The list filters as you type. The code in brackets is the one used by the Ministry of Health.",
                         "fr": "La liste se filtre pendant la frappe. Le code entre parenthèses est celui du ministère de la "
                               "Santé."},
    "read.fs.what": {"en": "What it is", "fr": "Ce que c'est"},
    "read.fs.origin": {"en": "Where it comes from", "fr": "D'où ça vient"},
    "read.fs.health": {"en": "Possible effects on health", "fr": "Effets possibles sur la santé"},
    "read.fs.threshold": {"en": "Its threshold, and why", "fr": "Son seuil, et pourquoi"},
    "read.fs.exceed": {"en": "When it is exceeded", "fr": "En cas de dépassement"},
    "read.fs.data": {"en": "What the data says", "fr": "Ce que disent les données"},
    "read.fs.sources": {"en": "Official sources", "fr": "Sources officielles"},
    "read.fs.family": {"en": "Family: {fam}", "fr": "Famille : {fam}"},
    "read.fs.datatext": {
        "en": "Measured in {n} samples between 2016 and {last}, first in {first}. In {last}, {k} of {m} samples were above "
              "the threshold of {thr} ({share}), and the highest value was {max} {unit}.",
        "fr": "Mesuré dans {n} prélèvements entre 2016 et {last}, pour la première fois en {first}. En {last}, {k} des {m} "
              "prélèvements étaient au-dessus du seuil de {thr} ({share}), et la valeur la plus haute était de {max} {unit}."},
    "read.fs.datatext.nothr": {
        "en": "Measured in {n} samples between 2016 and {last}, first in {first}. In {last}, it was quantified in {d} of {m} "
              "samples, and the highest value was {max} {unit}.",
        "fr": "Mesuré dans {n} prélèvements entre 2016 et {last}, pour la première fois en {first}. En {last}, il a été "
              "quantifié dans {d} des {m} prélèvements, et la valeur la plus haute était de {max} {unit}."},
    "read.fs.notlast": {"en": "Measured in {n} samples between 2016 and 2026, first in {first}, but not in {last}.",
                        "fr": "Mesuré dans {n} prélèvements entre 2016 et 2026, pour la première fois en {first}, mais pas "
                              "en {last}."},
    "read.fs.none": {
        "en": "There is no fact sheet for this parameter: this app wrote sheets only for the twenty parameters that matter "
              "most for its story, from official sources. Here is what the data itself contains.",
        "fr": "Il n'y a pas de fiche pour ce paramètre : cette application n'a rédigé de fiches que pour les vingt paramètres "
              "qui comptent le plus pour son récit, à partir de sources officielles. Voici ce que contiennent les données "
              "elles-mêmes."},
    "read.fs.meta": {
        "en": "Label in the data: {label}. Family in this app: {fam}. Unit: {unit}. Threshold written in the data: {thr}. "
              "Results in the data: {n}, of which {d} quantified (a real number above the quantification limit). Years "
              "measured: {y0} to {y1}.",
        "fr": "Libellé dans les données : {label}. Famille dans cette application : {fam}. Unité : {unit}. Seuil écrit dans "
              "les données : {thr}. Résultats dans les données : {n}, dont {d} quantifiés (un vrai nombre au-dessus de la "
              "limite de quantification). Années mesurées : {y0} à {y1}."},
    "read.fs.nothr": {"en": "none", "fr": "aucun"},
    "fam.info": {"en": "Information", "fr": "Information"},

    "read.chart.intro": {
        "en": "Now that each substance has a name and a threshold, how often are those thresholds crossed in France? This "
              "chart puts the key parameters side by side for one year. Each bar is the share of the samples where the "
              "parameter was searched and found above its threshold: the longer the bar, the more frequent the problem. "
              "The colour gives the family, so that health limits and comfort references are not confused.",
        "fr": "Maintenant que chaque substance a un nom et un seuil, à quelle fréquence ces seuils sont-ils franchis en "
              "France ? Ce graphique met côte à côte les paramètres clés pour une année. Chaque barre est la part des "
              "prélèvements où le paramètre a été cherché et trouvé au-dessus de son seuil : plus la barre est longue, plus "
              "le problème est fréquent. La couleur donne la famille, pour ne pas confondre limites sanitaires et "
              "références de confort."},
    "read.table.intro": {
        "en": "The table below gives the threshold used for each of these parameters, exactly as it is written next to each "
              "result in the data. Read the kind column first: a limit protects health, a reference is a warning light, and "
              "an indicative value applies to the pesticide residues judged non-relevant.",
        "fr": "Le tableau ci-dessous donne le seuil utilisé pour chacun de ces paramètres, tel qu'il est écrit à côté de "
              "chaque résultat dans les données. Lisez d'abord la colonne du type : une limite protège la santé, une "
              "référence est un voyant, et une valeur indicative s'applique aux résidus de pesticides jugés non pertinents."},
    "read.table.take": {
        "en": "Two things stand out. Thresholds span more than five orders of magnitude, from 0.1 µg/L for a pesticide to "
              "50 mg/L for nitrates, because they answer different questions: a quality indicator not built on toxicity for "
              "pesticides, a dose studied by "
              "the WHO for nitrates. And several thresholds are not health thresholds at all, which is why a single number "
              "above its threshold does not always mean the water is unsafe.",
        "fr": "Deux choses ressortent. Les seuils couvrent plus de cinq ordres de grandeur, de 0,1 µg/L pour un pesticide à "
              "50 mg/L pour les nitrates, parce qu'ils répondent à des questions différentes : un indicateur de qualité non fondé sur la "
              "toxicité pour les "
              "pesticides, une dose étudiée par l'OMS pour les nitrates. Et plusieurs seuils ne sont pas du tout sanitaires : "
              "c'est pourquoi un chiffre au-dessus de son seuil ne veut pas toujours dire que l'eau est dangereuse."},
}

"""Page "The water of my town": search, score, gauge, sub-scores, report per network, history of a parameter."""

T = {
    "town.kicker": {"en": "Your town", "fr": "Votre commune"},
    "town.title": {"en": "The water of my town", "fr": "L'eau de ma commune"},
    "town.lede": {
        "en": "Choose a town to see its score, what pulls it down, and a plain-language report on every network that "
              "brings water to it.",
        "fr": "Choisissez une commune pour voir son score, ce qui le fait baisser, et un rapport en langage clair sur "
              "chaque réseau qui l'alimente."},
    "town.pick": {"en": "Town", "fr": "Commune"},
    "town.pick.help": {
        "en": "Start typing: the list filters as you type. Towns with the same name are told apart by their department "
              "number in brackets.",
        "fr": "Commencez à taper : la liste se filtre au fur et à mesure. Les communes homonymes se distinguent par leur "
              "numéro de département entre parenthèses."},
    "town.facts.pop": {"en": "{n} inhabitants", "fr": "{n} habitants"},
    "town.facts.mountain": {"en": "Mountain Act town", "fr": "commune de montagne (loi Montagne)"},
    "town.facts.med": {"en": "Mediterranean coastal department, outside mountain areas",
                       "fr": "département du littoral méditerranéen, hors montagne"},
    "town.facts.nets": {"en": "served by {n} distribution networks", "fr": "desservie par {n} réseaux de distribution"},
    "town.facts.nets.one": {"en": "served by one distribution network", "fr": "desservie par un seul réseau de distribution"},
    "town.noscore": {"en": "No score for this town: none of its networks has samples in the last twelve to thirty-six "
                           "months.",
                     "fr": "Pas de score pour cette commune : aucun de ses réseaux n'a de prélèvement sur les douze à "
                           "trente-six derniers mois."},
    "town.headline": {"en": "{town}: {score}/100, grade {grade}, confidence {conf}.",
                      "fr": "{town} : {score}/100, note {grade}, confiance {conf}."},
    "town.how": {
        "en": "**How the score is built.** Each network gets three marks out of 100: bacteria (share of failed samples "
              "over twelve months), health chemistry (how close each substance came to its limit over three years) and "
              "comfort (the warning lights). The score is their weighted mean, 40% bacteria, 40% chemistry, 20% "
              "comfort, using only the families that were actually measured. The grade follows: A from 90, B from 75, "
              "C from 60, D from 40, E below. The **confidence** says how much evidence there is: it is high when all "
              "three families were measured, with at least twelve bacterial samples in the year.",
        "fr": "**Comment le score est construit.** Chaque réseau reçoit trois notes sur 100 : bactéries (part des "
              "prélèvements non conformes sur douze mois), chimie sanitaire (à quel point chaque substance s'est "
              "approchée de sa limite sur trois ans) et confort (les voyants). Le score est leur moyenne pondérée, 40 % "
              "bactéries, 40 % chimie, 20 % confort, en ne gardant que les familles réellement mesurées. La note suit : "
              "A dès 90, B dès 75, C dès 60, D dès 40, E en dessous. La **confiance** dit combien de preuves il y a : "
              "elle est élevée quand les trois familles ont été mesurées, avec au moins douze prélèvements "
              "bactériologiques dans l'année."},
    "town.gauge.title": {"en": "The score of {town} on the A to E scale", "fr": "Le score de {town} sur l'échelle de A à E"},
    "town.gauge.caption": {
        "en": "Gauge from 0 to 100; the coloured bands are the grades, from E (brick, below 40) to A (teal, 90 and "
              "above), and the grade is written in words above the number.",
        "fr": "Jauge de 0 à 100 ; les bandes colorées sont les notes, de E (brique, sous 40) à A (bleu-vert, 90 et "
              "plus), et la note est écrite en toutes lettres au-dessus du chiffre."},
    "town.gauge.take.above": {
        "en": "Half of French towns score {median} or more. {town} is {gap} points above that middle mark.",
        "fr": "La moitié des communes françaises a un score de {median} ou plus. {town} est {gap} points au-dessus de ce "
              "milieu."},
    "town.gauge.take.below": {
        "en": "Half of French towns score {median} or more. {town} is {gap} points below that middle mark: the report "
              "further down says why.",
        "fr": "La moitié des communes françaises a un score de {median} ou plus. {town} est {gap} points en dessous de "
              "ce milieu : le rapport plus bas dit pourquoi."},
    "town.subs.title": {"en": "The three marks behind the score", "fr": "Les trois notes derrière le score"},
    "town.subs.caption": {
        "en": "Horizontal bars, one per family, with the mark written at the end and the weight in brackets; \"not "
              "measured\" means the family is left out of the score.",
        "fr": "Barres horizontales, une par famille, avec la note écrite au bout et le poids entre parenthèses ; « non "
              "mesuré » veut dire que la famille est exclue du score."},
    "town.subs.take": {"en": "The weakest mark is {fam} ({v}/100): it is what pulls the score of {town} down.",
                       "fr": "La note la plus faible est {fam} ({v}/100) : c'est elle qui tire le score de {town} vers le bas."},
    "town.subs.take.perfect": {"en": "All measured families get 100: nothing pulls the score down.",
                               "fr": "Toutes les familles mesurées obtiennent 100 : rien ne fait baisser le score."},
    "town.subs.weight": {"en": "{fam} (weight {w})", "fr": "{fam} (poids {w})"},
    "town.subs.x": {"en": "Mark (out of 100)", "fr": "Note (sur 100)"},
    "town.notmeasured": {"en": "not measured", "fr": "non mesuré"},

    "town.why.kicker": {"en": "The report", "fr": "Le rapport"},
    "town.why.title": {"en": "Why this score, network by network", "fr": "Pourquoi ce score, réseau par réseau"},
    "town.why.several": {
        "en": "{town} gets its water from {n} networks, each with its own quality. The town's score is the mean of its "
              "scored networks; the table lists them from the weakest to the strongest, and each tab below holds the "
              "report of one network.",
        "fr": "{town} reçoit son eau de {n} réseaux, chacun avec sa propre qualité. Le score de la commune est la "
              "moyenne de ses réseaux notés ; le tableau les classe du plus faible au plus fort, et chaque onglet "
              "ci-dessous contient le rapport d'un réseau."},
    "town.why.one": {
        "en": "{town} gets its water from a single network, so the report below is the report of the town.",
        "fr": "{town} reçoit son eau d'un seul réseau : le rapport ci-dessous est donc celui de la commune."},
    "town.col.net": {"en": "Network", "fr": "Réseau"},
    "town.col.code": {"en": "Code", "fr": "Code"},
    "town.col.score": {"en": "Score", "fr": "Score"},
    "town.col.grade": {"en": "Grade", "fr": "Note"},
    "town.col.conf": {"en": "Confidence", "fr": "Confiance"},
    "town.col.nbact": {"en": "Bacterial samples (12 months)", "fr": "Prélèvements bactério (12 mois)"},
    "town.col.districts": {"en": "Districts served", "fr": "Quartiers desservis"},
    "town.tab.nodata": {"en": "{net}: no data", "fr": "{net} : pas de données"},
    "town.nodata": {"en": "No sample in the score windows for this network.",
                    "fr": "Aucun prélèvement dans les fenêtres du score pour ce réseau."},
    "town.districts": {"en": "Districts served: {d}", "fr": "Quartiers desservis : {d}"},
    "town.legend": {
        "en": "How to read the labels: Good is a strength; Above limit means a health limit was crossed; Watch means a "
              "value came close to a limit, or a comfort threshold was crossed; Note is useful context; Not tested "
              "means nobody looked. The report covers the last twelve months for bacteria and comfort, and the last "
              "three years for chemistry, up to 31 August 2026.",
        "fr": "Comment lire les étiquettes : Bon est un point fort ; Hors limite veut dire qu'une limite sanitaire a été "
              "dépassée ; À surveiller signale une valeur proche d'une limite, ou un seuil de confort dépassé ; À savoir "
              "donne du contexte ; Non mesuré veut dire que personne n'a regardé. Le rapport couvre les douze derniers "
              "mois pour les bactéries et le confort, et les trois dernières années pour la chimie, jusqu'au 31 août 2026."},

    "town.hist.kicker": {"en": "Ten years back", "fr": "Dix ans en arrière"},
    "town.hist.title": {"en": "{param} in the water of {town}, year by year", "fr": "{param} dans l'eau de {town}, année par année"},
    "town.hist.pick": {"en": "Substance to follow", "fr": "Substance à suivre"},
    "town.hist.pick.help": {"en": "Only the substances measured on the networks of this town are listed.",
                            "fr": "Seules les substances mesurées sur les réseaux de cette commune sont proposées."},
    "town.hist.caption": {
        "en": "Lines, one colour per network: the solid line is the highest value of each year, the dotted line the "
              "average; the dashed brick line is the threshold when there is one.",
        "fr": "Courbes, une couleur par réseau : le trait plein est la valeur la plus haute de chaque année, le "
              "pointillé la moyenne ; la ligne brique en tirets est le seuil quand il existe."},
    "town.hist.take": {
        "en": "The highest value over the period was {max} {unit} in {year}{thr_part}. Following one substance over ten "
              "years shows whether a problem is a one-off or a lasting feature of the water.",
        "fr": "La valeur la plus haute de la période était {max} {unit} en {year}{thr_part}. Suivre une substance sur "
              "dix ans montre si un problème est ponctuel ou s'il fait partie durablement de l'eau."},
    "town.hist.thr_part": {"en": ", for a {kind} of {thr} {unit}", "fr": ", pour une {kind} de {thr} {unit}"},
    "town.hist.max": {"en": "{net}, highest", "fr": "{net}, maximum"},
    "town.hist.mean": {"en": "{net}, average", "fr": "{net}, moyenne"},
    "town.hist.hover": {"en": "{y}: {v} {unit}<br>{n} measurements, {k} above the threshold",
                        "fr": "{y} : {v} {unit}<br>{n} mesures, {k} au-dessus du seuil"},
    "town.hist.none": {"en": "No history for these networks.", "fr": "Pas d'historique pour ces réseaux."},
    "town.kind.limit": {"en": "limit", "fr": "limite"},
    "town.kind.reference": {"en": "reference", "fr": "référence"},
    "town.kind.indicative": {"en": "indicative value", "fr": "valeur indicative"},
}

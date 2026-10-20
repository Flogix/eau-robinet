"""Texts of the downloadable town report (PDF, utils/town_report.py) and of its download button."""

T = {
    "pdf.button": {"en": "Download the report (PDF, English)", "fr": "Télécharger le rapport (PDF, anglais)"},
    "pdf.button.fr": {"en": "Download the report (PDF, French)", "fr": "Télécharger le rapport (PDF, français)"},
    "pdf.button.help": {
        "en": "A two to four page report on this town: score, marks, networks, substances in question, ten-year history "
              "of the substance chosen below, position against the medians, formulas and sources. Every sentence is "
              "written by fixed rules from the data, without artificial intelligence.",
        "fr": "Un rapport de deux à quatre pages sur cette commune : score, notes, réseaux, substances en cause, "
              "historique sur dix ans de la substance choisie plus bas, position face aux médianes, formules et sources. "
              "Chaque phrase est écrite par des règles fixes à partir des données, sans intelligence artificielle."},
    "pdf.section": {"en": "Take the report with you", "fr": "Emportez le rapport"},
    "pdf.section.text": {
        "en": "Everything on this page fits in a PDF you can print or send, in English or in French. It follows the "
              "substance chosen in the history chart at the bottom of the page.",
        "fr": "Tout ce qui est sur cette page tient dans un PDF à imprimer ou à envoyer, en anglais ou en français. Il "
              "suit la substance choisie dans le graphique d'historique en bas de page."},

    "pdf.doc_title": {"en": "Tap water report", "fr": "Rapport sur l'eau du robinet"},
    "pdf.dep": {"en": "Department: {dep}", "fr": "Département : {dep}"},
    "pdf.generated": {
        "en": "Generated on {today} from the official tests up to {end} (dataset updated on {updated}).",
        "fr": "Généré le {today} à partir des contrôles officiels jusqu'au {end} (jeu de données mis à jour le "
              "{updated})."},
    "pdf.warning.title": {"en": "Please read first", "fr": "À lire d'abord"},
    "pdf.warning": {
        "en": "This report gives a teaching indicator computed by a student project from public data. It is not a health "
              "opinion. The official opinion on your water is given by your regional health agency (ARS), and a "
              "summary note from the ARS comes with the water bill (source 7 of docs/sources.md). A substance that was not measured is not "
              "a substance that is absent.",
        "fr": "Ce rapport donne un indicateur pédagogique calculé par un projet étudiant à partir de données publiques. "
              "Ce n'est pas un avis sanitaire. L'avis officiel sur votre eau est celui de votre agence régionale de santé "
              "(ARS), et une note "
              "de synthèse de l'ARS est jointe à la facture d'eau (source 7 de docs/sources.md). Une substance non "
              "mesurée n'est pas une substance absente."},
    "pdf.k.score": {"en": "The score", "fr": "Le score"},
    "pdf.score_line": {"en": "{score} / 100", "fr": "{score} / 100"},
    "pdf.grade_line": {"en": "Grade {grade}", "fr": "Note {grade}"},
    "pdf.conf_line": {"en": "Confidence: {conf}", "fr": "Confiance : {conf}"},
    "pdf.facts": {"en": "{pop} · {nets}", "fr": "{pop} · {nets}"},
    "pdf.k.marks": {"en": "The three marks", "fr": "Les trois notes"},
    "pdf.k.why": {"en": "In short: why this score", "fr": "En bref : pourquoi ce score"},
    "pdf.k.position": {"en": "Against the medians", "fr": "Face aux médianes"},
    "pdf.position.text": {
        "en": "Each line places one score on the same scale from 0 to 100. A median is the middle value: half of the "
              "towns score more, half score less.",
        "fr": "Chaque ligne place un score sur la même échelle de 0 à 100. Une médiane est la valeur du milieu : la moitié "
              "des communes a un score plus haut, l'autre moitié un score plus bas."},
    "pdf.pos.nat": {"en": "Median of French towns", "fr": "Médiane des communes françaises"},
    "pdf.pos.dep": {"en": "Median of the department, {dep}", "fr": "Médiane du département, {dep}"},
    "pdf.k.networks": {"en": "The networks", "fr": "Les réseaux"},
    "pdf.k.report": {"en": "The report, network by network", "fr": "Le rapport, réseau par réseau"},
    "pdf.more_nets": {"en": "{n} more networks are described in the app.",
                      "fr": "{n} autres réseaux sont décrits dans l'application."},
    "pdf.k.history": {"en": "Ten years back", "fr": "Dix ans en arrière"},
    "pdf.hist.legend.max": {"en": "highest value of the year", "fr": "valeur la plus haute de l'année"},
    "pdf.hist.legend.mean": {"en": "average of the year", "fr": "moyenne de l'année"},
    "pdf.hist.legend.net": {"en": "{net}: {max} (dotted: {mean})", "fr": "{net} : {max} (pointillé : {mean})"},
    "pdf.hist.legend.thr": {"en": "{kind}: {thr} {unit}", "fr": "{kind} : {thr} {unit}"},
    "pdf.hist.more": {"en": "Only the six networks with the most measurements are drawn.",
                      "fr": "Seuls les six réseaux les plus mesurés sont tracés."},
    "pdf.k.method": {"en": "The method", "fr": "La méthode"},
    "pdf.k.sources": {"en": "Sources and data", "fr": "Sources et données"},
    "pdf.sources": {
        "en": "Data: French Ministry of Health, \"Résultats du contrôle sanitaire de l'eau distribuée commune par "
              "commune\", data.gouv.fr, Licence Ouverte 2.0, last updated on 5 October 2026: {url}. The score covers the "
              "last twelve months for bacteria and comfort, and the last three years for health chemistry, up to "
              "{end}. Year 2026 is partial (January to August). The method, its validation and every other source are "
              "described in the README and in docs/sources.md of the public repository: {repo}. Interactive version: "
              "{app}.",
        "fr": "Données : ministère de la Santé, « Résultats du contrôle sanitaire de l'eau distribuée commune par "
              "commune », data.gouv.fr, Licence Ouverte 2.0, dernière mise à jour le 5 octobre 2026 : {url}. Le score "
              "couvre les douze derniers mois pour les bactéries et le confort, et les trois dernières années pour la "
              "chimie sanitaire, jusqu'au {end}. L'année 2026 est partielle (janvier à août). La méthode, sa validation "
              "et toutes les autres sources sont décrites dans le README et dans docs/sources.md du dépôt public : "
              "{repo}. Version interactive : {app}."},
    "pdf.rules": {
        "en": "How this text was written: every sentence of this report comes from fixed rules applied to the data (for "
              "example \"if a measurement went above the limit, say how many, the limit and the peak\"). No artificial "
              "intelligence wrote or changed any number.",
        "fr": "Comment ce texte a été écrit : chaque phrase de ce rapport vient de règles fixes appliquées aux données "
              "(par exemple « si une mesure a dépassé la limite, dire combien, la limite et le pic »). Aucune "
              "intelligence artificielle n'a écrit ni modifié de chiffre."},
    "pdf.page": {"en": "Page {p} of {n}", "fr": "Page {p} sur {n}"},
    "pdf.footer": {"en": "Au robinet · teaching indicator, not a health opinion",
                   "fr": "Au robinet · indicateur pédagogique, pas un avis sanitaire"},
    "pdf.formula.micro": {"en": "S_bact = 100 × (1 − t)^5,  t = non-compliant samples / samples",
                          "fr": "S_bact = 100 × (1 − t)^5,  t = prélèvements non conformes / prélèvements"},
    "pdf.formula.ratio": {"en": "r = value / threshold", "fr": "r = valeur / seuil"},
    "pdf.formula.penalty": {"en": "g(r) = 0 if r ≤ 0.5;  40 (r − 0.5) up to r = 1;  20 + 60 (r − 1) up to r = 2;  80 beyond",
                            "fr": "g(r) = 0 si r ≤ 0,5 ;  40 (r − 0,5) jusqu'à r = 1 ;  20 + 60 (r − 1) jusqu'à r = 2 ;  "
                                  "80 au-delà"},
    "pdf.formula.chem": {"en": "S_chem = max(0, 100 − worst g − 0.25 × sum of the other g)",
                         "fr": "S_chim = max(0, 100 − pire g − 0,25 × somme des autres g)"},
    "pdf.formula.score": {"en": "Score = (0.4 S_bact + 0.4 S_chem + 0.2 S_comfort) / sum of the weights of the measured "
                                "families",
                          "fr": "Score = (0,4 S_bact + 0,4 S_chim + 0,2 S_confort) / somme des poids des familles mesurées"},
    "pdf.formula.town": {"en": "Score of the town = mean of the scores of its networks",
                         "fr": "Score de la commune = moyenne des scores de ses réseaux"},
    "pdf.filename": {"en": "tap-water-report-{slug}-en.pdf", "fr": "rapport-eau-{slug}-fr.pdf"},

    # comparison report (utils/compare_report.py), page "Town against town"
    "pdf.cmp.section": {"en": "Take the comparison with you", "fr": "Emportez la comparaison"},
    "pdf.cmp.section.text": {
        "en": "The towns compared above fit in a PDF you can print or send, in English or in French: each town with its "
              "score, grade and three marks, a chart that puts them side by side, why the best does better than the "
              "worst, the position of each against the national median, the method and the sources.",
        "fr": "Les communes comparées ci-dessus tiennent dans un PDF à imprimer ou à envoyer, en anglais ou en français : "
              "chaque commune avec son score, sa note et ses trois notes, un graphique qui les met côte à côte, pourquoi "
              "la meilleure fait mieux que la moins bonne, la position de chacune face à la médiane nationale, la méthode "
              "et les sources."},
    "pdf.cmp.button": {"en": "Download the comparison (PDF, English)", "fr": "Télécharger la comparaison (PDF, anglais)"},
    "pdf.cmp.button.fr": {"en": "Download the comparison (PDF, French)",
                          "fr": "Télécharger la comparaison (PDF, français)"},
    "pdf.cmp.button.help": {
        "en": "A report of two to four pages on the towns compared. Every sentence is written by fixed rules from the "
              "data, without artificial intelligence.",
        "fr": "Un rapport de deux à quatre pages sur les communes comparées. Chaque phrase est écrite par des règles "
              "fixes à partir des données, sans intelligence artificielle."},
    "pdf.cmp.doc_title": {"en": "Tap water comparison", "fr": "Comparaison de l'eau du robinet"},
    "pdf.cmp.title": {"en": "{first} and {last}", "fr": "{first} et {last}"},
    "pdf.cmp.facts": {"en": "{n} towns compared, each with the score of its networks over the latest tests.",
                      "fr": "{n} communes comparées, chacune avec le score de ses réseaux sur les derniers contrôles."},
    "pdf.cmp.k.towns": {"en": "The towns, one by one", "fr": "Les communes, une par une"},
    "pdf.cmp.marks": {"en": "The three marks: {marks}", "fr": "Les trois notes : {marks}"},
    "pdf.cmp.unscored": {
        "en": "{town} has no score: none of its networks had enough tests in the windows of the score, so it is left "
              "out of the comparison.",
        "fr": "{town} n'a pas de score : aucun de ses réseaux n'a eu assez de contrôles dans les fenêtres du score, elle "
              "est donc laissée hors de la comparaison."},
    "pdf.cmp.k.chart": {"en": "Side by side", "fr": "Côte à côte"},
    "pdf.cmp.score": {"en": "Score out of 100", "fr": "Score sur 100"},
    "pdf.cmp.chart.caption": {
        "en": "Bars: the score, then each of the three marks, on the same scale from 0 to 100; the name of the town is on "
              "the left of its bar and the value on the right; \"n/a\" when the family was not measured.",
        "fr": "Barres : le score, puis chacune des trois notes, sur la même échelle de 0 à 100 ; le nom de la commune est "
              "à gauche de sa barre et la valeur à droite ; « n.d. » quand la famille n'a pas été mesurée."},
    "pdf.cmp.k.why": {"en": "Why one town does better than the other", "fr": "Pourquoi une commune fait mieux que l'autre"},
    "pdf.cmp.k.position": {"en": "Against the national median", "fr": "Face à la médiane nationale"},
    "pdf.cmp.pos.text": {"en": "Half of the French towns score {nat} or more. Against this middle: {list}.",
                         "fr": "La moitié des communes françaises a {nat} ou plus. Face à ce milieu : {list}."},
    "pdf.cmp.pos.town": {"en": "{town} {pos}", "fr": "{town} {pos}"},
    "pdf.cmp.more": {"en": "and-{n}-more", "fr": "et-{n}-autres"},
    "pdf.cmp.more.one": {"en": "and-{n}-more", "fr": "et-{n}-autre"},
    "pdf.cmp.filename": {"en": "tap-water-comparison-{slug}-en.pdf", "fr": "comparaison-eau-{slug}-fr.pdf"},
}

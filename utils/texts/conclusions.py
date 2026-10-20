"""Page "What it all means": each hypothesis restated, the numbers, the verdict and what we conclude; one summary chart;
implications for a resident and for local authorities; limits and next steps."""

T = {
    "con.kicker": {"en": "Conclusions", "fr": "Conclusions"},
    "con.title": {"en": "What it all means", "fr": "Ce qu'il faut en retenir"},
    "con.preview": {
        "en": "This page comes second on purpose: it is the summary of the findings, given before the evidence. The pages "
              "that follow bring the proof, one question at a time: how to read a water test, the water of your own "
              "town, towns side by side, the map of France and its two hypotheses on small networks and on bacteria "
              "against chemistry, what the monitoring looks for and finds over ten years, and a score you can build "
              "yourself to test our method. Each hypothesis below also links to the page that tests it.",
        "fr": "Cette page vient en deuxième, à dessein : c'est le résumé des résultats, donné avant les preuves. Les pages "
              "suivantes apportent ces preuves, une question à la fois : lire une analyse d'eau, l'eau de votre propre "
              "commune, des communes côte à côte, la carte de France et ses deux hypothèses sur les petits réseaux et sur "
              "les bactéries face à la chimie, ce que le contrôle cherche et trouve sur dix ans, et un score à construire "
              "vous-même pour mettre notre méthode à l'épreuve. Chaque hypothèse ci-dessous renvoie aussi à la page qui "
              "la teste."},
    "con.proof": {"en": "The evidence: {page}", "fr": "Les preuves : {page}"},
    "con.lede": {
        "en": "In {year}, {bact} of bacterial samples and {chem} of chemical samples met the health limits. French tap "
              "water is good in the vast majority of places; the problems exist, but they are concentrated and, for a "
              "large part, explainable. Here is what each of our four hypotheses became.",
        "fr": "En {year}, {bact} des prélèvements bactériologiques et {chem} des prélèvements chimiques respectaient les "
              "limites sanitaires. L'eau du robinet française est bonne dans l'immense majorité des endroits ; les problèmes "
              "existent, mais ils sont concentrés et, pour une large part, explicables. Voici ce que sont devenues nos "
              "quatre hypothèses."},
    "con.found.kicker": {"en": "Hypothesis by hypothesis", "fr": "Hypothèse par hypothèse"},
    "con.found.title": {"en": "Four hypotheses, four answers", "fr": "Quatre hypothèses, quatre réponses"},
    "con.lab.hyp": {"en": "The hypothesis.", "fr": "L'hypothèse."},
    "con.lab.data": {"en": "What the data says.", "fr": "Ce que disent les données."},
    "con.lab.verdict": {"en": "Verdict.", "fr": "Verdict."},

    "con.h1.title": {"en": "H1. Small networks", "fr": "H1. Les petits réseaux"},
    "con.h1.hyp": {
        "en": "Problems concentrate in small networks, those of villages and hamlets, which are tested only a few times a "
              "year.",
        "fr": "Les problèmes se concentrent dans les petits réseaux, ceux des villages et des hameaux, contrôlés seulement "
              "quelques fois par an."},
    "con.h1.data": {
        "en": "Networks tested fewer than twelve times a year carry {share_nc} of the bacterial failures for only {share_s} "
              "of the samples ({y0} to {y1}). Their failure rate is {a}, against {b} in the most tested networks.",
        "fr": "Les réseaux contrôlés moins de douze fois par an portent {share_nc} des échecs bactériologiques pour seulement "
              "{share_s} des prélèvements ({y0} à {y1}). Leur taux d'échec est de {a}, contre {b} dans les réseaux les plus "
              "contrôlés."},
    "con.h1.verdict": {
        "en": "Confirmed. The risk of a bacterial incident is not spread evenly: it sits in the smallest networks. This is "
              "also where a score rests on the fewest samples, which is why each score comes with a confidence level.",
        "fr": "Confirmée. Le risque d'incident bactériologique n'est pas réparti également : il se trouve dans les plus "
              "petits réseaux. C'est aussi là qu'un score repose sur le moins de prélèvements, d'où le niveau de confiance "
              "affiché avec chaque score."},

    "con.h2.title": {"en": "H2. Two different maps", "fr": "H2. Deux cartes différentes"},
    "con.h2.hyp": {
        "en": "Bacteria and chemistry do not hit the same places, because they do not have the same causes.",
        "fr": "Bactéries et chimie ne touchent pas les mêmes endroits, parce qu'elles n'ont pas les mêmes causes."},
    "con.h2.data": {
        "en": "Between mainland departments, the rank correlation of the two failure rates is ρ = {rho}, close to zero. The "
              "most affected departments are {top_b} for bacteria and {top_c} for chemistry.",
        "fr": "Entre départements de métropole, la corrélation de rang des deux taux d'échec est ρ = {rho}, proche de zéro. "
              "Les départements les plus touchés sont {top_b} pour les bactéries et {top_c} pour la chimie."},
    "con.h2.verdict": {
        "en": "Confirmed. A department can have very clean water on one side and repeated problems on the other, so a "
              "single national ranking hides more than it shows. The causes themselves are not in the data: the map says "
              "where, not why.",
        "fr": "Confirmée. Un département peut avoir une eau très propre d'un côté et des problèmes répétés de l'autre : un "
              "classement national unique cache plus qu'il ne montre. Les causes elles-mêmes ne sont pas dans les données : "
              "la carte dit où, pas pourquoi."},

    "con.h3.title": {"en": "H3. What we look for", "fr": "H3. Ce qu'on cherche"},
    "con.h3.hyp": {
        "en": "Part of the recent chemical non-compliance comes from what laboratories search and how molecules are "
              "classified, rather than from worse water.",
        "fr": "Une partie des non-conformités chimiques récentes vient de ce que cherchent les laboratoires et de la façon "
              "de classer les molécules, plutôt que d'une eau plus mauvaise."},
    "con.h3.data": {
        "en": "Officially non-compliant samples went from {before} a year (2016 to 2020) to {during} (2021 to 2024), then "
              "{y2025} in 2025. Without three families of pesticide metabolites, limit exceedances would have gone from "
              "{w0} in 2016 to {w1} in 2025, while with them they went from {a0} to {a1}.",
        "fr": "Les prélèvements officiellement non conformes sont passés de {before} par an (2016 à 2020) à {during} (2021 à "
              "2024), puis {y2025} en 2025. Sans trois familles de métabolites de pesticides, les dépassements de limite "
              "seraient passés de {w0} en 2016 à {w1} en 2025, alors qu'avec elles ils sont passés de {a0} à {a1}."},
    "con.h3.verdict": {
        "en": "Confirmed, and the main finding. The rise of 2021 and the fall of 2025 follow molecules entering the "
              "monitoring and then being reclassified by Anses. Without them, exceedances still grow a little, which deserves "
              "attention, but nothing like the official curve suggests.",
        "fr": "Confirmée, et c'est le résultat principal. La hausse de 2021 et la baisse de 2025 suivent l'entrée de "
              "molécules dans le contrôle puis leur reclassement par l'Anses. Sans elles, les dépassements augmentent quand "
              "même un peu, ce qui mérite l'attention, mais rien de comparable à ce que suggère la courbe officielle."},

    "con.h4.title": {"en": "H4. Limescale", "fr": "H4. Le calcaire"},
    "con.h4.hyp": {
        "en": "Hardness varies a lot across France, without health stakes.",
        "fr": "La dureté varie énormément selon les territoires, sans enjeu sanitaire."},
    "con.h4.data": {
        "en": "Network hardness ranges from {lo} °f to {hi} °f between the 5th and the 95th percentile, a percentile being "
              "the value below which a given share of the networks falls.",
        "fr": "La dureté des réseaux va de {lo} °f à {hi} °f entre le 5e et le 95e centile, un centile étant la valeur sous "
              "laquelle se trouve une part donnée des réseaux."},
    "con.h4.verdict": {
        "en": "Confirmed. It is the difference people notice most in daily life and the one that matters least for health: "
              "the health agencies state that hard water has no effect on health (source 37), and it never lowers the score.",
        "fr": "Confirmée. C'est la différence que l'on remarque le plus au quotidien et celle qui compte le moins pour la "
              "santé : les agences de santé indiquent qu'une eau calcaire n'a aucune incidence sur la santé (source 37), et "
              "elle ne fait jamais baisser le score."},

    "con.score": {
        "en": "**And the score?** Its ranking barely moves when weights or rules change (rank correlation of 0.95 or more for "
              "{k} of {n} variants), and networks with official failures score clearly lower than the others. It is a "
              "reliable way to compare places, not a health verdict.",
        "fr": "**Et le score ?** Son classement bouge à peine quand les poids ou les règles changent (corrélation de rang de "
              "0,95 ou plus pour {k} des {n} variantes), et les réseaux avec des échecs officiels ont des scores nettement "
              "plus bas que les autres. C'est un moyen fiable de comparer des lieux, pas un verdict sanitaire."},

    "con.chart.title": {"en": "Limit exceedances per year, with and without the three pesticide metabolite families",
                        "fr": "Dépassements de limite par année, avec et sans les trois familles de métabolites de pesticides"},
    "con.chart.with": {"en": "All substances", "fr": "Toutes les substances"},
    "con.chart.without": {"en": "Without the three metabolite families", "fr": "Sans les trois familles de métabolites"},
    "con.chart.y": {"en": "Limit exceedances (sample × substance)", "fr": "Dépassements de limite (prélèvement × substance)"},
    "con.chart.caption": {
        "en": "Two lines per year: all chemical limit exceedances (dark grey) and the same count without the metabolites of "
              "chloridazon, ESA-metolachlor and chlorothalonil (teal, dashed); one count per sample and substance.",
        "fr": "Deux courbes par année : tous les dépassements de limites chimiques (gris foncé) et le même compte sans les "
              "métabolites de la chloridazone, l'ESA-métolachlore et le chlorothalonil (bleu-vert, tirets) ; un compte par "
              "prélèvement et par substance."},
    "con.chart.take": {
        "en": "This single chart sums up the investigation. The full line climbs from {a0} to a peak of {apeak}; the dashed "
              "line, without the three metabolite families, only goes from {w0} to {w1}. Most of the official rise is about "
              "what was searched, not about what changed in the water.",
        "fr": "Ce seul graphique résume l'enquête. La courbe pleine monte de {a0} à un pic de {apeak} ; la courbe en tirets, "
              "sans les trois familles de métabolites, va seulement de {w0} à {w1}. L'essentiel de la hausse officielle tient "
              "à ce qui a été cherché, pas à ce qui a changé dans l'eau."},

    "con.means.kicker": {"en": "What it means", "fr": "Ce que cela change"},
    "con.means.title": {"en": "For a resident, and for local authorities", "fr": "Pour un habitant, et pour les collectivités"},
    "con.resident": {
        "en": "**For a resident.** Look up your town and read the report rather than the grade alone: it says what was "
              "found, when, and what was never measured. Keep an eye on the confidence level, because a small network with "
              "few samples can lose a grade after a single bad day. If you live in an old building, lead is a matter for "
              "the pipes of the building: let the cold water run before drinking and use only cold water for cooking "
              "(ARS Pays de la Loire, source 26). The official opinion on your water remains the one of your regional health "
              "agency, also summarised in the note attached to your water bill.",
        "fr": "**Pour un habitant.** Cherchez votre commune et lisez le rapport plutôt que la seule note : il dit ce qui a été "
              "trouvé, quand, et ce qui n'a jamais été mesuré. Regardez le niveau de confiance, car un petit réseau avec peu "
              "de prélèvements peut perdre une note après une seule mauvaise journée. Si vous habitez un immeuble ancien, le "
              "plomb est une affaire de canalisations de l'immeuble : laissez couler l'eau froide avant de boire et "
              "n'utilisez que l'eau froide pour cuisiner (ARS Pays de la Loire, source 26). L'avis officiel sur votre eau "
              "reste celui de votre agence régionale de santé, aussi résumé dans la note jointe à votre facture d'eau."},
    "con.authorities": {
        "en": "**For local authorities.** Bacterial failures concentrate in small networks, and the causes listed by the "
              "health agencies are poorly protected catchments, inadequate disinfection and bad weather (source 33): this is "
              "where protection and treatment bring the most. A rise in non-compliance should always be read together with "
              "the history of the monitoring, since new molecules or new thresholds can move the curve on their own. Two "
              "deadlines are coming: PFAS are part of the routine control since 1 January 2026 (source 11), and the lead "
              "limit will drop from 10 to 5 µg/L in January 2036 (source 26), which means replacing the remaining lead "
              "pipes.",
        "fr": "**Pour les collectivités.** Les échecs bactériologiques se concentrent dans les petits réseaux, et les causes "
              "citées par les agences de santé sont des captages mal protégés, une désinfection inadaptée et les intempéries "
              "(source 33) : c'est là que la protection et le traitement rapportent le plus. Une hausse des non-conformités "
              "doit toujours se lire avec l'histoire du contrôle, puisque de nouvelles molécules ou de nouveaux seuils "
              "peuvent faire bouger la courbe à eux seuls. Deux échéances arrivent : les PFAS font partie du contrôle courant "
              "depuis le 1er janvier 2026 (source 11), et la limite du plomb passera de 10 à 5 µg/L en janvier 2036 "
              "(source 26), ce qui veut dire remplacer les canalisations en plomb restantes."},
    "con.limits.kicker": {"en": "Limits and next steps", "fr": "Limites et suites"},
    "con.limits": {
        "en": "The score is a teaching indicator, not a health opinion. Some families are judged by our own recomputation, the "
              "population served by each network is unknown, 2026 is incomplete and the Mediterranean coast is approximated; "
              "and everywhere in this app, a correlation is not a cause. The natural next steps are a score for every year, "
              "to follow each town over time, the complete 2026 PFAS results, and the population of each network to weigh "
              "the indicators.",
        "fr": "Le score est un indicateur pédagogique, pas un avis sanitaire. Certaines familles sont jugées par notre propre "
              "recalcul, la population desservie par chaque réseau est inconnue, 2026 est incomplète et le littoral "
              "méditerranéen est approché ; et partout dans cette application, une corrélation n'est pas une cause. Les "
              "suites naturelles sont un score pour chaque année, pour suivre chaque commune dans le temps, les résultats "
              "PFAS complets de 2026, et la population de chaque réseau pour pondérer les indicateurs."},
}

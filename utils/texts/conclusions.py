"""Page "What it all means": answers to the four hypotheses, one summary chart, implications, limits, next steps."""

T = {
    "con.kicker": {"en": "Conclusions", "fr": "Conclusions"},
    "con.title": {"en": "What it all means", "fr": "Ce qu'il faut en retenir"},
    "con.lede": {
        "en": "In {year}, {bact} of bacterial samples and {chem} of chemical samples met the health limits. French tap "
              "water is good in the vast majority of places; the problems exist, but they are concentrated and, for a "
              "large part, explainable.",
        "fr": "En {year}, {bact} des prélèvements bactériologiques et {chem} des prélèvements chimiques respectaient les "
              "limites sanitaires. L'eau du robinet française est bonne dans l'immense majorité des endroits ; les "
              "problèmes existent, mais ils sont concentrés et, pour une large part, explicables."},
    "con.found.kicker": {"en": "What the data says", "fr": "Ce que disent les données"},
    "con.found.title": {"en": "Four hypotheses, four answers", "fr": "Quatre hypothèses, quatre réponses"},
    "con.h1": {
        "en": "**Small networks fail more often (H1, confirmed).** Networks tested fewer than twelve times a year carry "
              "{share_nc} of the bacterial failures for only {share_s} of the samples. Their failure rate is {a}, against "
              "{b} in the most tested networks.",
        "fr": "**Les petits réseaux échouent plus souvent (H1, confirmée).** Les réseaux contrôlés moins de douze fois par "
              "an portent {share_nc} des échecs bactériologiques pour seulement {share_s} des prélèvements. Leur taux "
              "d'échec est de {a}, contre {b} dans les réseaux les plus contrôlés."},
    "con.h2": {
        "en": "**Bacteria and chemistry draw two different maps (H2, confirmed).** Between mainland departments, the rank "
              "correlation of the two failure rates is ρ = {rho}, close to zero. The most affected departments are {top_b} "
              "for bacteria and {top_c} for chemistry.",
        "fr": "**Bactéries et chimie dessinent deux cartes différentes (H2, confirmée).** Entre départements de métropole, "
              "la corrélation de rang des deux taux d'échec est ρ = {rho}, proche de zéro. Les départements les plus "
              "touchés sont {top_b} pour les bactéries et {top_c} pour la chimie."},
    "con.h3": {
        "en": "**Chemical failures follow what we look for (H3, confirmed, the main finding).** Non-compliant samples went "
              "from {before} a year (2016 to 2020) to {during} (2021 to 2024), then {y2025} in 2025. The rise and the fall "
              "follow pesticide metabolites that entered the monitoring, then were reclassified by Anses.",
        "fr": "**Les échecs chimiques suivent ce qu'on cherche (H3, confirmée, le résultat principal).** Les prélèvements "
              "non conformes sont passés de {before} par an (2016 à 2020) à {during} (2021 à 2024), puis {y2025} en 2025. "
              "La hausse et la baisse suivent des métabolites de pesticides entrés dans le contrôle, puis reclassés par "
              "l'Anses."},
    "con.h4": {
        "en": "**Limescale varies a lot, without health stakes (H4, confirmed).** Network hardness ranges from {lo} °f to "
              "{hi} °f between the 5th and the 95th percentile, a percentile being the value below which a given share "
              "of networks falls. It never lowers the score.",
        "fr": "**Le calcaire varie beaucoup, sans enjeu sanitaire (H4, confirmée).** La dureté des réseaux va de {lo} °f à "
              "{hi} °f entre le 5e et le 95e centile, un centile étant la valeur sous laquelle se trouve une part donnée "
              "des réseaux. Elle ne fait jamais baisser le score."},
    "con.score": {
        "en": "**The score holds up.** Its ranking barely moves when weights or rules change (rank correlation of 0.95 or "
              "more for {k} of {n} variants), and networks with official failures score clearly lower than the others.",
        "fr": "**Le score tient la route.** Son classement bouge à peine quand les poids ou les règles changent "
              "(corrélation de rang de 0,95 ou plus pour {k} des {n} variantes), et les réseaux avec des échecs officiels "
              "ont des scores nettement plus bas que les autres."},
    "con.chart.title": {"en": "Limit exceedances per year, with and without the three pesticide metabolite families",
                        "fr": "Dépassements de limite par année, avec et sans les trois familles de métabolites de pesticides"},
    "con.chart.with": {"en": "All substances", "fr": "Toutes les substances"},
    "con.chart.without": {"en": "Without the three metabolite families", "fr": "Sans les trois familles de métabolites"},
    "con.chart.y": {"en": "Limit exceedances (sample × substance)", "fr": "Dépassements de limite (prélèvement × substance)"},
    "con.chart.caption": {
        "en": "Two lines per year: all chemical limit exceedances (dark grey) and the same count without the metabolites "
              "of chloridazon, ESA-metolachlor and chlorothalonil (teal, dashed); one count per sample and substance.",
        "fr": "Deux courbes par année : tous les dépassements de limites chimiques (gris foncé) et le même compte sans les "
              "métabolites de la chloridazone, l'ESA-métolachlore et le chlorothalonil (bleu-vert, tirets) ; un compte "
              "par prélèvement et par substance."},
    "con.chart.take": {
        "en": "Remove three families of molecules and the 2021 jump almost disappears: the dashed line stays close to "
              "its 2016 level. This single chart sums up the investigation.",
        "fr": "Retirez trois familles de molécules et le saut de 2021 disparaît presque : la ligne en tirets reste proche "
              "de son niveau de 2016. Ce seul graphique résume l'enquête."},

    "con.means.kicker": {"en": "What it means", "fr": "Ce que cela change"},
    "con.means.title": {"en": "For you, and for those who decide", "fr": "Pour vous, et pour ceux qui décident"},
    "con.resident": {
        "en": "**If you live somewhere.** Look up your town and read the report rather than the grade alone: it says what "
              "was found, when, and what was never measured. Keep an eye on the confidence level, because a small network "
              "with few samples can lose a grade after a single bad day. The official opinion on your water remains the "
              "one of your regional health agency, also summarised in the note attached to your water bill.",
        "fr": "**Si vous habitez quelque part.** Cherchez votre commune et lisez le rapport plutôt que la seule note : il "
              "dit ce qui a été trouvé, quand, et ce qui n'a jamais été mesuré. Regardez le niveau de confiance, car un "
              "petit réseau avec peu de prélèvements peut perdre une note après une seule mauvaise journée. L'avis "
              "officiel sur votre eau reste celui de votre agence régionale de santé, aussi résumé dans la note jointe à "
              "votre facture d'eau."},
    "con.decider": {
        "en": "**If you decide, report or teach.** Small networks are where bacterial failures concentrate, so that is "
              "where attention brings the most. And a rise in non-compliance can come from new molecules searched or new "
              "thresholds as much as from pollution: a trend should always be read together with the history of the "
              "monitoring. PFAS, measured everywhere only since 2026, will be the next test of that lesson.",
        "fr": "**Si vous décidez, informez ou enseignez.** Les petits réseaux concentrent les échecs bactériologiques : "
              "c'est là que l'attention rapporte le plus. Et une hausse des non-conformités peut venir de nouvelles "
              "molécules cherchées ou de nouveaux seuils autant que d'une pollution : une tendance doit toujours se lire "
              "avec l'histoire du contrôle. Les PFAS, mesurés partout seulement depuis 2026, seront la prochaine épreuve "
              "de cette leçon."},
    "con.limits.kicker": {"en": "Limits and next steps", "fr": "Limites et suites"},
    "con.limits": {
        "en": "The score is a teaching indicator, not a health opinion. Some families are judged by our own recomputation, "
              "the population served by each network is unknown, 2026 is incomplete and the Mediterranean coast is "
              "approximated; and everywhere in this app, a correlation is not a cause. The natural next steps are a score "
              "for every year, to follow each town over time, the complete 2026 PFAS results, and the population of each "
              "network to weigh the indicators.",
        "fr": "Le score est un indicateur pédagogique, pas un avis sanitaire. Certaines familles sont jugées par notre "
              "propre recalcul, la population desservie par chaque réseau est inconnue, 2026 est incomplète et le littoral "
              "méditerranéen est approché ; et partout dans cette application, une corrélation n'est pas une cause. Les "
              "suites naturelles sont un score pour chaque année, pour suivre chaque commune dans le temps, les résultats "
              "PFAS complets de 2026, et la population de chaque réseau pour pondérer les indicateurs."},
}

"""Page "Build your score": the reader's own weights, severities and thresholds, against the official settings."""

T = {
    "nav.myscore": {"en": "Build your own score", "fr": "Construisez votre score"},
    "my.kicker": {"en": "Your rules", "fr": "Vos règles"},
    "my.title": {"en": "Build your own score", "fr": "Construisez votre score"},
    "my.lede": {
        "en": "Our score rests on choices: how much bacteria count against chemistry, how severe a pesticide is compared "
              "with a metal, which value a measurement is compared with. Here you make those choices yourself, and you "
              "see at once what they change for a town and for the ranking of all French towns.",
        "fr": "Notre score repose sur des choix : combien comptent les bactéries face à la chimie, quelle gravité donner "
              "à un pesticide par rapport à un métal, à quelle valeur comparer une mesure. Ici, c'est vous qui faites ces "
              "choix, et vous voyez tout de suite ce qu'ils changent pour une commune et pour le classement de toutes les "
              "communes de France."},
    "my.warning": {
        "en": "These settings are yours and only yours. They are a way to explore the method, not a health rule: the "
              "regulatory limits stay what they are, and only the regional health agency (ARS) can say whether the "
              "water of a town is fit to drink. A town that looks bad with stricter settings does not have unsafe water "
              "because of it.",
        "fr": "Ces réglages sont les vôtres et seulement les vôtres. Ils servent à explorer la méthode, pas à fixer une "
              "règle sanitaire : les limites réglementaires restent ce qu'elles sont, et seule l'agence régionale de "
              "santé (ARS) peut dire si l'eau d'une commune est propre à la consommation. Une commune qui paraît moins "
              "bonne avec des réglages plus sévères n'a pas une eau dangereuse pour autant."},
    "my.pick": {"en": "Town to follow", "fr": "Commune à suivre"},
    "my.pick.help": {
        "en": "Its official score and your score are shown side by side. The same town is used on the page \"The water "
              "of my town\".",
        "fr": "Son score officiel et votre score sont affichés côte à côte. C'est la même commune que sur la page "
              "« L'eau de ma commune »."},
    "my.reset": {"en": "Back to the official settings", "fr": "Revenir aux réglages officiels"},
    "my.reset.help": {"en": "Puts every weight, severity and threshold back to the values used everywhere else in the app.",
                      "fr": "Remet chaque poids, chaque gravité et chaque seuil aux valeurs utilisées partout ailleurs "
                            "dans l'application."},
    "my.official_now": {"en": "You are using the official settings: your score is the published score.",
                        "fr": "Vous utilisez les réglages officiels : votre score est le score publié."},

    # --- settings ---------------------------------------------------------------------------------------------------
    "my.set.weights": {"en": "1. How much each family counts", "fr": "1. Combien compte chaque famille"},
    "my.set.weights.text": {
        "en": "The global score is a weighted mean of three marks. The weights are rescaled so that they add up to 100%. "
              "Official setting: 40% bacteria, 40% health chemistry, 20% comfort.",
        "fr": "Le score global est une moyenne pondérée de trois notes. Les poids sont remis à l'échelle pour que leur "
              "somme fasse 100 %. Réglage officiel : 40 % bactéries, 40 % chimie sanitaire, 20 % confort."},
    "my.w.micro.help": {"en": "Bacteria: share of samples that failed the bacteriological limits over twelve months.",
                        "fr": "Bactéries : part des prélèvements non conformes aux limites bactériologiques sur douze mois."},
    "my.w.chem.help": {"en": "Health chemistry: how close each substance with a health limit came to it over three years.",
                       "fr": "Chimie sanitaire : à quel point chaque substance soumise à une limite sanitaire s'en est "
                             "approchée sur trois ans."},
    "my.w.comfort.help": {"en": "Comfort: the warning lights (taste, colour, treatment indicators), which have no health "
                                "limit.",
                          "fr": "Confort : les voyants (goût, couleur, indicateurs de traitement), qui n'ont pas de limite "
                                "sanitaire."},
    "my.set.severity": {"en": "2. How severe each kind of problem is", "fr": "2. Quelle gravité pour chaque problème"},
    "my.set.severity.text": {
        "en": "A multiplier on the points lost by one group of substances. \"×2\" means that a pesticide close to its "
              "limit costs twice as many points as in the official score. For bacteria, the setting says how hard one "
              "failed sample hits a network.",
        "fr": "Un multiplicateur sur les points perdus par un groupe de substances. « ×2 » veut dire qu'un pesticide "
              "proche de sa limite coûte deux fois plus de points que dans le score officiel. Pour les bactéries, le "
              "réglage dit à quel point un prélèvement non conforme pénalise un réseau."},
    "my.sev.pesticides": {"en": "Pesticides and their metabolites", "fr": "Pesticides et leurs métabolites"},
    "my.sev.nitrates": {"en": "Nitrates and nitrites", "fr": "Nitrates et nitrites"},
    "my.sev.metals": {"en": "Metals (lead, arsenic, nickel...)", "fr": "Métaux (plomb, arsenic, nickel...)"},
    "my.sev.pfas": {"en": "PFAS (sum of 20)", "fr": "PFAS (somme de 20)"},
    "my.sev.disinfection_byproducts": {"en": "Disinfection by-products", "fr": "Sous-produits de désinfection"},
    "my.sev.help": {
        "en": "×1 is the official setting. A metabolite is what a pesticide turns into once it breaks down in soil or "
              "water. Disinfection by-products form when chlorine reacts with natural organic matter.",
        "fr": "×1 est le réglage officiel. Un métabolite est ce que devient un pesticide quand il se dégrade dans le sol "
              "ou l'eau. Les sous-produits de désinfection se forment quand le chlore réagit avec la matière organique "
              "naturelle."},
    "my.k": {"en": "Bacteria: weight of one failed sample", "fr": "Bactéries : poids d'un prélèvement non conforme"},
    "my.k.help": {
        "en": "The bacteria mark is 100 × (1 − t)^k, where t is the share of failed samples. The higher k, the harder one "
              "failure hits. Official setting: k = 5, where one failure in twenty samples gives a mark of 77.",
        "fr": "La note bactéries vaut 100 × (1 − t)^k, où t est la part de prélèvements non conformes. Plus k est grand, "
              "plus un échec pèse lourd. Réglage officiel : k = 5, où un échec sur vingt prélèvements donne une note "
              "de 77."},
    "my.k.2.5": {"en": "lenient (k = 2.5)", "fr": "indulgent (k = 2,5)"},
    "my.k.5.0": {"en": "official (k = 5)", "fr": "officiel (k = 5)"},
    "my.k.10.0": {"en": "strict (k = 10)", "fr": "sévère (k = 10)"},
    "my.k.20.0": {"en": "very strict (k = 20)", "fr": "très sévère (k = 20)"},
    "my.set.thr": {"en": "3. Which value a measurement is compared with", "fr": "3. À quelle valeur comparer une mesure"},
    "my.set.thr.text": {
        "en": "Each measurement is divided by a threshold, and points are lost from half of it. Lowering a threshold "
              "makes the score stricter for that substance. The official values are the regulatory limits written on "
              "every analysis result (sources 9 and 10).",
        "fr": "Chaque mesure est divisée par un seuil, et des points sont perdus dès la moitié de ce seuil. Baisser un "
              "seuil rend le score plus sévère pour cette substance. Les valeurs officielles sont les limites "
              "réglementaires inscrites sur chaque résultat d'analyse (sources 9 et 10)."},
    "my.thr.NO3": {"en": "Nitrates (mg/L)", "fr": "Nitrates (mg/L)"},
    "my.thr.PB": {"en": "Lead (µg/L)", "fr": "Plomb (µg/L)"},
    "my.thr.AS": {"en": "Arsenic (µg/L)", "fr": "Arsenic (µg/L)"},
    "my.thr.SPFAS": {"en": "PFAS, sum of 20 (µg/L)", "fr": "PFAS, somme de 20 (µg/L)"},
    "my.thr.PEST": {"en": "Each pesticide (µg/L)", "fr": "Chaque pesticide (µg/L)"},
    "my.thr.help": {"en": "Official value: {v} {unit}.", "fr": "Valeur officielle : {v} {unit}."},
    "my.thr.PEST.help": {
        "en": "Official value: 0.1 µg/L for each pesticide (0.03 µg/L for aldrin, dieldrin, heptachlor and its epoxides, moved in proportion). The "
              "0.5 µg/L limits on sums (total of pesticides, atrazine and its metabolites, terbuthylazine and its "
              "metabolites) are not changed.",
        "fr": "Valeur officielle : 0,1 µg/L pour chaque pesticide (0,03 µg/L pour l'aldrine, la dieldrine, "
              "l'heptachlore et ses époxydes, déplacés en proportion). Les limites de 0,5 µg/L sur des sommes (total des pesticides, atrazine et ses métabolites, terbuthylazine "
              "et ses métabolites) ne sont pas modifiées."},
    "my.w.zero": {"en": "At least one weight must be above zero.", "fr": "Au moins un poids doit être supérieur à zéro."},

    # --- results ----------------------------------------------------------------------------------------------------
    "my.res.kicker": {"en": "What your rules change", "fr": "Ce que vos règles changent"},
    "my.res.title": {"en": "Your score against the official one", "fr": "Votre score face au score officiel"},
    "my.res.headline": {
        "en": "With your settings, {town} scores {mine}/100 (grade {g_mine}) against {off}/100 (grade {g_off}) officially, "
              "and ranks {r_mine} of {n} towns instead of {r_off}.",
        "fr": "Avec vos réglages, {town} obtient {mine}/100 (note {g_mine}) contre {off}/100 (note {g_off}) "
              "officiellement, et se classe {r_mine} sur {n} communes au lieu de {r_off}."},
    "my.res.headline.same": {
        "en": "With your settings, {town} scores {mine}/100 (grade {g_mine}) against {off}/100 (grade {g_off}) "
              "officially, and keeps its rank: {r_mine} of {n} towns.",
        "fr": "Avec vos réglages, {town} obtient {mine}/100 (note {g_mine}) contre {off}/100 (note {g_off}) "
              "officiellement, et garde son rang : {r_mine} sur {n} communes."},
    "my.res.noscore": {"en": "{town} has no score, official or personal: none of its networks was sampled recently.",
                       "fr": "{town} n'a pas de score, ni officiel ni personnel : aucun de ses réseaux n'a été contrôlé "
                             "récemment."},
    "my.m.official": {"en": "Official score", "fr": "Score officiel"},
    "my.m.mine": {"en": "Your score", "fr": "Votre score"},
    "my.m.rank": {"en": "Your rank", "fr": "Votre rang"},
    "my.m.rank.help": {"en": "1 is the best score among the {n} towns with a score; towns with the same score share a rank.",
                       "fr": "1 est le meilleur score parmi les {n} communes notées ; des communes à égalité partagent "
                             "le même rang."},
    "my.m.changed": {"en": "Towns changing grade", "fr": "Communes changeant de note"},
    "my.subs.title": {"en": "The three marks of {town}, official settings against yours",
                      "fr": "Les trois notes de {town}, réglages officiels contre les vôtres"},
    "my.subs.caption": {
        "en": "Grouped horizontal bars: for each family, the official mark (grey, hatched) and yours (blue), out of 100, "
              "value written at the end of each bar. A family that was not measured has no bar.",
        "fr": "Barres horizontales groupées : pour chaque famille, la note officielle (gris, hachuré) et la vôtre (bleu), "
              "sur 100, valeur écrite au bout de chaque barre. Une famille non mesurée n'a pas de barre."},
    "my.subs.take.same": {
        "en": "Your settings do not change the marks of {town}: what you made stricter or lighter is not what this town "
              "is measured or penalised on.",
        "fr": "Vos réglages ne changent pas les notes de {town} : ce que vous avez rendu plus sévère ou plus léger n'est "
              "pas ce sur quoi cette commune est mesurée ou pénalisée."},
    "my.subs.take": {
        "en": "The biggest move is in {fam}: {off} officially, {mine} with your settings. This is where your choices "
              "touch what was actually measured in {town}.",
        "fr": "Le plus grand changement porte sur la famille {fam} : {off} officiellement, {mine} avec vos réglages. "
              "C'est là que vos choix touchent ce qui a vraiment été mesuré à {town}."},
    "my.official": {"en": "Official settings", "fr": "Réglages officiels"},
    "my.yours": {"en": "Your settings", "fr": "Vos réglages"},
    "my.dist.title": {"en": "Share of French towns in each grade, official settings against yours",
                      "fr": "Part des communes françaises dans chaque note, réglages officiels contre les vôtres"},
    "my.dist.caption": {
        "en": "Grouped bars: share of the towns with a score in each grade from A to E, with the official settings "
              "(grey, hatched) and with yours (blue), values written on top.",
        "fr": "Barres groupées : part des communes notées dans chaque note de A à E, avec les réglages officiels (gris, "
              "hachuré) et avec les vôtres (bleu), valeurs écrites au-dessus."},
    "my.dist.take": {
        "en": "{changed} of the towns change grade, but the order of the towns keeps a rank correlation of {rho} with "
              "the official one (1 would mean exactly the same order, 0 no link at all). A rank correlation compares "
              "the positions in the two rankings, not the scores themselves.",
        "fr": "{changed} des communes changent de note, mais l'ordre des communes garde une corrélation de rang de "
              "{rho} avec l'ordre officiel (1 voudrait dire exactement le même ordre, 0 aucun lien). Une corrélation de "
              "rang compare les positions dans les deux classements, pas les scores eux-mêmes."},
    "my.dist.take.same": {
        "en": "With the official settings, every town keeps its grade. Move a weight, a severity or a threshold above and "
              "the blue bars will show how the grades of all French towns shift.",
        "fr": "Avec les réglages officiels, chaque commune garde sa note. Déplacez un poids, une gravité ou un seuil "
              "ci-dessus et les barres bleues montreront comment les notes de toutes les communes se déplacent."},
    "my.low.title": {"en": "The ten lowest-scoring towns of more than 10,000 inhabitants with your settings",
                     "fr": "Les dix communes de plus de 10 000 habitants au score le plus bas avec vos réglages"},
    "my.low.caption": {
        "en": "Table: for each town, your score and grade, then the official ones and the official rank among the same "
              "large towns. Large towns are shown because their scores rest on many samples.",
        "fr": "Tableau : pour chaque commune, votre score et votre note, puis le score et la note officiels et le rang "
              "officiel parmi ces mêmes grandes communes. Les grandes communes sont montrées parce que leur score repose "
              "sur beaucoup de prélèvements."},
    "my.col.town": {"en": "Town", "fr": "Commune"},
    "my.col.mine": {"en": "Your score", "fr": "Votre score"},
    "my.col.g_mine": {"en": "Your grade", "fr": "Votre note"},
    "my.col.off": {"en": "Official score", "fr": "Score officiel"},
    "my.col.g_off": {"en": "Official grade", "fr": "Note officielle"},
    "my.col.r_off": {"en": "Official rank (from the bottom)", "fr": "Rang officiel (depuis le bas)"},
    "my.analysis.seen": {
        "en": "Most settings move the letters more than the order: the towns at the bottom stay at the bottom, because "
              "a network that fails in one family loses many points there whatever the weights.",
        "fr": "La plupart des réglages déplacent les lettres plus que l'ordre : les communes du bas restent en bas, "
              "parce qu'un réseau qui échoue dans une famille y perd beaucoup de points, quels que soient les poids."},
    "my.analysis.why": {
        "en": "Thresholds and severities only act on substances that were measured and found. Making PFAS twice as "
              "severe changes nothing where none was found: in the three years scored, PFAS were measured in {pfas} of "
              "the {nets} scored networks and found above the quantification limit in {found}; they joined the routine "
              "control only on 1 January 2026 (source 11).",
        "fr": "Les seuils et les gravités n'agissent que sur les substances mesurées et trouvées. Rendre les PFAS deux "
              "fois plus graves ne change rien là où aucun n'a été trouvé : sur les trois années notées, les PFAS ont été "
              "mesurés dans {pfas} des {nets} réseaux notés et trouvés au-dessus de la limite de quantification dans "
              "{found} ; ils ne sont entrés dans le contrôle courant que le 1er janvier 2026 (source 11)."},
    "my.analysis.lim": {
        "en": "A personal score is a thought experiment. It does not say that a threshold is wrong, and an absence of "
              "measurement is not an absence of pollutant.",
        "fr": "Un score personnel est une expérience de pensée. Il ne dit pas qu'un seuil est faux, et une absence de "
              "mesure n'est pas une absence de polluant."},
    "my.dist.y": {"en": "Towns (%)", "fr": "Communes (%)"},
    "my.rank.fmt.one": {"en": "1st", "fr": "1re"},

    # --- link from "What we look for" -----------------------------------------------------------------------------
    "mon.whatif.link.text": {
        "en": "The default weights, 40% bacteria, 40% health chemistry and 20% comfort, are a choice, not a law. On the "
              "page \"Build your own score\" you can change them, make some substances more severe (pesticides, lead, "
              "PFAS...) and move the key thresholds, then see how a town and the whole ranking react. The fourteen "
              "variants of the sensitivity analysis are there too.",
        "fr": "Les poids par défaut, 40 % bactéries, 40 % chimie sanitaire et 20 % confort, sont un choix, pas une loi. "
              "Sur la page « Construisez votre score », vous pouvez les changer, rendre certaines substances plus graves "
              "(pesticides, plomb, PFAS...) et déplacer les seuils clés, puis voir comment réagissent une commune et "
              "tout le classement. Les quatorze variantes de l'analyse de sensibilité s'y trouvent aussi."},
    "mon.whatif.link": {"en": "Build your own score", "fr": "Construisez votre score"},
}

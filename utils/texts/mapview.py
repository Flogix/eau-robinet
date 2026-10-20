"""Page "The map of France": KPIs, department map, rankings, H2 scatter, H1 bars, distribution, trend, networks."""

T = {
    "map.kicker": {"en": "The national picture", "fr": "Le tableau national"},
    "map.title": {"en": "The map of France", "fr": "La carte de France"},
    "map.lede": {
        "en": "Where do problems happen? Use the sidebar to choose a family of substances, a period and a region; the "
              "map, the rankings and the trend follow.",
        "fr": "Où les problèmes se produisent-ils ? Choisissez dans la barre latérale une famille de substances, une "
              "période et une région : la carte, les classements et la tendance suivent."},
    "map.kpi.note": {"en": "These four numbers are explained in detail on the home page.",
                     "fr": "Ces quatre chiffres sont expliqués en détail sur la page d'accueil."},
    "map.headline.score": {"en": "The median score of the towns ranges from {lo_v}/100 in {lo} to {hi_v}/100 in {hi}.",
                           "fr": "Le score médian des communes va de {lo_v}/100 en {lo} à {hi_v}/100 en {hi}."},
    "map.headline.var": {
        "en": "{var}: from {lo_v} of networks with at least one problem a year in {lo} to {hi_v} in {hi}, {period}.",
        "fr": "{var} : de {lo_v} des réseaux avec au moins un problème par an en {lo} à {hi_v} en {hi}, {period}."},
    "map.value.score": {"en": "Median town score (out of 100)", "fr": "Score médian des communes (sur 100)"},
    "map.value.var": {"en": "Networks with at least one problem in a year (%)",
                      "fr": "Réseaux avec au moins un problème dans l'année (%)"},
    "map.hover.score": {"en": "{dep}<br>median score {v}/100<br>{n} towns",
                        "fr": "{dep}<br>score médian {v}/100<br>{n} communes"},
    "map.hover.var": {"en": "{dep}<br>{v} of network-years with at least one problem<br>{n} network-years",
                      "fr": "{dep}<br>{v} des réseaux-années avec au moins un problème<br>{n} réseaux-années"},
    "map.title.score": {"en": "Median score of the towns, department by department",
                        "fr": "Score médian des communes, département par département"},
    "map.title.var": {"en": "{var}: share of networks with at least one problem a year, {period}",
                      "fr": "{var} : part des réseaux avec au moins un problème par an, {period}"},
    "map.caption": {
        "en": "Map of mainland departments: the darker the colour, the {dir}. Departments with too little data are left "
              "blank; overseas departments are listed below the map. Hover a department for its value.",
        "fr": "Carte des départements de métropole : plus la couleur est foncée, {dir}. Les départements avec trop peu "
              "de données sont laissés en blanc ; les départements d'outre-mer sont listés sous la carte. Survolez un "
              "département pour voir sa valeur."},
    "map.dir.score": {"en": "better the score", "fr": "meilleur est le score"},
    "map.dir.var": {"en": "more networks were affected", "fr": "plus de réseaux ont été touchés"},
    "map.take.var": {
        "en": "A \"network-year\" is one network observed during one year; the map gives the share of them with at "
              "least one problem of the chosen family. The contrasts are strong and they are not the same from one "
              "family to the next: switch between bacteria and chemistry in the sidebar and the dark areas move. "
              "That is hypothesis H2, tested further down.",
        "fr": "Un « réseau-année » est un réseau observé pendant une année ; la carte donne la part d'entre eux avec au "
              "moins un problème de la famille choisie. Les contrastes sont forts et ne sont pas les mêmes d'une "
              "famille à l'autre : passez des bactéries à la chimie dans la barre latérale et les zones foncées se "
              "déplacent. C'est l'hypothèse H2, testée plus bas."},
    "map.take.score": {
        "en": 'In {k} of the {n} departments, the median town is graded B or better (75 and above). The differences that matter show up inside departments, between networks, which is why the score is computed town by town.',
        "fr": "Dans {k} des {n} départements, la commune médiane est notée B ou mieux (75 et plus). Les différences qui comptent apparaissent à l'intérieur des départements, entre réseaux, et c'est pourquoi le score est calculé commune par commune."},
    "map.overseas": {"en": "Overseas departments, not on the map: {list}",
                     "fr": "Départements d'outre-mer, absents de la carte : {list}"},
    "map.recomputed": {
        "en": "For this family the verdict is recomputed by us: a result above the threshold written next to it. The "
              "official verdict can differ (temporary exemptions, limits that changed over time): see Behind the numbers.",
        "fr": "Pour cette famille, le verdict est recalculé par nous : un résultat au-dessus du seuil écrit à côté de "
              "lui. Le verdict officiel peut différer (dérogations temporaires, limites qui ont changé) : voir Les "
              "coulisses des chiffres."},

    "map.rank.kicker": {"en": "Rankings", "fr": "Classements"},
    "map.rank.n": {"en": "Departments shown at each end", "fr": "Départements montrés à chaque extrémité"},
    "map.rank.title": {"en": "The {n} best and the {n} worst departments", "fr": "Les {n} meilleurs et les {n} moins bons départements"},
    "map.rank.best": {"en": "best", "fr": "meilleur"},
    "map.rank.worst": {"en": "worst", "fr": "moins bon"},
    "map.rank.caption": {
        "en": "Horizontal bars: best departments in teal plain bars, worst in brick hatched bars, with \"best\" or "
              "\"worst\" written next to the value. Minimum {min} per department.",
        "fr": "Barres horizontales : meilleurs départements en barres pleines bleu-vert, moins bons en barres hachurées "
              "brique, avec « meilleur » ou « moins bon » écrit à côté de la valeur. Minimum {min} par département."},
    "map.rank.min.score": {"en": "5 towns", "fr": "5 communes"},
    "map.rank.min.var": {"en": "10 network-years", "fr": "10 réseaux-années"},
    "map.rank.take": {
        "en": "A ranking is easy to read and easy to misread. A department at the bottom is not a place where the water "
              "is dangerous: it is a place where problems, often brief, were found more often than elsewhere. The "
              "report of each town tells what lies behind.",
        "fr": "Un classement se lit facilement et se lit facilement de travers. Un département en bas de liste n'est pas "
              "un endroit où l'eau est dangereuse : c'est un endroit où des problèmes, souvent brefs, ont été trouvés "
              "plus souvent qu'ailleurs. Le rapport de chaque commune dit ce qu'il y a derrière."},

    "map.h2.kicker": {"en": "Hypothesis H2", "fr": "Hypothèse H2"},
    "map.h2.title": {"en": "Bacteria and chemistry do not hit the same departments",
                     "fr": "Bactéries et chimie ne touchent pas les mêmes départements"},
    "map.h2.headline": {
        "en": "Across mainland departments, the rank correlation between the two failure rates is ρ = {rho}: almost "
              "none. H2 is confirmed.",
        "fr": "Entre départements de métropole, la corrélation de rang entre les deux taux d'échec est ρ = {rho} : "
              "presque nulle. H2 est confirmée."},
    "map.h2.chart": {"en": "Each department placed by its bacterial and its chemical failure rate, {period}",
                     "fr": "Chaque département placé selon son taux d'échec bactériologique et chimique, {period}"},
    "map.h2.x": {"en": "Bacterial samples non-compliant (%)", "fr": "Prélèvements bactério non conformes (%)"},
    "map.h2.y": {"en": "Chemical samples non-compliant (%)", "fr": "Prélèvements chimiques non conformes (%)"},
    "map.h2.caption": {
        "en": "Scatter plot: one dot per mainland department; the five departments with the highest rate on each axis "
              "are named. Hover a dot for its name and values.",
        "fr": "Nuage de points : un point par département de métropole ; les cinq départements au taux le plus élevé "
              "sur chaque axe sont nommés. Survolez un point pour voir son nom et ses valeurs."},
    "map.h2.take": {
        "en": "If bacterial and chemical problems had the same causes, the dots would line up along a diagonal. They "
              "do not. The departments with the most bacterial failures ({top_b}) are not those with the most chemical "
              "failures ({top_c}). The rank correlation ρ measures how well the two orders agree, from -1 to 1; here "
              "it is close to zero. This says where problems happen, not why: the chart alone cannot tell the causes.",
        "fr": "Si les problèmes bactériologiques et chimiques avaient les mêmes causes, les points s'aligneraient sur "
              "une diagonale. Ce n'est pas le cas. Les départements avec le plus d'échecs bactériologiques ({top_b}) "
              "ne sont pas ceux avec le plus d'échecs chimiques ({top_c}). La corrélation de rang ρ mesure à quel point "
              "les deux classements concordent, de -1 à 1 ; ici elle est proche de zéro. Cela dit où se produisent "
              "les problèmes, pas pourquoi : le graphique seul ne donne pas les causes."},

    "map.h1.kicker": {"en": "Hypothesis H1", "fr": "Hypothèse H1"},
    "map.h1.title": {"en": "Small networks fail more often", "fr": "Les petits réseaux échouent plus souvent"},
    "map.h1.headline": {
        "en": "Networks tested fewer than 12 times a year carry {share_nc} of the bacterial failures for {share_s} of "
              "the samples. H1 is confirmed.",
        "fr": "Les réseaux contrôlés moins de 12 fois par an portent {share_nc} des échecs bactériologiques pour "
              "{share_s} des prélèvements. H1 est confirmée."},
    "map.h1.chart": {"en": "Share of bacterial samples that failed, by size of the network, {period}",
                     "fr": "Part des prélèvements bactériologiques non conformes, selon la taille du réseau, {period}"},
    "map.h1.x": {"en": "Bacterial samples per network and per year", "fr": "Prélèvements bactériologiques par réseau et par an"},
    "map.h1.y": {"en": "Non-compliant samples (%)", "fr": "Prélèvements non conformes (%)"},
    "map.h1.caption": {
        "en": "Bars: one per size class, the size of a network being measured by how many bacterial samples it gets "
              "in a year, which depends on the size of the network; the value is written on each bar.",
        "fr": "Barres : une par classe de taille, la taille d'un réseau étant mesurée par le nombre de prélèvements "
              "bactériologiques qu'il reçoit dans l'année, qui dépend de la taille du réseau ; la valeur est "
              "écrite sur chaque barre."},
    "map.h1.take": {
        "en": 'The smallest networks fail {ratio} times more often than the largest ones ({a} against {b}). They serve the smallest places, and they are also where a single bad day weighs most on a score, which is why the app shows a confidence level next to every score.',
        "fr": "Les plus petits réseaux échouent {ratio} fois plus souvent que les plus grands ({a} contre {b}). Ils desservent les plus petites localités, et c'est aussi là qu'une seule mauvaise journée pèse le plus sur un score : c'est pourquoi l'application affiche un niveau de confiance à côté de chaque score."},
    "map.h1.few": {"en": "Too few networks of every size in this selection to compare small and large networks; choose a "
                         "larger region or period.",
                   "fr": "Trop peu de réseaux de chaque taille dans cette sélection pour comparer petits et grands "
                         "réseaux ; choisissez une région ou une période plus large."},
    "map.h1.hover": {"en": "{c} samples a year: {v} non-compliant<br>{k} of {n} samples",
                     "fr": "{c} prélèvements par an : {v} non conformes<br>{k} sur {n} prélèvements"},

    "map.dist.kicker": {"en": "All the towns", "fr": "Toutes les communes"},
    "map.dist.headline": {"en": "{a} of the {n} towns selected are graded A, and {de} are graded D or E ({type}, {scope}).",
                          "fr": "{a} des {n} communes sélectionnées sont notées A, et {de} sont notées D ou E ({type}, {scope})."},
    "map.dist.title": {"en": "How many towns get each score", "fr": "Combien de communes obtiennent chaque score"},
    "map.dist.x": {"en": "Town score (out of 100)", "fr": "Score de la commune (sur 100)"},
    "map.dist.y": {"en": "Number of towns", "fr": "Nombre de communes"},
    "map.dist.hover": {"en": "score %{x}: %{y:,} towns", "fr": "score %{x} : %{y:,} communes"},
    "map.dist.caption": {
        "en": "Histogram: number of towns in each band of 2.5 points, with the grade bands E, D, C, B and A shaded and "
              "lettered in the background.",
        "fr": "Histogramme : nombre de communes dans chaque tranche de 2,5 points, avec les bandes des notes E, D, C, B "
              "et A en fond, chacune marquée de sa lettre."},
    "map.dist.take": {
        "en": '{share} of the towns score 85 or more and pile up on the right. The tail on the left is short but real: {low} towns score below 60, grades D and E.',
        "fr": "{share} des communes ont 85 ou plus et s'entassent à droite. La traîne à gauche est courte mais réelle : {low} communes ont moins de 60, notes D et E."},

    "map.trend.kicker": {"en": "Over time", "fr": "Dans le temps"},
    "map.trend.headline": {"en": "In France, {a} of networks had at least one problem of this family in {y0}, {b} in {y1}{partial}.",
                           "fr": "En France, {a} des réseaux ont eu au moins un problème de cette famille en {y0}, {b} en {y1}{partial}."},
    "map.trend.partial": {"en": " (partial year)", "fr": " (année partielle)"},
    "map.trend.title": {"en": "{var}: networks with at least one problem, year by year",
                        "fr": "{var} : réseaux avec au moins un problème, année par année"},
    "map.trend.y": {"en": "Networks with at least one problem (%)", "fr": "Réseaux avec au moins un problème (%)"},
    "map.trend.france": {"en": "France", "fr": "France"},
    "map.trend.hover": {"en": "{y}: {v}<br>{k} of {n} networks", "fr": "{y} : {v}<br>{k} sur {n} réseaux"},
    "map.trend.caption": {
        "en": "Lines: share of distribution networks with at least one problem of the chosen family each year, for "
              "France{region}. A partial year has fewer samples, hence fewer chances to see a problem.",
        "fr": "Courbes : part des réseaux de distribution avec au moins un problème de la famille choisie chaque année, "
              "pour la France{region}. Une année partielle a moins de prélèvements, donc moins de chances de voir un "
              "problème."},
    "map.trend.take": {
        "en": "A rising line does not necessarily mean worse water. For pesticides and PFAS, the number of substances "
              "searched and of samples analysed grew a lot over the period: more searching means more finding. The "
              "page What we look for, what we find takes this apart.",
        "fr": "Une courbe qui monte ne veut pas forcément dire une eau plus mauvaise. Pour les pesticides et les PFAS, "
              "le nombre de substances cherchées et de prélèvements analysés a beaucoup augmenté : chercher plus, c'est "
              "trouver plus. La page Ce qu'on cherche, ce qu'on trouve démonte ce mécanisme."},

    "map.low.title": {"en": "The lowest-scored networks (at least 12 bacterial samples in twelve months)",
                      "fr": "Les réseaux les moins bien notés (au moins 12 prélèvements bactériologiques en douze mois)"},
    "map.low.caption": {"en": "Networks with fewer samples are left out of rankings: one incident weighs too much on them.",
                        "fr": "Les réseaux avec moins de prélèvements sont exclus des classements : un incident y pèse trop."},
    "map.col.net": {"en": "Network", "fr": "Réseau"},
    "map.col.code": {"en": "Code", "fr": "Code"},
    "map.col.dep": {"en": "Dept", "fr": "Dép."},
    "map.col.score": {"en": "Score", "fr": "Score"},
    "map.col.grade": {"en": "Grade", "fr": "Note"},
    "map.col.worst": {"en": "Main chemical issue", "fr": "Principal souci chimique"},
    "map.col.nbact": {"en": "Bacterial samples", "fr": "Prélèvements bactério"},

    # choice of the view, in the sidebar (map page only)
    "map.view": {"en": "What the map shows", "fr": "Ce que montre la carte"},
    "map.view.help": {
        "en": "The four score views describe today's water (last 12 months for bacteria, 36 for chemistry). The other views "
              "count, over the period chosen in the sidebar, the networks with at least one problem of one family.",
        "fr": "Les quatre vues de score décrivent l'eau d'aujourd'hui (12 derniers mois pour les bactéries, 36 pour la "
              "chimie). Les autres vues comptent, sur la période choisie dans la barre latérale, les réseaux avec au moins un "
              "problème d'une famille."},
    "map.view.score_all": {"en": "Score of the towns, overall", "fr": "Score des communes, global"},
    "map.view.score_micro": {"en": "Score of the towns, bacteria", "fr": "Score des communes, bactéries"},
    "map.view.score_chem": {"en": "Score of the towns, health chemistry", "fr": "Score des communes, chimie sanitaire"},
    "map.view.score_comfort": {"en": "Score of the towns, comfort", "fr": "Score des communes, confort"},
    "map.view.group.score": {"en": "Today", "fr": "Aujourd'hui"},
    "map.title.subscore": {"en": "{view}: median of the towns, department by department",
                           "fr": "{view} : médiane des communes, département par département"},
    "map.value.subscore": {"en": "Median mark of the towns (out of 100)", "fr": "Note médiane des communes (sur 100)"},

    # what we see
    "map.see.title": {"en": "What the map says", "fr": "Ce que dit la carte"},
    "map.see.score": {
        "en": "The lowest medians are in {worst}; the highest in {best}. At the scale of regions, {reg_lo} has the lowest "
              "average of its departments ({reg_lo_v}) and {reg_hi} the highest ({reg_hi_v}).",
        "fr": "Les médianes les plus basses sont dans : {worst} ; les plus hautes dans : {best}. À l'échelle des régions, "
              "{reg_lo} a la moyenne de ses départements la plus basse ({reg_lo_v}) et {reg_hi} la plus haute ({reg_hi_v})."},
    "map.see.var": {
        "en": "The departments most affected are {worst}; the least affected are {best}. At the scale of regions, {reg_hi} "
              "has the highest average of its departments ({reg_hi_v}) and {reg_lo} the lowest ({reg_lo_v}).",
        "fr": "Les départements les plus touchés sont : {worst} ; les moins touchés : {best}. À l'échelle des régions, "
              "{reg_hi} a la moyenne de ses départements la plus haute ({reg_hi_v}) et {reg_lo} la plus basse ({reg_lo_v})."},
    "map.see.small": {
        "en": "One factor can be measured right away: the share of small networks, those tested fewer than twelve times a "
              "year. Across departments, its rank correlation with what the map shows is ρ = {rho} ({strength}).",
        "fr": "Un facteur se mesure tout de suite : la part de petits réseaux, ceux contrôlés moins de douze fois par an. "
              "Entre départements, sa corrélation de rang avec ce que montre la carte est ρ = {rho} ({strength})."},
    "map.strength.strong": {"en": "a clear link", "fr": "un lien net"},
    "map.strength.moderate": {"en": "a moderate link", "fr": "un lien modéré"},
    "map.strength.weak": {"en": "almost no link", "fr": "presque aucun lien"},
    "map.hyp.title": {"en": "Careful hypotheses", "fr": "Hypothèses prudentes"},
    "map.hyp.score_all": {
        "en": "The overall score mixes three families, so its map is the sum of several stories: small networks for "
              "bacteria, farming areas for pesticides, soft or mineral water for comfort. The views by family tell them "
              "apart.",
        "fr": "Le score global mélange trois familles : sa carte est la somme de plusieurs histoires, les petits réseaux pour "
              "les bactéries, les zones agricoles pour les pesticides, l'eau douce ou minérale pour le confort. Les vues par "
              "famille permettent de les distinguer."},
    "map.hyp.micro": {
        "en": "Bacterial problems concentrate in small networks (hypothesis H1, confirmed on this page): where they are "
              "numerous, the map should be darker, and the correlation above measures it. Health agencies list as causes poorly protected catchments, "
              "missing or inadequate disinfection and bad weather (ARS Occitanie). The map shows where problems were found, "
              "not why: these causes are not in the data.",
        "fr": "Les problèmes bactériologiques se concentrent dans les petits réseaux (hypothèse H1, confirmée sur cette page) : là où ils "
              "sont nombreux, la carte devrait être plus foncée, et la corrélation ci-dessus le mesure. Les agences de santé citent comme causes des "
              "captages mal protégés, une désinfection absente ou inadaptée et les intempéries (ARS Occitanie). La carte "
              "montre où des problèmes ont été trouvés, pas pourquoi : ces causes ne sont pas dans les données."},
    "map.hyp.chem": {
        "en": "Chemical failures are dominated by pesticide residues. The most frequent ones come from herbicides used on "
              "sugar beet (chloridazon) and maize (S-metolachlor), according to the health agencies, which would point to "
              "areas of field crops. This app has no data on crops, so this remains a hypothesis; and part of the map "
              "reflects which molecules each region chose to search.",
        "fr": "Les échecs chimiques sont dominés par les résidus de pesticides. Les plus fréquents viennent d'herbicides "
              "utilisés sur la betterave (chloridazone) et le maïs (S-métolachlore), selon les agences de santé, ce qui "
              "orienterait vers les zones de grandes cultures. Cette application n'a pas de données sur les cultures : cela "
              "reste une hypothèse ; et une partie de la carte reflète les molécules que chaque région a choisi de chercher."},
    "map.hyp.nitrates": {
        "en": "According to the World Health Organization, nitrates come mostly from agriculture (fertilisers and manure) "
              "and from wastewater. The departments that stand out may be those where intensive farming meets vulnerable "
              "aquifers, but the data does not contain farming practices: this is a hypothesis to check with other sources.",
        "fr": "Selon l'Organisation mondiale de la santé, les nitrates viennent surtout de l'agriculture (engrais et fumier) "
              "et des eaux usées. Les départements qui ressortent pourraient être ceux où une agriculture intensive "
              "rencontre des nappes vulnérables, mais les données ne contiennent pas les pratiques agricoles : c'est une "
              "hypothèse à vérifier avec d'autres sources."},
    "map.hyp.pfas": {
        "en": "PFAS were rarely measured before 2025, so this map shows first where they were searched. Where they were "
              "found above the limit, health agencies have traced some cases to industrial sites. Read it as a map of "
              "monitoring as much as a map of pollution.",
        "fr": "Les PFAS étaient rarement mesurés avant 2025 : cette carte montre d'abord où ils ont été cherchés. Là où ils "
              "ont été trouvés au-dessus de la limite, les agences de santé ont relié certains cas à des sites industriels. "
              "À lire comme une carte du contrôle autant que de la pollution."},
    "map.hyp.metals": {
        "en": "Two very different stories hide behind metals: lead comes from old pipes inside buildings (ARS Pays de la "
              "Loire), arsenic from the natural geology of some aquifers (WHO). A department can stand out for either.",
        "fr": "Deux histoires très différentes se cachent derrière les métaux : le plomb vient des vieilles canalisations des "
              "immeubles (ARS Pays de la Loire), l'arsenic de la géologie naturelle de certaines nappes (OMS). Un "
              "département peut ressortir pour l'une ou l'autre."},
    "map.hyp.dbp": {
        "en": "By-products of disinfection form when chlorine meets organic matter (Anses). Departments that rely on surface "
              "water, richer in organic matter, could be more exposed; the data does not say which resource each network "
              "uses, so this stays a hypothesis.",
        "fr": "Les sous-produits de désinfection se forment quand le chlore rencontre de la matière organique (Anses). Les "
              "départements qui dépendent d'eaux de surface, plus riches en matière organique, pourraient être plus "
              "exposés ; les données ne disent pas quelle ressource utilise chaque réseau : cela reste une hypothèse."},
    "map.hyp.comfort": {
        "en": "Comfort indicators are warning lights for operators, not health limits. Soft mountain water, low in minerals, "
              "can fall outside the expected range of conductivity, as in Chamonix, which is why mountain departments can stand out "
              "here without any health concern.",
        "fr": "Les indicateurs de confort sont des voyants pour les exploitants, pas des limites sanitaires. L'eau douce de "
              "montagne, peu minéralisée, peut sortir de la plage attendue de conductivité, comme à Chamonix : c'est pourquoi des "
              "départements de montagne peuvent ressortir ici sans aucun enjeu sanitaire."},
    "map.hyp.caution": {
        "en": "Everything on this page is a correlation between places: it says where, not why.",
        "fr": "Tout ce qui figure sur cette page est une corrélation entre des lieux : elle dit où, pas pourquoi."},
}

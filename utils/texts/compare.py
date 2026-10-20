"""Page "Town against town": towns side by side, then groups of towns."""

T = {
    "cmp.kicker": {"en": "Side by side", "fr": "Côte à côte"},
    "cmp.title": {"en": "Town against town", "fr": "Commune contre commune"},
    "cmp.lede": {
        "en": "Is the water of a big city better than the water of a village? Of a mountain resort than of a seaside "
              "town? Put towns next to each other, then look at whole groups.",
        "fr": "L'eau d'une grande ville est-elle meilleure que celle d'un village ? Celle d'une station de montagne que "
              "celle d'une ville de bord de mer ? Mettez des communes côte à côte, puis regardez des groupes entiers."},
    "cmp.pick": {"en": "Towns compared (up to six)", "fr": "Communes comparées (jusqu'à six)"},
    "cmp.add": {"en": "Add a town", "fr": "Ajouter une commune"},
    "cmp.add.full": {"en": "Six towns already: remove one to add another.",
                     "fr": "Déjà six communes : retirez-en une pour en ajouter une autre."},
    "cmp.pick.help": {
        "en": "The towns compared. Click the cross on a town to remove it; add one with the search box below, where the "
              "list filters as you type and homonyms show their department.",
        "fr": "Les communes comparées. Cliquez sur la croix d'une commune pour la retirer ; ajoutez-en une avec le champ "
              "de recherche ci-dessous, où la liste se filtre au fur et à mesure et les homonymes affichent leur "
              "département."},
    "cmp.need2": {"en": "Choose at least two towns that have a score.",
                  "fr": "Choisissez au moins deux communes qui ont un score."},
    "cmp.headline": {"en": "{best} scores {bs}/100 ({bg}) and {worst} {ws}/100 ({wg}): a gap of {gap} points.",
                     "fr": "{best} obtient {bs}/100 ({bg}) et {worst} {ws}/100 ({wg}) : un écart de {gap} points."},
    "cmp.headline.lt2": {"en": "{best} scores {bs}/100 ({bg}) and {worst} {ws}/100 ({wg}): a gap of {gap} points.",
                     "fr": "{best} obtient {bs}/100 ({bg}) et {worst} {ws}/100 ({wg}) : un écart de {gap} point."},
    "cmp.metric.delta": {"en": "grade {g}, confidence {c}", "fr": "note {g}, confiance {c}"},
    "cmp.bars.title": {"en": "Where the towns differ: the three marks of each town",
                       "fr": "Là où les communes diffèrent : les trois notes de chaque commune"},
    "cmp.bars.caption": {
        "en": "Grouped bars: for each family (bacteria, health chemistry, comfort), one bar per town with its mark out "
              "of 100 written on top; \"n/a\" when the family was not measured.",
        "fr": "Barres groupées : pour chaque famille (bactéries, chimie sanitaire, confort), une barre par commune avec "
              "sa note sur 100 écrite au-dessus ; « n.d. » quand la famille n'a pas été mesurée."},
    "cmp.bars.take": {
        "en": "The largest gap between these towns is in {fam}: {hi} gets {vhi} and {lo} gets {vlo}. Two towns can share "
              "the same grade for very different reasons, which is why the report of each town matters more than its "
              "letter.",
        "fr": "Le plus grand écart entre ces communes porte sur la famille {fam} : {hi} obtient {vhi} et {lo} {vlo}. Deux communes "
              "peuvent avoir la même note pour des raisons très différentes : c'est pourquoi le rapport de chaque "
              "commune compte plus que sa lettre."},
    "cmp.na": {"en": "n/a", "fr": "n.d."},
    "cmp.y": {"en": "Mark (out of 100)", "fr": "Note (sur 100)"},
    "cmp.table.title": {"en": "Key facts, over the windows of the score", "fr": "Les faits clés, sur les fenêtres du score"},
    "cmp.table.caption": {
        "en": "Bacteria over the last twelve months, chemistry over the last three years, summed over all the networks "
              "of each town. An empty cell means the substance was not measured, or never found above the "
              "quantification limit.",
        "fr": "Bactéries sur les douze derniers mois, chimie sur les trois dernières années, en additionnant tous les "
              "réseaux de chaque commune. Une case vide veut dire que la substance n'a pas été mesurée, ou jamais "
              "trouvée au-dessus de la limite de quantification."},
    "cmp.col.town": {"en": "Town", "fr": "Commune"},
    "cmp.col.nets": {"en": "Networks", "fr": "Réseaux"},
    "cmp.col.nbact": {"en": "Bacterial samples", "fr": "Prélèvements bactério"},
    "cmp.col.nc": {"en": "Of which non-compliant", "fr": "Dont non conformes"},
    "cmp.col.no3": {"en": "Nitrates, highest (mg/L)", "fr": "Nitrates, max (mg/L)"},
    "cmp.col.pest": {"en": "Pesticide results above limit", "fr": "Résultats pesticides hors limite"},
    "cmp.col.pfas": {"en": "PFAS, highest (µg/L)", "fr": "PFAS, max (µg/L)"},
    "cmp.col.th": {"en": "Hardness (°f)", "fr": "Dureté (°f)"},

    "cmp.groups.kicker": {"en": "Groups of towns", "fr": "Groupes de communes"},
    "cmp.groups.title": {"en": "Mountain or coast, city or village", "fr": "Montagne ou littoral, ville ou village"},
    "cmp.groups.by": {"en": "Group the towns by", "fr": "Grouper les communes par"},
    "cmp.groups.help": {
        "en": "The Mediterranean coast is approximated by the towns of the Mediterranean coastal departments outside "
              "mountain areas, because the national list of coastal towns was not available.",
        "fr": "Le littoral méditerranéen est approché par les communes des départements côtiers méditerranéens hors "
              "zones de montagne, car la liste nationale des communes littorales n'était pas disponible."},
    "cmp.groups.territory": {"en": "Territory", "fr": "Territoire"},
    "cmp.groups.density": {"en": "Urban or rural", "fr": "Urbain ou rural"},
    "cmp.groups.size": {"en": "Population", "fr": "Population"},
    "cmp.grp.mountain": {"en": "Mountain", "fr": "Montagne"},
    "cmp.grp.med": {"en": "Mediterranean coast (approx.)", "fr": "Littoral méditerranéen (approx.)"},
    "cmp.grp.other": {"en": "Other towns", "fr": "Autres communes"},
    "cmp.grp.dense": {"en": "Dense urban", "fr": "Urbain dense"},
    "cmp.grp.inter": {"en": "Intermediate urban", "fr": "Urbain intermédiaire"},
    "cmp.grp.rural": {"en": "Rural", "fr": "Rural"},
    "cmp.groups.headline": {
        "en": "In {scope}, the median score is {hi_v} for \"{hi}\" and {lo_v} for \"{lo}\"; {de_lo} of the \"{lo}\" "
              "towns are graded D or E, against {de_hi} of the \"{hi}\" towns.",
        "fr": "Pour {scope}, le score médian est de {hi_v} pour « {hi} » et de {lo_v} pour « {lo} » ; {de_lo} des "
              "communes « {lo} » sont notées D ou E, contre {de_hi} des communes « {hi} »."},
    "cmp.box.title": {"en": "How the scores of the towns spread in each group",
                      "fr": "Comment se répartissent les scores des communes dans chaque groupe"},
    "cmp.box.caption": {
        "en": "Box plots: the line inside each box is the median town, the box holds the middle half of the towns, the "
              "whiskers go to the lowest and highest scores; the number of towns is written under each group.",
        "fr": "Boîtes à moustaches : le trait dans chaque boîte est la commune médiane, la boîte contient la moitié "
              "centrale des communes, les moustaches vont jusqu'aux scores le plus bas et le plus haut ; le nombre de "
              "communes est écrit sous chaque groupe."},
    "cmp.box.take": {
        "en": "Looking at whole distributions rather than averages shows two things at once: where most towns of a "
              "group stand, and how long the tail of poorly graded towns is. A difference between groups is not a "
              "cause, though: small rural networks are tested less often, mountain water is often very low in "
              "minerals, and the Mediterranean group is an approximation.",
        "fr": "Regarder des distributions entières plutôt que des moyennes montre deux choses à la fois : où se situent "
              "la plupart des communes d'un groupe, et la longueur de la traîne des communes mal notées. Une différence "
              "entre groupes n'est pourtant pas une cause : les petits réseaux ruraux sont moins souvent contrôlés, l'eau "
              "de montagne est souvent très peu minéralisée, et le groupe méditerranéen est une approximation."},
    "cmp.box.y": {"en": "Town score (out of 100)", "fr": "Score de la commune (sur 100)"},
    "cmp.box.n": {"en": "{n} towns", "fr": "{n} communes"},

    # why one town does better than another
    "cmp.why.title": {"en": "Why one town does better than the other", "fr": "Pourquoi une commune fait mieux que l'autre"},
    "cmp.why.lead": {
        "en": "The gap comes mostly from {fam}: {worst} gets {vw} out of 100 there, {best} {vb}.",
        "fr": "L'écart vient surtout de la famille {fam} : {worst} y obtient {vw} sur 100, {best} {vb}."},
    "cmp.why.same": {
        "en": "{best} and {worst} are almost level: their differences are too small to mean much.",
        "fr": "{best} et {worst} sont presque à égalité : leurs différences sont trop faibles pour vouloir dire "
              "grand-chose."},
    "cmp.why.town": {"en": "Where {town} loses points: {causes}.", "fr": "Là où {town} perd des points : {causes}."},
    "cmp.why.clean": {"en": "{town} loses almost no points.", "fr": "{town} ne perd presque aucun point."},
    "cmp.and": {"en": " and ", "fr": " et "},
    "cmp.cause.micro": {"en": "bacteria ({k} failed samples out of {n} in twelve months)",
                        "fr": "bactéries ({k} prélèvements non conformes sur {n} en douze mois)"},
    "cmp.cause.micro.one": {"en": "bacteria ({k} failed sample out of {n} in twelve months)",
                            "fr": "bactéries ({k} prélèvement non conforme sur {n} en douze mois)"},
    "cmp.cause.chem": {"en": "{param} (health substance)", "fr": "{param} (substance sanitaire)"},
    "cmp.cause.comfort": {"en": "{param} (comfort indicator)", "fr": "{param} (indicateur de confort)"},
    "cmp.why.end": {
        "en": "The other towns sit between these two; the page The water of my town details each one.",
        "fr": "Les autres communes se situent entre ces deux-là ; la page L'eau de ma commune détaille chacune."},
}

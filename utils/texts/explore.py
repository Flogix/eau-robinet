"""Page "Explore the data": the three files and their keys, real rows, key distributions, rank correlations."""

T = {
    "nav.explore": {"en": "Explore the data", "fr": "Explorer les données"},
    "ex.kicker": {"en": "The raw material", "fr": "La matière première"},
    "ex.title": {"en": "Explore the data", "fr": "Explorer les données"},
    "ex.lede": {
        "en": "Before any score or map, there are three plain text files a year, published by the Ministry of Health. "
              "This page opens them: how they fit together, what a row looks like, how the values are spread, and "
              "which indicators move together from one department to another.",
        "fr": "Avant tout score et toute carte, il y a trois simples fichiers texte par an, publiés par le ministère de "
              "la Santé. Cette page les ouvre : comment ils s'emboîtent, à quoi ressemble une ligne, comment les valeurs "
              "se répartissent, et quels indicateurs varient ensemble d'un département à l'autre."},
    "ex.headline": {
        "en": "From {y0} to {y1}: {samples} samples, {results} analysis results and {gb} GB of text. Each sample "
              "brings about {per} results.",
        "fr": "De {y0} à {y1} : {samples} prélèvements, {results} résultats d'analyse et {gb} Go de texte. Chaque "
              "prélèvement apporte environ {per} résultats."},

    # --- schema --------------------------------------------------------------------------------------------------
    "ex.schema.kicker": {"en": "Three files a year", "fr": "Trois fichiers par an"},
    "ex.schema.title": {"en": "How the files fit together", "fr": "Comment les fichiers s'emboîtent"},
    "ex.schema.text": {
        "en": "Each year comes as a zip archive with three files. **PLV** lists the samples: one row per sample and "
              "per network, with its date and the official verdicts of the regional health agency (ARS). **RESULT** "
              "holds the analysis results: one row per sample and per parameter, a parameter being anything the "
              "laboratory measures, from nitrates to E. coli. **COM_UDI** says which networks serve which town. The "
              "files are linked by **keys**, columns found in two files that let a row of one be matched with rows of "
              "the other: `referenceprel`, the identifier of a sample, links RESULT to PLV, and `cdreseau`, the code of "
              "a network, links PLV to COM_UDI.",
        "fr": "Chaque année arrive sous la forme d'une archive zip de trois fichiers. **PLV** liste les prélèvements : "
              "une ligne par prélèvement et par réseau, avec sa date et les verdicts officiels de l'agence régionale de "
              "santé (ARS). **RESULT** contient les résultats d'analyse : une ligne par prélèvement et par paramètre, "
              "un paramètre étant tout ce que le laboratoire mesure, des nitrates à E. coli. **COM_UDI** dit quels "
              "réseaux desservent quelle commune. Les fichiers sont reliés par des **clés**, des colonnes présentes "
              "dans deux fichiers qui permettent de retrouver les lignes de l'un dans l'autre : `referenceprel`, "
              "l'identifiant d'un prélèvement, relie RESULT à PLV, et `cdreseau`, le code d'un réseau, relie PLV à "
              "COM_UDI."},
    "ex.diag.title": {"en": "The three files of {year} and the two keys that link them",
                      "fr": "Les trois fichiers de {year} et les deux clés qui les relient"},
    "ex.diag.caption": {
        "en": "Diagram. COM_UDI links each town to its networks through the network code cdreseau; PLV lists the "
              "samples of each network, identified by referenceprel; RESULT holds the results of each sample, found "
              "again with referenceprel. Row counts of the {year} files.",
        "fr": "Schéma. COM_UDI relie chaque commune à ses réseaux par le code de réseau cdreseau ; PLV liste les "
              "prélèvements de chaque réseau, identifiés par referenceprel ; RESULT contient les résultats de chaque "
              "prélèvement, retrouvés grâce à referenceprel. Nombre de lignes des fichiers {year}."},
    "ex.diag.take": {
        "en": "Reading the water of a town always takes two jumps: from the town to its networks, then from the "
              "networks to their samples and results. The first jump goes both ways, since a town can have several "
              "networks and a network can serve several towns; a join made carelessly at that step would count the "
              "same result several times.",
        "fr": "Lire l'eau d'une commune demande toujours deux sauts : de la commune vers ses réseaux, puis des réseaux "
              "vers leurs prélèvements et leurs résultats. Le premier saut va dans les deux sens, car une commune peut "
              "avoir plusieurs réseaux et un réseau desservir plusieurs communes ; une jointure faite sans précaution à "
              "cette étape compterait plusieurs fois le même résultat."},
    "ex.diag.com_udi": {"en": "Towns and networks", "fr": "Communes et réseaux"},
    "ex.diag.plv": {"en": "Samples", "fr": "Prélèvements"},
    "ex.diag.result": {"en": "Analysis results", "fr": "Résultats d'analyse"},
    "ex.diag.rows": {"en": "{n} rows", "fr": "{n} lignes"},
    "ex.diag.rows_samples": {"en": "{n} rows, {s} samples", "fr": "{n} lignes, {s} prélèvements"},
    "ex.diag.c.insee": {"en": "town code (INSEE)", "fr": "code commune (INSEE)"},
    "ex.diag.c.quartier": {"en": "district served", "fr": "quartier desservi"},
    "ex.diag.c.cdreseau": {"en": "network code", "fr": "code du réseau"},
    "ex.diag.c.nomreseau": {"en": "network name", "fr": "nom du réseau"},
    "ex.diag.c.referenceprel": {"en": "sample identifier", "fr": "identifiant du prélèvement"},
    "ex.diag.c.dateprel": {"en": "date of the sample", "fr": "date du prélèvement"},
    "ex.diag.c.amont": {"en": "upstream plant, if any", "fr": "installation amont, s'il y a lieu"},
    "ex.diag.c.conf": {"en": "official verdicts", "fr": "verdicts officiels"},
    "ex.diag.c.param": {"en": "parameter code", "fr": "code du paramètre"},
    "ex.diag.c.value": {"en": "result, as text and number", "fr": "résultat, en texte et en nombre"},
    "ex.diag.c.limits": {"en": "limit and reference", "fr": "limite et référence"},
    "ex.diag.nn": {"en": "many to many", "fr": "plusieurs à plusieurs"},
    "ex.diag.1n": {"en": "one sample, about {per} results", "fr": "un prélèvement, environ {per} résultats"},

    "ex.vol.title": {"en": "Between {lo} and {hi} million analysis results per complete year",
                     "fr": "Entre {lo} et {hi} millions de résultats d'analyse par année complète"},
    "ex.vol.x": {"en": "Year of the file", "fr": "Année du fichier"},
    "ex.vol.y": {"en": "Rows of the RESULT file (millions)", "fr": "Lignes du fichier RESULT (millions)"},
    "ex.vol.hover": {
        "en": "{year}: {res} million results, {smp} samples, {plv} sample rows, {mb} MB of text",
        "fr": "{year} : {res} millions de résultats, {smp} prélèvements, {plv} lignes de prélèvement, {mb} Mo de texte"},
    "ex.vol.caption": {
        "en": "Bars: number of rows of the RESULT file each year, in millions; hover for the samples and the size of "
              "the files. The 2026 file stops at the end of August.",
        "fr": "Barres : nombre de lignes du fichier RESULT chaque année, en millions ; survolez pour voir les "
              "prélèvements et la taille des fichiers. Le fichier 2026 s'arrête fin août."},
    "ex.vol.take": {
        "en": "The volume barely moves from one year to the next. The RESULT file is what makes the data heavy: "
              "{share} of the {gb} GB of text. That is why it is never loaded whole in memory: it is read with DuckDB, a "
              "database engine that works on files bigger than the memory of the computer, then stored as Parquet, a "
              "compressed format by column, which brings the eleven years down to {pq} MB.",
        "fr": "Le volume bouge à peine d'une année à l'autre. C'est le fichier RESULT qui rend les données lourdes : "
              "{share} des {gb} Go de texte. C'est pourquoi il n'est jamais chargé en entier en mémoire : il est lu "
              "avec DuckDB, un moteur de base de données qui travaille sur des fichiers plus gros que la mémoire de "
              "l'ordinateur, puis stocké en Parquet, un format compressé par colonne, qui ramène les onze années à "
              "{pq} Mo."},
    "ex.vol.table": {"en": "The numbers behind the chart, year by year", "fr": "Les chiffres du graphique, année par année"},
    "ex.vol.col.annee": {"en": "Year", "fr": "Année"},
    "ex.vol.col.zip_mb": {"en": "Zip (MB)", "fr": "Zip (Mo)"},
    "ex.vol.col.result_txt_mb": {"en": "RESULT text (MB)", "fr": "Texte RESULT (Mo)"},
    "ex.vol.col.plv_rows": {"en": "PLV rows", "fr": "Lignes PLV"},
    "ex.vol.col.samples": {"en": "Samples", "fr": "Prélèvements"},
    "ex.vol.col.result_rows": {"en": "RESULT rows", "fr": "Lignes RESULT"},
    "ex.vol.col.com_udi_rows": {"en": "COM_UDI rows", "fr": "Lignes COM_UDI"},
    "ex.vol.col.communes": {"en": "Towns", "fr": "Communes"},
    "ex.vol.col.networks_linked": {"en": "Networks", "fr": "Réseaux"},
    "ex.vol.partial": {"en": "Jan. to Aug.", "fr": "janv. à août"},

    "ex.net.kicker": {"en": "The base unit", "fr": "L'unité de base"},
    "ex.net.title": {"en": "Why everything starts from the network", "fr": "Pourquoi tout part du réseau"},
    "ex.net.text": {
        "en": "A **distribution network** (UDI in French, for *unité de distribution*) is a set of pipes in which the "
              "water has the same origin and the same quality. The health agency samples each network, not each town, "
              "so the network is the only level at which a measurement truly describes the water that flows. In "
              "{year}, {t1} of the {tn} towns are served by a single network, {t2} by two and {t10} by ten or more; on "
              "the other side, {n1} of the {nn} networks serve a single town and {n20} serve twenty or more. That is "
              "why every table of this app is first computed per network, and a town gets the average of its "
              "networks only at the end.",
        "fr": "Un **réseau de distribution** (UDI, pour *unité de distribution*) est un ensemble de tuyaux dans lequel "
              "l'eau a la même origine et la même qualité. L'agence de santé prélève dans chaque réseau, pas dans "
              "chaque commune : le réseau est donc le seul niveau où une mesure décrit vraiment l'eau qui coule. En "
              "{year}, {t1} des {tn} communes sont desservies par un seul réseau, {t2} par deux et {t10} par dix ou "
              "plus ; dans l'autre sens, {n1} des {nn} réseaux desservent une seule commune et {n20} en desservent "
              "vingt ou plus. C'est pourquoi chaque table de cette application est d'abord calculée par réseau, et une "
              "commune ne reçoit la moyenne de ses réseaux qu'à la fin."},
    "ex.net.upstream": {
        "en": "One more subtlety. Some samples are taken upstream, at a treatment plant or a well, and then copied "
              "for each network that this plant feeds. In {year}, {share} of the {n} samples are attached to more than "
              "one network, and one of them to {max}. Counting the samples of a network must keep these copies; "
              "counting the samples of France must remove them, which the pipeline does.",
        "fr": "Une subtilité de plus. Certains prélèvements sont faits en amont, dans une usine de traitement ou un "
              "captage, puis recopiés pour chaque réseau que cette installation alimente. En {year}, {share} des {n} "
              "prélèvements sont rattachés à plus d'un réseau, et l'un d'eux à {max}. Compter les prélèvements d'un "
              "réseau doit garder ces copies ; compter ceux de la France doit les retirer, ce que fait la chaîne de "
              "traitement."},

    # --- rows ----------------------------------------------------------------------------------------------------
    "ex.rows.kicker": {"en": "What a row looks like", "fr": "À quoi ressemble une ligne"},
    "ex.rows.title": {"en": "Real rows, as they are published", "fr": "De vraies lignes, telles qu'elles sont publiées"},
    "ex.rows.text": {
        "en": "Here are real rows of each file. The ten rows of each raw file were drawn at random in the {year} files "
              "during the exploration of the data, with a fixed seed (42) so that the draw can be repeated; they are "
              "the rows printed in the data dictionary of the project, and the app holds no other raw row. The last "
              "choice is a processed table, as the app reads it, to show what the pipeline makes of the raw files.",
        "fr": "Voici de vraies lignes de chaque fichier. Les dix lignes de chaque fichier brut ont été tirées au hasard "
              "dans les fichiers {year} pendant l'exploration des données, avec une graine fixe (42) pour que le "
              "tirage puisse être refait ; ce sont les lignes imprimées dans le dictionnaire des données du projet, et "
              "l'application ne contient aucune autre ligne brute. Le dernier choix est une table traitée, telle que "
              "l'application la lit, pour montrer ce que la chaîne de traitement fait des fichiers bruts."},
    "ex.rows.pick": {"en": "Table to show", "fr": "Table à afficher"},
    "ex.rows.help": {"en": "PLV, RESULT and COM_UDI are the raw files; udi_year is a table computed from them.",
                     "fr": "PLV, RESULT et COM_UDI sont les fichiers bruts ; udi_year est une table calculée à partir d'eux."},
    "ex.rows.opt.PLV": {"en": "PLV, samples", "fr": "PLV, prélèvements"},
    "ex.rows.opt.RESULT": {"en": "RESULT, results", "fr": "RESULT, résultats"},
    "ex.rows.opt.COM_UDI": {"en": "COM_UDI, towns and networks", "fr": "COM_UDI, communes et réseaux"},
    "ex.rows.opt.udi_year": {"en": "udi_year, processed", "fr": "udi_year, table traitée"},
    "ex.rows.caption": {
        "en": "{n} rows of the {table} table for {year}, every column as published; scroll sideways to see them all.",
        "fr": "{n} lignes de la table {table} pour {year}, toutes les colonnes telles que publiées ; faites défiler "
              "sur le côté pour toutes les voir."},
    "ex.rows.PLV": {
        "en": "`cdreseau` is the network sampled and `referenceprel` the sample, the key to its results. When "
              "`cdreseauamont` is filled, the sample was taken upstream, at the plant named in `nomreseauamont`, and "
              "`pourcentdebit` says how much of the network's water comes from it. `conclusionprel` is the verdict of the "
              "health agency in plain words. The four `plvconformite…` columns are the official verdicts, as letters: "
              "C compliant, N not compliant, D compliant under a temporary exemption granted by the prefect, S not "
              "applicable. *Bacterio* and *chimique* refer to the **limits**, the health thresholds; *reference* to the "
              "**references**, the comfort and monitoring thresholds.",
        "fr": "`cdreseau` est le réseau prélevé et `referenceprel` le prélèvement, la clé vers ses résultats. Quand "
              "`cdreseauamont` est rempli, le prélèvement a été fait en amont, dans l'installation nommée dans "
              "`nomreseauamont`, et `pourcentdebit` dit quelle part de l'eau du réseau en vient. `conclusionprel` est "
              "le verdict de l'agence de santé, en toutes lettres. Les quatre colonnes `plvconformite…` sont les "
              "verdicts officiels, en lettres : C conforme, N non conforme, D conforme sous dérogation (un délai "
              "accordé par le préfet), S sans objet. *Bacterio* et *chimique* renvoient aux **limites**, les seuils "
              "sanitaires ; *reference* aux **références**, les seuils de confort et de surveillance."},
    "ex.rows.RESULT": {
        "en": "`cdparametresiseeaux` is the code of the parameter and `libminparametre` its name. `rqana` is the result "
              "as the laboratory wrote it, and `valtraduite` the same result turned into a number: \"<0,020\" becomes "
              "0, which means *below the quantification limit*, not *zero*. `cdunitereferencesiseeaux` is the unit. "
              "`limitequal` and `refqual` are the limit and the reference that apply to this very row, written as "
              "text (\"<=0,1 µg/L\"); the same parameter can have different thresholds depending on where it was "
              "sampled, so the threshold of each row is used. `insituana` tells a field measurement (T) from a "
              "laboratory one (L).",
        "fr": "`cdparametresiseeaux` est le code du paramètre et `libminparametre` son nom. `rqana` est le résultat tel "
              "que le laboratoire l'a écrit, et `valtraduite` le même résultat converti en nombre : « <0,020 » devient "
              "0, ce qui veut dire *sous la limite de quantification*, pas *zéro*. `cdunitereferencesiseeaux` est "
              "l'unité. `limitequal` et `refqual` sont la limite et la référence qui s'appliquent à cette ligne précise, "
              "écrites en texte (« <=0,1 µg/L ») ; un même paramètre peut avoir des seuils différents selon le lieu du "
              "prélèvement, c'est donc le seuil de chaque ligne qui est utilisé. `insituana` distingue une mesure "
              "de terrain (T) d'une mesure de laboratoire (L)."},
    "ex.rows.COM_UDI": {
        "en": "`inseecommune` is the official code of the town (INSEE) and `cdreseau` the network that serves it. "
              "`quartier` says which part of the town the network serves; \"-\" means the whole town, and the other "
              "values are free text written by each agency (\"totalité\", \"Village\", a hamlet name), so they are "
              "only shown, never counted. `debutalim` is the date the network started to serve the town.",
        "fr": "`inseecommune` est le code officiel de la commune (INSEE) et `cdreseau` le réseau qui la dessert. "
              "`quartier` dit quelle partie de la commune le réseau dessert ; « - » signifie la commune entière, et les "
              "autres valeurs sont du texte libre écrit par chaque agence (« totalité », « Village », un nom de "
              "hameau) : elles sont seulement affichées, jamais comptées. `debutalim` est la date à laquelle le réseau "
              "a commencé à desservir la commune."},
    "ex.rows.udi_year": {
        "en": "One row per network and per year. `n_samples` counts the samples, `n_bact` those with bacteriological "
              "tests and `n_bact_nc` those that failed them; `n_chem`, `n_chem_nc` and `n_chem_derog` do the same "
              "for chemistry, the last one counting the failures under exemption. `n_ref_bact_nc` and `n_ref_chem_nc` "
              "count the samples outside a reference, and `n_upstream` those taken upstream. Millions of rows have "
              "become a table that fits in a few megabytes.",
        "fr": "Une ligne par réseau et par année. `n_samples` compte les prélèvements, `n_bact` ceux qui ont des "
              "analyses bactériologiques et `n_bact_nc` ceux qui y ont échoué ; `n_chem`, `n_chem_nc` et "
              "`n_chem_derog` font de même pour la chimie, le dernier comptant les échecs sous dérogation. "
              "`n_ref_bact_nc` et `n_ref_chem_nc` comptent les prélèvements hors référence, et `n_upstream` ceux faits "
              "en amont. Des millions de lignes sont devenues une table de quelques mégaoctets."},

    # --- distributions -------------------------------------------------------------------------------------------
    "ex.dist.kicker": {"en": "How the values are spread", "fr": "Comment les valeurs se répartissent"},
    "ex.dist.title": {"en": "Four distributions that explain the rest", "fr": "Quatre distributions qui expliquent le reste"},
    "ex.dist.text": {
        "en": "A **distribution** shows how often each value occurs. Two words come back below: the **median**, the "
              "value that splits a group into two halves of equal size, and the **percentiles**: the 95th percentile "
              "is the value that 95% of the group stays under.",
        "fr": "Une **distribution** montre à quelle fréquence chaque valeur apparaît. Deux mots reviennent plus bas : "
              "la **médiane**, la valeur qui coupe un groupe en deux moitiés de même taille, et les **centiles** : le "
              "95e centile est la valeur sous laquelle restent 95 % du groupe."},
    "ex.smp.title": {"en": "Half of the networks were sampled {median} times or fewer in {year}",
                     "fr": "La moitié des réseaux a été prélevée {median} fois ou moins en {year}"},
    "ex.smp.x": {"en": "Samples taken in the year (classes)", "fr": "Prélèvements dans l'année (classes)"},
    "ex.smp.y": {"en": "Networks", "fr": "Réseaux"},
    "ex.smp.more": {"en": "{lo} or more", "fr": "{lo} ou plus"},
    "ex.smp.hover": {"en": "%{x} samples: %{y} networks", "fr": "%{x} prélèvements : %{y} réseaux"},
    "ex.smp.caption": {
        "en": "Bars: number of networks in each class of number of samples taken in {year}; the classes get wider to "
              "the right, so that small and big networks fit on the same chart.",
        "fr": "Barres : nombre de réseaux dans chaque classe de nombre de prélèvements faits en {year} ; les classes "
              "s'élargissent vers la droite, pour que petits et grands réseaux tiennent sur le même graphique."},
    "ex.smp.take": {
        "en": "Most networks are small. {share} of them had fewer than twelve bacteriological tests in {year}, the size "
              "that hypothesis H1 calls a small network, while {big} networks, those of the big cities, were sampled "
              "{lo} times or more. A "
              "score built on five samples is less certain than one built on five hundred, which is why the town page "
              "always shows a confidence level.",
        "fr": "La plupart des réseaux sont petits. {share} d'entre eux ont eu moins de douze analyses bactériologiques "
              "en {year}, la taille que l'hypothèse H1 appelle un petit réseau, tandis que {big} réseaux, ceux des "
              "grandes villes, ont été prélevés {lo} fois ou plus. Un score construit sur cinq prélèvements est moins sûr qu'un "
              "score construit sur cinq cents, c'est pourquoi la page commune affiche toujours un niveau de confiance."},

    "ex.lq.title": {"en": "For most groups of substances, nearly every result says \"not found\"",
                    "fr": "Pour la plupart des groupes de substances, presque chaque résultat dit « pas trouvé »"},
    "ex.lq.text": {
        "en": "The **quantification limit** is the smallest amount a laboratory can measure reliably. Below it, the "
              "result is written \"<0,02\" and means \"not found at this level\", which is not the same as zero.",
        "fr": "La **limite de quantification** est la plus petite quantité qu'un laboratoire sait mesurer de façon "
              "fiable. En dessous, le résultat s'écrit « <0,02 » et veut dire « pas trouvé à ce niveau », ce qui n'est "
              "pas la même chose que zéro."},
    "ex.lq.x": {"en": "Results below the quantification limit in {year} (%)",
                "fr": "Résultats sous la limite de quantification en {year} (%)"},
    "ex.lq.hover": {"en": "{group}: {share} of {n} results not found ({k} parameters)",
                    "fr": "{group} : {share} des {n} résultats non trouvés ({k} paramètres)"},
    "ex.lq.caption": {
        "en": "Bars: share of the {year} results below the quantification limit, by group of parameters; the word "
              "after each bar names the family. Groups with fewer than 1,000 results are left out.",
        "fr": "Barres : part des résultats {year} sous la limite de quantification, par groupe de paramètres ; le mot "
              "après chaque barre nomme la famille. Les groupes de moins de 1 000 résultats sont écartés."},
    "ex.lq.take": {
        "en": "{pest} of the pesticide results and {bact} of the bacteria counts are below the limit: most of the time, "
              "nothing is found. Nitrates are the opposite, found in most samples ({no3} below the limit); their main "
              "sources, according to the WHO, are farming (fertilisers, manure) and waste water (source 23). This is why the data is "
              "mostly made of \"<\" values, and why the pipeline keeps the quantification limit next to each value: "
              "a result below it is a real measurement, the substance was looked for, but the absence of a "
              "measurement is not the absence of a substance.",
        "fr": "{pest} des résultats de pesticides et {bact} des comptages de bactéries sont sous la limite : la plupart "
              "du temps, rien n'est trouvé. Les nitrates sont l'inverse, trouvés dans la plupart des prélèvements "
              "({no3} sous la limite) ; leurs sources principales, selon l'OMS, sont l'agriculture (engrais, fumier) "
              "et les eaux usées (source 23). C'est pourquoi les données sont surtout faites de valeurs « < », et "
              "pourquoi la chaîne de traitement garde la limite de quantification à côté de chaque valeur : un "
              "résultat en dessous est une vraie mesure, la substance a été cherchée, mais l'absence de mesure n'est "
              "pas l'absence de substance."},
    "ex.sub.cyanotoxins": {"en": "Cyanotoxins", "fr": "Cyanotoxines"},
    "ex.sub.bacteria": {"en": "Bacteria (E. coli, enterococci)", "fr": "Bactéries (E. coli, entérocoques)"},
    "ex.sub.pesticides": {"en": "Pesticides and relevant metabolites", "fr": "Pesticides et métabolites pertinents"},
    "ex.sub.bacteria_indicators": {"en": "Indicator bacteria (coliforms, spores)",
                                   "fr": "Bactéries indicatrices (coliformes, spores)"},
    "ex.sub.radioactivity": {"en": "Radioactivity", "fr": "Radioactivité"},
    "ex.sub.other_chemicals": {"en": "Other chemicals", "fr": "Autres substances chimiques"},
    "ex.sub.metals": {"en": "Metals", "fr": "Métaux"},
    "ex.sub.pesticide_metabolite_non_relevant": {"en": "Non-relevant metabolites", "fr": "Métabolites non pertinents"},
    "ex.sub.pfas": {"en": "PFAS (sum of 20)", "fr": "PFAS (somme de 20)"},
    "ex.sub.turbidity": {"en": "Turbidity", "fr": "Turbidité"},
    "ex.sub.indicators": {"en": "Comfort indicators (iron, ammonium…)", "fr": "Indicateurs de confort (fer, ammonium…)"},
    "ex.sub.disinfection_byproducts": {"en": "Disinfection by-products", "fr": "Sous-produits de désinfection"},
    "ex.sub.nitrates": {"en": "Nitrates and nitrites", "fr": "Nitrates et nitrites"},

    "ex.top.title": {"en": "The {n} most measured parameters are the routine ones: pH, temperature, bacteria",
                     "fr": "Les {n} paramètres les plus mesurés sont ceux de la routine : pH, température, bactéries"},
    "ex.top.x": {"en": "Results from {y0} to {y1} (millions)", "fr": "Résultats de {y0} à {y1} (millions)"},
    "ex.top.hover": {"en": "{name} ({code}): {n} million results, {fam}",
                     "fr": "{name} ({code}) : {n} millions de résultats, {fam}"},
    "ex.top.caption": {
        "en": "Bars: number of results of each parameter over the eleven files, in millions; the colour and the word "
              "after the bar give its family.",
        "fr": "Barres : nombre de résultats de chaque paramètre sur les onze fichiers, en millions ; la couleur et le "
              "mot après la barre donnent sa famille."},
    "ex.top.take": {
        "en": "The routine check, done at nearly every sample, weighs the most: pH, temperature, the bacteria, "
              "turbidity, chlorine. Nitrates are the first health chemical, with {no3} million results. The "
              "{pest} pesticides of the catalogue are each measured far less often, but together they make "
              "{pshare} of all the results: the data is wide (many parameters) as well as long (many samples).",
        "fr": "Le contrôle de routine, fait à presque chaque prélèvement, pèse le plus : pH, température, bactéries, "
              "turbidité, chlore. Les nitrates sont la première substance chimique sanitaire, avec {no3} millions de "
              "résultats. Les {pest} pesticides du catalogue sont chacun mesurés bien moins souvent, mais ensemble ils "
              "font {pshare} de tous les résultats : les données sont larges (beaucoup de paramètres) autant que "
              "longues (beaucoup de prélèvements)."},
    "ex.p.TEAU": {"en": "Water temperature", "fr": "Température de l'eau"},
    "ex.p.GT36_44": {"en": "Heterotrophic bacteria at 36 °C", "fr": "Bactéries revivifiables à 36 °C"},
    "ex.p.GT22_68": {"en": "Heterotrophic bacteria at 22 °C", "fr": "Bactéries revivifiables à 22 °C"},
    "ex.p.CL2LIB": {"en": "Free chlorine", "fr": "Chlore libre"},
    "ex.p.CL2TOT": {"en": "Total chlorine", "fr": "Chlore total"},
    "ex.p.COULF": {"en": "Colour", "fr": "Coloration"},

    "ex.val.title": {"en": "{name}: how the {year} averages of the networks are spread",
                     "fr": "{name} : comment se répartissent les moyennes {year} des réseaux"},
    "ex.val.pick": {"en": "Parameter", "fr": "Paramètre"},
    "ex.val.help": {"en": "Eight parameters followed in every network, chosen for the story of this app.",
                    "fr": "Huit paramètres suivis dans chaque réseau, choisis pour le récit de cette application."},
    "ex.val.x": {"en": "Average of the network over {year} ({unit})", "fr": "Moyenne du réseau sur {year} ({unit})"},
    "ex.val.hover": {"en": "{lo} to {hi} {unit}: {n} networks", "fr": "{lo} à {hi} {unit} : {n} réseaux"},
    "ex.val.limit": {"en": "limit {v} {unit}", "fr": "limite {v} {unit}"},
    "ex.val.reference": {"en": "reference {v} {unit}", "fr": "référence {v} {unit}"},
    "ex.val.caption": {
        "en": "Bars: number of networks by their average value in {year}; a result below the quantification limit "
              "counts as zero. Dashed line: the threshold, when there is one. The last bar gathers every network "
              "above {top} {unit}.",
        "fr": "Barres : nombre de réseaux selon leur valeur moyenne en {year} ; un résultat sous la limite de "
              "quantification compte pour zéro. Trait pointillé : le seuil, quand il existe. La dernière barre "
              "regroupe tous les réseaux au-dessus de {top} {unit}."},
    "ex.val.take": {
        "en": "Over the {n} networks measured, half average less than {p50} {unit}, and nine in ten lie between {p05} "
              "and {p95} {unit}. {zero} of them never had a result above the quantification limit. {thr}",
        "fr": "Sur les {n} réseaux mesurés, la moitié a une moyenne inférieure à {p50} {unit}, et neuf sur dix se "
              "situent entre {p05} et {p95} {unit}. {zero} d'entre eux n'ont jamais eu de résultat au-dessus de la "
              "limite de quantification. {thr}"},
    "ex.val.thr": {
        "en": "{share} of the networks have an average above the {kind} of {v} {unit}; an average above the "
              "threshold is rarer than a single result above it, which is what the official verdicts count.",
        "fr": "{share} des réseaux ont une moyenne au-dessus de la {kind} de {v} {unit} ; une moyenne au-dessus du "
              "seuil est plus rare qu'un seul résultat au-dessus, qui est ce que comptent les verdicts officiels."},
    "ex.val.kind.limit": {"en": "limit", "fr": "limite"},
    "ex.val.kind.reference": {"en": "reference", "fr": "référence"},
    "ex.val.nothr": {
        "en": "Hardness has no limit: it measures the calcium and magnesium dissolved in the water (source 37), and it shows how "
              "different the waters of France are, from very soft to very hard.",
        "fr": "La dureté n'a pas de limite : elle mesure le calcium et le magnésium dissous dans l'eau (source 37), et montre à "
              "quel point les eaux de France diffèrent, de très douces à très dures."},
    "ex.val.p.CL": {"en": "Chlorides", "fr": "Chlorures"},
    "ex.val.p.SO4": {"en": "Sulphates", "fr": "Sulfates"},

    # --- correlations --------------------------------------------------------------------------------------------
    "ex.cor.kicker": {"en": "What goes with what", "fr": "Ce qui va avec quoi"},
    "ex.cor.title": {"en": "Which indicators move together from one department to another",
                     "fr": "Quels indicateurs varient ensemble d'un département à l'autre"},
    "ex.cor.text": {
        "en": "To compare departments, we rank them on each indicator and check whether two rankings agree. That is "
              "the **Spearman rank correlation**, written ρ (rho): +1 when the two orders are the same, −1 when one is "
              "the reverse of the other, 0 when they have nothing to do with each other. Working on ranks rather than "
              "on values means that a few extreme departments, such as Paris and its density, cannot drive the "
              "result alone. The eight indicators are computed for the {n} departments of mainland France: the "
              "bacterial and chemical failure rates over {y0}–{y1} (share of samples officially not compliant), the "
              "median score of the towns (departments with at least five scored towns), the share of small networks "
              "(network-years with fewer than twelve bacteriological tests), the hardness and the nitrates (median of "
              "the networks' {year} averages), the population, and the density (inhabitants per km², the area being "
              "computed from the contours used by the map).",
        "fr": "Pour comparer les départements, on les classe sur chaque indicateur et on regarde si deux classements "
              "concordent. C'est la **corrélation des rangs de Spearman**, notée ρ (rho) : +1 quand les deux ordres "
              "sont les mêmes, −1 quand l'un est l'inverse de l'autre, 0 quand ils n'ont rien à voir. Travailler sur "
              "les rangs plutôt que sur les valeurs évite que quelques départements extrêmes, comme Paris et sa "
              "densité, ne décident seuls du résultat. Les huit indicateurs sont calculés pour les {n} départements "
              "de métropole : les taux d'échec bactériologique et chimique sur {y0}–{y1} (part des prélèvements "
              "officiellement non conformes), le score médian des communes (départements d'au moins cinq communes "
              "notées), la part de petits réseaux (années-réseaux avec moins de douze analyses bactériologiques), la "
              "dureté et les nitrates (médiane des moyennes {year} des réseaux), la population, et la densité "
              "(habitants par km², la surface étant calculée à partir des contours de la carte)."},
    "ex.cor.chart": {"en": "Rank correlation between eight indicators of the departments of mainland France",
                     "fr": "Corrélation des rangs entre huit indicateurs des départements de métropole"},
    "ex.cor.hover": {"en": "%{y} and %{x}: ρ = %{text}", "fr": "%{y} et %{x} : ρ = %{text}"},
    "ex.cor.cb": {"en": "ρ", "fr": "ρ"},
    "ex.cor.caption": {
        "en": "Each cell gives ρ between the indicator of its row and that of its column, written in the cell; blue "
              "when one goes down as the other goes up, ochre when they go up together, paler near zero.",
        "fr": "Chaque case donne ρ entre l'indicateur de sa ligne et celui de sa colonne, écrit dans la case ; bleu "
              "quand l'un baisse pendant que l'autre monte, ocre quand ils montent ensemble, plus pâle près de zéro."},
    "ex.cor.take1": {
        "en": "Hypothesis H2 first: the bacterial and chemical failure rates are almost unrelated (ρ = {h2}), so the two "
              "kinds of problems do not hit the same departments. The share of small networks, on the other hand, "
              "goes almost hand in hand with the bacterial failure rate (ρ = {sb}), and both go the other way from "
              "population (ρ = {sp} and {bp}) and density: departments with few people and many small networks fail "
              "more bacteria tests. Yet the share of small networks says little about the median score (ρ = {ss}), "
              "because the score also weighs chemistry, and the median score is lower where there are more nitrates "
              "(ρ = {sn}). Harder water and more nitrates also go together (ρ = {hn}), a pattern of geography that "
              "this table alone cannot explain.",
        "fr": "L'hypothèse H2 d'abord : les taux d'échec bactériologique et chimique n'ont presque aucun lien (ρ = {h2}), "
              "les deux types de problèmes ne touchent donc pas les mêmes départements. La part de petits réseaux, en "
              "revanche, va presque de pair avec le taux d'échec bactériologique (ρ = {sb}), et tous deux vont dans le "
              "sens inverse de la population (ρ = {sp} et {bp}) et de la densité : les départements peu peuplés et "
              "riches en petits réseaux échouent plus souvent aux analyses de bactéries. Pourtant, la part de petits "
              "réseaux dit peu de chose du score médian (ρ = {ss}), car le score pèse aussi la chimie, et le score "
              "médian est plus bas là où il y a plus de nitrates (ρ = {sn}). Une eau plus dure et plus de nitrates vont "
              "aussi ensemble (ρ = {hn}), un trait de géographie que ce tableau seul ne peut pas expliquer."},
    "ex.cor.take2": {
        "en": "A correlation is not a cause. Small networks, low density and bacterial failures come together, and "
              "this table cannot say which one drives the others: a rural department has both more small networks "
              "and fewer people, and either could matter, or something else that goes with both. ρ also only "
              "captures a link that keeps the same direction. And with {n} departments, a ρ between −{crit} and "
              "{crit} could come from chance alone (the usual 5% test).",
        "fr": "Une corrélation n'est pas une cause. Petits réseaux, faible densité et échecs bactériologiques vont "
              "ensemble, et ce tableau ne peut pas dire lequel entraîne les autres : un département rural a à la fois "
              "plus de petits réseaux et moins d'habitants, et l'un comme l'autre pourrait compter, ou une troisième "
              "chose liée aux deux. ρ ne capte en outre qu'un lien qui garde le même sens. Et avec {n} départements, "
              "un ρ compris entre −{crit} et {crit} pourrait venir du seul hasard (le test habituel à 5 %)."},
    "ex.ind.bact_rate": {"en": "Bacterial failures", "fr": "Échecs bactério"},
    "ex.ind.chem_rate": {"en": "Chemical failures", "fr": "Échecs chimie"},
    "ex.ind.score_median": {"en": "Median score", "fr": "Score médian"},
    "ex.ind.small_share": {"en": "Small networks", "fr": "Petits réseaux"},
    "ex.ind.hardness": {"en": "Hardness", "fr": "Dureté"},
    "ex.ind.nitrates": {"en": "Nitrates", "fr": "Nitrates"},
    "ex.ind.population": {"en": "Population", "fr": "Population"},
    "ex.ind.density": {"en": "Density", "fr": "Densité"},
    "ex.ax.bact_rate": {"en": "Bacterial failures, {y0}–{y1} (% of samples)",
                        "fr": "Échecs bactério, {y0}–{y1} (% des prélèvements)"},
    "ex.ax.chem_rate": {"en": "Chemical failures, {y0}–{y1} (% of samples)",
                        "fr": "Échecs chimie, {y0}–{y1} (% des prélèvements)"},
    "ex.ax.score_median": {"en": "Median score of the towns (out of 100)", "fr": "Score médian des communes (sur 100)"},
    "ex.ax.small_share": {"en": "Share of small networks, {y0}–{y1} (%)", "fr": "Part de petits réseaux, {y0}–{y1} (%)"},
    "ex.ax.hardness": {"en": "Hardness, networks' median, {year} (°f)",
                       "fr": "Dureté, médiane des réseaux, {year} (°f)"},
    "ex.ax.nitrates": {"en": "Nitrates, networks' median, {year} (mg/L)",
                       "fr": "Nitrates, médiane des réseaux, {year} (mg/L)"},
    "ex.ax.population": {"en": "Population (inhabitants)", "fr": "Population (habitants)"},
    "ex.ax.density": {"en": "Density (inhabitants per km²)", "fr": "Densité (habitants par km²)"},

    "ex.sc.kicker": {"en": "Your turn", "fr": "À vous"},
    "ex.sc.title": {"en": "Pick two indicators and look at the departments",
                    "fr": "Choisissez deux indicateurs et regardez les départements"},
    "ex.sc.x": {"en": "Horizontal axis", "fr": "Axe horizontal"},
    "ex.sc.y": {"en": "Vertical axis", "fr": "Axe vertical"},
    "ex.sc.help": {"en": "Any of the eight indicators of the matrix above.",
                   "fr": "N'importe lequel des huit indicateurs de la matrice ci-dessus."},
    "ex.sc.chart": {"en": "{y} against {x}, one dot per department", "fr": "{y} selon {x}, un point par département"},
    "ex.sc.caption": {
        "en": "Each dot is a department of mainland France; hover to read its name and its two values. The five "
              "departments with the highest values on the vertical axis are named.{log}",
        "fr": "Chaque point est un département de métropole ; survolez-le pour lire son nom et ses deux valeurs. Les "
              "cinq départements aux valeurs les plus hautes sur l'axe vertical sont nommés.{log}"},
    "ex.sc.log": {"en": " The axis of {var} is logarithmic: each step multiplies the value by ten.",
                  "fr": " L'axe {var} est logarithmique : chaque graduation multiplie la valeur par dix."},
    "ex.sc.take": {
        "en": "For this pair, ρ = {rho} over {n} departments: {strength}. {direction}{chance} Whatever the "
              "pair, the dots say where things happen together, not why.",
        "fr": "Pour ce couple, ρ = {rho} sur {n} départements : {strength}. {direction}{chance} Quel que soit le "
              "couple, les points disent où les choses vont ensemble, pas pourquoi."},
    "ex.sc.up": {"en": "When one is higher, the other tends to be higher too.",
                 "fr": "Quand l'un est plus élevé, l'autre tend à l'être aussi."},
    "ex.sc.down": {"en": "When one is higher, the other tends to be lower.",
                   "fr": "Quand l'un est plus élevé, l'autre tend à être plus bas."},
    "ex.sc.flat": {"en": "The dots show no clear direction.", "fr": "Les points ne montrent pas de sens net."},
    "ex.sc.chance": {"en": " Such a weak value could come from chance alone.",
                     "fr": " Une valeur aussi faible pourrait venir du seul hasard."},
    "ex.sc.same": {"en": "Pick two different indicators to draw the chart.",
                   "fr": "Choisissez deux indicateurs différents pour tracer le graphique."},
    "ex.strength.very_strong": {"en": "a very strong link", "fr": "un lien très fort"},
    "ex.strength.strong": {"en": "a strong link", "fr": "un lien fort"},
    "ex.strength.moderate": {"en": "a moderate link", "fr": "un lien modéré"},
    "ex.strength.weak": {"en": "a weak link", "fr": "un lien faible"},
    "ex.strength.none": {"en": "almost no link", "fr": "presque aucun lien"},
}

"""Fact sheets of the key parameters (page "How to read a water test").

Every health statement, origin, threshold rationale and management rule below comes from an official source listed in
docs/sources.md; the numbers in "sources" are those of docs/sources.md. Fields: what it is, where it comes from, possible
effects on health, the threshold and why, what happens when it is exceeded. The figures of the data are added by the page.
"""

SOURCES = {
    3: ("WHO, Drinking-water fact sheet (2023)", "https://www.who.int/news-room/fact-sheets/detail/drinking-water"),
    5: ("Assemblée nationale, written question 2237 (2023)",
        "https://questions.assemblee-nationale.fr/dyn/16/questions/QANR5L16QE2237.pdf"),
    6: ("ARS Hauts-de-France, chlorothalonil metabolites (2025)",
        "https://www.hauts-de-france.ars.sante.fr/les-metabolites-du-chlorothalonil-0"),
    11: ("ARS Nouvelle-Aquitaine, PFAS monitoring (2026)",
         "https://www.nouvelle-aquitaine.ars.sante.fr/surveillance-des-pfas-polluants-chimiques-eternels-dans-leau-en-nouvelle-aquitaine"),
    18: ("Anses, Pesticides in tap water (2024)", "https://www.anses.fr/fr/content/pesticides-dans-eau-du-robinet"),
    19: ("ARS Hauts-de-France, chloridazon metabolites FAQ (2026)",
         "https://www.hauts-de-france.ars.sante.fr/metabolites-de-la-chloridazone-dans-leau-du-robinet-les-reponses-aux-questions-les-plus-frequentes"),
    20: ("ARS Grand Est, drinking water and pesticides FAQ", "https://www.grand-est.ars.sante.fr/media/97663/download"),
    21: ("Anses, national campaign on emerging pollutants (2023)",
         "https://www.anses.fr/en/content/emerging-pollutants-drinking-water-review-main-findings-latest-national-campaign"),
    22: ("ARS Centre-Val de Loire, drinking water quality in 2024", "https://centre-val-de-loire.ars.sante.fr/media/146900/download"),
    23: ("WHO, Nitrate and nitrite in drinking-water (2016)",
         "https://cdn.who.int/media/docs/default-source/wash-documents/wash-chemicals/nitrate-nitrite-background-jan17.pdf"),
    24: ("ARS Normandie, nitrates press release (2024)", "https://www.normandie.ars.sante.fr/media/127448/download"),
    25: ("WHO, Lead poisoning fact sheet (2026)", "https://www.who.int/news-room/fact-sheets/detail/lead-poisoning-and-health"),
    26: ("ARS Pays de la Loire, water and lead in old housing (2026)",
         "https://www.pays-de-la-loire.ars.sante.fr/eau-plomb-dans-logements-anciens-degrades"),
    27: ("WHO, Arsenic fact sheet (2022)", "https://www.who.int/news-room/fact-sheets/detail/arsenic"),
    28: ("ARS Occitanie, vinyl chloride monomer (2024)", "https://www.sante.fr/node/7609835"),
    29: ("ARS Nouvelle-Aquitaine, vinyl chloride guide (2021)", "https://www.nouvelle-aquitaine.ars.sante.fr/media/133978/download"),
    30: ("WHO, Trihalomethanes chemical fact sheet (2022)",
         "https://cdn.who.int/media/docs/default-source/wash-documents/water-safety-and-quality/chemical-fact-sheets-2022/trihalomethanes-fact-sheet-2022.pdf"),
    31: ("Afssa (Anses), opinion on trihalomethanes (2004)", "https://www.anses.fr/fr/system/files/RCCP2004sa0070.pdf"),
    32: ("ARS Guadeloupe, bromates questions and answers (2018)",
         "https://www.guadeloupe.ars.sante.fr/system/files/2018-08/1808_QR_bromates%20V5%20stabilis%C3%A9.pdf"),
    33: ("ARS Occitanie, bacteriology (2026)", "https://www.occitanie.ars.sante.fr/la-bacteriologie"),
    34: ("ARS Normandie, water quality control (2026)", "https://www.normandie.ars.sante.fr/le-controle-de-la-qualite-de-leau"),
    35: ("Afssa (Anses), aluminium fact sheet (2005)", "https://www.anses.fr/fr/system/files/EAUX-Fi-AluminiumJanvier05.pdf"),
    36: ("Anses, opinion on manganese (2018)", "https://www.anses.fr/en/system/files/EAUX2016SA0203.pdf"),
    37: ("ARS Île-de-France, information on tap water quality (2025)",
         "https://www.iledefrance.ars.sante.fr/alimentation-en-eau-potable-linformation-sur-la-qualite-de-leau-du-robinet"),
    38: ("ARS Hauts-de-France, PFAS in 3 questions (2025)", "https://www.hauts-de-france.ars.sante.fr/les-pfas-en-3-questions-cles"),
    39: ("ARS Hauts-de-France, PFAS and drinking water control (2026)",
         "https://www.hauts-de-france.ars.sante.fr/pfas-controle-de-leau-potable"),
}

FIELDS = ["what", "origin", "health", "threshold", "exceed"]

FACTS = {
    "CLDZ_D": {
        "sources": [18, 19, 20],
        "what": {"en": "A metabolite, that is a breakdown product, of chloridazon, a herbicide used mainly on sugar beet. "
                       "Chloridazon has been banned since the end of 2020.",
                 "fr": "Un métabolite, c'est-à-dire un produit de dégradation, de la chloridazone, un herbicide utilisé "
                       "principalement sur la betterave. La chloridazone est interdite depuis fin 2020."},
        "origin": {"en": "It forms when chloridazon breaks down in soil or water, and reaches the groundwater that supplies "
                         "drinking water. Years after the ban, it is still there.",
                   "fr": "Il se forme quand la chloridazone se dégrade dans le sol ou l'eau, et rejoint les nappes qui "
                         "alimentent l'eau potable. Des années après l'interdiction, il est toujours là."},
        "health": {"en": "In April 2020 Anses classified it as relevant by default, as a precaution, because the available "
                         "toxicological studies were not sufficient; the agency could not conclude on its genotoxic potential.",
                   "fr": "En avril 2020, l'Anses l'a classé pertinent par défaut, par précaution, car les études "
                         "toxicologiques disponibles étaient insuffisantes ; l'agence n'a pas pu conclure sur son potentiel "
                         "génotoxique."},
        "threshold": {"en": "0.1 µg/L, the limit of every pesticide and relevant metabolite. It is an environmental quality "
                            "limit set at European level, not a toxicity threshold. The maximum health value set by Anses in "
                            "July 2024 is 11 µg/L: below it, drinking the water is considered without health risk.",
                      "fr": "0,1 µg/L, la limite de tout pesticide et métabolite pertinent. C'est une limite de qualité "
                            "environnementale fixée au niveau européen, pas un seuil de toxicité. La valeur sanitaire "
                            "maximale fixée par l'Anses en juillet 2024 est de 11 µg/L : en dessous, boire l'eau est "
                            "considéré sans risque pour la santé."},
        "exceed": {"en": "Above 0.1 µg/L the water is declared non-compliant but it is not unfit to drink as long as the "
                         "maximum health value is respected; the supplier must take corrective action and the ARS tests "
                         "more often.",
                   "fr": "Au-dessus de 0,1 µg/L, l'eau est déclarée non conforme mais elle n'est pas impropre à la "
                         "consommation tant que la valeur sanitaire maximale est respectée ; le distributeur doit agir et "
                         "l'ARS contrôle plus souvent."},
    },
    "471811R": {
        "sources": [6, 21, 22],
        "what": {"en": "A metabolite of chlorothalonil, a fungicide widely used in France on cereals, potatoes and "
                       "vegetables until May 2020.",
                 "fr": "Un métabolite du chlorothalonil, un fongicide très utilisé en France sur les céréales, la pomme de "
                       "terre et les légumes jusqu'en mai 2020."},
        "origin": {"en": "It forms when chlorothalonil breaks down in the environment. In the national campaign of Anses it "
                         "was found in more than half of the samples, and in Centre-Val de Loire it caused 87.5% of the "
                         "recurring exceedances of 2024.",
                   "fr": "Il se forme quand le chlorothalonil se dégrade dans l'environnement. Dans la campagne nationale de "
                         "l'Anses, il a été trouvé dans plus de la moitié des prélèvements, et en Centre-Val de Loire il "
                         "expliquait 87,5 % des dépassements récurrents de 2024."},
        "health": {"en": "Classified relevant by default in 2023, it was reclassified non-relevant by Anses on "
                         "29 April 2024, on the basis of new scientific knowledge.",
                   "fr": "Classé pertinent par défaut en 2023, il a été reclassé non pertinent par l'Anses le "
                         "29 avril 2024, sur la base de nouvelles connaissances scientifiques."},
        "threshold": {"en": "Since that date it is compared with an indicative value of 0.9 µg/L instead of the 0.1 µg/L "
                            "limit. In the data, older results still carry the 0.1 µg/L limit.",
                      "fr": "Depuis cette date, il est comparé à une valeur indicative de 0,9 µg/L au lieu de la limite de "
                            "0,1 µg/L. Dans les données, les résultats plus anciens portent encore la limite de 0,1 µg/L."},
        "exceed": {"en": "Water above 0.9 µg/L can still be drunk. The exceedance shows that the resource is vulnerable to "
                         "diffuse pollution, and the supplier must set up an action plan.",
                   "fr": "Une eau au-dessus de 0,9 µg/L peut toujours être bue. Le dépassement montre que la ressource est "
                         "vulnérable aux pollutions diffuses, et le distributeur doit mettre en place un plan d'actions."},
    },
    "MTCESA": {
        "sources": [5, 6, 20, 21],
        "what": {"en": "A metabolite of S-metolachlor, a herbicide that is still authorised and used mainly on maize.",
                 "fr": "Un métabolite du S-métolachlore, un herbicide encore autorisé et utilisé surtout sur le maïs."},
        "origin": {"en": "It forms in the soil and reaches the groundwater. The national campaign of Anses measured it in "
                         "more than half of the samples.",
                   "fr": "Il se forme dans le sol et rejoint les nappes. La campagne nationale de l'Anses l'a mesuré dans "
                         "plus de la moitié des prélèvements."},
        "health": {"en": "Anses classified it non-relevant on 30 September 2022.",
                   "fr": "L'Anses l'a classé non pertinent le 30 septembre 2022."},
        "threshold": {"en": "An indicative value of 0.9 µg/L applies since then, instead of the 0.1 µg/L limit. In the "
                            "national campaign fewer than 2% of the samples were above it.",
                      "fr": "Une valeur indicative de 0,9 µg/L s'applique depuis, au lieu de la limite de 0,1 µg/L. Dans "
                            "la campagne nationale, moins de 2 % des prélèvements la dépassaient."},
        "exceed": {"en": "As for any non-relevant metabolite, going above 0.9 µg/L does not prevent drinking the water but "
                         "requires an action plan from the supplier.",
                   "fr": "Comme pour tout métabolite non pertinent, dépasser 0,9 µg/L n'empêche pas de boire l'eau mais "
                         "impose un plan d'actions au distributeur."},
    },
    "ADET": {
        "sources": [18, 22],
        "what": {"en": "The main metabolite of atrazine, a herbicide banned in France since 2003.",
                 "fr": "Le principal métabolite de l'atrazine, un herbicide interdit en France depuis 2003."},
        "origin": {"en": "It persists in groundwater more than twenty years after the ban, and is still among the causes of "
                         "pesticide non-compliance in some regions in 2024.",
                   "fr": "Il persiste dans les nappes plus de vingt ans après l'interdiction, et fait encore partie des "
                         "causes de non-conformité en pesticides dans certaines régions en 2024."},
        "health": {"en": "We did not find a recent official health value for this metabolite in our sources, so the app does "
                         "not give one.",
                   "fr": "Nous n'avons pas trouvé de valeur sanitaire officielle récente pour ce métabolite dans nos "
                         "sources : l'application n'en donne donc pas."},
        "threshold": {"en": "0.1 µg/L, like every pesticide and relevant metabolite: an indicator of quality that is not "
                            "built on the toxicity of the substance.",
                      "fr": "0,1 µg/L, comme tout pesticide et métabolite pertinent : un indicateur de qualité qui n'est "
                            "pas construit sur la toxicité de la substance."},
        "exceed": {"en": "The water is declared non-compliant and the supplier must take corrective action, for instance "
                         "protecting the resource, mixing waters or adding a treatment.",
                   "fr": "L'eau est déclarée non conforme et le distributeur doit agir, par exemple en protégeant la "
                         "ressource, en mélangeant des eaux ou en ajoutant un traitement."},
    },
    "PESTOT": {
        "sources": [18, 20],
        "what": {"en": "Not a molecule but a sum: the laboratory adds up the concentrations of all the pesticides and "
                       "relevant metabolites it searched in the sample.",
                 "fr": "Pas une molécule mais une somme : le laboratoire additionne les concentrations de tous les "
                       "pesticides et métabolites pertinents qu'il a cherchés dans le prélèvement."},
        "origin": {"en": "It reflects the pesticides used around the resource, and also the list of molecules searched, which "
                         "each regional health agency sets according to local crops and past detections.",
                   "fr": "Elle reflète les pesticides utilisés autour de la ressource, et aussi la liste des molécules "
                         "cherchées, que chaque agence régionale de santé fixe selon les cultures locales et les détections "
                         "passées."},
        "health": {"en": "Like the limit per substance, the limit on the total is not built on toxicity: it is a quality "
                         "indicator meant to account for several molecules being present together.",
                   "fr": "Comme la limite par substance, la limite du total n'est pas construite sur la toxicité : c'est un "
                         "indicateur de qualité destiné à tenir compte de la présence simultanée de plusieurs molécules."},
        "threshold": {"en": "0.5 µg/L for the sum.", "fr": "0,5 µg/L pour la somme."},
        "exceed": {"en": "The dataset gives the total but not its breakdown. To know which molecules make it, one must read "
                         "the individual results of the same sample; the report of each network in this app lists the "
                         "substances that went above their own limit.",
                   "fr": "Le jeu de données donne le total mais pas sa composition. Pour savoir quelles molécules le "
                         "composent, il faut lire les résultats individuels du même prélèvement ; le rapport de chaque réseau "
                         "dans cette application liste les substances qui ont dépassé leur propre limite."},
    },
    "SPFAS": {
        "sources": [11, 38, 39],
        "what": {"en": "PFAS are man-made substances used since the 1950s for their non-stick, water-repellent "
                       "and heat-resistant properties. The control looks at the sum of twenty of them.",
                 "fr": "Les PFAS sont des substances fabriquées par l'homme, utilisées depuis les années 1950 "
                       "pour leurs propriétés antiadhésives, imperméabilisantes et résistantes à la chaleur. Le contrôle "
                       "porte sur la somme de vingt d'entre elles."},
        "origin": {"en": "They are called forever pollutants because they hardly break down. They are found in packaging, "
                         "non-stick pans and many products, and local contaminations have been traced to industrial sites.",
                   "fr": "On les appelle polluants éternels parce qu'ils se dégradent très peu. On les trouve dans des "
                         "emballages, des poêles antiadhésives et de nombreux produits, et des contaminations locales ont été "
                         "reliées à des sites industriels."},
        "health": {"en": "Four effects are frequently cited: a weaker immune response to vaccines, raised cholesterol or "
                         "triglycerides, a lower birth weight and a higher risk of kidney cancer. Others are suspected with "
                         "less evidence.",
                   "fr": "Quatre effets sont fréquemment cités : une moindre réponse immunitaire aux vaccins, un cholestérol "
                         "ou des triglycérides élevés, une baisse du poids de naissance et un risque accru de cancer du rein. "
                         "D'autres sont suspectés avec moins de preuves."},
        "threshold": {"en": "0.1 µg/L for the sum of the twenty PFAS in tap water, a regulatory quality limit, in the "
                            "routine control since 1 January 2026.",
                      "fr": "0,1 µg/L pour la somme des vingt PFAS dans l'eau du robinet, une limite de qualité "
                            "réglementaire, dans le contrôle courant depuis le 1er janvier 2026."},
        "exceed": {"en": "The supplier must take corrective measures and inform the users, the mayor, the prefect and the "
                         "ARS, which follows the case with new analyses.",
                   "fr": "Le distributeur doit prendre des mesures correctives et informer les usagers, le maire, le préfet "
                         "et l'ARS, qui suit le dossier par de nouvelles analyses."},
    },
    "NO3": {
        "sources": [23, 24, 37],
        "what": {"en": "Nitrates are nitrogen compounds dissolved in water.",
                 "fr": "Les nitrates sont des composés azotés dissous dans l'eau."},
        "origin": {"en": "Mostly agriculture (mineral fertilisers and manure), but also wastewater and industrial discharges.",
                   "fr": "Surtout l'agriculture (engrais minéraux et fumier), mais aussi les eaux usées et les rejets "
                         "industriels."},
        "health": {"en": "The World Health Organization set its value to protect the most sensitive people, bottle-fed "
                         "infants, against methaemoglobinaemia, a blood disorder, and thyroid effects, which epidemiological "
                         "studies did not find below 50 mg/L.",
                   "fr": "L'Organisation mondiale de la santé a fixé sa valeur pour protéger les plus sensibles, les "
                         "nourrissons nourris au biberon, contre la méthémoglobinémie, un trouble du sang, et des effets sur "
                         "la thyroïde, que les études épidémiologiques n'ont pas trouvés sous 50 mg/L."},
        "threshold": {"en": "50 mg/L at the consumer's tap, based on that WHO recommendation.",
                      "fr": "50 mg/L au robinet du consommateur, sur la base de cette recommandation de l'OMS."},
        "exceed": {"en": "Above 50 mg/L, pregnant women and infants must not drink the water nor use it for food; the rest of "
                         "the population can drink it normally.",
                   "fr": "Au-dessus de 50 mg/L, les femmes enceintes et les nourrissons ne doivent ni boire l'eau ni "
                         "l'utiliser pour l'alimentation ; le reste de la population peut la boire normalement."},
    },
    "PB": {
        "sources": [25, 26],
        "what": {"en": "A metal that does not come from the water source but from the pipes it flows through.",
                 "fr": "Un métal qui ne vient pas de la ressource mais des tuyaux dans lesquels l'eau circule."},
        "origin": {"en": "Mainly old lead service connections and the internal pipes of old buildings; lead pipes, solders "
                         "and fittings release it into the water, all the more when water stands still.",
                   "fr": "Surtout les anciens branchements en plomb et les canalisations intérieures des immeubles anciens ; "
                         "les tuyaux, soudures et raccords en plomb le libèrent dans l'eau, d'autant plus que l'eau stagne."},
        "health": {"en": "No level of exposure is known to be without harmful effects. Lead can permanently affect the "
                         "development of children's brains, and in adults it raises the risk of high blood pressure and "
                         "kidney damage.",
                   "fr": "Aucun niveau d'exposition n'est connu sans effet nocif. Le plomb peut affecter durablement le "
                         "développement du cerveau des enfants, et chez l'adulte il augmente le risque d'hypertension et "
                         "d'atteinte des reins."},
        "threshold": {"en": "10 µg/L at the tap, lowered to 5 µg/L from January 2036.",
                      "fr": "10 µg/L au robinet, abaissés à 5 µg/L à partir de janvier 2036."},
        "exceed": {"en": "In a building with lead pipes, let the cold water run for one or two minutes after it has stood, "
                         "use only cold water for food, and prefer bottled water for infants and pregnant women; the lasting "
                         "fix is replacing the pipes.",
                   "fr": "Dans un immeuble avec des canalisations en plomb, laisser couler l'eau froide une à deux minutes "
                         "après une stagnation, n'utiliser que l'eau froide pour l'alimentation, et préférer l'eau en "
                         "bouteille pour les nourrissons et les femmes enceintes ; la solution durable est de remplacer les "
                         "tuyaux."},
    },
    "AS": {
        "sources": [27],
        "what": {"en": "A natural chemical element.", "fr": "Un élément chimique naturel."},
        "origin": {"en": "It is naturally present at high levels in the groundwater of some areas, depending on the geology.",
                   "fr": "Il est naturellement présent à des niveaux élevés dans les nappes de certaines zones, selon la "
                         "géologie."},
        "health": {"en": "Over a long time, it can cause skin lesions and skin cancer, as well as cancers of the bladder and "
                         "the lungs.",
                   "fr": "Sur une longue durée, il peut causer des lésions et des cancers de la peau, ainsi que des cancers "
                         "de la vessie et du poumon."},
        "threshold": {"en": "10 µg/L, the WHO guideline value, called provisional because arsenic is technically difficult "
                            "to remove from water.",
                      "fr": "10 µg/L, la valeur guide de l'OMS, dite provisoire parce que l'arsenic est techniquement "
                            "difficile à retirer de l'eau."},
        "exceed": {"en": "The data does not say what was decided locally; the measures taken are published by the regional "
                         "health agency and the water supplier.",
                   "fr": "Les données ne disent pas ce qui a été décidé localement ; les mesures prises sont publiées par "
                         "l'agence régionale de santé et le distributeur d'eau."},
    },
    "CLVYL": {
        "sources": [28, 29],
        "what": {"en": "Vinyl chloride monomer, a synthetic chemical used to make PVC.",
                 "fr": "Le chlorure de vinyle monomère, un produit chimique de synthèse qui sert à fabriquer le PVC."},
        "origin": {"en": "Mostly the slow degradation of PVC pipes made before 1980, which slowly releases it into the water.",
                   "fr": "Surtout la dégradation lente des canalisations en PVC fabriquées avant 1980, qui le libère lentement dans "
                         "l'eau."},
        "health": {"en": "The International Agency for Research on Cancer has classified it as carcinogenic to humans since "
                         "1987, on the basis of high exposures by inhalation at work; it can cause liver cancers.",
                   "fr": "Le Centre international de recherche sur le cancer le classe cancérogène certain pour l'homme "
                         "depuis 1987, sur la base d'expositions professionnelles fortes par inhalation ; il peut causer des "
                         "cancers du foie."},
        "threshold": {"en": "0.5 µg/L, set by the European directives.", "fr": "0,5 µg/L, fixé par les directives européennes."},
        "exceed": {"en": "The operator informs the ARS and flushes the pipes as an emergency measure; the lasting fix is to "
                         "replace them. Meanwhile consumers can be told not to drink the water unless it is boiled, or be "
                         "given bottled water.",
                   "fr": "L'exploitant informe l'ARS et purge les canalisations en urgence ; la solution durable est de les "
                         "remplacer. En attendant, les consommateurs peuvent recevoir la consigne de ne boire l'eau que "
                         "bouillie, ou de l'eau en bouteille."},
    },
    "THM4": {
        "sources": [30, 31],
        "what": {"en": "The sum of four by-products of chlorination: chloroform, bromoform, dibromochloromethane and "
                       "bromodichloromethane.",
                 "fr": "La somme de quatre sous-produits de la chloration : chloroforme, bromoforme, dibromochlorométhane "
                       "et bromodichlorométhane."},
        "origin": {"en": "They form when the chlorine used to disinfect water reacts with natural organic matter.",
                   "fr": "Ils se forment quand le chlore utilisé pour désinfecter l'eau réagit avec la matière organique "
                         "naturelle."},
        "health": {"en": "Chloroform is classified as possibly carcinogenic to humans. Studies found associations between THM "
                         "levels from 50 µg/L and bladder cancer, without proving that one causes the other.",
                   "fr": "Le chloroforme est classé cancérogène possible pour l'homme. Des études ont trouvé des "
                         "associations entre des teneurs en THM dès 50 µg/L et le cancer de la vessie, sans prouver de lien "
                         "de cause à effet."},
        "threshold": {"en": "100 µg/L for the total, with the aim of staying as low as possible without weakening "
                            "disinfection.",
                      "fr": "100 µg/L pour le total, avec l'objectif de rester aussi bas que possible sans affaiblir la "
                            "désinfection."},
        "exceed": {"en": "Once formed they are hard to remove, so the answer is prevention: less organic matter before "
                         "chlorination and better-adjusted chlorine doses.",
                   "fr": "Une fois formés, ils sont difficiles à retirer : la réponse est la prévention, avec moins de "
                         "matière organique avant la chloration et des doses de chlore mieux ajustées."},
    },
    "BRATE": {
        "sources": [32],
        "what": {"en": "Bromates do not exist in nature; they appear during water treatment.",
                 "fr": "Les bromates n'existent pas dans la nature ; ils apparaissent pendant le traitement de l'eau."},
        "origin": {"en": "They form when bromide in the water is oxidised during disinfection, or come from impurities in the "
                         "chlorine disinfectant.",
                   "fr": "Ils se forment quand les bromures de l'eau sont oxydés pendant la désinfection, ou viennent "
                         "d'impuretés du désinfectant chloré."},
        "health": {"en": "No study in humans is available; in rats they caused tumours, and the European Union and the WHO "
                         "classify potassium bromate as a probable human carcinogen.",
                   "fr": "Aucune étude chez l'homme n'est disponible ; chez le rat, ils ont causé des tumeurs, et l'Union "
                         "européenne et l'OMS classent le bromate de potassium cancérogène probable pour l'homme."},
        "threshold": {"en": "10 µg/L.", "fr": "10 µg/L."},
        "exceed": {"en": "In a case at Saint-Barthélemy in 2018, the health agency banned drinking and cooking with the water "
                         "while the cause was investigated.",
                   "fr": "Dans un cas à Saint-Barthélemy en 2018, l'agence de santé a interdit de boire l'eau et de cuisiner "
                         "avec pendant la recherche de la cause."},
    },
    "ECOLI": {
        "sources": [3, 33],
        "what": {"en": "A bacterium whose presence in water is the sign of faecal contamination.",
                 "fr": "Une bactérie dont la présence dans l'eau est le signe d'une contamination fécale."},
        "origin": {"en": "Poorly maintained or unprotected catchments, missing or inadequate disinfection, heavy rain, storms "
                         "and droughts, livestock or wildlife near the source.",
                   "fr": "Des captages mal entretenus ou mal protégés, une désinfection absente ou inadaptée, de fortes "
                         "pluies, des orages et des sécheresses, du bétail ou des animaux sauvages près de la ressource."},
        "health": {"en": "Its presence means that disease-causing germs may be there too. Symptoms are most often those of "
                         "gastroenteritis, with young children, elderly and immunocompromised people more at risk.",
                   "fr": "Sa présence veut dire que des germes pathogènes peuvent l'accompagner. Les symptômes sont le plus "
                         "souvent ceux d'une gastro-entérite, et les jeunes enfants, les personnes âgées et immunodéprimées "
                         "sont plus à risque."},
        "threshold": {"en": "None in 100 mL of water.", "fr": "Aucune dans 100 mL d'eau."},
        "exceed": {"en": "When the contamination poses a health risk, the authorities ban drinking tap water until the "
                         "situation is back to normal.",
                   "fr": "Quand la contamination présente un risque sanitaire, les autorités interdisent de boire l'eau du "
                         "robinet jusqu'au retour à la normale."},
    },
    "STRF": {
        "sources": [33],
        "what": {"en": "Enterococci are bacteria that, like E. coli, reveal a faecal contamination of the water.",
                 "fr": "Les entérocoques sont des bactéries qui, comme E. coli, révèlent une contamination fécale de l'eau."},
        "origin": {"en": "The same failures as for E. coli: poorly protected catchments, insufficient disinfection, bad weather.",
                   "fr": "Les mêmes défaillances que pour E. coli : captages mal protégés, désinfection insuffisante, "
                         "intempéries."},
        "health": {"en": "Disease-causing germs may be present; symptoms are most often those of gastroenteritis.",
                   "fr": "Des germes pathogènes peuvent être présents ; les symptômes sont le plus souvent ceux d'une "
                         "gastro-entérite."},
        "threshold": {"en": "None in 100 mL of water.", "fr": "Aucun dans 100 mL d'eau."},
        "exceed": {"en": "Same management as for E. coli: when there is a health risk, drinking the water is banned.",
                   "fr": "Même gestion que pour E. coli : en cas de risque sanitaire, la consommation de l'eau est "
                         "interdite."},
    },
    "CTF": {
        "sources": [33, 34],
        "what": {"en": "Coliform bacteria are a broad group of bacteria.",
                 "fr": "Les bactéries coliformes forment un large groupe de bactéries."},
        "origin": {"en": "They show how well the network is maintained and whether disinfection works.",
                   "fr": "Elles montrent si le réseau est bien entretenu et si la désinfection fonctionne."},
        "health": {"en": "They are not dangerous to health in themselves.", "fr": "Elles ne sont pas dangereuses pour la "
                                                                               "santé en elles-mêmes."},
        "threshold": {"en": "A quality reference of zero in 100 mL, not a health limit.",
                      "fr": "Une référence de qualité de zéro dans 100 mL, pas une limite sanitaire."},
        "exceed": {"en": "An exceedance is a warning for the operator, who checks the treatment and the cleanliness of the "
                         "installations.",
                   "fr": "Un dépassement est un avertissement pour l'exploitant, qui vérifie le traitement et la propreté "
                         "des installations."},
    },
    "TURBNFU": {
        "sources": [34],
        "what": {"en": "Turbidity measures how cloudy the water is, in nephelometric units (NFU).",
                 "fr": "La turbidité mesure à quel point l'eau est trouble, en unités néphélométriques (NFU)."},
        "origin": {"en": "Fine mineral particles (silt, clay, iron, manganese, aluminium) or organic matter.",
                   "fr": "De fines particules minérales (limons, argiles, fer, manganèse, aluminium) ou de la matière "
                         "organique."},
        "health": {"en": "At the tap it is a quality reference, which the health agencies describe as having no direct "
                         "effect on health.",
                   "fr": "Au robinet, c'est une référence de qualité, que les agences de santé décrivent comme sans "
                         "incidence directe sur la santé."},
        "threshold": {"en": "2 NFU at the tap (reference); for surface water, a limit of 1 NFU applies when it leaves the "
                            "treatment plant.",
                      "fr": "2 NFU au robinet (référence) ; pour les eaux de surface, une limite de 1 NFU s'applique à la "
                            "sortie de l'usine de traitement."},
        "exceed": {"en": "Cloudy water at the tap tells the operator that treatment or the network needs attention.",
                   "fr": "Une eau trouble au robinet signale à l'exploitant que le traitement ou le réseau demande de "
                         "l'attention."},
    },
    "ALTMICR": {
        "sources": [35],
        "what": {"en": "A light metal.", "fr": "Un métal léger."},
        "origin": {"en": "Either natural, from rocks, or from the aluminium salts used to make particles clump together "
                         "during treatment (coagulation).",
                   "fr": "Soit naturel, venu des roches, soit des sels d'aluminium utilisés pour agglomérer les particules "
                         "pendant le traitement (coagulation)."},
        "health": {"en": "Its threshold is not set on health grounds: it is an indicator of how well the treatment works.",
                   "fr": "Son seuil n'est pas fixé pour des raisons sanitaires : c'est un indicateur du bon fonctionnement "
                         "du traitement."},
        "threshold": {"en": "A quality reference of 200 µg/L.", "fr": "Une référence de qualité de 200 µg/L."},
        "exceed": {"en": "It points to a treatment that needs adjusting.", "fr": "Il signale un traitement à régler."},
    },
    "FET": {
        "sources": [34],
        "what": {"en": "A common metal, dissolved or as fine particles.", "fr": "Un métal courant, dissous ou en fines "
                                                                             "particules."},
        "origin": {"en": "Mineral matter present in some waters, which can also make the water cloudy.",
                   "fr": "Une matière minérale présente dans certaines eaux, qui peut aussi rendre l'eau trouble."},
        "health": {"en": "The health agencies list it among the references with no direct effect on health; it mostly affects "
                         "the colour of the water.",
                   "fr": "Les agences de santé le classent parmi les références sans incidence directe sur la santé ; il "
                         "joue surtout sur la couleur de l'eau."},
        "threshold": {"en": "A quality reference of 200 µg/L.", "fr": "Une référence de qualité de 200 µg/L."},
        "exceed": {"en": "A comfort problem (coloured water) that the operator must fix.",
                   "fr": "Un problème de confort (eau colorée) que l'exploitant doit corriger."},
    },
    "MN": {
        "sources": [34, 36],
        "what": {"en": "A metal, measured in water like iron.",
                 "fr": "Un métal, mesuré dans l'eau comme le fer."},
        "origin": {"en": "Present naturally in some water resources.",
                   "fr": "Présent naturellement dans certaines ressources en eau."},
        "health": {"en": "Its reference is set for taste and appearance: people notice it from about 20 µg/L. At high "
                         "exposure, manganese can affect the nervous system, which Anses studied in 2018.",
                   "fr": "Sa référence est fixée pour le goût et l'aspect : on le perçoit dès environ 20 µg/L. À forte "
                         "exposition, le manganèse peut affecter le système nerveux, ce que l'Anses a étudié en 2018."},
        "threshold": {"en": "A quality reference of 50 µg/L, \"for organoleptic and aesthetic reasons\" according to Anses.",
                      "fr": "Une référence de qualité de 50 µg/L, « pour des raisons organoleptiques et esthétiques » selon "
                            "l'Anses."},
        "exceed": {"en": "A comfort problem that the operator must fix by adjusting the treatment.",
                   "fr": "Un problème de confort que l'exploitant doit corriger en ajustant le traitement."},
    },
    "TH": {
        "sources": [37],
        "what": {"en": "Hardness measures the calcium and magnesium dissolved in water, in French degrees (°f).",
                 "fr": "La dureté mesure le calcium et le magnésium dissous dans l'eau, en degrés français (°f)."},
        "origin": {"en": "The geology of the ground the water flows through.",
                   "fr": "La géologie des terrains que traverse l'eau."},
        "health": {"en": "According to the health agencies, hard water has no effect on health.",
                   "fr": "Selon les agences de santé, une eau calcaire n'a aucune incidence sur la santé."},
        "threshold": {"en": "No limit and no reference: it is information only, and it never lowers the score.",
                      "fr": "Ni limite ni référence : c'est une simple information, qui ne fait jamais baisser le score."},
        "exceed": {"en": "Nothing to exceed; hard water mainly means limescale in kettles, pipes and water heaters.",
                   "fr": "Rien à dépasser ; une eau dure veut surtout dire du tartre dans les bouilloires, les tuyaux et les "
                         "chauffe-eau."},
    },
}

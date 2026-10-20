# Sources

Toute valeur affichée dans l'app est soit calculée depuis les données, soit appuyée sur une source de cette liste.
La date de consultation est indiquée entre crochets. Les numéros sont cités dans le code et dans `docs/AVANCEMENT.md`.

## A. Données

1. **Jeu de données principal.** Ministère des Solidarités et de la Santé, « Résultats du contrôle sanitaire de l'eau distribuée
   commune par commune », data.gouv.fr, Licence Ouverte / Open Licence 2.0, dernière mise à jour le 05/10/2026.
   https://www.data.gouv.fr/datasets/resultats-du-controle-sanitaire-de-leau-distribuee-commune-par-commune [19/10/2026]
   Liste des fichiers (tailles, SHA1) : https://www.data.gouv.fr/api/1/datasets/resultats-du-controle-sanitaire-de-leau-distribuee-commune-par-commune/
2. **Documentation du producteur.** « Description des fichiers : résultats du contrôle sanitaire de l'eau distribuée, commune par commune »,
   version 7 du 03/09/2021 (copie : `docs/eau-distrib-documentation.pdf`).
   https://www.data.gouv.fr/api/1/datasets/r/36afc708-42dc-4a89-b039-7fde6bcc83d8 [19/10/2026]
   Utilisée pour : les définitions (unité de distribution, limites et références de qualité), la table de traduction `rqana` vers
   `valtraduite`, les valeurs des indicateurs de conformité, la phrase « l'eau du robinet est l'aliment le plus contrôlé », et
   « plus de 300 000 prélèvements et de l'ordre de 12 millions d'analyses par an ».

## B. Contexte sanitaire (page d'accueil)

3. **Organisation mondiale de la santé (OMS)**, fiche « Drinking-water », 13/09/2023. En 2022, au moins **1,7 milliard** de personnes
   utilisent une source d'eau contaminée par des matières fécales ; l'eau contaminée sur le plan microbiologique causerait environ
   **505 000 décès par diarrhée** chaque année ; elle peut transmettre diarrhées, choléra, dysenterie, typhoïde et poliomyélite.
   https://www.who.int/news-room/fact-sheets/detail/drinking-water [19/10/2026]
4. **Santé publique France**, D. Mouly et al., « Premier bilan épidémiologique du dispositif national de surveillance des épidémies de
   gastro-entérites aiguës d'origine hydrique en France entre 2010 et 2022 », Bulletin épidémiologique hebdomadaire n° 15, 10/09/2024.
   **145 épidémies** confirmées, **219 unités de distribution** desservant **plus de 790 000 habitants**, 46,2 cas médicalisés en moyenne
   par épidémie, la plus grande à Grasse en 2019 (717 cas, Cryptosporidium). Vulnérabilités repérées : ressource 31 %, traitement 20 %,
   distribution 35 % des épidémies investiguées. Les auteurs parlent d'une « forte sous-estimation de l'impact réel ».
   Aucun décès ni hospitalisation n'est chiffré.
   https://beh.santepubliquefrance.fr/beh/2024/15/2024_15_2.html [19/10/2026]
   Recherche faite le 19/10/2026 : aucune source officielle trouvée donnant un nombre national de décès ou d'intoxications dus à l'eau
   du robinet en France. L'app le dit et n'avance aucun chiffre.

## C. Métabolites de pesticides « non pertinents » (insight H3 : ce qu'on mesure, et la façon de le classer, change ce qu'on trouve)

5. **Assemblée nationale, question écrite n° 2237 (16e législature)**, « Eau potable : ANSES », question publiée au JO le 18/10/2022,
   réponse du Gouvernement publiée au JO le 28/03/2023.
   https://questions.assemblee-nationale.fr/dyn/16/questions/QANR5L16QE2237.pdf [19/10/2026]
   L'Anses a publié le **30/09/2022** deux avis classant les métabolites **ESA et NOA du S-métolachlore** « non pertinents » dans l'eau
   potable. Le décret n° 2022-1720 du 29/12/2022 introduit la notion de **valeur indicative** (art. R. 1321-3-1 du code de la santé
   publique) ; l'arrêté du 11/01/2007 modifié la fixe à **0,9 µg/L** pour les métabolites de pesticides non pertinents. En 2021, ces
   deux métabolites étaient responsables de la non-conformité de plus de 900 UDI desservant près de 4 millions d'habitants (chiffre du
   ministère cité dans la réponse, à citer comme tel, pas recalculé).
6. **ARS Hauts-de-France**, « Les métabolites du chlorothalonil », page mise à jour le 12/03/2025.
   https://www.hauts-de-france.ars.sante.fr/les-metabolites-du-chlorothalonil-0 [19/10/2026]
   Chlorothalonil **R471811** jugé pertinent en 2023 (limite 0,1 µg/L), **non pertinent depuis l'avis Anses du 29/04/2024**.
   Un dépassement de la valeur indicative de 0,9 µg/L **n'empêche pas de consommer l'eau** mais impose un **plan d'actions** à la personne
   responsable de la production ou de la distribution d'eau.
7. **ARS Bourgogne-Franche-Comté**, « Informations complémentaires sur le contenu des infofactures 2023 concernant le paramètre pesticides :
   évaluation sanitaire du métabolite Chlorothalonil R471811 », Dijon, 24/07/2024.
   https://bourgogne-franche-comte.ars.sante.fr/media/127554/download [19/10/2026]
   Confirme la source 6. Le mot « infofacture » désigne la note de l'ARS jointe à la facture d'eau.

## D. Limites du sélénium et de l'antimoine (changement du 01/01/2023)

8. **Directive 98/83/CE** du Conseil du 3 novembre 1998 (version consolidée du 27/10/2015), annexe I partie B :
   **antimoine 5,0 µg/L**, **sélénium 10 µg/L**.
   https://eur-lex.europa.eu/legal-content/FR/TXT/HTML/?uri=CELEX:01998L0083-20151027 [19/10/2026]
9. **Directive (UE) 2020/2184** du 16 décembre 2020 (refonte), annexe I partie B : **antimoine 10 µg/L** ; **sélénium 20 µg/L**,
   « 30 µg/l » pour les régions où les conditions géologiques pourraient occasionner des niveaux élevés dans les eaux souterraines.
   Article 24 : transposition au plus tard le 12 janvier 2023. Article 25 : au plus tard le **12 janvier 2026**, respect des valeurs pour,
   entre autres, « la somme des PFAS ».
   https://eur-lex.europa.eu/legal-content/FR/TXT/HTML/?uri=CELEX:32020L2184 [19/10/2026]
10. **Arrêté du 30 décembre 2022** modifiant l'arrêté du 11 janvier 2007 relatif aux limites et références de qualité des eaux brutes et
    des eaux destinées à la consommation humaine (NOR SPRP2221010A, JO n° 303 du 31/12/2022). Il transpose la directive 2020/2184 ;
    article 2 : **entrée en vigueur le 1er janvier 2023**.
    https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046849403 [19/10/2026]
    Valeurs de l'annexe (antimoine 10 µg/L ; sélénium 20 µg/L, 30 µg/L dans les zones géologiques concernées) lues dans la reproduction
    INERIS/AIDA du texte, car le tableau n'est pas affiché en texte sur Légifrance :
    https://aida.ineris.fr/reglementation/arrete-301222-modifiant-larrete-11-janvier-2007-relatif-limites-references-qualite [19/10/2026]
    Usage : explique l'écart « non conforme officiel sans dépassement recalculé » de 2016 à 2022 (conformités jugées avec les anciennes
    limites, alors que la colonne `limitequal` donne la limite actuelle). Les fenêtres du score commencent le 01/09/2023, après le changement.

## E. PFAS (somme de 20)

11. **ARS Nouvelle-Aquitaine**, « Surveillance des PFAS (polluants chimiques éternels) dans l'eau en Nouvelle-Aquitaine », article du 12/05/2026.
    À partir du **1er janvier 2026**, l'intégration des 20 PFAS dans les programmes de contrôle sanitaire des ARS est obligatoire ;
    limite de qualité **0,1 µg/L pour la somme des 20 PFAS** ; textes cités : directive 2020/2184 (source 9) et décret n° 2025-1287 du 22/12/2025.
    https://www.nouvelle-aquitaine.ars.sante.fr/surveillance-des-pfas-polluants-chimiques-eternels-dans-leau-en-nouvelle-aquitaine [19/10/2026]

## F. Référentiels géographiques (`scripts/04_referentiels.py`, fichiers en cache dans `data/raw/ref/`)

12. **API Découpage administratif (geo.api.gouv.fr)**, Etalab / DINUM, Licence Ouverte 2.0 : communes actuelles (code INSEE, nom,
    département, région, population, centre), communes associées ou déléguées (ancien code vers commune actuelle), départements, régions.
    https://geo.api.gouv.fr/communes?fields=code,nom,codeDepartement,codeRegion,population,centre&format=json ;
    https://geo.api.gouv.fr/communes_associees_deleguees ; https://geo.api.gouv.fr/departements ; https://geo.api.gouv.fr/regions [19/10/2026]
13. **Contours administratifs 2025 (Etalab)**, départements simplifiés à 1 km, GeoJSON, Licence Ouverte 2.0.
    https://etalab-datasets.geo.data.gouv.fr/contours-administratifs/2025/geojson/departements-1000m.geojson [19/10/2026]
14. **INSEE, grille communale de densité** (grille 2025, géographie au 01/01/2026, mise en ligne le 15/05/2026) : urbain dense,
    urbain intermédiaire, rural (3 niveaux) et 7 niveaux. https://www.insee.fr/fr/information/8571524 ;
    fichier https://www.insee.fr/fr/statistiques/fichier/8571524/fichier_diffusion_2026.xlsx [19/10/2026]
15. **Cerema, « Application des dispositions d'urbanisme de la loi Montagne en France métropolitaine »**, tableau des communes 2019
    (totalité ou partie), Licence Ouverte 2.0, mis à jour le 18/11/2024.
    https://www.data.gouv.fr/datasets/673319c4104ba60b2030ed4d ; fichier
    https://static.data.gouv.fr/resources/application-des-dispositions-durbanisme-de-la-loi-montagne-en-france-metropolitaine/20241112-091136/l-commune-loimontagne85-000-2019-.csv [19/10/2026]
    Les codes 2019 fusionnés depuis sont rattachés à leur commune actuelle via la source 12 (une commune est « montagne » si l'une de ses
    parties l'est).
16. **Communes littorales (loi Littoral)** : la liste nationale référencée sur data.gouv.fr (« Communes de la loi littoral », fichier de
    l'Observatoire des territoires) renvoie une erreur 404 le 19/10/2026. **Repli documenté du cahier des charges, validé par Florian** :
    « littoral méditerranéen » = communes des départements 06, 11, 13, 30, 34, 66, 83, 2A et 2B non classées montagne. C'est une
    approximation (elle inclut des communes de l'arrière-pays), présentée comme telle dans l'app.

## G. Outils et polices

17. **Polices** de l'interface : Fraunces, IBM Plex Sans et IBM Plex Mono, servies par Google Fonts sous licence SIL Open Font License 1.1.
    https://fonts.google.com/specimen/Fraunces ; https://fonts.google.com/specimen/IBM+Plex+Sans [19/10/2026]
    Pour le rapport PDF, les fichiers TTF sont copiés dans `assets/fonts/` avec leurs licences (`OFL-Plex.txt`, `OFL-Fraunces.txt`),
    ce que la licence OFL autorise : IBM Plex Sans (Regular, SemiBold, Italic) et IBM Plex Mono Regular depuis le dépôt officiel
    https://github.com/IBM/plex (dossier `packages/*/fonts/complete/ttf`), Fraunces 72pt SemiBold depuis https://github.com/undercasetype/Fraunces
    (dossier `fonts/ttf`) [20/10/2026].
    Bibliothèque PDF : **fpdf2** 2.8.9 (licence LGPL v3), https://py-pdf.github.io/fpdf2/ : Python pur (dépendances fontTools, defusedxml,
    Pillow), donc installable sur Streamlit Community Cloud sans paquet système ; polices TrueType Unicode pour les accents.

## H. Fiches des paramètres (page « Lire une analyse d'eau »), vérifiées le 20/10/2026

18. **Anses**, « Pesticides dans l'eau du robinet », 22/05/2024. La limite de 0,1 µg/L est « un indicateur de qualité » qui « ne constitue en
    aucun cas un seuil de risque pour la santé », car elle « n'est pas élaborée sur la base de la toxicité des substances » ; total des
    pesticides et métabolites pertinents limité à 0,5 µg/L ; valeurs sanitaires maximales (Vmax) établies par l'Anses ; 0,9 µg/L pour les
    métabolites non pertinents. https://www.anses.fr/fr/content/pesticides-dans-eau-du-robinet [20/10/2026]
19. **ARS Hauts-de-France**, « Métabolites de la chloridazone dans l'eau du robinet : les réponses aux questions les plus fréquentes », 03/06/2026.
    Herbicide utilisé principalement sur la betterave, interdit depuis fin 2020 ; métabolites classés pertinents par défaut en avril 2020 faute
    d'études suffisantes ; Vmax fixées par l'Anses en juillet 2024 : 11 µg/L (desphényl) et 110 µg/L (méthyl desphényl) ; 0,1 µg/L est une
    limite environnementale, pas sanitaire.
    https://www.hauts-de-france.ars.sante.fr/metabolites-de-la-chloridazone-dans-leau-du-robinet-les-reponses-aux-questions-les-plus-frequentes [20/10/2026]
20. **ARS Grand Est**, « Eaux potables & pesticides : foire aux questions ». S-métolachlore : « herbicide encore autorisé, notamment utilisé pour
    le maïs » ; chloridazone : herbicide interdit depuis 2020, utilisé pour la betterave ; définition d'un métabolite pertinent selon la
    directive 2020/2184. https://www.grand-est.ars.sante.fr/media/97663/download [20/10/2026]
21. **Anses**, « Emerging pollutants in drinking water: review of the main findings of the latest national campaign », 06/04/2023. Chlorothalonil
    R471811 trouvé dans plus de la moitié des prélèvements, au-dessus de 0,1 µg/L dans plus d'un sur trois ; ESA-métolachlore mesuré dans plus
    de la moitié, moins de 2 % au-dessus de 0,9 µg/L.
    https://www.anses.fr/en/content/emerging-pollutants-drinking-water-review-main-findings-latest-national-campaign [20/10/2026]
22. **ARS Centre-Val de Loire**, « La qualité de l'eau potable en 2024 » : métabolites de l'atrazine (« herbicide interdit d'usage depuis 2003 »)
    et de la chloridazone (interdite en 2020) ; R471811 responsable de 87,5 % des dépassements récurrents de la région en 2024.
    https://centre-val-de-loire.ars.sante.fr/media/146900/download [20/10/2026]
23. **OMS**, « Nitrate and Nitrite in Drinking-water », document de référence des lignes directrices, WHO/FWC/WSH/16.52, 2016. Valeur guide de
    50 mg/L, protectrice des nourrissons nourris au biberon, fondée sur l'absence de méthémoglobinémie et d'effets thyroïdiens sous 50 mg/L dans
    les études épidémiologiques ; sources : activités agricoles (engrais, fumier), traitement des eaux usées, rejets industriels.
    https://cdn.who.int/media/docs/default-source/wash-documents/wash-chemicals/nitrate-nitrite-background-jan17.pdf [20/10/2026]
24. **ARS Normandie et préfet de l'Eure**, communiqué du 25/07/2024 : limite de 50 mg/L « fondée sur une recommandation de l'Organisation
    Mondiale de la Santé » ; au-dessus, l'eau ne doit pas être consommée par les femmes enceintes et les nourrissons, les autres peuvent la boire.
    https://www.normandie.ars.sante.fr/media/127448/download [20/10/2026]
25. **OMS**, fiche « Lead poisoning », 10/06/2026 : aucun niveau d'exposition connu sans effet nocif ; atteinte possible et durable du
    développement cérébral des enfants ; contamination de l'eau par les canalisations, soudures et raccords en plomb.
    https://www.who.int/news-room/fact-sheets/detail/lead-poisoning-and-health [20/10/2026]
26. **ARS Pays de la Loire**, « L'eau et le plomb dans des logements anciens / dégradés », 06/05/2026 : plomb venant surtout des branchements et
    réseaux intérieurs des immeubles ; limite de 10 µg/L au robinet, 5 µg/L à partir de janvier 2036 ; laisser couler l'eau froide 1 à 2 minutes,
    eau froide seulement pour l'alimentation, eau en bouteille préférable pour nourrissons et femmes enceintes.
    https://www.pays-de-la-loire.ars.sante.fr/eau-plomb-dans-logements-anciens-degrades [20/10/2026]
27. **OMS**, fiche « Arsenic », 07/12/2022 : présent naturellement à des niveaux élevés dans les eaux souterraines de certains pays ; lésions et
    cancers de la peau, cancers de la vessie et du poumon en exposition prolongée ; valeur guide de 10 µg/L, provisoire à cause des difficultés
    pratiques d'élimination. https://www.who.int/news-room/fact-sheets/detail/arsenic [20/10/2026]
28. **ARS Occitanie sur Santé.fr**, « Le chlorure de vinyle monomère (CVM) », 09/01/2024 : produit de synthèse servant à fabriquer le PVC ;
    dégradation lente des canalisations en PVC fabriquées avant 1980 ; limite de 0,5 µg/L ; purges en urgence, remplacement des conduites,
    consignes aux consommateurs. https://www.sante.fr/node/7609835 [20/10/2026]
29. **ARS Nouvelle-Aquitaine**, « Guide méthodologique : chlorure de vinyle monomère (CVM) dans les eaux destinées à la consommation humaine »,
    avril 2021 : cancérogène certain pour l'homme selon le CIRC depuis 1987, sur la base d'expositions professionnelles par inhalation à fortes
    doses ; cancers du foie. https://www.nouvelle-aquitaine.ars.sante.fr/media/133978/download [20/10/2026]
30. **OMS**, fiche chimique « Trihalomethanes », chemical fact sheets 2022 : le CIRC classe le chloroforme cancérogène possible (groupe 2B).
    https://cdn.who.int/media/docs/default-source/wash-documents/water-safety-and-quality/chemical-fact-sheets-2022/trihalomethanes-fact-sheet-2022.pdf [20/10/2026]
31. **Afssa (devenue Anses)**, avis 2004-SA-0070 sur les trihalométhanes : formation par réaction du chlore avec la matière organique naturelle ;
    associations épidémiologiques avec le cancer de la vessie dès 50 µg/L, sans causalité démontrée ; limite de 100 µg/L pour le total.
    https://www.anses.fr/fr/system/files/RCCP2004sa0070.pdf [20/10/2026]
32. **ARS Guadeloupe**, « Présence de bromates dans l'eau potable à Saint-Barthélemy : questions / réponses », 21/08/2018 : formés par oxydation
    des bromures pendant la désinfection ou venant d'impuretés du désinfectant chloré ; tumeurs chez le rat ; bromate de potassium classé
    cancérogène probable par l'Union européenne et l'OMS ; limite de 10 µg/L.
    https://www.guadeloupe.ars.sante.fr/system/files/2018-08/1808_QR_bromates%20V5%20stabilis%C3%A9.pdf [20/10/2026]
33. **ARS Occitanie**, « La bactériologie », 04/02/2026 : E. coli et entérocoques, témoins d'une contamination fécale ; absence exigée dans
    100 mL ; symptômes le plus souvent de type gastro-entérite ; coliformes et germes aérobies non dangereux en eux-mêmes, témoins de l'entretien
    et de la désinfection ; interdiction de consommer en cas de risque. https://www.occitanie.ars.sante.fr/la-bacteriologie [20/10/2026]
34. **ARS Normandie**, « Le contrôle de la qualité de l'eau », 12/10/2026 : limites (effets possibles sur la santé) et références (« sans
    incidence directe sur la santé », par exemple couleur ou fer) ; turbidité : 1 NFU en sortie de traitement pour les eaux superficielles,
    2 NFU au robinet ; coliformes et bactéries sulfito-réductrices en références.
    https://www.normandie.ars.sante.fr/le-controle-de-la-qualite-de-leau [20/10/2026]
35. **Afssa (devenue Anses)**, fiche « Aluminium », janvier 2005 : référence de qualité de 200 µg/L, indicateur d'efficacité du traitement ;
    origine naturelle ou sels d'aluminium utilisés pour la coagulation. https://www.anses.fr/fr/system/files/EAUX-Fi-AluminiumJanvier05.pdf [20/10/2026]
36. **Anses**, avis du 20/04/2018 (saisine 2016-SA-0203) relatif à une valeur sanitaire maximale pour le manganèse : référence de 50 µg/L « pour
    des raisons organoleptiques et esthétiques » ; perceptible par le consommateur au-delà de 20 µg/L ; effets neurotoxiques étudiés.
    https://www.anses.fr/en/system/files/EAUX2016SA0203.pdf [20/10/2026]
37. **ARS Île-de-France**, « Alimentation en eau potable : l'information sur la qualité de l'eau du robinet », 18/12/2025 : « Une eau calcaire
    n'a aucune incidence pour la santé » ; nitrates entre 50 et 100 mg/L : consommation restreinte pour femmes enceintes et nourrissons.
    https://www.iledefrance.ars.sante.fr/alimentation-en-eau-potable-linformation-sur-la-qualite-de-leau-du-robinet [20/10/2026]
38. **ARS Hauts-de-France**, « Les PFAS en 3 questions clés », 07/02/2025 : utilisés depuis les années 1950 ; « polluants éternels » car ils se
    dégradent très peu ; quatre effets fréquemment cités : moindre réponse immunitaire aux vaccins, cholestérol ou triglycérides élevés, baisse
    du poids de naissance, risque accru de cancer du rein. https://www.hauts-de-france.ars.sante.fr/les-pfas-en-3-questions-cles [20/10/2026]
39. **ARS Hauts-de-France**, « PFAS : contrôle de l'eau potable », 28/04/2026 : en cas de dépassement, mesures correctives, information des
    usagers, du maire, du préfet et de l'ARS, nouvelles analyses. https://www.hauts-de-france.ars.sante.fr/pfas-controle-de-leau-potable [20/10/2026]

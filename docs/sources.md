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

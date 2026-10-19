# Sources

Toute valeur affichée dans l'app est soit calculée depuis les données, soit appuyée sur une source de cette liste.
Date de consultation indiquée entre crochets.

## Données

1. **Jeu de données principal** — Ministère des Solidarités et de la Santé, « Résultats du contrôle sanitaire de l'eau distribuée
   commune par commune », data.gouv.fr, Licence Ouverte / Open Licence 2.0, dernière mise à jour le 05/10/2026.
   https://www.data.gouv.fr/datasets/resultats-du-controle-sanitaire-de-leau-distribuee-commune-par-commune [19/10/2026]
   - Liste des fichiers (tailles, SHA1) : https://www.data.gouv.fr/api/1/datasets/resultats-du-controle-sanitaire-de-leau-distribuee-commune-par-commune/
2. **Documentation du producteur** — « Description des fichiers — Résultats du contrôle sanitaire de l'eau distribuée, commune par commune »,
   version 7 du 03/09/2021 (copie : `docs/eau-distrib-documentation.pdf`).
   https://www.data.gouv.fr/api/1/datasets/r/36afc708-42dc-4a89-b039-7fde6bcc83d8 [19/10/2026]
   - Utilisé pour : définitions (UDI, limites vs références de qualité), table de traduction `rqana` → `valtraduite`,
     valeurs des indicateurs de conformité, « l'eau du robinet est l'aliment le plus contrôlé », « plus de 300 000 prélèvements
     et de l'ordre de 12 millions d'analyses par an ».

## Métabolites de pesticides « non pertinents » (insight H3 : ce qu'on mesure, et la façon de le classer, change ce qu'on trouve)

3. **Assemblée nationale, question écrite n° 2237 (16e législature)**, « Eau potable — ANSES », question publiée au JO le 18/10/2022,
   réponse du Gouvernement publiée au JO le 28/03/2023.
   https://questions.assemblee-nationale.fr/dyn/16/questions/QANR5L16QE2237.pdf [19/10/2026]
   - L'Anses a publié le **30/09/2022** deux avis classant les métabolites **ESA et NOA du S-métolachlore** « non pertinents » dans les EDCH.
   - Le décret n° 2022-1720 du 29/12/2022 introduit la notion de **valeur indicative** (art. R. 1321-3-1 du code de la santé publique) ;
     l'arrêté du 11/01/2007 modifié la fixe à **0,9 µg/L** pour les métabolites de pesticides non pertinents.
   - En 2021, ces deux métabolites étaient responsables de la non-conformité de plus de 900 UDI desservant près de 4 millions d'habitants
     (chiffre du ministère cité dans la réponse — à citer comme tel, pas recalculé).
4. **ARS Hauts-de-France, « Les métabolites du chlorothalonil »**, page mise à jour le 12/03/2025.
   https://www.hauts-de-france.ars.sante.fr/les-metabolites-du-chlorothalonil-0 [19/10/2026]
   - Chlorothalonil **R471811** jugé pertinent en 2023 (limite 0,1 µg/L) ; **non pertinent depuis l'avis Anses du 29/04/2024**.
   - Valeur indicative 0,9 µg/L : son dépassement **n'empêche pas de consommer l'eau** mais impose un **plan d'actions** à la personne
     responsable de la production / distribution d'eau (PRPDE).
5. **ARS Bourgogne-Franche-Comté**, « Informations complémentaires sur le contenu des infofactures 2023 concernant le paramètre pesticides —
   Évaluation sanitaire du métabolite Chlorothalonil R471811 », Dijon, 24/07/2024.
   https://bourgogne-franche-comte.ars.sante.fr/media/127554/download [19/10/2026]
   - Confirme : R471811 pertinent en 2023, classé non pertinent par l'avis Anses du 29/04/2024 ; depuis, valeur indicative de 0,9 µg/L.

## À sourcer (ne pas afficher dans l'app sans source)

- Limite de qualité du **sélénium** : les conclusions ARS 2016–2022 citent 10 µg/L, la colonne `limitequal` affiche 20 µg/L pour toutes
  les années (et 30 µg/L « si conditions géologiques particulières » depuis 2023). Hypothèse : relèvement lors de la transposition de la
  directive (UE) 2020/2184. Même question pour l'**antimoine**.

## Référentiels géographiques (`scripts/04_referentiels.py`, fichiers en cache dans `data/raw/ref/`)

6. **API Découpage administratif (geo.api.gouv.fr)** — Etalab / DINUM, Licence Ouverte 2.0 : communes actuelles (code INSEE, nom,
   département, région, population, centre), communes associées/déléguées (code → commune actuelle), départements, régions.
   https://geo.api.gouv.fr/communes?fields=code,nom,codeDepartement,codeRegion,population,centre&format=json ·
   https://geo.api.gouv.fr/communes_associees_deleguees · https://geo.api.gouv.fr/departements · https://geo.api.gouv.fr/regions [19/10/2026]
7. **Contours administratifs 2025 (Etalab)**, départements simplifiés à 1 km, GeoJSON, Licence Ouverte 2.0.
   https://etalab-datasets.geo.data.gouv.fr/contours-administratifs/2025/geojson/departements-1000m.geojson [19/10/2026]
8. **INSEE, grille communale de densité** (grille 2025, géographie au 01/01/2026, mise en ligne le 15/05/2026) : urbain dense /
   urbain intermédiaire / rural (3 niveaux) et 7 niveaux. https://www.insee.fr/fr/information/8571524 —
   fichier https://www.insee.fr/fr/statistiques/fichier/8571524/fichier_diffusion_2026.xlsx [19/10/2026]
9. **Cerema, « Application des dispositions d'urbanisme de la loi Montagne en France métropolitaine »**, tableau des communes 2019
   (totalité / partie), Licence Ouverte 2.0, mis à jour le 18/11/2024.
   https://www.data.gouv.fr/datasets/673319c4104ba60b2030ed4d — fichier
   https://static.data.gouv.fr/resources/application-des-dispositions-durbanisme-de-la-loi-montagne-en-france-metropolitaine/20241112-091136/l-commune-loimontagne85-000-2019-.csv [19/10/2026]
   - Codes 2019 fusionnés depuis : rattachés à leur commune actuelle via la source 6 (une commune est « montagne » si l'une de ses parties l'est).
10. **Communes littorales (loi Littoral)** : la liste nationale référencée sur data.gouv.fr (« Communes de la loi littoral »,
    fichier de l'Observatoire des territoires) renvoie une erreur 404 le 19/10/2026. **Repli documenté du cahier des charges** :
    « départements côtiers méditerranéens » = communes des départements 06, 11, 13, 30, 34, 66, 83, 2A, 2B non classées montagne.
    C'est une approximation (elle inclut des communes de l'arrière-pays) : à dire dans l'app.

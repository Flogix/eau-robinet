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

## Référentiels géographiques

*À compléter en phase 2 (`scripts/04_referentiels.py`).*

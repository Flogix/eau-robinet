# AVANCEMENT : « Is my tap water good? »

Journal du projet (mémoire entre sessions). Le plus récent en haut de chaque section.
Rendu : **samedi 24/10/2026 à 12:00**, 1re remise visée jeudi 22 au soir.

## État actuel

| Phase | Statut | Date |
|---|---|---|
| 0. Reconnaissance (lecture seule) | ✅ validée | 19/10 |
| 1. Setup | ✅ terminée (commit `0f7ab0b`) | 19/10 |
| 2. Pipeline | ✅ validée | 19/10 |
| 3. Score | ✅ validée (k = 5) | 19/10 |
| 4. App | ✅ déployée : https://eau-robinet.streamlit.app/ | 19/10 |
| 5. Finitions | ✅ terminée (score personnalisé, rapport PDF, vérification complète) | 20/10 |
| 6. Livraison | 🟡 livrables prêts (README, storyboard, zip ; script vidéo gardé en local) ; reste la vidéo à enregistrer et la remise | 20/10 |
| Session 5 | ✅ A, B, C, D, E faits : LinkedIn, page « Explorer les données », audit complet, push, vérification en ligne, zip | 20/10 |
| Session 6 | ✅ doublon retiré, F (filtres masqués), G (PDF de comparaison), H (en-tête de la barre latérale), I (conclusions en 2e), E refaite | 20/10 |
| Session 7 | ✅ en-tête (logos selon le thème), retours de l'utilisateur test (2a à 2g), chiffres harmonisés, tests, push, vérification en ligne, zip | 20/10 |
| 7. Bonus bouteille | hors périmètre (accord de Florian requis) |, |

**Pour reprendre** : `make data` / `.\make.ps1 data` reconstruit tout ; chaque étape reprend là où elle s'est arrêtée
(voir « Reprise » ci-dessous). Traitements longs : `.\scripts\run_logged.ps1 <script>` (arrière-plan, priorité basse,
journal dans `data/interim/logs/`).

## Environnement (mesuré le 19/10/2026)

- Windows 11, 16 cœurs logiques, RAM 15,7 Go (**≈ 4 Go libres seulement**), disque C: 117 Go libres avant le pipeline (`data/interim/` en occupe 2,9 Go).
- Python 3.12.9 dans `.venv` ; versions épinglées dans `requirements.txt` (streamlit 1.66.0, pandas 3.0.6, duckdb 1.5.6,
  pyarrow 26.0.0, plotly 7.1.0, requests 2.34.2, pytest 9.1.1, openpyxl 3.1.5, numpy 2.5.4).
- DuckDB : **`memory_limit=3GB`, `threads=4`** (dans `config.py`), `temp_directory=data/interim/duckdb_tmp`.
- `C:\.git` supprimé par Florian le 19/10 ; le dépôt du projet est autonome (`git init` dans le dossier du projet).
- Fichiers parasites de `data/raw/ref/` (`departements-100m.geojson`, `geo_arrondissements.json`) : **supprimés par Florian** (19/10).

## Phase 5 : Finitions, première passe (19/10/2026)
- App déployée par Florian sur Streamlit Community Cloud (Python 3.12) : https://eau-robinet.streamlit.app/, les 8 pages
  s'ouvrent en ligne sans erreur, en 2,6 à 4,8 s (chargement complet).
- Accueil : encadré « pour qui / quelles questions » avec la page qui répond à chacune (critère narratif du barème).
- KPIs : étiquettes courtes (plus de troncature sur écran étroit), aides détaillées.
- Phrases-titres revues (Comprendre, nitrates = « moitié de la limite (25 mg/L) »), nombre de résultats calculé.
- Thème : l'app suit le réglage clair/sombre du lecteur ; vérifié en sombre → corrigés : ligne noire invisible (devenue gris moyen),
  fond blanc de la carte (transparent), aiguille de la jauge, ordre des sous-scores, « None » dans les quartiers.
- Robustesse : tests des 8 pages avec des filtres extrêmes (Mayotte + PFAS + 2026 seule, Corse 2016, Guyane…) et recherche
  d'homonymes ; un plantage trouvé et corrigé (saisonnalité sans année complète). **153 tests verts.**

## Phase 4 : App, version 1 (19/10/2026)

### Fait
- 8 pages en anglais dans l'ordre du storyboard ; sidebar globale (`utils/filters.py`) : période, région, famille de paramètres,
  type de commune, chaque filtre a un `help=` qui dit ce qu'il change.
- KPIs liés aux filtres (`utils/metrics.render_kpis`, accueil + carte) : % de prélèvements conformes bactério / chimie avec delta
  vs l'année précédente, communes avec ≥ 1 non-conformité (+ population, borne haute), score médian.
- Graphes Plotly interactifs avec infobulles, texte alternatif (`alt=`) + `st.caption` sous chaque graphe, phrases-titres calculées.
- Carte des départements (choroplèthe : famille × période, ou score actuel), classements, histogramme des scores, tendances.
- Ma commune : recherche sans accents + homonymes (département), jauge, sous-scores, rapport « pourquoi » par réseau, historique
  d'un paramètre avec seuil (requête DuckDB ciblée sur `udi_param_year`, jamais chargé en entier). Lien partageable `?insee=`.
- Comparer : Paris vs Villejuif par défaut (2 à 4 communes), groupes montagne / Méditerranée (approximation affichée) / urbain-rural /
  taille, en boîtes à moustaches.
- Plongées : **H3 en tête** (barres empilées des dépassements par groupe de paramètres + non-conformités officielles, dates des
  reclassements Anses sourcées), nitrates, PFAS, saisonnalité bactério, dureté (H4), sliders what-if des poids, table de sensibilité.
- Qualité des données : manquants (heatmap), statuts des résultats, officiel vs recalculé, couverture, 88 contrôles, biais et limites.
- Conclusions : H1–H4 testées et chiffrées (H1 : réseaux < 12 prélèvements/an = 73 % des non-conformités bactério pour 26 % des
  prélèvements ; H2 : ρ = 0,05 entre départements bactério et chimie ; H3 ; H4 : dureté 1 à 36 °f entre P5 et P95).
- `scripts/06_build_app_tables.py` → `dept_family_year` (28 Ko). Tests : 148 verts, y compris depuis un clone propre sans données brutes.
- Mémoire de l'app : 874 Mo → **507 Mo** (catégories + 32 bits pour les grosses tables, `st.cache_resource` sans copie).
  Chargement des pages : 2,8 à 4,6 s (rechargement complet du navigateur, en local).
- Repo public créé : https://github.com/Flogix/eau-robinet (vérifié : rien de `data/raw`, `data/interim`, ni le PDF du prof).

## Phase 3 : Score (19/10/2026)

### Fait
- `utils/score.py` : formules (micro, pénalités chimie/confort, combinaison, note, confiance), score par UDI, score par commune
  (moyenne des UDI du dernier lien 2026, sinon 2025 ; pire UDI gardée), rapport « pourquoi » par règles. Tout en pandas sur
  `data/processed/` → les sliders what-if de l'app pourront recalculer sans données brutes.
- `scripts/03_build_aggregates.py` : nouvelle table `udi_param_p95` (P95 du ratio valeur/seuil par UDI × paramètre, ≥ 10 mesures),
  calculée en **8 paquets d'UDI** l'un après l'autre (≈ 5 s chacun, DuckDB 3 Go) ; 88/88 contrôles OK.
- `scripts/05_build_scores.py` (pandas seul, ≈ 3 min) : `udi_scores`, `commune_scores`, `score_validation`, `score_sensitivity`,
  `docs/score_witnesses.md`. Branché dans `Makefile` et `make.ps1`.
- Tests : `tests/test_score.py` (35 tests sur données synthétiques) ; suite complète **145 verts**.
- README : section méthode du score + validation + sensibilité. Ligne 38 corrigée (retour chariot invisible dans `.\scripts\run_logged.ps1`).

### Décisions (phase 3)
- Formule du cahier des charges gardée (k = 10, courbe 0,5/1/2 → 0/20/80, 0,25 × autres pénalités, plafond confort 50, poids 0,4/0,4/0,2).
- **P95 au lieu du max dès 10 mesures** (équité envers les grandes villes) **+ plancher** : tout dépassement mesuré compte au moins
  comme r = 1 (pénalité 20) → un dépassement n'est jamais effacé par le P95.
- **pH et conductivité** (références en plage min–max) et **références à 0** (coliformes, spores) : pénalité selon la **part des
  prélèvements hors référence**, 50 × (1 − (1 − t)^10). Raison : un pH de 8 pour un max de 9 n'est pas « presque en dépassement ».
- **Nitrates et « nitrates/50 + nitrites/3 »** : une seule pénalité (la pire), comme les codes jumeaux des métabolites.
- Score calculé seulement si la microbiologie OU la chimie est mesurée (le confort seul ne suffit pas).
- Confiance : élevée = 3 familles, ≥ 12 prélèvements bactériologiques en 12 mois, nitrates et pesticides mesurés en 36 mois ;
  faible = ≤ 3 prélèvements bactériologiques ou pas de micro ou pas de chimie ; moyenne sinon. Commune = la plus faible de ses UDI.
- Commune « petite rurale » témoin tirée au sort (graine 42) : < 500 hab., rural dispersé/très dispersé, métropole.
- Spearman calculé comme corrélation des rangs (pas de scipy ajouté).

### Chiffres clés (calculés)
- 23 733 UDI notées ; médiane 89,6 ; A 48,4 % · B 27,3 % · C 8,3 % · D 14,8 % · E 1,3 % ; confiance élevée 31 %, moyenne 56 %, faible 13 %.
- 34 826 communes notées sur 34 827 (25322 : aucune UDI avec données dans les fenêtres).
- Validation : UDI avec non-conformité bactério officielle (3 020) → score médian 52 contre 90 ; avec non-conformité chimique officielle
  (3 178) → sous-score chimie médian 19 contre 100 ; probabilité qu'une UDI non conforme ait un score plus bas : 0,95 (bactério), 0,85 (chimie).
- Sensibilité (14 variantes) : Spearman 0,85 (sans confort) à 0,998.
- Témoins : Paris 84,0 B · Villejuif 81,0 B · Chamonix 78,7 B · Sète 100 A · Fouchères (89) 95,0 A.

### Petits réseaux (décision de Florian à la validation de la phase 3)
- Constat : avec k = 10, 1 non-conformité sur 5 prélèvements → t = 20 % → micro ≈ 11 → souvent note D (pic de 14,8 % de D).
- Options présentées : garder k = 10 ; **k = 5** ; lissage (12 prélèvements fictifs au taux national : D 11,4 % mais A 34,7 %).
- **Choix : k = 5** (aussi utilisé pour la pénalité « part hors référence » du confort). La note est calculée sur le score
  **arrondi à 0,1** (valeur affichée) : un score affiché 60,0 n'est jamais noté D.
- Après recalcul : UDI A 50,4 % · B 26,7 % · C 10,8 % · D 11,2 % · E 0,9 % (médiane 90,0) ; communes A 47,2 % · B 27,6 % ·
  C 12,7 % · D 12,2 % · E 0,4 % (médiane 89,1). Validation : score médian 61 (non-conformité bactério officielle) contre 90 ;
  chimie 19 contre 100 ; probabilités 0,91 et 0,88. Sensibilité : Spearman 0,95 à 0,998 (0,86 sans confort).
- Témoins : Paris 84,1 B · Villejuif 81,1 B · Chamonix 83,1 B (Le Tour passe de D à C 70,5) · Sète 100 A · Fouchères 95,0 A.

## Phase 2 : Pipeline (19/10/2026)

### Fait
- `scripts/01_download.py` : liste l'API data.gouv.fr, compare taille + SHA1 (cache des empreintes), télécharge seulement ce
  qui manque, n'écrase jamais un fichier existant (option `--update` : nouvelle version enregistrée à côté). Résultat : 11/11 à jour.
  Écrit `data/processed/source_manifest.json`.
- `scripts/02_build_parquet.py` : une année à la fois → extraction dans `data/interim/extract/`, Parquet brut (contrôle lignes lues =
  lignes du fichier), puis tables propres `data/interim/clean/{plv,result,com_udi}` :
  PLV clé (prélèvement, UDI) ; RESULT une ligne par (prélèvement, paramètre), **mesure labo gardée** si terrain + labo ;
  valeurs parsées (statut, valeur, LQ), limites/références parsées (bornes, unité normalisée) ; COM_UDI sans doublons.
  Durée : 590 s pour les 11 années.
- `scripts/03_build_aggregates.py` : catalogue des paramètres et familles ; jointure résultats × prélèvements par année
  (`data/interim/joined/`, 1,7 Go) avec **le seuil applicable à chaque ligne** (limite / valeur indicative 0,9 µg/L / référence) ;
  agrégats et tables de qualité dans `data/processed/` ; **84 contrôles automatiques, 84 OK**. Durée : 692 s (1er passage), 65 s si tout est en cache.
- `scripts/04_referentiels.py` : communes (population, centre, département, région), anciennes communes → commune actuelle,
  grille de densité INSEE, loi Montagne, contours des départements (1 km) → `dim_communes`, `dim_departements`, `departements.geojson`.
- Règles de dépassement en macros SQL testées (`utils/prep.py`) ; tests : **106 verts** (parsing, seuils, familles, tables produites, pages).
- App relancée : les 8 pages s'ouvrent sans erreur.

### Incident et précautions (19/10)
- L'app Claude a figé pendant le 1er passage du script 03 (RAM saturée : DuckDB réglé à 4 Go sur une machine à ≈ 4 Go libres,
  agrégats `count(DISTINCT)` et P95 exacts sur 190 M lignes). Le script était en fait allé au bout (83/83 contrôles).
- Corrections : `memory_limit=3GB`, `threads=4` ; agrégats lourds **une année à la fois** ; comptages distincts remplacés par une
  **agrégation en deux temps** (par prélèvement, puis par UDI) ; P95 retiré des agrégats (voir décisions).
- **Reprise** : 02 saute les années déjà construites (`build_state.json`) ; 03 saute chaque table déjà construite par la même requête
  avec des entrées inchangées (tampons dans `data/interim/stamps/`), y compris chaque année des tables partielles
  (`data/interim/parts/`) ; 04 garde ses téléchargements en cache. Vérifié : 2e passage de 03 = tout en cache.
- Lanceur `scripts/run_logged.ps1` : arrière-plan, priorité basse, journal horodaté.

### Chiffres clés (calculés)
- `data/processed/` : **49,6 Mo, 25 fichiers**, plus gros fichier 22,9 Mo (`udi_param_year`). `data/interim/` : 2,9 Go (non versionné).
- 1 789 paramètres : 916 chimie (dont 838 pesticides et métabolites), 50 confort/indicateurs (dont 6 codes de métabolites non pertinents),
  6 microbiologie, 817 information (sans seuil ou qualitatifs).
- Statuts des résultats (une ligne par prélèvement × paramètre) : 87,9 M non quantifiés (< LQ), 33,1 M quantifiés, 10,1 M qualitatifs,
  0,93 M non mesurés (exclus), 98 519 vides, 11 734 illisibles.
- Fenêtres « situation actuelle » : 23 089 UDI avec un prélèvement entre le 01/09/2025 et le 31/08/2026 ; 23 720 UDI avec de la chimie
  entre le 01/09/2023 et le 31/08/2026.
- Référentiels : 34 812 communes en 2026, toutes avec une population ; 5 494 communes de montagne ; 1 219 communes des départements
  méditerranéens hors montagne ; 104 anciens codes (fusions), dont 87 rattachés à leur commune actuelle.

### Écart chimie officielle vs recalculée (expliqué)
| Période | Officiel N sans dépassement recalculé | Dépassement recalculé, officiellement C ou D |
|---|---|---|
| 2016–2022 | 253 à 674 / an | 732 à 783 / an |
| 2023–2026 | 2 à 12 / an | 452, 671, 869, 707, dont 438, 669, 869, 707 sous **dérogation (D)** |
- **Dérogations** : « D » = conforme officiellement malgré un dépassement, sous dérogation préfectorale → explique presque tout depuis 2023.
- **Chlorites (2016–2022)** : 3 893 prélèvements au-dessus de 0,25 mg/L (limite écrite sur la ligne) mais conformes ; 3 688 (95 %)
  sont ≤ 0,7 mg/L, la limite du code « chlorites en cas de traitement pouvant en générer » (`CLITE_T`). L'effet disparaît en 2023 (8 cas).
- **Sélénium et antimoine (2016–2022)** : la majorité des « N officiel sans dépassement » ; valeurs médianes 14–15 µg/L sous la limite
  de 20 µg/L écrite sur la ligne, alors que **les conclusions de l'ARS citent une limite de 10 µg/L** (1 627 conclusions mentionnent le
  sélénium). Les conformités ont été jugées avec la limite de l'époque, la colonne `limitequal` montre la limite actuelle.
  **Sourcé le 19/10** (`docs/sources.md` n° 10–12) : directive 98/83/CE Sb 5 / Se 10 µg/L → directive (UE) 2020/2184 Sb 10 / Se 20 µg/L
  (30 µg/L si géologie), transposée par l'arrêté du 30/12/2022, en vigueur le 01/01/2023.
- Bactériologie : recalcul = officiel (ex. 2025 : 4 659 / 4 659).
- Conséquence : l'app s'appuie sur les **conformités officielles** pour les KPIs historiques ; le recalcul sert au score (fenêtres
  2023–2026, où l'accord est quasi parfait) et à la page qualité des données.

### Décisions (phase 2)
- Familles de paramètres : règles dans `utils/prep.py` (unité microbio, valeur de la limite, listes de codes explicites pour les
  nitrates, métaux, sous-produits de désinfection, PFAS, cyanotoxines ; non-pesticides à 0,1 µg/L listés à part).
- P95 retiré des agrégats annuels (trop coûteux en mémoire) : il sera calculé en phase 3 seulement pour les UDI × paramètres
  chimiques avec ≥ 10 mesures dans la fenêtre de 36 mois.
- 32 paramètres clés suivis par UDI et par an (`udi_param_year`, codes jumeaux fusionnés) ; chlore libre, température, pH et
  conductivité retirés de cette table (mesurés partout, peu utiles au récit, ≈ 1 M lignes).
- Valeurs agrégées stockées en float32 (7 chiffres significatifs) pour tenir le budget de taille.
- Littoral : liste nationale loi Littoral introuvable (lien mort) → repli « départements côtiers méditerranéens hors montagne ».
- Anciens codes communes : pas de population (évite le double comptage avec la commune actuelle).
- Métabolites non pertinents, contrôle `dq_metabolites` : le producteur bascule vers les codes sans limite au moment des avis Anses ;
  restent 587 lignes R471811 avec limite après le 29/04/2024 (on garde la limite de la ligne, règle a) et 262 lignes 471811R sans limite
  avant cette date (valeur indicative appliquée).

## Phase 1 : Setup (19/10/2026)
- `.gitignore` (data/raw, data/interim, .venv…) créé **avant** le `git init` ; `.gitattributes` (fins de ligne LF, sinon le Makefile casse sous Linux).
- `requirements.txt` épinglé, `Makefile` + `make.ps1` (PowerShell sans make), `config.py`, `app.py` avec `st.navigation`,
  8 pages squelettes, `utils/` (io, prep, score, viz), tests, README squelette, `docs/sources.md`.

## Phase 0 : Reconnaissance (19/10/2026)

### Fait
- Lecture complète de CLAUDE.md, du cahier des charges, des consignes et de la doc producteur (PDF v7, 16 p.).
- Vérification des 11 zips contre l'API data.gouv.fr : **tailles et SHA1 identiques** (et PDF de doc identique). Rien retéléchargé.
- Conversion des 33 fichiers texte (≈ 22 Go) en Parquet brut tout-texte dans `data/interim/raw_parquet/` (428 Mo, ≈ 4 min),
  une année à la fois, texte extrait supprimé après chaque fichier. `data/raw/` jamais modifié.
- Exploration DuckDB : schémas, volumétrie, clés, doublons, intégrité, formats des valeurs et limites, paramètres, thèmes.
- `docs/data_dictionary.md` rédigé (tous les chiffres viennent des requêtes de `scripts/explore/sql/`).

### Chiffres clés (mesurés)
- Années 2016 → 2026, **2026 partielle : prélèvements jusqu'au 31/08/2026**.
- 2 991 181 prélèvements distincts, 4 262 629 lignes PLV, **133 474 398 résultats d'analyse**, 1 789 codes paramètres,
  34 945 codes communes, 24 461 codes UDI.
- ≈ 270 000 à 295 000 prélèvements et 11,4 à 13,3 millions de résultats par année complète.
- 0 ligne rejetée, 0 doublon exact, en-têtes identiques sur 11 ans, intégrité PLV↔RESULT↔COM_UDI quasi parfaite.
- Recalcul « valeur > limite » vs conclusion officielle : bactério quasi identique (ex. 2025 : 4 659 = 4 659).
- Non-conformités chimiques officielles (prélèvements) : ≈ 5 600–7 000/an en 2016–2020 → ≈ 10 900–11 900/an en 2021–2024 → 8 742 en 2025.
  Ce saut coïncide avec de **nouveaux métabolites de pesticides** surveillés (ESA-métolachlore, chloridazone desphényl, chlorothalonil R471811).
- Somme de 20 PFAS : 122 prélèvements mesurés en 2022 → 16 475 en 2025 ; 386 au-dessus de 0,1 µg/L en 2025.

### Surprises / problèmes
1. `referenceprel` **n'est pas unique** dans PLV : un prélèvement fait en amont est recopié pour chaque UDI aval (×1,43 en moyenne).
2. Décimales mixtes : virgule dans `rqana`, point dans `valtraduite`, les deux dans `limitequal`/`refqual`.
3. Codes « jumeaux » : un même métabolite passe d'un code avec limite à un code sans limite (`ESAMTC`→`MTCESA`, `R471811`→`471811R`).
4. `N.M.` (non mesuré) : ≈ 0,94 M lignes à exclure. `libwebparametre` toujours vide.
5. Paris = un seul code INSEE `75056` (4 UDI, arrondissements dans le champ quartier) → la jointure avec geo.api.gouv.fr sera simple.
6. Pas de paramètre « microplastiques » dans les données.
7. Un même paramètre peut avoir plusieurs limites (nitrites 0,5 ou 0,1 mg/L) → utiliser la limite **de chaque ligne**.

### Décisions prises (phase 0)
- **Traiter toutes les années 2016–2026** : le plan B du cahier des charges est inutile (conversion complète en 4 min, 428 Mo).
- Garder la copie Parquet brute tout-texte dans `data/interim/` comme étape intermédiaire du pipeline (évite de relire 22 Go de texte).
- Clé paramètre = `cdparametresiseeaux` ; clé PLV par UDI = (`referenceprel`, `cdreseau`) ; stats nationales sur `referenceprel` dédoublonné.
- Scripts d'exploration conservés dans `scripts/explore/` (preuve et reproductibilité de la reconnaissance).

### Reste à faire / à vérifier plus tard
- ✅ Écart chimie recalculée vs officielle : expliqué en phase 2 (dérogations, chlorites, sélénium).
- ✅ Source officielle sur les métabolites non pertinents : fournie par Florian, vérifiée (`docs/sources.md`).
- ✅ Règle terrain vs labo : on garde la mesure de laboratoire (décision du 19/10).
- ✅ Évolution des limites sélénium/antimoine sourcée (EUR-Lex + Légifrance), 19/10.

## Journal des décisions
- 20/10, `docs/script_video.md` retiré du suivi git (choix de Florian) : gardé sur le disque, ajouté au `.gitignore`,
  historique non réécrit.
- 20/10, **Repo nettoyé avant la présentation** (choix de Florian) : `CLAUDE.md`, `docs/CAHIER_DES_CHARGES.md` et `.devcontainer/`
  retirés du suivi git (gardés sur le disque, ajoutés au `.gitignore`, historique non réécrit). Les mentions ci-dessous
  de ces documents sont l'historique du projet.
- 19/10, `docs/consignes.pdf` (sujet du prof, avec son e-mail) **retiré de l’historique git** avant la publication (choix de Florian),
  gardé sur le disque et ajouté au `.gitignore`. Les hash des commits ont changé (phase 1 = `0f7ab0b`).
- 19/10, **Phase 3 validée par Florian** : option k = 5 pour les petits réseaux, note sur score arrondi. Phases 4–5 enchaînées,
  repo GitHub public « eau-robinet » confirmé (création + push autorisés).
- 19/10, **Phase 2 validée par Florian.** Parasites de `data/raw/ref/` supprimés par lui. Littoral : repli « départements
  méditerranéens hors montagne » accepté, **à présenter clairement comme une approximation dans l'app**.
- 19/10, Sélénium/antimoine : piste de Florian vérifiée sur EUR-Lex et Légifrance → on peut en parler dans l'app (sources 10–12).
- 19/10, PFAS : « dans le contrôle de routine depuis le 01/01/2026 » sourcé (ARS Nouvelle-Aquitaine, décret 2025-1287 ; directive art. 25).
- 19/10, **Phase 0 validée par Florian.** Phases 1 et 2 enchaînées sans arrêt intermédiaire, sur toutes les années 2016–2026.
- 19/10, `C:\.git` supprimé par Florian ; vérifié : plus aucun dépôt parent détecté avant le `git init`.
- 19/10, Consignes renommées (pas copiées) en `docs/consignes.pdf`.
- 19/10, **Métabolites de pesticides** : on suit la limite inscrite sur chaque ligne (option a). En plus, les métabolites
  classés **non pertinents** par l'Anses sont traités comme une **référence à 0,9 µg/L** (valeur indicative), famille
  confort/vigilance, pénalité légère. Rapport : « ⚠️ » au-dessus de 0,9 µg/L, « ℹ️ » si détecté en dessous.
  Métabolites concernés (sources dans `docs/sources.md`) : ESA-métolachlore et NOA-métolachlore (avis Anses du 30/09/2022),
  chlorothalonil R471811 (avis Anses du 29/04/2024). Vérifié : `refqual` ne contient **jamais** 0,9 µg/L (0 ligne) →
  la règle est appliquée par nous. Règle de ligne : si la ligne porte une limite → la limite ; sinon, pour ces codes → référence 0,9 µg/L.
  Les autres métabolites sans limite dans les données (OXA-métolachlore, ESA/OXA-métazachlore, ESA-alachlore…) n'ont pas
  de source fournie → pas de pénalité, simple « ℹ️ » s'ils sont détectés.
- 19/10, 2026 : situation actuelle = fenêtres de 12 et 36 mois se terminant le 31/08/2026 ; évolutions sur 2016–2025 ;
  2026 montrée à part et marquée partielle.
- 19/10, Paramètre mesuré deux fois dans un prélèvement : on garde la mesure de **laboratoire**.
- 19/10, Microbiologie du score : calculée à partir de la **conformité officielle** par prélèvement (`plvconformitebacterio`).
- 19/10, Repo GitHub : `eau-robinet`, public. **Confirmation de Florian requise avant le premier push.**
- 19/10, Après le gel de l'app : DuckDB 3 Go / 4 threads, une année à la fois, traitements longs en arrière-plan avec journal,
  reprise étape par étape (demande de Florian).
- 19/10, Toutes les années traitées (pas de plan B). Raison : volumétrie maîtrisée grâce à DuckDB + Parquet.
- 19/10, `.venv` en Python 3.12.9 (version stable déjà installée ; même version à choisir sur Streamlit Community Cloud, à confirmer au déploiement).

## Session identité, écriture, accueil, ergonomie (19/10/2026, en cours)
- Fait : règles d'écriture dans CLAUDE.md ; direction visuelle A « Au robinet » (papier et encre, Fraunces + IBM Plex, palette validée daltonisme en clair et en sombre) ; module de traduction `utils/i18n.py` + `utils/texts/` (EN officiel, FR via le sélecteur, 559 clés, tests de complétude) ; accueil refait (OMS, Santé publique France, absence de chiffre officiel de décès dite honnêtement, méthode, H1 à H4, indicateurs expliqués) ; pages renommées ; recherche de commune en une seule liste (exemples Paris, Lyon, Marseille, Bordeaux, Lille) ; filtres grisés hors de leurs pages ; rapport « pourquoi » traduit avec étiquettes au lieu d'emojis ; pied de page et page À propos ; `docs/sources.md` renuméroté (sources 1 à 17), sans tiret cadratin ; H1 et H2 testées sur la carte. 167 tests verts avant les derniers ajustements.
- Terminé le 20/10 : 18 pages ouvertes (9 en anglais, 9 en français) sans erreur ; niveaux de densité INSEE 3 et 4 inversés corrigés ;
  accord du singulier dans les rapports (« 1 mesure sur 1 a dépassé ») ; tirets cadratins retirés du README, des docs et du code ;
  correctif `app.py` : les modules du projet modifiés depuis leur chargement sont rechargés (une `ImportError` apparaissait en ligne
  après un push, le serveur gardant l'ancienne version de `utils/i18n.py`).

## Session 2 : rendre l'app compréhensible (20/10/2026)
- **Lire une analyse d'eau** : moteur de recherche sur les 1 789 paramètres (liste unique filtrée pendant la frappe) ; **20 fiches**
  sourcées (ce que c'est, d'où ça vient, effets possibles sur la santé, seuil et pourquoi, en cas de dépassement), chacune avec
  « ce que disent les données » calculé ; pour les autres paramètres, les données brutes du catalogue et une phrase honnête.
  22 sources officielles ajoutées et vérifiées sur les pages primaires (`docs/sources.md`, sources 18 à 39 : Anses, OMS, ARS).
  Non trouvé et dit tel quel : valeur sanitaire récente de l'atrazine déséthyl ; conduite à tenir en France pour l'arsenic.
  Graphe des dépassements et tableau des seuils introduits et commentés.
- **L'eau de ma commune** : réseaux de distribution expliqués (pourquoi plusieurs, pourquoi ces noms) ; lecture de la jauge et des
  barres (ce qui doit inquiéter ou non) ; **6 formules en LaTeX**, chacune suivie d'une phrase ; texte généré « pourquoi ce score »
  (points perdus par famille et paramètre en cause) avec comparaison aux médianes nationale et départementale.
- **Carte** : la vue se choisit sur la page (score global, bactéries, chimie, confort, ou une famille sur la période) ; le filtre
  « famille » quitte la barre latérale ; texte calculé « ce que dit la carte » (départements et régions extrêmes, corrélation avec la
  part de petits réseaux) et hypothèses prudentes sourcées par vue.
- **Comparer** : texte généré qui explique l'écart entre la meilleure et la moins bonne commune (famille, paramètres en cause).
- **Plongées et Qualité des données** : sous chacun des 12 graphes, interprétation en trois temps (ce qu'on observe, pourquoi
  probablement avec sources, limites).
- **Conclusions** : chaque hypothèse rappelée, chiffrée, avec verdict et conclusion ; H3 chiffré avec et sans les trois familles de
  métabolites (6 177 → 7 592 dépassements sans elles, 6 676 → 20 769 au pic avec elles) ; implications pour un habitant et pour les
  collectivités (sources 11, 26, 33).
- Tests : **168 verts** (dont complétude des fiches et des traductions).

## Session 3 : finalisation (20/10/2026)
- **Construisez votre score** (`sections/mon_score.py`, `utils/custom_score.py`) : poids des familles, gravité de cinq groupes de
  substances (×0,5 à ×3), sévérité des bactéries (k = 2,5 à 20), seuils de nitrates, plomb, arsenic, PFAS et de chaque pesticide ;
  score officiel et personnel d'une commune côte à côte, rang, part des communes qui changent de note, notes de toutes les
  communes, dix plus basses communes de plus de 10 000 habitants, tableau de sensibilité (déplacé depuis les Plongées, où les
  curseurs what-if sont remplacés par un lien : plus de doublon). Bouton « Revenir aux réglages officiels », avertissement en tête.
  Moteur rapide : tout ce qui ne dépend pas des réglages est préparé une fois (pic 92 Mo, 24 Mo gardés), puis 0,1 s par recalcul ;
  **avec les réglages officiels il redonne exactement les scores publiés** (test). Seuil d'un pesticide : seules les limites
  individuelles (0,1 et 0,03 µg/L) bougent, pas les sommes à 0,5 µg/L (total, atrazine et métabolites, terbuthylazine et métabolites).
- **Rapport PDF** depuis la page commune, en anglais et en français (`utils/town_report.py`, textes `utils/texts/pdf.py`) :
  score, note, trois notes, réseaux, rapport par réseau, historique sur dix ans (par défaut la substance qui coûte le plus de points,
  le total des pesticides pour un pesticide seul), position face aux médianes nationale et départementale, formules, sources, date
  des données, avertissement. Texte généré par règles (le même que dans l'app : l'explication « pourquoi ce score » est désormais une
  fonction partagée). **fpdf2 2.8.9** : Python pur, s'installe sur Streamlit Cloud ; polices Plex et Fraunces embarquées
  (`assets/fonts/`, licences OFL) → accents, µ, ≤, × corrects ; graphiques dessinés avec fpdf2 (pas de navigateur sans tête).
  Génération à la demande au clic (0,2 à 1 s), langue forcée par une variable de contexte (sans effet sur les autres sessions).
  Dates des rapports au format de la langue (« 26/02/2024 », « 26 Feb 2024 ») au lieu du format ISO.
- Corrections : « for a indicative value » → « under the indicative value » ; « desservie par 0 réseau » → phrase dédiée ;
  pesticides à limite 0,5 µg/L exclus du curseur « chaque pesticide » (repéré par un test).
- Vérification : pages ouvertes en EN et FR avec Paris, Germaines (52, 47 hab., note E), Cayenne, Ouanary, Mamoudzou, une commune
  sans score (Péreyres), réglages extrêmes (tous les poids à zéro → avertissement) ; PDF générés pour ces communes dans les deux
  langues. Relecture automatique des 819 textes : aucun tiret cadratin, aucun emoji, aucune liste, toutes les clés traduites.
- Mémoire en local (serveur neuf, toutes les pages ouvertes) : 437 Mo pour les 8 pages historiques, 518 Mo avec la commune,
  527 Mo avec le score personnalisé. Temps de chargement local : 0,8 à 4,2 s à la première visite, 1 à 3 s ensuite.
- Livraison : README complet en anglais (rapport), `docs/storyboard.md`, `docs/script_video.md` (3 min, 436 mots ; retiré du dépôt le 20/10, gardé en local), `DATASET.md`,
  `docs/sources.md` (polices embarquées, fpdf2).
- **En ligne (après le push du 20/10)** : les 10 pages s'ouvrent sans erreur, en 1,5 à 5,9 s (chargement complet, premier passage) ;
  le rapport PDF est généré sur Streamlit Cloud (Cayenne, anglais : PDF valide de 59 Ko, polices Plex et Fraunces embarquées),
  donc fpdf2 s'installe bien. La mémoire en ligne n'est pas visible depuis l'extérieur : l'app n'a pas redémarré pendant le
  parcours complet ; la mesure locale (527 Mo) reste sous la limite basse annoncée (environ 690 Mo).
- Zip `dist/StApp26_20230851_GIRAUD_DAI.zip` (dossier ignoré par git), construit avec `git archive` depuis le dernier commit :
  environ 52 Mo, 124 fichiers (code, README, docs sans les consignes, `data/processed`, `DATASET.md`), aucune donnée brute ni
  `data/interim`. Tests : 198 verts, y compris depuis un clone propre.

## Session 4 : performance de la recherche de commune (20/10/2026)
**Symptôme (signalé par Florian)** : sur la page commune (et le même composant dans Comparer et Construisez votre score),
effacer le nom d'une ville pour en taper une autre gelait la page environ 5 secondes, en ligne.

**Diagnostic (mesures avant correction, Playwright + Chrome, `scripts/perf_audit.py`)** : ce n'était pas un rerun.
Effacer le texte n'envoie **aucun message au serveur** (0 message WebSocket), mais le navigateur reste bloqué sur des
« long tasks » de 4,2 à 4,5 s. Cause : `st.selectbox` (Streamlit 1.66, react-aria) filtre et dessine ses options dans le
navigateur, sans virtualisation, avec une comparaison `Intl.Collator` sur chaque nom ; quand le filtre redevient vide, il
dessine les 34 812 communes. Même chose à la fermeture de la liste après un choix (6 à 7 s pour Lyon) et dans le
multiselect de Comparer (retirer une ville : 3 s). Côté serveur, choisir une ville ne coûte que 0,16 à 0,47 s.
Le gel croît avec le nombre d'options (environ 0,12 ms par option : la liste des 1 785 paramètres ne bloque que 0,28 s).

**Choix** : alléger la liste envoyée au navigateur, la seule correction à la source (un fragment ou un cache côté serveur
n'auraient rien changé, le serveur n'étant pas en cause). `utils/town_search.py` : champ de recherche
**streamlit-searchbox** 0.1.24 (MIT, Python pur côté serveur, interface déjà compilée) dans un `st.fragment`. La recherche
tourne sur le serveur (accents ignorés, homonymes avec leur département) et le navigateur ne reçoit que les 5 exemples
(Paris, Lyon, Marseille, Bordeaux, Lille) ou les 20 meilleures correspondances. Chaque frappe ne relance que le fragment ;
choisir une ville relance la page en un seul aller-retour, vide le champ et affiche la ville courante en texte indicatif.
Comparer garde son multiselect pour retirer une ville, limité aux villes comparées et aux exemples, avec un champ
« Ajouter une commune ». En plus : rapport de chaque réseau mis en cache par langue (`town_report.network_report`, Marseille
a 16 réseaux : 0,98 s au premier passage, 0,18 s ensuite) ; décision de cache de `utils/io.py` prise à chaque appel et non
à l'import (un test qui importait le module hors Streamlit désactivait tout le cache de la suite : suite de tests 2 min 30
→ 1 min).

**Tests ajoutés** (`tests/test_performance.py`, 15 tests) : aucun widget de l'app n'envoie plus de 2 000 options ; recherche
rapide et correcte ; rerun serveur sous 3 s pour la page commune (Lyon, Marseille, Mamoudzou, Saint-Denis, commune sans
score), les curseurs du score personnel et Comparer à six villes ; test dans un vrai Chrome : vider le champ bloque moins
d'1 s, choisir Lyon prend moins de 4 s et un clic rapide ouvre la bonne commune (ignoré si Playwright ou Chrome manquent).
**219 tests verts.**
Outils de développement dans `requirements-dev.txt` (Playwright), pas dans `requirements.txt`.

**Tableau (secondes, anglais / français ; « total » = jusqu'à ce que l'app soit de nouveau utilisable)**. Local : machine
de développement ; en ligne : https://eau-robinet.streamlit.app/, à chaud. Les lignes « type » comprennent la frappe
simulée (60 ms par lettre : 0,24 s pour « Lyon », 0,66 s pour « Saint-Denis ») ; après la correction elles ne bloquent
jamais le navigateur.

| Page | Action | Local avant | Local après | En ligne avant | En ligne après |
|---|---|---|---|---|---|
| town | erase the name (Backspace x12), list open | 4,69 / 4,73 | 0,00 / 0,00 | 4,95 / 4,25 | 0,00 / 0,00 |
| town | empty the field then click away | 13,72 / 24,82 | 0,00 / 0,00 | 13,75 / 11,41 | 0,00 / 0,00 |
| town | type 'Lyon' until it is proposed | 0,60 / 0,61 | 0,66 / 0,99 | 0,69 / 0,60 | 0,30 / 1,54 |
| town | choose Lyon (69) (page updated) | 7,01 / 6,20 | 0,49 / 2,30 | 7,45 / 6,62 | 1,32 / 1,19 |
| town | choose Marseille (13) (page updated) | 1,08 / 1,07 | 1,10 / 1,03 | 1,82 / 1,61 | 1,19 / 1,35 |
| town | choose Lille (59) (page updated) | 3,21 / 2,81 | 1,03 / 0,58 | 3,03 / 2,82 | 0,99 / 0,93 |
| town | choose Péreyres (07) (page updated) | 0,49 / 0,51 | 0,29 / 0,51 | 0,72 / 0,73 | 0,66 / 0,61 |
| town | choose Mamoudzou (976) (page updated) | 0,80 / 0,80 | 0,67 / 0,71 | 1,30 / 1,08 | 0,99 / 0,93 |
| town | choose Saint-Denis (974) (page updated) | 2,15 / 3,22 | 0,95 / 1,05 | 3,50 / 2,55 | 1,11 / 1,10 |
| town | choose Saint-Denis (93) (page updated) | 2,85 / 3,79 | 0,49 / 0,54 | 2,64 / 2,18 | 0,89 / 0,85 |
| town | type 'Saint-Denis' | 0,78 / 2,08 | 1,17 / 1,22 | 0,76 / 0,77 | 1,51 / 1,51 |
| town | download PDF (EN) | 0,90 / 0,71 | 0,76 / 0,35 | 0,91 / 0,89 | 0,96 / 0,90 |
| town | download PDF (FR) | 0,42 / 0,75 | 0,43 / 0,38 | 0,85 / 0,88 | 0,94 / 0,89 |
| town | switch language EN/FR | 0,79 / 0,75 | 0,40 / 0,34 | 0,96 / 1,42 | 0,59 / 0,58 |
| compare | add a town (Villejuif) | 1,56 / 1,71 | 1,55 / 1,52 | 1,87 / 0,34 | 2,49 / 2,35 |
| compare | remove a town (Lille) | 3,49 / 3,13 | 0,31 / 0,33 | 2,80 / 2,96 | 0,63 / 0,58 |
| map | period slider (start year +1) | 0,71 / 0,68 | 0,67 / 0,68 | 1,17 / 1,12 | 1,14 / 1,06 |
| map | region -> Bretagne | 0,75 / 0,72 | 0,74 / 0,79 | 1,19 / 1,19 | 1,16 / 1,10 |
| map | kind of town -> mountain | 0,48 / 0,49 | 0,44 / 0,46 | 0,77 / 0,85 | 0,97 / 0,73 |
| map | map view -> nitrates | 0,64 / 0,71 | 0,64 / 0,65 | 1,02 / 1,11 | 1,12 / 1,00 |
| my-score | move a slider (each of 14) | 0,84 / 0,64 | 0,79 / 0,47 | 1,03 / 0,89 | 0,92 / 0,63 |
| my-score | back to the official settings | 0,35 / 0,34 | 0,32 / 0,35 | 0,59 / 0,58 | 0,56 / 0,58 |
| monitor | change tab (each of 4) | 0,00 / 0,00 | 0,00 / 0,00 | 0,00 / 0,00 | 0,00 / 0,00 |
| home | load (warm) | 2,84 / 1,03 | 2,23 / 0,89 | 3,68 / 2,18 | 7,15 / 1,80 |
| reading | load (warm) | 1,01 / 0,95 | 1,03 / 0,96 | 2,26 / 2,15 | 2,07 / 2,46 |
| town | load (warm) | 1,13 / 1,21 | 1,13 / 1,02 | 2,36 / 2,53 | 2,00 / 2,44 |
| compare | load (warm) | 1,19 / 1,49 | 1,05 / 1,05 | 2,80 / 2,81 | 1,91 / 2,18 |
| map | load (warm) | 1,48 / 1,40 | 1,48 / 1,40 | 3,06 / 2,91 | 2,57 / 2,44 |
| monitor | load (warm) | 1,14 / 1,15 | 1,12 / 1,14 | 2,94 / 2,12 | 2,21 / 2,25 |
| my-score | load (warm) | 1,10 / 1,15 | 1,01 / 1,01 | 2,56 / 2,72 | 2,32 / 1,97 |
| conclusions | load (warm) | 0,97 / 0,97 | 0,91 / 1,04 | 2,72 / 2,54 | 2,18 / 2,20 |
| quality | load (warm) | 1,02 / 0,99 | 1,06 / 1,30 | 2,14 / 2,10 | 2,04 / 3,03 |
| about | load (warm) | 0,86 / 0,93 | 0,85 / 0,85 | 1,91 / 1,93 | 1,71 / 1,70 |

**Bug trouvé pendant la vérification en ligne, puis corrigé** : le composant renvoie la *position* de l'option cliquée,
et le serveur la traduisait avec sa dernière liste. Un clic sur « Lyon (69) » parmi les exemples, fait pendant que les
résultats de « Lyon » arrivaient, ouvrait le 2e résultat (Lyons-la-Forêt) : 5 mauvaises communes sur 8 clics rapides,
reproduit en local. Correction : chaque option porte son code INSEE (`town_search._options_js`), lu tel quel par le
serveur ; 8 bonnes communes sur 8 ensuite, test unitaire et test navigateur ajoutés.

**Ce qui dépasse encore 1 s, et pourquoi** :
- Chargement d'une page (1 à 2,5 s en ligne) : envoi de la page, dessin de 3 à 8 graphiques Plotly et des formules ; la
  première page d'une nouvelle session télécharge en plus les fichiers JavaScript de Streamlit (1 à 3 s chacun sur Streamlit
  Cloud, très variable : un premier chargement a pris 8 s, les suivants 1,6 s).
- À froid, juste après un redémarrage du serveur en ligne (après un push ou une mise en veille) : accueil 10,3 s, commune
  7,3 s, le temps de lire les tables Parquet une première fois. D'où le réchauffement avant une démonstration.
- Choisir une ville en ligne (0,85 à 1,35 s) : le serveur recalcule la page (0,2 à 0,5 s, 1 s pour une grande ville au premier
  passage), puis le navigateur redessine 3 graphiques, le tableau et les formules ; plus le trajet réseau.
- Taper un nom : les propositions arrivent 0,4 à 0,9 s après la dernière touche en ligne (attente de 150 ms pour ne pas
  chercher à chaque lettre, puis un aller-retour), sans bloquer la page.
- Carte (curseur, région, vue : 1,0 à 1,2 s en ligne, 0,5 à 0,8 s en local) : rerun de la page avec la carte des 101
  départements ; identique avant et après.
- Premier PDF anglais en ligne (une fois 2,2 s) : chargement des polices ; ensuite 0,9 s.
- Ajouter une ville dans Comparer en ligne : 1,4 s pour taper « Villejuif » (dont 0,54 s de frappe), puis 0,75 à 1,0 s pour
  le choix.
- Les onglets des Plongées s'affichent sans aller au serveur (0 s).

## Session 5 : reprise, LinkedIn, page « Explorer les données » (20/10/2026)
**Point de reprise** : la session 4 s'était arrêtée après le correctif du clic rapide (commit `198cce8`), arbre propre et
poussé. A était terminé : rien à reprendre. Un test (`test_paris_is_not_compared_with_its_own_department`) a échoué une
fois dans la suite complète puis est passé à chaque relance (seul et dans la suite) : instable, à surveiller.

**B. LinkedIn** (commit `8c389a2` après rebase) : le nom de Florian dans le pied de page de toutes les pages pointe vers
https://www.linkedin.com/in/florian-giraud-67883a291/ (EN et FR), bouton « LinkedIn » à côté du bouton GitHub sur la
page À propos, lien dans la section Credits du README. Liens du pied de page en nouvel onglet avec `rel="noopener noreferrer"`
(`utils/viz._md`), constantes `config.AUTHOR_LINKEDIN` et `config.REPO_URL`. Test : `test_footer_and_about_link_to_linkedin`.

**C. Page « Explore the data » / « Explorer les données »** (`sections/explore.py`, textes `utils/texts/explore.py`),
dans « Méthode et crédits » juste avant « Les coulisses des chiffres ». Tout est pré-calculé par
`scripts/07_build_explore_tables.py` (3 s, branché dans `Makefile` et `make.ps1`) : 10 petites tables (64 Ko en tout).
- Schéma des 3 fichiers (SVG en ligne, couleurs du thème) avec les clés `referenceprel` et `cdreseau` et les lignes 2025 ;
  volume par année (lignes, prélèvements, tailles des zips, du texte et de la copie Parquet brute : 22 Go de texte, 449 Mo
  de Parquet) ; pourquoi le réseau est l'unité de base (2026 : 28 419 communes sur 34 812 avec un seul réseau, 17 363 réseaux
  sur 22 798 pour une seule commune ; 2025 : 18,6 % des prélèvements rattachés à plusieurs réseaux, jusqu'à 66).
- Vraies lignes : les 30 lignes brutes du data dictionary (graine 42, déjà dans le dépôt, copiées dans
  `explore_examples.json` ; un test vérifie qu'aucune autre ligne brute n'est ajoutée) + 6 lignes de `udi_year`.
- Distributions : prélèvements par réseau en 2025 (médiane 9, 67 % sous 12 analyses bactériologiques) ; part des résultats
  sous la limite de quantification par groupe (pesticides 98,8 %, bactéries 98,9 %, nitrates 38,4 %) ; 15 paramètres les plus
  mesurés ; moyennes 2025 des réseaux pour 8 paramètres avec leur seuil.
- Matrice de Spearman de 8 indicateurs des 96 départements de métropole, calculée paire par paire. **Même règle que la
  carte** : médiane du score seulement pour les départements d'au moins 5 communes notées (Paris exclu de cet indicateur).
  Sans cette règle on trouvait −0,12 au lieu du −0,14 affiché par la carte. Résultats : H2 ρ = 0,05 ; petits réseaux et échecs
  bactério 0,93 ; petits réseaux et score médian −0,14 ; score médian et nitrates −0,45 ; dureté et nitrates 0,55 ; seuil de
  hasard à 5 % pour 96 départements : 1,96/√95 = 0,20. Densité = population / surface calculée sur les contours de la carte
  (Paris 19 900 hab./km²).
- Nuage de points avec choix des deux axes (axes logarithmiques pour population et densité), ρ et force du lien calculés.
- Sources citées dans les textes : n° 23 (OMS, origines des nitrates) et n° 37 (dureté). Deux phrases non sourcées retirées
  avant publication (« le nombre de prélèvements suit la population, comme le veut la réglementation », origine des nitrates).
- Vérifié dans Chrome (Playwright) : anglais et français, thème clair et sombre (valeurs de la matrice écrites en
  annotations, sinon illisibles en sombre), largeur téléphone 390 px sans défilement horizontal.
- Barre latérale : note propre aux pages sans filtre (`NO_FILTER_NOTE` : « elle décrit les fichiers eux-mêmes » pour cette
  page, phrase neutre pour À propos ; l'ancienne note parlait des fenêtres du score).
- Tests : `tests/test_explore.py` (17 tests : tables petites et cohérentes avec le data dictionary et les autres pages,
  aucune ligne brute nouvelle, chaque contrôle de la page rerun sous 1,5 s en EN et FR, textes calculés et propres).
  **241 tests verts** (aussi depuis un clone propre sans données brutes).
- À trancher par Florian : « Les coulisses des chiffres » garde son histogramme de couverture (prélèvements par réseau, suit
  le filtre de période), proche de celui de la nouvelle page (année 2025, classes lisibles). Les deux sont gardés.

### E. Fin de session 5 : audit, push, vérification en ligne, zip
- **Fragments** sur la page « Explorer les données » : les trois contrôles (table affichée, paramètre, axes du nuage) sont
  chacun dans un `st.fragment`, si bien qu'un changement ne redessine qu'un graphique. Mesuré dans Chrome en local :
  axes du nuage 1,08–1,15 s → 0,28–0,38 s ; table et paramètre 0,7–0,9 s → 0,15–0,28 s.
- **Audit** (`scripts/perf_audit.py`) : la nouvelle page est couverte (chargement et chaque contrôle) ; une interaction qui
  échoue est notée « failed » sans arrêter l'audit, et les mesures déjà prises sont écrites même en cas de plantage
  (un premier passage avait perdu ses mesures sur un mauvais sélecteur : les boutons segmentés ont le rôle `radio`).
- **Comparaison A/B** dans les mêmes conditions (même machine, même Chrome, code du commit `198cce8` sur le port 8504 contre
  le code actuel sur 8501) : les chargements de toutes les pages sont aujourd'hui de 1,5 à 2,8 s en local pour **les deux**
  versions, contre 0,85 à 2,2 s mesurés en session 4. Le ralentissement vient de la machine, pas du code ; le code actuel
  reste 0,15 à 0,3 s plus lent en médiane, l'ordre de grandeur de l'écart entre deux séries de mesures du même code.
- **Push** : refusé une première fois, origin contenait `febc6e9 Added Dev Container Folder` (14:16, compte de Florian,
  message type de Streamlit Cloud) qui remet `.devcontainer/devcontainer.json` dans le suivi, alors qu'il en avait été retiré
  le 20/10. Contenu identique à la copie locale : les 5 commits ont été rebasés dessus (copie locale sauvegardée dans le
  scratchpad puis restaurée à l'identique par git), rien n'a été supprimé. **À trancher par Florian** : le garder suivi ou
  le retirer de nouveau. Le zip l'exclut, comme avant.
- **En ligne** (après le push) : les 11 pages en anglais et en français s'ouvrent sans erreur, avec le lien LinkedIn dans le
  pied de page ; toutes réchauffées. Chargement de la nouvelle page répété trois fois : 2,3 à 2,5 s (Behind the numbers 1,9 s,
  About 1,7 s) ; une mesure isolée à 4,65 s et une carte à 9,2 s sont des pics de Streamlit Cloud (non reproduits). Le premier
  chargement d'une session neuve prend encore jusqu'à 8 s (téléchargement des scripts de Streamlit).

**Tableau de performance (secondes, anglais / français ; « total » = jusqu'à ce que l'app soit de nouveau utilisable).**
S4 = mesures de la session 4 ; S5 = cette session ; « code du 198cce8 » = l'ancien code mesuré aujourd'hui dans les mêmes
conditions (chargements anglais seulement). Les lignes « type » comprennent la frappe simulée (60 ms par lettre) et ne
bloquent jamais le navigateur ; « – » = non mesuré.

| Page | Action | S4 local avant | S4 local après | S5 local, code du 198cce8 (A/B) | S5 local | S4 en ligne avant | S4 en ligne après | S5 en ligne |
|---|---|---|---|---|---|---|---|---|
| about | load (cold) | 0,86 / 0,87 | 0,83 / 0,85 |  | 1,66 / 1,67 |  | 1,76 / – | 1,83 / 1,80 |
| about | load (warm) | 0,86 / 0,93 | 0,85 / 0,85 | 1,52 / – | 1,64 / – | 1,91 / 1,93 | 1,71 / 1,70 | 1,84 / 1,98 |
| compare | add a town (Villejuif) | 1,56 / 1,71 | 1,55 / 1,52 |  | 1,78 / 1,67 | 1,87 / 0,34 | 2,49 / 2,35 | 2,42 / 2,33 |
| compare | load (cold) | 1,20 / 1,26 | 1,04 / 1,07 |  | 2,04 / 2,10 |  | 3,21 / – | 2,48 / 2,10 |
| compare | load (warm) | 1,19 / 1,49 | 1,05 / 1,05 | 1,88 / – | 2,12 / – | 2,80 / 2,81 | 1,91 / 2,18 | 2,48 / 2,48 |
| compare | remove a town (Lille) | 3,49 / 3,13 | 0,31 / 0,33 |  | 0,40 / 0,47 | 2,80 / 2,96 | 0,63 / 0,58 | 0,67 / 0,67 |
| conclusions | load (cold) | 0,96 / 0,92 | 0,88 / 0,89 |  | 1,54 / 1,70 |  | 1,90 / – | 1,98 / 1,99 |
| conclusions | load (warm) | 0,97 / 0,97 | 0,91 / 1,04 | 1,64 / – | 1,66 / – | 2,72 / 2,54 | 2,18 / 2,20 | 1,89 / 1,91 |
| explore | change an axis of the scatter (each) |  |  |  | 0,33 / 0,35 |  |  | 0,71 / 0,75 |
| explore | change the parameter (each) |  |  |  | 0,22 / 0,26 |  |  | 0,52 / 0,41 |
| explore | change the table shown (each) |  |  |  | 0,15 / 0,19 |  |  | 0,37 / 0,39 |
| explore | load (cold) |  |  |  | 2,58 / 2,14 |  |  | 2,81 / 2,51 |
| explore | load (warm) |  |  | 1,67 / – | 2,12 / – |  |  | 2,74 / 4,65 |
| home | load (cold) | 4,16 / 2,82 | 2,64 / 2,52 |  | 2,56 / 1,89 |  | 10,31 / – | 3,21 / 1,88 |
| home | load (warm) | 2,84 / 1,03 | 2,23 / 0,89 | 2,72 / – | 2,76 / – | 3,68 / 2,18 | 7,15 / 1,80 | 2,82 / 1,71 |
| map | kind of town -> mountain | 0,48 / 0,49 | 0,44 / 0,46 |  | 0,58 / 0,65 | 0,77 / 0,85 | 0,97 / 0,73 | 0,81 / 0,78 |
| map | load (cold) | 1,92 / 1,53 | 1,56 / 2,43 |  | 2,41 / 2,41 |  | 2,83 / – | 3,12 / 2,70 |
| map | load (warm) | 1,48 / 1,40 | 1,48 / 1,40 | 2,28 / – | 2,38 / – | 3,06 / 2,91 | 2,57 / 2,44 | 2,62 / 9,19 |
| map | map view -> nitrates | 0,64 / 0,71 | 0,64 / 0,65 |  | 0,85 / 0,93 | 1,02 / 1,11 | 1,12 / 1,00 | 1,12 / 1,13 |
| map | period slider (start year +1) | 0,71 / 0,68 | 0,67 / 0,68 |  | 0,88 / 0,95 | 1,17 / 1,12 | 1,14 / 1,06 | 1,25 / 1,10 |
| map | region -> Bretagne | 0,75 / 0,72 | 0,74 / 0,79 |  | 0,84 / 1,08 | 1,19 / 1,19 | 1,16 / 1,10 | 1,32 / 1,23 |
| monitor | change tab (each) | 0,00 / 0,00 | 0,00 / 0,00 |  | 0,00 / 0,00 | 0,00 / 0,00 | 0,00 / 0,00 | 0,00 / 0,00 |
| monitor | load (cold) | 1,17 / 1,15 | 1,07 / 1,67 |  | 2,08 / 2,10 |  | 2,19 / – | 2,65 / 2,45 |
| monitor | load (warm) | 1,14 / 1,15 | 1,12 / 1,14 | 1,89 / – | 1,94 / – | 2,94 / 2,12 | 2,21 / 2,25 | 2,16 / 2,27 |
| my-score | load (cold) | 1,70 / 1,63 | 1,46 / 1,62 |  | 2,37 / 2,07 |  | 1,91 / – | 2,02 / 1,86 |
| my-score | load (warm) | 1,10 / 1,15 | 1,01 / 1,01 | 1,76 / – | 1,82 / – | 2,56 / 2,72 | 2,32 / 1,97 | 1,87 / 1,96 |
| my-score | move a slider (each) | 0,54 / 0,27 | 0,46 / 0,28 |  | 0,31 / 0,35 | 0,85 / 0,58 | 0,78 / 0,53 | 0,85 / 0,57 |
| quality | load (cold) | 1,06 / 1,01 | 0,96 / 0,99 |  | 1,92 / 1,93 |  | 2,39 / – | 2,11 / 2,24 |
| quality | load (warm) | 1,02 / 0,99 | 1,06 / 1,30 | 1,58 / – | 1,87 / – | 2,14 / 2,10 | 2,04 / 3,03 | 3,70 / 2,35 |
| reading | load (cold) | 1,07 / 1,03 | 0,97 / 1,01 |  | 2,04 / 2,01 |  | 2,18 / – | 2,03 / 1,74 |
| reading | load (warm) | 1,01 / 0,95 | 1,03 / 0,96 | 1,78 / – | 1,91 / – | 2,26 / 2,15 | 2,07 / 2,46 | 1,92 / 1,88 |
| town | choose Bordeaux (33) (page updated) | 0,84 / 0,77 | 0,74 / 0,64 |  | 0,76 / 0,97 | 1,22 / 1,14 | 1,09 / 1,28 | 1,42 / 1,33 |
| town | choose Lille (59) (page updated) | 3,21 / 2,81 | 1,03 / 0,58 |  | 0,64 / 0,77 | 3,03 / 2,82 | 1,25 / 1,02 | 1,40 / 0,95 |
| town | choose Lyon (69) (page updated) | 7,01 / 6,20 | 0,49 / 2,30 |  | 0,68 / 0,58 | 7,45 / 6,62 | 1,06 / 0,85 | 0,90 / 0,73 |
| town | choose Mamoudzou (976) (page updated) | 0,80 / 0,80 | 0,67 / 0,71 |  | 0,46 / 0,92 | 1,30 / 1,08 | 1,28 / 1,17 | 1,53 / 0,99 |
| town | choose Marseille (13) (page updated) | 1,08 / 1,07 | 1,10 / 1,03 |  | 0,93 / 1,56 | 1,82 / 1,61 | 1,45 / 1,78 | 1,34 / 1,20 |
| town | choose Péreyres (07) (page updated) | 0,49 / 0,51 | 0,29 / 0,51 |  | 0,31 / 0,28 | 0,72 / 0,73 | 0,63 / 0,69 | 0,78 / 0,59 |
| town | choose Saint-Denis (93) (page updated) | 2,85 / 3,79 | 0,49 / 0,54 |  | 0,41 / 0,70 | 2,64 / 2,18 | 0,89 / 0,86 | 1,02 / 0,93 |
| town | choose Saint-Denis (974) (page updated) | 2,15 / 3,22 | 0,95 / 1,05 |  | 0,54 / 1,33 | 3,50 / 2,55 | 1,76 / 1,62 | 1,65 / 1,66 |
| town | download PDF (English) | 0,90 / – | 0,76 / – |  | 0,36 / – | 0,91 / – | 2,17 / – | 0,90 / – |
| town | download PDF (French) | 0,42 / – | 0,43 / – |  | 0,35 / – | 0,85 / – | 0,92 / – | 0,99 / – |
| town | download PDF (anglais) | – / 0,71 | – / 0,35 |  | – / 0,56 | – / 0,89 | – / 0,86 | – / 0,88 |
| town | download PDF (français) | – / 0,75 | – / 0,38 |  | – / 0,58 | – / 0,88 | – / 0,85 | – / 0,92 |
| town | empty the field then click away | 13,72 / 24,82 | 0,00 / 0,00 |  | 0,00 / 0,00 | 13,75 / 11,41 | 0,00 / 0,00 | 0,00 / 0,00 |
| town | erase the name (Backspace x12), list open | 4,69 / 4,73 | 0,00 / 0,00 |  | 0,00 / 0,00 | 4,95 / 4,25 | 0,00 / 0,00 | 0,00 / 0,00 |
| town | load (cold) | 1,93 / 1,90 | 1,58 / 1,58 |  | 2,90 / 2,39 |  | 7,30 / – | 2,25 / 2,21 |
| town | load (warm) | 1,13 / 1,21 | 1,13 / 1,02 | 2,03 / – | 2,19 / – | 2,36 / 2,53 | 2,00 / 2,44 | 2,83 / 1,91 |
| town | switch language EN/FR | 0,79 / 0,75 | 0,40 / 0,34 |  | 0,65 / 0,63 | 0,96 / 1,42 | 0,59 / 0,58 | 0,75 / 0,58 |
| town | type 'Bordeaux' until it is proposed | 0,36 / 0,35 | 0,00 / 0,00 |  | 0,00 / 0,00 | 0,35 / 0,20 | 0,00 / 0,00 | 0,00 / 0,00 |
| town | type 'Lille' (retyped town) | 4,65 / 4,51 | 0,66 / 0,68 |  | 0,69 / 0,73 | 4,38 / 4,25 | 0,96 / 0,94 | 1,13 / 1,02 |
| town | type 'Lyon' until it is proposed | 0,60 / 0,61 | 0,66 / 0,99 |  | 1,09 / 0,73 | 0,69 / 0,60 | 0,93 / 0,84 | 0,97 / 0,82 |
| town | type 'Mamoudzou' (overseas town) | 0,42 / 0,42 | 0,99 / 1,11 |  | 1,05 / 1,00 | 0,42 / 0,42 | 1,35 / 1,25 | 2,21 / 1,36 |
| town | type 'Marseille' until it is proposed | 0,45 / 0,43 | 0,00 / 0,00 |  | 0,00 / 0,00 | 0,45 / 0,44 | 0,00 / 0,00 | 0,00 / 0,00 |
| town | type 'Péreyres' (town without score) | 0,26 / 0,24 | 0,90 / 0,95 |  | 0,97 / 0,97 | 0,25 / 0,23 | 1,27 / 1,18 | 2,23 / 1,24 |
| town | type 'Saint-Denis' (homonym) | 0,77 / 1,42 | 1,17 / 1,21 |  | 1,17 / 1,22 | 0,74 / 0,76 | 1,44 / 1,42 | 1,58 / 1,56 |

**Ce qui dépasse encore 1 s, et pourquoi** (en plus de la liste de la session 4, toujours valable) :
- Chargement d'une page (1,5 à 3 s) : envoi de la page, dessin de 3 à 8 graphiques ; la nouvelle page en dessine 7, plus deux
  tableaux et un schéma, d'où 0,4 à 0,6 s de plus que « Behind the numbers ». Rien n'y est calculé : tout est pré-calculé.
- Choisir une ville en ligne (1,0 à 1,65 s) : rerun de la page commune et dessin de ses graphiques et formules, plus le trajet
  réseau ; Marseille et Saint-Denis (974) ont plusieurs réseaux dont le rapport est calculé une fois par langue puis mis en cache.
- Carte (curseur, région, vue : 1,1 à 1,3 s en ligne, 0,6 à 1,1 s en local) : rerun de la page avec la carte des 101
  départements, inchangé depuis la session 4.
- Ajouter une ville dans Comparer (1,7 s en local, 2,3 à 2,4 s en ligne) : la frappe simulée de « Villejuif » (0,54 s), l'attente
  des propositions, puis le rerun de la page à 3 villes ; le navigateur n'est pas bloqué (0 à 0,1 s).
- Axe du nuage en français en ligne (une mesure à 1,02 s, l'autre à 0,48 s) : trajet réseau variable, aucun blocage.

## Session 6 : filtres, PDF de comparaison, en-tête, ordre du menu (20/10/2026)
**Décisions de Florian (validation de A à E)** : `.devcontainer/` reste suivi (Streamlit Cloud le recrée) et reste hors du
zip ; l'histogramme des prélèvements par réseau est retiré de « Explorer les données » (gardé dans « Les coulisses des
chiffres », qui suit le filtre de période), remplacé par une phrase et un lien vers cette page ; la table
`explore_samples_hist` est supprimée du pipeline et du dépôt.

**F. Filtres masqués là où ils n'agissent pas.** Effet mesuré page par page (on change chaque filtre et on compare le
contenu affiché), identique à `PAGE_FILTERS` :

| Page | Filtres affichés |
|---|---|
| What's in my glass? | période, région, type de commune |
| What it all means | aucun (section masquée) |
| How to read a water test | période (année de fin du graphique des dépassements) |
| The water of my town | aucun |
| Town against town | région (groupes de communes) |
| The map of France | période, région, type de commune (+ vue de la carte) |
| What we look for, what we find | période |
| Build your own score | aucun |
| Explore the data | aucun |
| Behind the numbers | période |
| About this project | aucun |

Sur les pages où des filtres agissent, seuls ceux-là sont affichés (plus de filtres grisés). Un widget non dessiné perd
sa valeur : les valeurs sont réaffectées à chaque exécution (procédé documenté par Streamlit), si bien qu'une période
choisie sur la carte survit au passage par une page sans filtres (testé avec AppTest et dans Chrome). Régression trouvée
pendant H puis corrigée : avec `None` dans `session_state`, le filtre Région affichait « Choose an option » ; il vaut
désormais `"all"` (« All of France » / « Toute la France », vérifié en ligne). Notes « side.none » supprimées.

**G. PDF de comparaison** (`utils/compare_report.py`) : bouton EN et FR sous le tableau de « Town against town », pour les 2
à 6 communes comparées. Contenu : en-tête de marque, avertissement, chaque commune (carré de note avec la lettre, score,
confiance, population, trois notes), graphique en barres (score puis trois notes ; nom de la commune à gauche, valeur à
droite : la couleur n'est jamais nécessaire), explication de l'écart entre la meilleure et la moins bonne (même fonction
que la page), position face à la médiane nationale, formules, sources, date des données. Les communes sans score sont
nommées et écartées. `town_report._Doc` regroupe la mise en page commune aux deux rapports ; le rapport d'une commune est
resté identique octet pour octet (hors date de création, vérifié sur Paris et Froncles en EN et FR). Corrections de texte
au passage (page et PDF) : substance en minuscule après « À Paris : » (`lower_name`), « porte sur la famille confort ».
Génération 0,2 à 0,3 s (1 s la première fois, polices) ; en ligne 0,95 à 1,03 s. Tests : `tests/test_compare_report.py` (13).

**H. En-tête de la barre latérale** : logo EFREI blanc sur une pastille couleur encre de l'identité (#1B2A41) : pastille
visible en clair, fondue dans le fond en sombre (#1A2230), logo lisible dans les deux cas. Logo réduit à 400 px et 16
couleurs : `assets/efrei-logo-white.png`, 6,8 Ko (l'original fait 2560 × 1280 px), inclus en data URI (aucune requête de
plus). Puis Florian Giraud, Data & AI (groupe DAI), liens LinkedIn et GitHub (nouvel onglet), « Data Analysis &
Visualization, coordinateur : MATHEW Mano Joseph ». Streamlit place toujours son menu natif tout en haut : il est masqué
(`position="hidden"`) et redessiné avec `st.page_link` sous l'en-tête (mêmes sections, icônes, page active surlignée).
Différence connue : sur téléphone, la barre latérale reste ouverte après un clic dans le menu (le menu natif la refermait).
Les trois logos d'origine déposés par Florian dans `assets/` ne sont pas suivis par git ni mis dans le zip.

**I. Ordre du menu** : « What it all means » en 2e position. La page s'ouvre sur une phrase qui dit que c'est le résumé
des résultats, avant les preuves, avec des liens vers les six pages de preuves ; chaque hypothèse renvoie à la page qui la
teste (H1 et H2 : la carte ; H3 et H4 : « What we look for, what we find »). Storyboard renuméroté (conclusions = section 2)
et récit d'ouverture réécrit ; README (arc du récit, structure).

**E.** 271 tests verts, aussi depuis un clone propre. Audit Playwright local sans échec ni régression (ex. carte, période :
0,67 s ; nuage de points : 0,24 à 0,27 s ; PDF de comparaison : 0,20 s ; seule « ajouter une ville » dépasse 1 s, frappe
simulée comprise, navigateur non bloqué). En ligne après le push : les 11 pages en EN et FR sans erreur, en-tête présent,
filtres exactement là où ils agissent, menu dans le nouvel ordre, PDF de comparaison valides ; pages réchauffées.

## Session 7 : en-tête, retours d'un utilisateur test, cohérence des chiffres (20/10/2026)
**1. En-tête de la barre latérale.** Plus de pastille : logo noir en thème clair, blanc en thème sombre, sur le fond de la
barre. Choix du noir plutôt que du bleu : contraste mesuré sur le fond clair #ECE5D6 de 16,8:1 contre 3,6:1 pour le bleu
(CMJN, sous le seuil de 4,5:1 du texte). PNG d'origine vérifiés (fond transparent pour le noir et le blanc) ; versions
optimisées `assets/efrei-logo-black.png` (5,2 Ko) et `efrei-logo-white.png` (7,1 Ko), 400 px, 16 couleurs, fond
transparent ; les originaux `assets/Logo-Efrei-*-scaled.png` sont dans le `.gitignore` (commit `a25539d`), restés sur le
disque. Le thème vient de `st.context.theme` (testé dans Chrome : bon dès la première exécution ; un changement de thème
en cours de session se voit au clic suivant, Streamlit ne relançant pas la page). Espacement : lignes séparées, liens et
cours décollés, « coordinator: MATHEW Mano Joseph » sur sa ligne, 1,6 rem avant « The story ».

**2. Retours de l'utilisateur test** (tous en EN et FR) :
- a. Accueil : choisir une ville n'ouvre plus la page commune ; un aperçu s'affiche sous la recherche (carré de note,
  score, note, confiance, la phrase « points perdus » de la page commune, fonction `town_report.points_lost` extraite de
  l'explication) et un lien « See the full report » / « Voir le rapport complet » ouvre la page commune sur cette ville.
- b. Sur-titres : marge basse négative remplacée par une vraie marge (0,75 rem) ; un titre juste sous un sur-titre garde
  un écart serré (CSS `:has`). Vérifié en clair et en sombre.
- c. Comparer : texte « pourquoi » réécrit en phrases courtes, un paragraphe chacune (la famille qui fait l'écart, puis
  « Là où X perd des points : … » pour chacune des deux communes), sans répéter les scores déjà dans la phrase-titre ;
  même fonction (`compare_report.why_lines`) sur la page et dans le PDF ; phrase de la médiane du PDF raccourcie ;
  « un écart de 0,5 point » au singulier.
- d. Comparer : la sélection survit à la navigation (clé gardée comme les filtres) et au rechargement (`?towns=` dans
  l'URL, ce qui rend une comparaison partageable).
- e. Filtres : encadré léger bordé de la couleur principale, titre en Fraunces ; sur les pages filtrables, une ligne en
  haut dit qu'on peut affiner dans la barre latérale et avec quels filtres.
- f. « Why, probably » / « Pourquoi, probablement » → « Possible explanations » / « Explications possibles » (une seule
  clé, tous les blocs d'interprétation).
- g. Carte des valeurs manquantes : phrase-titre calculée pour chaque fichier ; pour COM_UDI (aucune case vide) « 0 % de
  cases vides » dans la phrase, la légende et chaque case ; couleur du zéro visible et cases séparées dans les deux thèmes.

**3. Cohérence des chiffres** (relevé des chiffres de toutes les pages avec AppTest) :
- Paramètres : 1 276 (2016) et 1 405 (2025) = tous les codes du fichier RESULT (data dictionary) ; 1 260 et 1 391 = la table
  `param_year`, qui ne garde que les paramètres à résultat chiffré. La différence est exactement le nombre de codes à
  résultat texte (odeur, aspect, salmonelles…), 12 à 17 selon l'année (vérifié pour les onze années, test). Ce n'est pas la
  fusion des codes jumeaux (non fusionnés dans ces comptes). La page « What we look for » utilise désormais le décompte
  du fichier. **Erreur corrigée** : « la plupart des nouveaux paramètres sont des pesticides » était faux ; calcul
  (`explore_param_changes`, règles écrites dans le script 07) : 293 codes apparus et 164 disparus entre 2016 et 2025 ;
  parmi les nouveaux, 86 pesticides et métabolites, 75 comptages de cyanobactéries, 22 PFAS, 110 autres.
- Résultats : 133 474 398 lignes RESULT partout (12 630 636 en 2025) ; « 132 millions » (table nettoyée, terrain + labo
  comptés une fois) et « 12,5 millions » (sans les non-mesurés) remplacés.
- Réseaux : « plus de 25 000 » remplacé par les chiffres des données (23 130 réseaux prélevés en 2025, 24 461 codes depuis
  2016).
- Communes notées : 34 816 (communes actuelles avec un score) ; « Build your own score » comptait aussi 10 anciens codes
  (34 826). « Explorer les données » parle des 34 812 communes du fichier de liens 2026, précisé dans le texte.
- **Erreur corrigée** sur « Build your own score » : « seuls 5 726 des 23 708 réseaux ont eu une mesure de PFAS » ; la table
  utilisée ne garde que les paramètres détectés : PFAS mesurés dans 17 642 des 23 733 réseaux notés, trouvés dans 5 726.
- « chaîne de six scripts » → sept. Définitions ajoutées au README (section 2).

**4.** 287 tests verts, aussi depuis un clone propre (nouveaux : `tests/test_feedback.py` pour 2a, 2d, 2g et les
comptes ; logos ; filtres ; texte de comparaison). Audit Playwright local sans échec ni régression. En ligne après le
push : 22 pages sans erreur (anglais en clair, français en sombre), logo noir en clair et blanc en sombre, filtres et
phrase d'en-tête exactement sur les pages filtrables, aperçu de l'accueil, sélection de Comparer gardée, phrase 0 % de
COM_UDI, « Possible explanations » ; pages réchauffées. Storyboard et README à jour ; zip reconstruit.

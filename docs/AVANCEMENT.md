# AVANCEMENT — « Is my tap water good? »

Journal du projet (mémoire entre sessions). Le plus récent en haut de chaque section.
Rendu : **samedi 24/10/2026 à 12:00** — 1re remise visée jeudi 22 au soir.

## État actuel

| Phase | Statut | Date |
|---|---|---|
| 0. Reconnaissance (lecture seule) | ✅ validée | 19/10 |
| 1. Setup | ✅ terminée (commit `0f7ab0b`) | 19/10 |
| 2. Pipeline | ✅ validée | 19/10 |
| 3. Score | ✅ validée (k = 5) | 19/10 |
| 4. App | ✅ déployée : https://eau-robinet.streamlit.app/ | 19/10 |
| 5. Finitions | 🟡 première passe faite | 19/10 |
| 6. Livraison | ⏳ | prévu 23/10 |
| 7. Bonus bouteille | hors périmètre (accord de Florian requis) | — |

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

## Phase 5 — Finitions, première passe (19/10/2026)
- App déployée par Florian sur Streamlit Community Cloud (Python 3.12) : https://eau-robinet.streamlit.app/ — les 8 pages
  s'ouvrent en ligne sans erreur, en 2,6 à 4,8 s (chargement complet).
- Accueil : encadré « pour qui / quelles questions » avec la page qui répond à chacune (critère narratif du barème).
- KPIs : étiquettes courtes (plus de troncature sur écran étroit), aides détaillées.
- Phrases-titres revues (Comprendre, nitrates = « moitié de la limite (25 mg/L) »), nombre de résultats calculé.
- Thème : l'app suit le réglage clair/sombre du lecteur ; vérifié en sombre → corrigés : ligne noire invisible (devenue gris moyen),
  fond blanc de la carte (transparent), aiguille de la jauge, ordre des sous-scores, « None » dans les quartiers.
- Robustesse : tests des 8 pages avec des filtres extrêmes (Mayotte + PFAS + 2026 seule, Corse 2016, Guyane…) et recherche
  d'homonymes ; un plantage trouvé et corrigé (saisonnalité sans année complète). **153 tests verts.**

## Phase 4 — App, version 1 (19/10/2026)

### Fait
- 8 pages en anglais dans l'ordre du storyboard ; sidebar globale (`utils/filters.py`) : période, région, famille de paramètres,
  type de commune — chaque filtre a un `help=` qui dit ce qu'il change.
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

## Phase 3 — Score (19/10/2026)

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

## Phase 2 — Pipeline (19/10/2026)

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
| 2023–2026 | 2 à 12 / an | 452, 671, 869, 707 — dont 438, 669, 869, 707 sous **dérogation (D)** |
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

## Phase 1 — Setup (19/10/2026)
- `.gitignore` (data/raw, data/interim, .venv…) créé **avant** le `git init` ; `.gitattributes` (fins de ligne LF, sinon le Makefile casse sous Linux).
- `requirements.txt` épinglé, `Makefile` + `make.ps1` (PowerShell sans make), `config.py`, `app.py` avec `st.navigation`,
  8 pages squelettes, `utils/` (io, prep, score, viz), tests, README squelette, `docs/sources.md`.

## Phase 0 — Reconnaissance (19/10/2026)

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
- 19/10 — `docs/consignes.pdf` (sujet du prof, avec son e-mail) **retiré de l’historique git** avant la publication (choix de Florian),
  gardé sur le disque et ajouté au `.gitignore`. Les hash des commits ont changé (phase 1 = `0f7ab0b`).
- 19/10 — **Phase 3 validée par Florian** : option k = 5 pour les petits réseaux, note sur score arrondi. Phases 4–5 enchaînées,
  repo GitHub public « eau-robinet » confirmé (création + push autorisés).
- 19/10 — **Phase 2 validée par Florian.** Parasites de `data/raw/ref/` supprimés par lui. Littoral : repli « départements
  méditerranéens hors montagne » accepté, **à présenter clairement comme une approximation dans l'app**.
- 19/10 — Sélénium/antimoine : piste de Florian vérifiée sur EUR-Lex et Légifrance → on peut en parler dans l'app (sources 10–12).
- 19/10 — PFAS : « dans le contrôle de routine depuis le 01/01/2026 » sourcé (ARS Nouvelle-Aquitaine, décret 2025-1287 ; directive art. 25).
- 19/10 — **Phase 0 validée par Florian.** Phases 1 et 2 enchaînées sans arrêt intermédiaire, sur toutes les années 2016–2026.
- 19/10 — `C:\.git` supprimé par Florian ; vérifié : plus aucun dépôt parent détecté avant le `git init`.
- 19/10 — Consignes renommées (pas copiées) en `docs/consignes.pdf`.
- 19/10 — **Métabolites de pesticides** : on suit la limite inscrite sur chaque ligne (option a). En plus, les métabolites
  classés **non pertinents** par l'Anses sont traités comme une **référence à 0,9 µg/L** (valeur indicative), famille
  confort/vigilance, pénalité légère. Rapport : « ⚠️ » au-dessus de 0,9 µg/L, « ℹ️ » si détecté en dessous.
  Métabolites concernés (sources dans `docs/sources.md`) : ESA-métolachlore et NOA-métolachlore (avis Anses du 30/09/2022),
  chlorothalonil R471811 (avis Anses du 29/04/2024). Vérifié : `refqual` ne contient **jamais** 0,9 µg/L (0 ligne) →
  la règle est appliquée par nous. Règle de ligne : si la ligne porte une limite → la limite ; sinon, pour ces codes → référence 0,9 µg/L.
  Les autres métabolites sans limite dans les données (OXA-métolachlore, ESA/OXA-métazachlore, ESA-alachlore…) n'ont pas
  de source fournie → pas de pénalité, simple « ℹ️ » s'ils sont détectés.
- 19/10 — 2026 : situation actuelle = fenêtres de 12 et 36 mois se terminant le 31/08/2026 ; évolutions sur 2016–2025 ;
  2026 montrée à part et marquée partielle.
- 19/10 — Paramètre mesuré deux fois dans un prélèvement : on garde la mesure de **laboratoire**.
- 19/10 — Microbiologie du score : calculée à partir de la **conformité officielle** par prélèvement (`plvconformitebacterio`).
- 19/10 — Repo GitHub : `eau-robinet`, public. **Confirmation de Florian requise avant le premier push.**
- 19/10 — Après le gel de l'app : DuckDB 3 Go / 4 threads, une année à la fois, traitements longs en arrière-plan avec journal,
  reprise étape par étape (demande de Florian).
- 19/10 — Toutes les années traitées (pas de plan B). Raison : volumétrie maîtrisée grâce à DuckDB + Parquet.
- 19/10 — `.venv` en Python 3.12.9 (version stable déjà installée ; même version à choisir sur Streamlit Community Cloud, à confirmer au déploiement).

## Session identité, écriture, accueil, ergonomie (19/10/2026, en cours)
- Fait : règles d'écriture dans CLAUDE.md ; direction visuelle A « Au robinet » (papier et encre, Fraunces + IBM Plex, palette validée daltonisme en clair et en sombre) ; module de traduction `utils/i18n.py` + `utils/texts/` (EN officiel, FR via le sélecteur, 559 clés, tests de complétude) ; accueil refait (OMS, Santé publique France, absence de chiffre officiel de décès dite honnêtement, méthode, H1 à H4, indicateurs expliqués) ; pages renommées ; recherche de commune en une seule liste (exemples Paris, Lyon, Marseille, Bordeaux, Lille) ; filtres grisés hors de leurs pages ; rapport « pourquoi » traduit avec étiquettes au lieu d'emojis ; pied de page et page À propos ; `docs/sources.md` renuméroté (sources 1 à 17), sans tiret cadratin ; H1 et H2 testées sur la carte. 167 tests verts avant les derniers ajustements.
- Reste : relire chaque page en FR et EN dans le navigateur, retirer les tirets cadratins restants dans README et docs internes, vérifier l'app en ligne après le push.

# AVANCEMENT — « Is my tap water good? »

Journal du projet (mémoire entre sessions). Le plus récent en haut de chaque section.
Rendu : **samedi 24/10/2026 à 12:00** — 1re remise visée jeudi 22 au soir.

## État actuel

| Phase | Statut | Date |
|---|---|---|
| 0. Reconnaissance (lecture seule) | ✅ validée | 19/10 |
| 1. Setup | ✅ terminée (commit `e23dc07`) | 19/10 |
| 2. Pipeline | ✅ terminée — **en attente de validation** | 19/10 |
| 3. Score | ⏳ | prévu 20–21/10 |
| 4. App | ⏳ | prévu 21–22/10 |
| 5. Finitions | ⏳ | prévu 22/10 |
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
- Fichiers parasites dans `data/raw/ref/` créés par erreur lors d'un premier téléchargement manuel (non utilisés, laissés en
  place car on ne supprime rien dans `data/raw/`) : `departements-100m.geojson` (138 octets, page de redirection HTML) et
  `geo_arrondissements.json`. **Florian peut les supprimer à la main.**

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
  Le changement réglementaire exact (directive 2020/2184 ?) reste **à sourcer** avant d'en parler dans l'app.
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
- ⏳ Sourcer l'évolution de la limite du sélénium (10 → 20 µg/L) avant d'en parler dans l'app.

## Journal des décisions
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

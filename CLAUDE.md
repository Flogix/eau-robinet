# CLAUDE.md — « Is my tap water good? » / « Mon eau du robinet est-elle bonne ? »
Projet individuel EFREI 2026 — Streamlit Dashboard (data storytelling)

## Fiche étudiant
- Nom : GIRAUD — Prénom : Florian — N° étudiant : 20230851 — Groupe : DAI
- Zip final : `StApp26_20230851_GIRAUD_DAI.zip` (modèle du prof : `StApp26_20000_NOM_DAI.zip`)
- Langue des livrables (app, README, storyboard, script vidéo) : anglais (consignes en anglais)
- Langue des docs internes (AVANCEMENT, data_dictionary) et de nos échanges : français
- OS : Windows (PowerShell ; `make` n'est pas installé par défaut) — Python : à détecter en phase 0
- Dossier du projet : `C:\Users\flogi\projets\eau-robinet` (hors OneDrive)
- Comptes : GitHub = Flogix (connecté via GitHub CLI `gh`) ; Streamlit Community Cloud = compte créé avec GitHub
- **Rendu : samedi 24 octobre 2026 à 12:00.** Plusieurs remises autorisées → viser une 1re remise jeudi 22 au soir.

## Mission
App Streamlit qui raconte la qualité de l'eau du robinet en France (2016 → 2026).
Fil rouge : « Mon eau est-elle bonne ? » → score /100 par commune + rapport qui explique pourquoi,
comparaisons (ex. Paris vs Villejuif, montagne vs littoral méditerranéen, urbain vs rural), carte, évolution dans le temps.
Bonus eau en bouteille : hors périmètre pour l'instant, ne pas commencer sans mon accord.

Documents de référence — à lire en entier au début de chaque session si tu ne les as pas en contexte :
- `docs/consignes.pdf` : consignes officielles + barème. Elles priment en cas de doute.
- `docs/CAHIER_DES_CHARGES.md` : public, storyboard, méthode du score, pipeline, phases, planning.
- `docs/AVANCEMENT.md` : journal du projet (à créer en phase 0, puis à tenir à jour). C'est la mémoire entre sessions.

## Règles de travail
1. Une phase à la fois (voir cahier des charges §8). Fin de phase = résumé (fait / reste / décisions / chiffres clés) puis STOP pour validation.
2. Mets à jour `docs/AVANCEMENT.md` à chaque fin de phase et dès qu'une décision est prise.
3. Explique chaque choix important en 2-3 phrases simples : je dois pouvoir le défendre à l'oral et dans la vidéo.
4. N'invente jamais un chiffre, un seuil, une source ou un nom de colonne. Tout chiffre affiché est soit calculé depuis les données, soit cité avec son URL dans `docs/sources.md`.
5. Si quelque chose bloque (fichier, colonne, seuil, performance) : dis-le et propose 2 options. Ne contourne jamais en silence.
6. `data/raw/` est en lecture seule et n'est jamais commité. Ne supprime jamais rien dans `data/raw/`.
7. Avant de déclarer une phase finie : tests verts, app lancée, chaque page ouverte sans erreur.
8. Petits commits git fréquents avec des messages clairs.

## Les données
Faits vérifiés sur la page data.gouv.fr (le reste est à vérifier dans les fichiers, ne suppose rien) :
- Jeu : « Résultats du contrôle sanitaire de l'eau distribuée commune par commune ».
  Producteur : ministère chargé de la Santé. Licence Ouverte / Open Licence 2.0 (citer source + date de mise à jour).
  Page : https://www.data.gouv.fr/datasets/resultats-du-controle-sanitaire-de-leau-distribuee-commune-par-commune
  Liste des fichiers (URL, taille, date) via l'API : https://www.data.gouv.fr/api/1/datasets/resultats-du-controle-sanitaire-de-leau-distribuee-commune-par-commune/
  Fichier de documentation PDF du jeu : https://www.data.gouv.fr/api/1/datasets/r/36afc708-42dc-4a89-b039-7fde6bcc83d8 (copie dans `docs/`)
- Fichiers locaux : versions nationales `dis-2016.zip` à `dis-2026.zip` (pas les `-dept`), téléchargées à la main
  le 19/10/2026 dans `data/raw/dis/`, non décompressées. Toute extraction se fait dans `data/interim/`, jamais dans `data/raw/`.
- Citation à utiliser (README, app) : Ministère des Solidarités et de la Santé, « Résultats du contrôle sanitaire de l'eau
  distribuée commune par commune », data.gouv.fr, Licence Ouverte 2.0, dernière mise à jour le 5 octobre 2026, URL de la page ci-dessus.
- Couverture : prélèvements validés par les ARS depuis le 01/01/2016. L'année en cours est mise à jour chaque mois
  (le fichier annuel est remplacé) → 2026 est partielle. Les DROM sont complétés progressivement.
- Avertissement du producteur : une anomalie de diffusion a été corrigée, avec rattrapage des années passées jusqu'en 2024 inclus.
  → Vérifier que les fichiers locaux correspondent aux versions en ligne, et le mentionner dans la section qualité des données.
- 3 types de fichiers par année :
  - PLV = prélèvements (UDI, commune principale, date, conclusions de conformité du prélèvement)
  - RESULT = résultats d'analyse (paramètre, valeur, unité, limite et référence de qualité)
  - UDI_COM = lien commune ↔ unité de distribution (UDI), avec parfois des quartiers
  - Jointures : PLV ↔ RESULT par `referenceprel` ; PLV ↔ UDI_COM par `cdreseau` (code de l'UDI).
- UDI = réseau dans lequel la qualité de l'eau est homogène (plus de 25 000 en France). Relation commune ↔ UDI n-n :
  une commune peut avoir plusieurs UDI, une UDI dessert plusieurs communes. Attention aux doublons créés par les quartiers lors des jointures.
- Certains prélèvements sont faits en amont (usine, captage) puis rattachés à l'UDI : champs `cdreseauamont`, `nomreseauamont`, `pourcentdebit`.
- Les conclusions de conformité sont au niveau du prélèvement (bactério / physico-chimie ; limites / références).
- Volumétrie : plus de 300 000 prélèvements et environ 12 millions d'analyses par an → plusieurs Go de texte.
  **Ne jamais charger RESULT entier dans pandas** : DuckDB (hors mémoire) puis Parquet.
- Noms de colonnes probables, À CONFIRMER en phase 0 : valeur texte `rqana` (ex. "<0,05") et numérique `valtraduite` ;
  limites `limitequal` / `refqual` ; conformités `plvconformitebacterio`, `plvconformitechimique`,
  `plvconformitereferencebact`, `plvconformitereferencechim`. Équivalents dans l'API Hub'Eau :
  `limite_qualite_parametre`, `reference_qualite_parametre`, `conformite_limites_bact_prelevement`, etc.
- API Hub'Eau (mêmes données) : https://hubeau.eaufrance.fr/page/api-qualite-eau-potable — utile pour vérifier une commune,
  mais profondeur limitée à 20 000 résultats : pas pour le traitement national.

## Stack
- Python ≥ 3.11, environnement virtuel `.venv`, `requirements.txt` épinglé avec les versions exactes installées.
- Streamlit ≥ 1.33 (prendre la dernière stable), pandas, DuckDB, pyarrow, Plotly, requests, pytest.
  pydeck seulement si une carte à beaucoup de points l'exige. geopandas n'est pas nécessaire (GeoJSON + Plotly suffisent).
- Navigation multipage avec `st.navigation` / `st.Page`.
- DuckDB : régler `memory_limit` et `temp_directory` (dans `data/interim/`) selon la RAM de la machine ;
  lire d'abord en texte (`all_varchar`) puis convertir proprement (virgules décimales, préfixes "<", dates).

## Architecture (reprend la structure recommandée dans les consignes)
```
app.py                  # page config, navigation, sidebar globale
config.py               # chemins, constantes, seuils, poids du score, SEED
sections/               # une page = un fichier
  intro.py  comprendre.py  ma_commune.py  comparer.py  overview.py
  deep_dives.py  data_quality.py  conclusions.py  (bouteille.py en bonus)
utils/
  io.py                 # chargement Parquet (cache), connexion DuckDB, licence/sources
  prep.py               # parsing valeurs et limites, familles de paramètres, features
  score.py              # score /100, sous-scores, note A–E, confiance, rapport « pourquoi »
  viz.py                # graphes au style commun (palette, axes, unités, source, caption)
scripts/
  01_download.py  02_build_parquet.py  03_build_aggregates.py  04_referentiels.py
data/raw/ (gitignoré)   data/interim/ (gitignoré)   data/processed/ (commité, petit)
tests/                  # pytest
docs/                   # consignes.pdf, CAHIER_DES_CHARGES.md, AVANCEMENT.md, data_dictionary.md,
                        # sources.md, storyboard.md, script_video.md, eau-distrib-documentation.pdf
README.md  requirements.txt  Makefile  .gitignore  .streamlit/config.toml
```

## Déploiement (Streamlit Community Cloud)
- Mémoire disponible par app : environ 690 Mo à 2,7 Go → l'app ne lit QUE `data/processed/`.
- GitHub refuse les fichiers de plus de 100 Mo : viser < 50 Mo par fichier et ~150 Mo maximum au total dans `data/processed/`. Mesurer.
- Tout chargement passe par `@st.cache_data` (et `@st.cache_resource` pour une connexion DuckDB).
  Les agrégations lourdes sont faites dans les scripts, jamais dans l'app.
- Un clone propre + installation + `streamlit run app.py` doit fonctionner SANS les données brutes.

## Storytelling, visualisation, accessibilité
- Chaque section s'ouvre sur une phrase-titre qui énonce l'insight, calculée depuis les données (jamais inventée).
- Axes titrés avec unités, source sous chaque graphe, lignes de seuil réglementaire, annotations des changements
  (ex. contrôle des PFAS obligatoire depuis le 01/01/2026).
- Palette lisible par les daltoniens ; jamais la couleur seule pour dire bien/mal (ajouter texte, icône ou motif).
  Contrastes lisibles en thème clair et sombre.
- Texte alternatif : une `st.caption` d'une phrase sous chaque graphe qui décrit ce qu'il montre.
- Chaque contrôle de la sidebar change quelque chose d'utile à l'histoire ; `help=` sur les notions techniques.
- Ton pédagogique et honnête. Le score est un indicateur pédagogique, PAS un avis sanitaire (l'avis officiel est celui de l'ARS).
  Corrélation ≠ causalité. Absence de mesure ≠ absence de polluant.

## Commandes (créées en phase 1 ; le README donne aussi la version PowerShell sans `make`, car on est sous Windows)
- `make setup` → venv + dépendances
- `make data` → scripts 01 → 04 (idempotents, avec cache)
- `make test` → pytest
- `make run` → `streamlit run app.py`

# Cahier des charges : « Mon eau du robinet est-elle bonne ? »

Projet individuel EFREI 2026 (Streamlit Dashboard). Ce document traduit les consignes (`docs/consignes.pdf`)
en plan concret. En cas de conflit, les consignes du prof priment.

---

## 1. Ce que demande le prof (résumé fidèle des consignes)

**Livrables**
- App Streamlit déployable (Streamlit Community Cloud), narratif cohérent, composants interactifs.
- Vidéo de démo de 2 à 4 minutes (l'histoire + les interactions).
- Zip `StApp26_<n° étudiant>_<NOM>_DAI.zip` contenant : le dataset ou son lien, le README, le code Python.
- À soumettre : URL de l'app déployée, lien du repo (code + rapport), storyboard + lien de la vidéo.

**Exigences techniques minimales**
- Streamlit ≥ 1.33.
- Sidebar : filtres, plage de dates, région, choix de variable.
- Au moins 3 visuels interactifs avec infobulles (lignes, barres, carte…).
- Au moins une carte (on a de la géographie).
- En-tête de KPIs qui réagissent aux filtres.
- Section qualité des données : valeurs manquantes, doublons, contrôles de validation.
- Performance : `st.cache_data`, jointures efficaces, pré-agrégation.
- Accessibilité : texte alternatif, contrastes lisibles, axes et unités étiquetés.
- Reproductibilité : dépendances épinglées, fonctionne depuis un clone propre, Makefile ou instructions simples,
  script de téléchargement des données avec cache (pas de gros fichiers bruts dans le repo), constantes / seed pour tout échantillonnage.
- Éthique : documenter collecte, biais et limites ; respecter et citer les licences ; ne pas surinterpréter (pas de causalité abusive).

**Narratif obligatoire** : Hook → Contexte → Insight(s) clé(s) → Implications / prochaines étapes.
Patterns combinés ici : comparaison de territoires (carte + small multiples), classements & distributions,
avant/après dans le temps, what-if (pondérations du score).

**Barème (100 pts)** : Narratif & problématique 25 · Travail sur les données 25 · Visualisation & UX 25 · Qualité d'ingénierie 15 · Communication 10.

---

## 2. Public, questions, messages

**Public principal** : un habitant qui se demande si l'eau de son robinet est bonne.
**Public secondaire** : élu, journaliste, enseignant qui veut voir où sont les problèmes en France.

**Questions auxquelles l'app répond**
- Q1. Mon eau est-elle bonne ? → score /100, note A–E, rapport « pourquoi ».
- Q2. Qu'y a-t-il dans l'eau, et qu'est-ce qui est grave ou non ? → page pédagogique par famille de paramètres.
- Q3. Où sont les problèmes en France ? → carte, classements, distributions.
- Q4. Grande ville vs petite commune ? Montagne vs littoral méditerranéen ? Urbain vs rural ? → comparaisons de communes (ex. Paris vs Villejuif) et de groupes.
- Q5. Est-ce que ça s'améliore depuis 2016 ? → évolution, en tenant compte des changements de surveillance.
- Q6 (bonus). Mon eau du robinet vs les eaux en bouteille ?

**Hypothèses à TESTER** (ne les écrire comme conclusions qu'après calcul ; les réfuter est aussi un résultat) :
- H1. La grande majorité des prélèvements sont conformes ; les non-conformités se concentrent dans de petites UDI.
- H2. Les problèmes bactériologiques et chimiques n'ont pas la même géographie.
- H3. Une partie des « nouvelles » non-conformités vient de paramètres ajoutés à la surveillance (métabolites de pesticides,
  PFAS en 2026) plutôt que d'une dégradation de l'eau.
- H4. La dureté (calcaire) varie énormément selon les territoires, sans enjeu sanitaire.

**Accroche possible** (affirmation de la page officielle du jeu de données) : l'eau du robinet est présentée comme
l'aliment le plus contrôlé en France, avec de l'ordre de 12 millions d'analyses par an. « Mais que disent-elles de TON eau ? »

---

## 3. Storyboard (ordre des pages = ordre du récit)

| # | Page (fichier) | Rôle | Contenu | Visuels / interactions |
|---|---|---|---|---|
| 1 | Accueil (`intro.py`) | Hook + contexte | Question, KPIs nationaux, comment marche le contrôle (ARS, UDI, prélèvements, limites vs références), sources, licence, avertissements | `st.metric` avec delta vs année précédente, mini-carte, champ « ta commune » |
| 2 | Comprendre l'eau (`comprendre.py`) | Contexte pédagogique | Une fiche par famille : ce que c'est, d'où ça vient, seuil, pourquoi c'est surveillé, fréquence des dépassements en France (calculée), source officielle | Expanders, barres « % de prélèvements au-dessus de la limite » par famille |
| 3 | Ma commune (`ma_commune.py`) | Cœur de l'app | Score, note, sous-scores, rapport « pourquoi », niveau de confiance, détail par UDI/quartier, historique des paramètres clés | Jauge ou barre de score, barres de sous-scores, lignes avec seuil, tableau des derniers résultats |
| 4 | Comparer (`comparer.py`) | Insights | 2 à 4 communes côte à côte ; groupes : montagne vs littoral méditerranéen, urbain vs rural, taille d'UDI, région | Small multiples, box/violin plots (des distributions, pas seulement des moyennes), tableau |
| 5 | La France de l'eau (`overview.py`) | Insights | Carte des départements, classements top/bottom N (avec nombre minimum de prélèvements), distribution des scores | Choroplèthe, barres classées, histogramme |
| 6 | Plongées (`deep_dives.py`) | Insights + what-if | Focus nitrates, pesticides, bactério, PFAS 2026, dureté ; évolution 2016→2026 ; nombre de paramètres mesurés par an ; sliders de pondération du score → effet sur le classement | Lignes avec bandes et annotations, small multiples par région, sliders |
| 7 | Qualité des données (`data_quality.py`) | Transparence | Voir §6 | Tableaux, heatmap de couverture |
| 8 | Conclusions (`conclusions.py`) | Implications | 3 à 5 insights chiffrés, que faire (habitant / collectivité), limites, prochaines étapes | Texte + 1 visuel récapitulatif |
| 9 | Robinet vs bouteille (`bouteille.py`) | Bonus | Voir §7 | Nuage calcium/magnésium, plus proches voisins |

**Sidebar globale** : période (années), région/département, famille de paramètres (choix de variable), type de commune.
La commune choisie est gardée en `st.session_state` (et partageable via `st.query_params` si c'est simple).
Recherche de commune rapide (pas une liste brute de 35 000 noms) et gestion des homonymes (nom + département).

**KPIs liés aux filtres** : % de prélèvements conformes (bactério / physico-chimie), nombre de communes avec au moins
une non-conformité, population de ces communes (borne haute, voir §6), score médian.

---

## 4. Méthode du score /100 (`utils/score.py`, documentée dans l'app et le README)

**Principes** : transparent, reproductible, fondé sur les seuils officiels présents dans les données
(limites de qualité = enjeu sanitaire ; références de qualité = indicateurs / confort), testé,
juste envers les grandes villes (qui font beaucoup plus de prélèvements) comme envers les petites communes.

**Unité de calcul** : UDI × période. Score de la commune = moyenne des UDI qui la desservent ;
s'il y en a plusieurs, afficher aussi le détail et la pire UDI.

**Fenêtres** : « situation actuelle » = 12 derniers mois pour la microbiologie et le confort, 36 derniers mois pour la
chimie (les analyses complètes sont moins fréquentes dans les petites UDI) ; historique = année civile. À documenter.

**Étapes**
1. Parser chaque résultat : valeur numérique, drapeau « < limite de quantification » (non quantifié → compté à part,
   valeur 0 pour le calcul des dépassements), unité.
2. Parser les limites : opérateur (≤, ≥, intervalle comme le pH), valeur, unité ; vérifier que l'unité du résultat
   et celle de la limite concordent.
3. Classer chaque paramètre dans une famille :
   - A. Microbiologie (limites) : E. coli, entérocoques…
   - B. Chimie à enjeu sanitaire (limites) : nitrates/nitrites, pesticides et métabolites, PFAS, métaux et métalloïdes
     (plomb, arsenic…), sous-produits de désinfection, autres.
   - C. Indicateurs et confort (références) : turbidité, couleur/odeur/saveur, fer, manganèse, aluminium,
     conductivité, pH, ammonium, bactéries coliformes…
   - D. Information sans pénalité : dureté, calcium, magnésium, température…
4. Sous-scores, proposition de départ, à ajuster et justifier en phase 3 :
   - Micro : `S = 100 × (1 − t)^k`, t = part des prélèvements non conformes aux limites bactériologiques, k = 10
     (0,5 % de non-conformes → ≈ 95 ; 5 % → ≈ 60).
   - Chimie : pour chaque paramètre, `r = max / limite` (ou P95 / limite si ≥ 10 mesures).
     Pénalité `g(r)` : 0 si r ≤ 0,5 ; de 0 à 20 entre 0,5 et 1 ; de 20 à 80 entre 1 et 2 ; 80 au-delà.
     `S = 100 − pire pénalité − 0,25 × somme des autres pénalités`, borné entre 0 et 100.
   - Confort : même logique, pénalité plafonnée plus bas (ex. 50).
5. Score global = moyenne pondérée des familles MESURÉES. Poids par défaut 0,4 (micro) / 0,4 (chimie) / 0,2 (confort),
   dans `config.py` et modifiables par les sliders what-if. Une famille non mesurée n'est JAMAIS comptée comme parfaite :
   elle est exclue du calcul et fait baisser la confiance.
6. Note : A ≥ 90 · B ≥ 75 · C ≥ 60 · D ≥ 40 · E < 40. Confiance (élevée / moyenne / faible) selon le nombre de
   prélèvements et de familles mesurées.
7. Rapport « pourquoi » généré par règles (pas d'IA dans l'app) : points forts, points de vigilance (paramètre,
   valeur max, limite, date), paramètres non mesurés. Exemples de phrases :
   « ✅ 100 % des 48 prélèvements bactériologiques conformes » · « ⚠️ Nitrates : max 38 mg/L pour une limite de 50 mg/L » ·
   « ℹ️ Eau dure : calcaire, mais sans risque sanitaire » · « ❔ PFAS pas encore mesurés sur ce réseau ».

**Validation obligatoire du score**
- Cohérence avec les conclusions officielles de conformité des prélèvements (les UDI avec non-conformités officielles
  doivent avoir des scores plus bas).
- Sensibilité : corrélation de rang (Spearman) entre les classements obtenus avec différents poids et paramètres ;
  résultat montré dans `deep_dives`.
- Tests unitaires sur données synthétiques (UDI parfaite = 100 ; un dépassement de nitrates fait baisser la chimie ;
  famille absente ≠ 100 ; etc.).
- 5 communes témoins inspectées à la main : Paris, Villejuif, une commune de montagne, une commune du littoral
  méditerranéen, une petite commune rurale.

**Seuils de la page pédagogique** (à recouper avec les colonnes de limites des données et l'arrêté du 11 janvier 2007 modifié) :

| Paramètre | Limite de qualité |
|---|---|
| E. coli, entérocoques | 0 / 100 mL |
| Nitrates | 50 mg/L |
| Pesticides | 0,1 µg/L par substance (0,03 µg/L pour quelques-unes), 0,5 µg/L pour le total |
| Somme de 20 PFAS | 0,1 µg/L, contrôle obligatoire depuis le 01/01/2026 |
| Plomb | 10 µg/L |
| Arsenic | 10 µg/L |

Pour tout autre seuil et pour tout effet sur la santé : source officielle (ministère de la Santé, ARS, ANSES, OMS)
citée dans `docs/sources.md`. Si l'app parle de « microparticules / microplastiques » : vérifier s'il existe des
paramètres correspondants dans les données ; sinon le dire comme une limite, sans extrapoler.

---

## 5. Pipeline de données

- `01_download.py` : liste les ressources via l'API data.gouv.fr, ne télécharge que ce qui manque ou a changé
  (taille/date), idempotent. Si les fichiers sont déjà dans `data/raw/`, ne rien retélécharger.
- `02_build_parquet.py` : extraire UNE année à la fois dans `data/interim/`, la convertir en Parquet avec DuckDB
  (types explicites, virgules décimales, dates), puis supprimer le texte extrait (jamais les fichiers de `data/raw/`).
  Commencer par la dernière année complète pour tester, puis toutes les années.
- `03_build_aggregates.py` : petites tables pour l'app dans `data/processed/`, par exemple :
  - `dim_communes` : code INSEE, nom, département, région, population, latitude/longitude, typologies
  - `bridge_commune_udi` : année, INSEE, UDI, quartier, dédoublonné
  - `params_catalog` : code, libellé, famille, unité, limite/référence, nombre de mesures, 1re année mesurée
  - `udi_family_year` et `udi_param_year` (~30 paramètres clés) : n, n quantifiés, moyenne, max, P95, n dépassements
  - `commune_scores` : commune × période → score, sous-scores, note, confiance, raisons
  - `dept_year`, `national_year` : KPIs et carte
  - `data_quality` : tous les contrôles du §6, calculés sur les données brutes
- `04_referentiels.py` :
  - Communes (code, nom, département, région, population, centre) via l'API officielle Découpage administratif :
    `https://geo.api.gouv.fr/communes?fields=code,nom,codeDepartement,codeRegion,population,centre&format=json`
    vérifier le cas de Paris/Lyon/Marseille (arrondissements) face aux codes du dataset.
  - Contours des départements en GeoJSON simplifié (source et licence à citer).
  - Typologies pour les comparaisons : zone de montagne (loi Montagne), communes littorales, grille de densité INSEE
    (urbain/rural), de préférence depuis l'Observatoire des territoires ou l'INSEE. Si une source n'est pas trouvable
    rapidement, fallback documenté : « littoral méditerranéen » = départements côtiers 06, 11, 13, 30, 34, 66, 83, 2A, 2B.
- Features utiles : famille de paramètre, ratio valeur/limite, taille d'UDI approchée (nombre de communes desservies,
  population cumulée des communes desservies, nombre de prélèvements par an), typologie de la commune.
- Communes nouvelles (fusions 2016–2026) : les codes INSEE changent. Utiliser la table de passage INSEE si le temps
  le permet, sinon documenter la limite.
- Contrôles automatiques en fin de pipeline : nombres de lignes, clés uniques, pas d'explosion de lignes après une
  jointure, taille des fichiers de `data/processed/`.

---

## 6. Qualité des données (page dédiée + table `data_quality`)

- Valeurs manquantes par colonne et par année ; doublons (prélèvements, couples prélèvement × paramètre).
- Intégrité : résultats sans prélèvement, prélèvements sans UDI, codes INSEE inconnus du référentiel.
- Validité : dates hors période, valeurs négatives, unités incohérentes pour un même paramètre, limites non parsables,
  valeurs extrêmes à vérifier.
- Couverture : prélèvements par UDI et par an, familles mesurées, paramètres apparus au fil du temps
  (graphique « nombre de paramètres distincts mesurés par an »).
- Biais et limites à expliquer dans l'app : fréquence de contrôle qui dépend de la taille du réseau ; prélèvements
  faits en amont mais rattachés à l'UDI ; 2026 partielle ; DROM incomplets ; correction et rattrapage annoncés par
  le producteur ; population par UDI inconnue, donc les KPIs de population sont des bornes hautes.

---

## 7. Bonus : robinet vs bouteille (seulement si tout le reste est fini)

- Pas de jeu de données officiel ouvert repéré. Construire un petit CSV saisi à la main (15 à 25 eaux courantes)
  depuis les étiquettes ou les sites officiels des marques : marque, type, Ca, Mg, Na, K, HCO3, SO4, Cl, NO3, F,
  résidu sec, URL source, date du relevé. Source hors des portails approuvés → présenter clairement comme un bonus séparé.
- Comparer uniquement la composition minérale : « à quelle eau en bouteille ressemble mon eau du robinet ? »
  (plus proche voisin sur un profil standardisé) ; appliquer les mentions d'étiquetage à l'eau du robinet
  (ex. « pauvre en sodium » < 20 mg/L, « calcique » > 150 mg/L, « magnésienne » > 50 mg/L, à vérifier dans
  la directive 2009/54/CE, annexe III).
- Aucune conclusion sur la sécurité globale : les étiquettes n'indiquent ni pesticides ni PFAS.

---

## 8. Phases (STOP + validation à la fin de chacune)

0. **Reconnaissance (lecture seule)** : inventaire des fichiers (années, tailles, types, variantes), encodage,
   séparateur, schémas exacts, 10 lignes d'exemple par type, nombre de lignes (DuckDB), valeurs distinctes des
   colonnes de conformité, formats des valeurs et des limites, les 40 paramètres les plus mesurés (unité, limite),
   comparaison avec les tailles/dates annoncées par l'API data.gouv.fr, RAM et espace disque libres.
   → `docs/data_dictionary.md`, `docs/AVANCEMENT.md`, téléchargement du PDF de documentation dans `docs/`.
1. **Setup** : arborescence, venv, `requirements.txt`, Makefile, `.gitignore`, `git init`, `config.py`, README squelette.
2. **Pipeline** : scripts 01 → 04, Parquet, agrégats, référentiels, contrôles automatiques.
3. **Score** : implémentation, tests, analyse de sensibilité, communes témoins.
4. **App** : pages dans l'ordre du storyboard, sidebar, KPIs, carte, comparaisons.
5. **Finitions** : phrases-titres chiffrées, annotations, accessibilité, temps de chargement, relecture des textes.
6. **Livraison** : README complet (il sert de rapport), `docs/storyboard.md`, `docs/script_video.md` (2–4 min, minuté),
   instructions pas à pas pour GitHub + Streamlit Community Cloud, zip final vérifié (sans données brutes).
7. **Bonus** bouteille.

---

## 9. Planning (rendu samedi 24 octobre à 12:00)

- Lundi 19 : phases 0 et 1
- Mardi 20 : phase 2 (+ début de la 3)
- Mercredi 21 : phase 3 + phase 4 (pages principales)
- Jeudi 22 : fin de la phase 4, phase 5, déploiement → 1re remise
- Vendredi 23 : phase 6 (l'étudiant enregistre la vidéo), bonus si de l'avance
- Samedi 24 au matin : vérifications et remise finale, aucune nouvelle fonctionnalité

Plan B si le traitement de toutes les années est trop lent : traiter 2019–2026, ou 2016 + 2020 + 2025 pour
l'avant/après, et le documenter.

---

## 10. Barème → preuves dans le projet

| Critère | Ce qui le démontre |
|---|---|
| Narratif (25) | Public et questions annoncés sur l'accueil, phrases-titres chiffrées, storyboard aligné sur les pages, conclusions + implications |
| Données (25) | Pipeline reproductible, dictionnaire des données, nettoyage documenté (< LQ, unités, doublons, jointures n-n), contrôles et tests, features (familles, score, typologies, population), page qualité |
| Visualisation & UX (25) | Graphes adaptés (carte, small multiples, distributions, lignes avec seuils), annotations, légendes, palette accessible, interactions utiles |
| Ingénierie (15) | Structure modulaire, cache, pré-agrégation, requirements épinglés, Makefile, tests, temps de chargement, README |
| Communication (10) | README clair, vidéo de 2–4 min, transparence sur les limites et les incertitudes |

---

## 11. Définition de « terminé »

- Clone propre + installation + `streamlit run app.py` fonctionne sans les données brutes.
- `make data` reconstruit `data/processed/` depuis zéro.
- Tests verts, aucune page ne plante, app déployée et accessible publiquement.
- README : question, public, données (source, licence, date de mise à jour), méthode, insights, limites,
  instructions (avec et sans make), structure du projet, section « Outils » qui mentionne l'usage d'un assistant IA
  (selon la politique du cours).
- Zip au bon nom contenant le code, le README et le lien du dataset ; aucune donnée brute.

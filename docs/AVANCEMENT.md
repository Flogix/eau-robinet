# AVANCEMENT — « Is my tap water good? »

Journal du projet (mémoire entre sessions). Le plus récent en haut de chaque section.
Rendu : **samedi 24/10/2026 à 12:00** — 1re remise visée jeudi 22 au soir.

## État actuel

| Phase | Statut | Date |
|---|---|---|
| 0. Reconnaissance (lecture seule) | ✅ terminée — en attente de validation | 19/10 |
| 1. Setup | ⏳ à faire | prévu 19/10 |
| 2. Pipeline | ⏳ | prévu 20/10 |
| 3. Score | ⏳ | prévu 21/10 |
| 4. App | ⏳ | prévu 21–22/10 |
| 5. Finitions | ⏳ | prévu 22/10 |
| 6. Livraison | ⏳ | prévu 23/10 |
| 7. Bonus bouteille | hors périmètre (accord de Florian requis) | — |

## Environnement (mesuré le 19/10/2026)

- Windows 11, 16 cœurs logiques, RAM 15,7 Go (≈ 3,8 Go libres au moment du test), disque C: 117 Go libres.
- Python : 3.12.9 (`python`), 3.13 et 3.9 aussi installés (`py -0p`). `.venv` créé en **Python 3.12.9**.
- Paquets installés à ce stade (non encore épinglés dans `requirements.txt`) : duckdb 1.5.6, pandas 3.0.6, pyarrow 26.0.0.
- DuckDB : `memory_limit=4GB`, `threads=8`, `temp_directory=data/interim/duckdb_tmp`.
- ⚠️ Un dépôt git vide existe **à la racine du disque `C:\.git`** (créé le 09/11/2023, aucun commit). Le dossier du projet
  est donc « dans » ce dépôt. Pas touché. À traiter avant le `git init` de la phase 1 (voir questions).
- ⚠️ `docs/consignes.pdf` n'existe pas : les consignes sont dans `docs/IndividualStudentPRJ_ Data StorytellingDashboardWithStreamlit2026.pdf` (lues en entier).

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
- Expliquer l'écart chimie « recalculé vs officiel » (dérogations `D`, limites multiples) — phase 2.
- Trouver une **source officielle** sur le statut des métabolites « non pertinents » avant d'en parler dans l'app.
- Règle terrain (T) vs labo (L) quand un paramètre est mesuré deux fois dans un prélèvement.

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
- 19/10 — Toutes les années traitées (pas de plan B). Raison : volumétrie maîtrisée grâce à DuckDB + Parquet.
- 19/10 — `.venv` en Python 3.12.9 (version stable déjà installée ; même version à choisir sur Streamlit Community Cloud, à confirmer au déploiement).

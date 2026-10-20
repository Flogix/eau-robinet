# Dictionnaire des données : contrôle sanitaire de l'eau distribuée (2016 → 2026)

> Phase 0 (reconnaissance), 19/10/2026. Tous les chiffres ci-dessous sont **mesurés** sur les fichiers locaux
> avec DuckDB 1.5.6. Requêtes reproductibles : `scripts/explore/sql/*.sql` exécutées par `scripts/explore/q.py`
> sur la copie Parquet brute produite par `scripts/explore/p0_extract_to_parquet.py`.
> Description officielle des champs : `docs/eau-distrib-documentation.pdf` (v7 du 03/09/2021).

## 1. Source et fichiers

- Jeu : « Résultats du contrôle sanitaire de l'eau distribuée commune par commune », Ministère des Solidarités et de la Santé
  (SISE-Eaux, DGS/EA4), Licence Ouverte 2.0, dernière mise à jour du jeu le **05/10/2026** (API data.gouv.fr).
- Page : https://www.data.gouv.fr/datasets/resultats-du-controle-sanitaire-de-leau-distribuee-commune-par-commune
- 11 zips nationaux locaux dans `data/raw/dis/` (non modifiés). **Taille ET empreinte SHA1 identiques à l'API** pour
  les 11 zips et pour le PDF de documentation → rien à retélécharger, les fichiers locaux sont les versions en ligne.

| Zip | Taille (octets) | Date de la ressource (API) | PLV txt | RESULT txt | COM_UDI txt |
|---|---:|---|---:|---:|---:|
| dis-2016.zip | 242 496 598 | 2023-08-17 | 134 Mo | 1 767 Mo | 3,9 Mo |
| dis-2017.zip | 261 395 007 | 2023-08-16 | 135 Mo | 1 857 Mo | 3,9 Mo |
| dis-2018.zip | 269 372 524 | 2023-08-16 | 137 Mo | 1 901 Mo | 3,9 Mo |
| dis-2019.zip | 270 261 277 | 2023-08-16 | 139 Mo | 1 904 Mo | 3,9 Mo |
| dis-2020.zip | 274 406 666 | 2023-08-11 | 139 Mo | 1 917 Mo | 3,9 Mo |
| dis-2021.zip | 307 743 768 | 2026-07-20 | 137 Mo | 2 057 Mo | 3,9 Mo |
| dis-2022.zip | 307 961 806 | 2026-07-17 | 138 Mo | 2 057 Mo | 3,9 Mo |
| dis-2023.zip | 292 247 398 | 2026-07-17 | 139 Mo | 1 982 Mo | 3,9 Mo |
| dis-2024.zip | 288 286 468 | 2026-07-09 | 139 Mo | 1 961 Mo | 3,9 Mo |
| dis-2025.zip | 290 571 363 | 2026-07-10 | 138 Mo | 1 970 Mo | 4,0 Mo |
| dis-2026.zip | 199 658 053 | 2026-10-05 | 69 Mo | 1 290 Mo | 3,9 Mo |

- Chaque zip contient 3 fichiers : `DIS_PLV_<année>.txt`, `DIS_RESULT_<année>.txt`, `DIS_COM_UDI_<année>.txt`
  (attention : `COM_UDI`, et non `UDI_COM` comme dans la doc). Total texte ≈ 22 Go, dont ≈ 20,7 Go pour RESULT.
- Les fichiers 2021 → 2025 ont été republiés en juillet 2026, 2016 → 2020 datent d'août 2023 (dates de l'API).
  C'est cohérent avec le rattrapage annoncé par le producteur, mais on ne sait pas quelles années il concernait exactement.
- Copie Parquet brute (tout en texte, compression zstd) : **428 Mo** au total dans `data/interim/raw_parquet/`
  (RESULT 361 Mo, PLV 57 Mo, COM_UDI 10 Mo). Conversion des 11 années en ≈ 4 min.

## 2. Format physique (identique pour les 33 fichiers)

- CSV, séparateur `,`, champs entre guillemets `"`, 1 ligne d'en-tête, fins de ligne LF (pas CRLF), **UTF-8 sans BOM**.
- Champ vide `""` ou vide sans guillemets → lu comme NULL par DuckDB (réglage par défaut).
- Contrôle de lecture : pour les 33 fichiers, nombre de lignes lues par DuckDB = nombre de fins de ligne − 1 (en-tête).
  **Aucune ligne rejetée, aucun retour à la ligne dans un champ.**
- Les en-têtes sont **identiques de 2016 à 2026** pour chaque type de fichier (pas de dérive de schéma).
- Décimales : `rqana` utilise surtout la **virgule** (`11,00`, `<0,005`) ; `valtraduite` utilise le **point** (`560.000000`) ;
  `limitequal` / `refqual` mélangent **les deux** (`<=0,1 µg/L` et `<=0.1 µg/L`).

## 3. Volumétrie par année

| Année | Lignes PLV | Prélèvements distincts | Couples prélèvement × UDI | Lignes RESULT | Paramètres distincts | Lignes COM_UDI | Communes | UDI | Dates PLV |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2016 | 398 366 | 270 626 | 398 366 | 11 448 292 | 1 276 | 49 186 | 34 669 | 23 267 | 02/01 → 30/12 |
| 2017 | 402 015 | 273 937 | 402 015 | 12 017 782 | 1 276 | 49 247 | 34 682 | 23 304 | 02/01 → 29/12 |
| 2018 | 403 663 | 276 038 | 403 663 | 12 309 359 | 1 277 | 49 335 | 34 735 | 23 340 | 01/01 → 31/12 |
| 2019 | 409 081 | 279 678 | 409 081 | 12 321 161 | 1 264 | 49 403 | 34 772 | 23 377 | 02/01 → 31/12 |
| 2020 | 406 865 | 278 588 | 406 865 | 12 406 530 | 1 308 | 49 436 | 34 788 | 23 397 | 01/01 → 31/12 |
| 2021 | 402 874 | 286 231 | 402 874 | 13 293 889 | 1 349 | 49 622 | 34 814 | 23 665 | 04/01 → 31/12 |
| 2022 | 408 107 | 290 091 | 408 107 | 13 293 427 | 1 369 | 49 680 | 34 859 | 23 576 | 01/01 → 30/12 |
| 2023 | 411 970 | 292 739 | 411 970 | 12 796 992 | 1 332 | 49 673 | 34 857 | 23 434 | 02/01 → 31/12 |
| 2024 | 408 520 | 291 616 | 408 520 | 12 649 217 | 1 386 | 49 672 | 34 861 | 23 318 | 02/01 → 31/12 |
| 2025 | 409 398 | 295 134 | 409 396 | 12 630 636 | 1 405 | 49 805 | 34 818 | 23 135 | 02/01 → 31/12 |
| 2026 | 201 770 | 156 503 | 201 769 | 8 307 113 | 1 381 | 49 475 | 34 812 | 22 798 | 02/01 → **31/08** |
| **Total** | **4 262 629** | **2 991 181** | | **133 474 398** | **1 789** | | **34 945** codes | **24 461** codes | |

- **2026 est partielle : prélèvements du 02/01 au 31/08/2026** (8 mois).
- Aucune date de prélèvement hors de l'année du fichier, aucune date invalide.
- Un même `referenceprel` n'apparaît jamais dans deux fichiers annuels.
- Les 101 départements gestionnaires (`cddept`) sont présents chaque année, DROM compris (971, 972, 973, 974, 976).

## 4. Fichier PLV : prélèvements (18 colonnes)

| Colonne | Description (doc) | % NULL (toutes années) | Format observé / remarques |
|---|---|---:|---|
| `cddept` | Département gestionnaire (ARS) | 0 | 3 caractères : `001`…`095`, `02A`, `02B`, `971`…`976` |
| `cdreseau` | Code de l'UDI | 0 | 9 caractères, ex. `075000221` |
| `inseecommuneprinc` | Commune du point de surveillance | 0 | 5 car. ; 2 codes étrangers : `99001` Vintimille (421 lignes), `99004` Meix-devant-Virton (2) |
| `nomcommuneprinc` | Nom de cette commune | 0 | majuscules |
| `cdreseauamont` | Installation amont (si prélèvement en amont) | 53,6 | 9 car. ; renseigné ⇔ prélèvement fait en amont |
| `nomreseauamont` | Nom de l'installation amont | 53,6 | |
| `pourcentdebit` | Part du débit de l'amont dans l'UDI | 56,7 | texte `"100 %"`, `"50 %"`… → à convertir en nombre |
| `referenceprel` | Identifiant du prélèvement | 0 | 11 car. **Non unique dans PLV** (voir §7) |
| `dateprel` | Date du prélèvement | 0 | `AAAA-MM-JJ`, 100 % parsable |
| `heureprel` | Heure | 0,14 | `09h11` (quelques formats anormaux : `9:h54`, `h`), peu utile |
| `conclusionprel` | Conclusion sanitaire de l'ARS (texte libre) | 0 | ~131 000 textes distincts, parfois tabulation en tête |
| `ugelib` / `distrlib` / `moalib` | Unité de gestion / exploitant / maître d'ouvrage | 0 | texte libre, à `trim()` |
| `plvconformitebacterio` | Conformité bactério aux **limites** | 0 (58 lignes vides) | `C` conforme, `N` non conforme, `S` sans objet |
| `plvconformitechimique` | Conformité physico-chimique aux **limites** | 0 (58 vides) | `C`, `N`, `D` (conforme sous dérogation), `S` |
| `plvconformitereferencebact` | Conformité bactério aux **références** | 0 (58 vides) | `C`, `N`, `S` |
| `plvconformitereferencechim` | Conformité chimique aux **références** | 0 (58 vides) | `C`, `N`, `S`, et 15 lignes `D` (non documenté) |

Comptes toutes années (lignes PLV) : bactério C 3 892 002 · S 311 170 · N 59 399 ; chimique C 4 147 824 · N 107 726 · D 4 728 · S 2 293 ;
réf. bactério N 163 310 ; réf. chimique N 708 003.

## 5. Fichier RESULT : résultats d'analyse (17 colonnes)

| Colonne | Description (doc) | % NULL | Format observé / remarques |
|---|---|---:|---|
| `cddept` | Département gestionnaire | 0 | |
| `referenceprel` | Prélèvement (clé vers PLV) | 0 | |
| `cdparametresiseeaux` | Code SISE du paramètre | 0 | ex. `NO3`, `ECOLI`, `PESTOT`, `SPFAS`, **clé de paramètre retenue** |
| `cdparametre` | Code SANDRE | 0,09 | numérique en texte |
| `libmajparametre` / `libminparametre` | Libellés | 0 | `libmin` lisible (accents OK) |
| `libwebparametre` | Libellé « grand public » | **100** | **toujours vide** → inutilisable |
| `qualitparam` | `O` qualitatif / `N` quantitatif | 0 | N : 123,2 M lignes ; O : 10,2 M |
| `insituana` | `T` terrain / `L` laboratoire | 0 | L : 118,0 M ; T : 15,5 M |
| `rqana` | Résultat brut (texte) | 0,07 | voir §8 |
| `cdunitereferencesiseeaux` | Unité | 0 | 72 unités ; top : `µg/L`, `SANS OBJET`, `n/(100mL)`, `mg/L`, `mg(Cl2)/L` |
| `cdunitereference` | Code SANDRE de l'unité | 0 | |
| `limitequal` | Limite(s) de qualité en vigueur | 43,8 | texte, voir §9 |
| `refqual` | Référence(s) de qualité en vigueur | 80,3 | texte, voir §9 |
| `valtraduite` | Valeur numérique traduite | 0,79 | décimale avec **point**, toujours numérique quand non NULL |
| `casparam` | Code CAS | 41,8 | |
| `referenceanl` | Identifiant d'analyse labo | 11,6 | NULL pour les mesures de terrain |

- 75,0 M lignes ont une limite, 26,3 M une référence, 0,28 M les deux.
- 11 paramètres ont 2 écritures d'unité équivalentes (ex. `mg/L` | `mg(Mg)/L` pour le magnésium, `hPa` | `mbar`) :
  notation différente, même grandeur → à normaliser, pas d'incohérence réelle.

## 6. Fichier COM_UDI : lien commune ↔ UDI (6 colonnes)

| Colonne | Description (doc) | % NULL | Format observé / remarques |
|---|---|---:|---|
| `inseecommune` | Code INSEE de la commune desservie | 0 | 5 car., 100 % au format `[0-9][0-9AB][0-9]{3}` |
| `nomcommune` | Nom | 0 | |
| `quartier` | Quartier desservi | 0 | `-` = commune entière (25 561 lignes en 2026) ; texte libre très hétérogène (`totalité`, `VILLAGE`, `bourg`, `100`…) |
| `cdreseau` | Code de l'UDI | 0 | |
| `nomreseau` | Nom de l'UDI | 0 | |
| `debutalim` | Début d'alimentation | 0 | `AAAA-MM-JJ`, de 1900-01-01 (valeur par défaut probable) à 2026-08-27 |

- **Paris = un seul code `75056`** (pas d'arrondissements), desservi par 4 UDI dont les « quartiers » listent des
  arrondissements qui se recouvrent (CENTRE, NORD OUEST, SUD OUEST, EST). Lyon = `69123` (1 UDI), Marseille = `13055` (16 UDI).
- Villejuif (`94076`) : 1 UDI, `G.CHOISY MAJORITAIRE`, qui dessert 16 communes (788 couples prélèvement-UDI en 2025).
- Codes communes : 108 codes de 2016 absents en 2026, 251 codes de 2026 absents en 2016 (communes nouvelles / fusions).
- UDI : 24 461 codes au total, 22 118 présents à la fois en 2016 et en 2026.

## 7. Clés, jointures et doublons

| Contrôle | Résultat |
|---|---|
| Lignes strictement identiques (PLV, RESULT, COM_UDI, chaque année) | **0** |
| `referenceprel` unique dans PLV ? | **Non** : 2026 → 201 770 lignes pour 156 503 prélèvements |
| Clé de PLV | (`referenceprel`, `cdreseau`) : unique sauf **3 cas** au total (2025 : 2, 2026 : 1, même UDI `011001612` saisie à la fois « sur place » et comme sa propre installation amont) |
| Pourquoi un prélèvement a plusieurs lignes ? | Un prélèvement fait **en amont** (usine, captage) est rattaché à **chaque UDI aval** qu'il alimente. 2026 : 132 309 prélèvements → 1 UDI, 16 362 → 2 UDI, …, jusqu'à plus de 15 UDI |
| Date et conformités identiques entre les lignes d'un même prélèvement ? | **Oui** (0 écart en 2026) → on peut dédoublonner les conformités par `referenceprel` |
| Clé de RESULT | (`referenceprel`, `cdparametresiseeaux`, `insituana`, `referenceanl`) : **unique**, chaque année |
| Un paramètre mesuré 2 fois dans un prélèvement | 59 839 à 107 876 cas/an : surtout mesure terrain (T) + labo (L) du même paramètre (pH, chlore, température… ; 59 030 des 59 839 cas en 2026), plus rarement deux analyses labo |
| RESULT sans PLV | **0** chaque année |
| PLV sans RESULT | 0 sauf 2021 : 14, 2022 : 1, 2023 : 2, 2024 : 2, 2025 : 3 prélèvements |
| UDI de PLV absentes de COM_UDI | **0** chaque année |
| UDI de COM_UDI sans prélèvement | 0 sauf 2021 : 21, 2022 : 3, 2023 : 4, 2024 : 4, 2025 : 5 |
| Clé de COM_UDI | (`inseecommune`, `cdreseau`, `quartier`) : unique sauf 2021 : 1, 2022 : 2, 2023 : 3, 2024 : 14 doublons, qui ne diffèrent que par `debutalim` → garder la date la plus récente |
| Multiplicités commune ↔ UDI (2026) | 28 419 communes ont 1 UDI, 4 082 en ont 2, 65 en ont 10 ou plus ; 17 363 UDI desservent 1 seule commune, 156 en desservent 20 ou plus |

**Conséquence pour le pipeline** : joindre RESULT → PLV sur `referenceprel` **multiplie** les résultats d'un prélèvement amont
par le nombre d'UDI aval (lignes PLV / prélèvements distincts = ×1,43 sur 2016–2026, ×1,29 en 2026). C'est voulu pour le calcul **par UDI**, mais les statistiques
**nationales** (nombre de prélèvements, % conformes) doivent se faire sur `referenceprel` dédoublonné.
Et COM_UDI (avec quartiers) doit être réduit à (`inseecommune`, `cdreseau`) distincts avant toute jointure.

## 8. Valeurs de résultat (`rqana` → `valtraduite`)

Paramètres quantitatifs (`qualitparam = N`, 123,2 M lignes), classes de `rqana` observées :

| Classe | Lignes | `valtraduite` observée | Traitement prévu |
|---|---:|---|---|
| `<x` (sous la limite de quantification) | 87 942 072 | 0 (sauf 2 125 NULL et 12 non nulles) | drapeau `non_quantifie = vrai`, LQ = x ; valeur 0 pour les dépassements |
| nombre | 34 121 629 | = le nombre | valeur |
| `N.M.` (non mesuré) | 937 614 | NULL (1 seule exception à 0,14) | **exclure** (aucune mesure) |
| vide | 98 547 | NULL | exclure |
| `>x` | 81 506 | x | valeur (borne basse) |
| `-x` (négatif) | 22 381 | −x | légitime pour T° de l'air, CO2 agressif, écart de pH… ; 4 nitrites/nitrates/ammonium négatifs → à rejeter |
| `ILLISIBL` | 11 721 | NULL (2 lignes à 100) | exclure |
| `PRESENCE` | 11 396 | 1 | présence non quantifiée |
| `N.D.` | 11 295 | 0 | non détecté |
| `INCOMPT.` | 3 897 | 1,11 | indénombrable (microbio) : à traiter comme « > limite » |
| `?`, `TRACES`, `#NAME?`, `,81`… | < 2 500 | | cas marginaux |

- Variantes d'écriture : `< 0,1`, `<  0,026`, `<,019`, `<0.020`, `0.26`, `,71`, `11,` → parsing tolérant (espaces, virgule ou point).
- `N.M.` vient surtout de `SAV25` / `ODEUR25` (saveur, odeur par dilution), `CLO2`, `CL2TOT`, `O3` : 82 910 à 115 834 lignes/an (17 696 en 2026).
- Paramètres qualitatifs (`O`, 10,2 M lignes) : `Aucun changement anormal`, `Aspect normal`, `Eau agressive`, `OUI`… (odeur, saveur, couleur, aspect, équilibre calco-carbonique, questions sur le plomb). Pas de note chiffrée : utiles seulement pour le confort.
- La doc officielle (§1.3.1.8) donne la même table de traduction : `<XXX`→0, `TRACES`→0, `INCOMPT.`→1,11, `PRESENCE`→1, `N.D.`→0, `ILLISIBL`→NULL, `N.M.`→NULL.

## 9. Limites et références de qualité (`limitequal`, `refqual`)

- **Toutes les limites sont de la forme `<=valeur unité`** (une seule borne). Motifs (chiffres → 9) :
  `<=9,9 µg/L` (59,9 M lignes, 842 paramètres, surtout pesticides à 0,1), `<=9 n/(9mL)` (microbio, 0/100 mL),
  `<=9 µg/L`, `<=9 mg/L`, `<=9.9 µg/L`, `<=9,9 mg/L`, `<=9 µg(CN)/L`, `<=9 NFU`… plus un cas exotique
  `<=5 NG/(KG POIDS CORPOREL/J)` (3 964 lignes) qui n'est pas une concentration → à exclure du calcul.
- **Les références** sont `<=x` ou des **intervalles** `>=6,5 et <=9 unité pH`, `>=200 et <=1100 µS/cm`,
  `>=1 et <=2 SANS OBJET` (équilibre calco-carbonique).
- L'unité de la limite est écrite dans le texte : à comparer à `cdunitereferencesiseeaux` (contrôle de concordance en phase 2).
- Un même paramètre peut avoir plusieurs limites selon le point de prélèvement : nitrites `<=0,5` ou `<=0,1 mg/L`,
  turbidité limite `<=1 NFU`, références `<=0,5` ou `<=2 NFU`. **Il faut donc utiliser la limite de chaque ligne**, pas une limite par paramètre.
- Limites stables 2016 → 2026 pour NO3 (≤ 50 mg/L), Pb (≤ 10 µg/L), As (≤ 10 µg/L), E. coli (≤ 0/100 mL),
  total pesticides (≤ 0,5 µg/L), chlorure de vinyle (≤ 0,5 µg/L). Somme de 20 PFAS : ≤ 0,1 µg/L dès sa 1re mesure (2022).

### Validation du recalcul des dépassements vs conformités officielles (prélèvements distincts)

| Année | Bactério N officiel | Recalculé (valtraduite > limite, microbio) | Chimie N officiel | Recalculé (hors microbio) | Les deux |
|---|---:|---:|---:|---:|---:|
| 2016 | 6 225 | 6 220 | 5 941 | 6 035 | 5 267 |
| 2020 | 4 631 | 4 631 | 6 970 | 7 501 | 6 718 |
| 2021 | 4 795 | 4 794 | 10 912 | 11 434 | 10 653 |
| 2024 | 5 061 | 5 059 | 11 913 | 12 583 | 11 912 |
| 2025 | 4 659 | 4 659 | 8 742 | 9 609 | 8 740 |
| 2026 | 2 100 | 2 100 | 4 849 | 5 556 | 4 849 |

→ Bactériologie : le recalcul retrouve **quasi exactement** la conclusion officielle. Chimie : proche mais pas identique ;
écart **non encore expliqué**, pistes à tester en phase 2 : dérogations (`D` = conforme officiellement malgré un dépassement),
limites qui dépendent du point de prélèvement, paramètres sans limite chiffrée. Recalcul simplifié (limites `<=x` seulement,
`N.M.` exclus). Bonne base pour le score et pour sa validation.

## 10. Paramètres : top 40 (2025) et paramètres clés

| Code | Libellé | Mesures 2025 | Unité | Limite | Référence |
|---|---|---:|---|---|---|
| PH | pH | 347 218 | unité pH | | ≥6,5 et ≤9 |
| CDT25 | Conductivité à 25 °C | 280 874 | µS/cm | | ≥200 et ≤1100 |
| TEAU | Température de l'eau | 268 416 | °C | | ≤25 |
| CL2LIB | Chlore libre | 267 706 | mg(Cl2)/L | | |
| TURBNFU | Turbidité NFU | 266 955 | NFU | ≤1 | ≤0,5 / ≤2 |
| ECOLI | Escherichia coli /100 mL | 266 757 | n/(100mL) | ≤0 | |
| STRF | Entérocoques /100 mL | 266 737 | n/(100mL) | ≤0 | |
| CTF | Bactéries coliformes /100 mL | 266 661 | n/(100mL) | | ≤0 |
| GT36_44 | Bact. aér. revivifiables 36 °C | 265 926 | n/mL | | |
| GT22_68 | Bact. aér. revivifiables 22 °C | 265 563 | n/mL | | |
| CL2TOT | Chlore total | 264 829 | mg(Cl2)/L | | |
| ODQ | Odeur (qualitatif) | 261 969 |, | | |
| ASP | Aspect (qualitatif) | 253 871 |, | | |
| NH4 | Ammonium | 251 466 | mg/L | | ≤0,1 |
| SAVQ | Saveur (qualitatif) | 237 609 |, | | |
| COULQ | Couleur (qualitatif) | 192 567 |, | | |
| COULF | Coloration | 192 251 | mg(Pt)/L | | ≤15 |
| BSIR | Bact. et spores sulfito-réductrices | 161 656 | n/(100mL) | | ≤0 |
| NO3 | Nitrates | 120 503 | mg/L | ≤50 | |
| NO2 | Nitrites | 90 959 | mg/L | ≤0,5 / ≤0,1 | |
| FET | Fer total | 86 457 | µg/L | | ≤200 |
| TH | Titre hydrotimétrique (dureté) | 72 942 | °f | | |
| TAC | Titre alcalimétrique complet | 71 689 | °f | | |
| ALTMICR | Aluminium total | 68 080 | µg/L | | ≤200 |
| COT | Carbone organique total | 64 718 | mg(C)/L | | ≤2 |
| NO3_NO2 | Nitrates/50 + Nitrites/3 | 61 778 | mg/L | ≤1 | |
| SO4 | Sulfates | 58 054 | mg/L | | ≤250 |
| TEMP_PH | Température de mesure du pH | 57 814 | °C | | |
| CL | Chlorures | 57 699 | mg/L | | ≤250 |
| TA | Titre alcalimétrique | 38 238 | °f | | |
| MN | Manganèse total | 35 453 | µg/L | | ≤50 |
| CLVYL | Chlorure de vinyle monomère | 34 081 | µg/L | ≤0.5 | |
| CA | Calcium | 33 194 | mg/L | | |
| MG | Magnésium | 32 751 | mg(Mg)/L | | |
| CLF | Chloroforme | 32 741 | µg/L | ≤100 | |
| BRF | Bromoforme | 32 636 | µg/L | ≤100 | |
| DCLMBR | Dichloromonobromométhane | 32 636 | µg/L | ≤100 | |
| DBRMCL | Chlorodibromométhane | 32 631 | µg/L | ≤100 | |
| THM4 | Trihalométhanes (4 substances) | 32 583 | µg/L | ≤100 | |
| PESTOT | Total des pesticides analysés | 25 430 | µg/L | ≤0,5 | |

Autres codes utiles : `AS` arsenic (21 868 mesures en 2025, ≤10 µg/L), `PB` plomb (11 471, ≤10 µg/L), `SPFAS` somme de 20 PFAS.

### Thèmes (pour le storytelling)

- **Nombre de paramètres distincts mesurés** : 1 276 (2016) → 1 405 (2025) ; avec une limite : 790 → 827.
- **PFAS** : PFOS mesuré depuis 2016 ; les 20 PFAS de la somme réglementaire apparaissent en 2022. Somme de 20 PFAS (`SPFAS`) :

  | Année | Prélèvements mesurés | Quantifiés (> 0) | > 0,1 µg/L |
  |---|---:|---:|---:|
  | 2022 | 122 | 99 | 27 |
  | 2023 | 334 | 295 | 37 |
  | 2024 | 1 808 | 1 150 | 185 |
  | 2025 | 16 475 | 5 176 | 386 |
  | 2026 (jan.–août) | 12 236 | 3 957 | 93 |

- **Métabolites de pesticides, le même composé change de code** : `ESAMTC` (ESA-métolachlore, limite ≤0,1 µg/L)
  est mesuré de 2016 à 2023 (248 mesures en 2023) puis remplacé par `MTCESA` (même libellé, **sans limite**, depuis 2021).
  Idem `R471811` (chlorothalonil R471811, limite ≤0,1, 2022–2024) → `471811R` (sans limite, depuis 2023).
  Hypothèse à vérifier dans une source officielle avant de l'écrire : reclassement en « métabolite non pertinent ».
- **Principaux paramètres en dépassement de limite** (prélèvements distincts) :
  - 2016–2020 : E. coli et entérocoques en tête (≈ 3 000 à 4 600/an), puis nitrates (≈ 900 à 1 600), atrazine déséthyl, ESA-métolachlore.
  - 2021 : ESA-métolachlore 1er (3 894), chloridazone desphényl apparaît (2 319), total pesticides (1 958).
  - 2023–2024 : chloridazone desphényl (≈ 4 500 à 5 000) et chlorothalonil R471811 (≈ 4 200 à 4 500) devant E. coli.
  - 2025 : chloridazone desphényl (4 448), E. coli (3 073), entérocoques (3 000) ; R471811 a disparu du classement (code sans limite).
- **Références les plus dépassées en 2026** : température de l'eau (> 25 °C, 8 247 prélèvements en 8 mois contre 5 178 sur toute
  l'année 2025), coliformes, COT, turbidité.
- **Microplastiques / microparticules : aucun paramètre** dans les données (recherche sur les libellés `plasti`, `particul`).

## 11. Points d'attention pour le nettoyage (phase 2)

1. Dédoublonner PLV par `referenceprel` pour toute statistique « prélèvement » ; garder (`referenceprel`, `cdreseau`) pour le calcul par UDI ; retirer les 3 doublons (`referenceprel`, `cdreseau`).
2. COM_UDI : réduire à (`annee`, `inseecommune`, `cdreseau`) distincts ; les quartiers servent seulement à l'affichage.
3. Parser `rqana` (virgule/point, espaces, `<`, `>`, codes) en : `valeur`, `non_quantifie`, `lq`, `statut` ; exclure `N.M.`, vide, `ILLISIBL`.
4. Parser `limitequal` / `refqual` en (`borne_min`, `borne_max`, `unite`) ; ignorer `NG/(KG POIDS CORPOREL/J)`.
5. Normaliser les unités équivalentes (`mg(Mg)/L` = `mg/L`…), vérifier unité résultat = unité limite.
6. Mesures terrain + labo du même paramètre : choisir une règle (ex. garder le labo si présent), à décider.
7. Fusionner les codes « jumeaux » d'un même composé (`ESAMTC`/`MTCESA`, `R471811`/`471811R`) pour les séries temporelles, en gardant la limite **en vigueur à la date** pour le score.
8. `trim()` des textes (tabulations en tête), `pourcentdebit` → entier.
9. Codes INSEE étrangers (`99001`, `99004`) dans `inseecommuneprinc` : sans effet si l'on passe par COM_UDI.
10. Communes nouvelles : 108 codes disparus / 251 apparus entre 2016 et 2026 → raisonner sur le référentiel de l'année la plus récente.

## 12. Lignes d'exemple (10 par type, 2025, tirage reproductible graine 42 : `scripts/explore/p0_samples.py`)

**PLV** (2025)

```csv
cddept,cdreseau,inseecommuneprinc,nomcommuneprinc,cdreseauamont,nomreseauamont,pourcentdebit,referenceprel,dateprel,heureprel,conclusionprel,ugelib,distrlib,moalib,plvconformitebacterio,plvconformitechimique,plvconformitereferencebact,plvconformitereferencechim
"032","032000202","32127","ESTANG",,,,"03200096268","2025-04-24","09h14","Eau d'alimentation conforme aux exigences de qualité en vigueur pour l'ensemble des paramètres mesurés.","SETA","SETA","SETA","C","C","C","C"
"033","033000437","33263","MADIRAC",,,,"03300271315","2025-08-07","11h00","Eau d'alimentation conforme aux limites de qualité des eaux destinées à la consommation humaine pour l'ensemble des paramètres mesurés et ne satisfaisant pas à la référence de qualité concernant le paramètre température de l'eau. Valeur de chlore élevée.","SIEA PORTES DE L'ENTRE-DEUX-MERS","S.I.E.A. PORTES DE L'ENTRE 2 MERS","SIEA  PORTES DE L'ENTRE-DEUX-MERS","C","C","C","N"
"033","033001174","33069","BOUSCAT (LE)",,,,"03300274543","2025-12-15","12h20","Eau d'alimentation conforme aux exigences de qualité en vigueur pour l'ensemble des paramètres mesurés.","BORDEAUX METROPOLE","REGIE DE L'EAU BORDEAUX METROPOLE","REGIE DE L'EAU BORDEAUX METROPOLE","C","C","C","C"
"062","062000591","62523","LOISON-SOUS-LENS",,,,"06200291711","2025-05-27","10h24","Eau d'alimentation conforme aux exigences de qualité en vigueur pour l'ensemble des paramètres mesurés.","COMMUNAUTE D'AGGLO DE LENS LIEVIN","VEOLIA ARTOIS DOUAISIS","COMMUNAUTE D'AGGLOMERATION DE LENS-LIEVIN","C","C","C","C"
"062","062000754","62638","OISY-LE-VERGER","062001234","PRODUCTION OISY LE VERGER","100 %","06200295917","2025-11-06","10h38","Eau d’alimentation conforme aux exigences de qualité en vigueur, pour l’ensemble des paramètres mesurés. ","NOREADE PECQUENCOURT- ARTOIS EST","NOREADE","NOREADE PECQUENCOURT (SUD)","C","C","C","C"
"062","062004265","62604","NEUFCHATEL-HARDELOT","062000534","CAB RIVE GAUCHE","100 %","06200295041","2025-10-09","09h48","Eau d'alimentation conforme aux exigences de qualité en vigueur pour l'ensemble des paramètres mesurés.","COMM. D'AGGLO DU BOULONNAIS","VEOLIA LITTORAL AUDOMAROIS","COMMUNAUTE D'AGGLO DU BOULONNAIS","C","C","C","C"
"063","063001447","63124","COURNON-D'AUVERGNE",,,,"06300221345","2025-12-04","08h07","Eau d'alimentation conforme aux exigences de qualité en vigueur pour l'ensemble des paramètres mesurés.","CLERMONT AUVERGNE METROPOLE AEP REG","CLERMONT AUVERGNE METROPOLE AEP","CLERMONT AUVERGNE METROPOLE AEP","C","C","C","C"
"063","063001910","63265","ORLEAT",,,,"06300221585","2025-12-22","09h38","Eau d'alimentation conforme aux exigences de qualité en vigueur pour l'ensemble des paramètres mesurés.","SIAEP DORE ALLIER","SIAEP DORE ALLIER","SIAEP DORE ALLIER","C","C","C","C"
"064","064000471","64067","ASSAT",,,,"06400216111","2025-01-14","10h00","Eau d'alimentation conforme aux exigences de qualité en vigueur pour l'ensemble des paramètres mesurés.","SMEP DE LA REGION DE JURANCON","SOCIETE AGUR","SMEP DE LA REGION DE JURANCON","C","C","C","C"
"064","064001508","64354","LOUVIE-SOUBIRON","064001507","STATION QUARTIER HAUT","100 %","06400216407","2025-02-03","11h20","Eau d'alimentation conforme aux exigences de qualité en vigueur pour l'ensemble des paramètres mesurés.","LOUVIE-SOUBIRON","MAIRIE DE LOUVIE-SOUBIRON","MAIRIE DE LOUVIE-SOUBIRON","C","C","C","C"
```

**RESULT** (2025)

```csv
cddept,referenceprel,cdparametresiseeaux,cdparametre,libmajparametre,libminparametre,libwebparametre,qualitparam,insituana,rqana,cdunitereferencesiseeaux,cdunitereference,limitequal,refqual,valtraduite,casparam,referenceanl
"001","00100144364","TFU","1714","THIAZFLURON","Thiazfluron",,"N","L","<0,020","µg/L","133","<=0,1 µg/L",,"0.000000","25366-23-8","00100153448"
"001","00100144394","ASP","6489","ASPECT (QUALITATIF)","Aspect (qualitatif)",,"O","L","Aspect normal","SANS OBJET","X",,,"0.000000",,"00100153480"
"001","00100144495","NO3_NO2","6374","NITRATES/50 + NITRITES/3","Nitrates/50 + Nitrites/3",,"N","L","0,02","mg/L","162","<=1 mg/L",,"0.020000",,"00100153581"
"001","00100144647","ECOLI","1449","ESCHERICHIA COLI /100ML - MF","Escherichia coli /100ml - MF",,"N","L","<1","n/(100mL)","226","<=0 n/(100mL)",,"0.000000",,"00100153732"
"001","00100144791","TURBNFU","1295","TURBIDITÉ NÉPHÉLOMÉTRIQUE NFU","Turbidité néphélométrique NFU",,"N","L","0,29","NFU","232",,"<=2 NFU","0.290000",,"00100153876"
"001","00100144902","GT36_44","5441","BACT. AÉR. REVIVIFIABLES À 36°-44H","Bact. aér. revivifiables à 36°-44h",,"N","L","1","n/mL","222",,,"1.000000",,"00100153987"
"001","00100144971","QUIZO","2069","QUIZALOFOP","Quizalofop",,"N","L","<0,050","µg/L","133","<=0,1 µg/L",,"0.000000","76578-12-6","00100154056"
"001","00100144987","CLTHALS","7717","CHLOROTHALONIL R417888","Chlorothalonil R417888",,"N","L","<0,010","µg/L","133","<=0,1 µg/L",,"0.000000","1418095-02-9","00100154072"
"001","00100145108","ATRZ","1107","ATRAZINE","Atrazine",,"N","L","<0,005","µg/L","133","<=0,1 µg/L",,"0.000000","1912-24-9","00100154191"
"001","00100145136","PYR","1537","PYRÈNE","Pyrène",,"N","L","<0,001","µg/L","133",,,"0.000000","129-00-0","00100154219"
```

**COM_UDI** (2025)

```csv
inseecommune,nomcommune,quartier,cdreseau,nomreseau,debutalim
"33423","SAINT-JULIEN-BEYCHEVELLE","-","033001472","SAINT JULIEN BEYCHEVELLE","2010-10-15"
"38357","SAINT-ANDRE-LE-GAZ","-","038008633","ST ANDRE LE GAZ AMPERE","2025-01-07"
"45061","CEPOY","totalité","045000617","CEPOY GIROLLES CORQUILLEROY PAUCOURT","2010-09-21"
"48128","RIMEIZE","Mazel","048001711","RIMEIZE","2010-09-02"
"54075","BIONVILLE","Village / Noire Colas","054002000","BIONVILLE CENTRE/BASSE DU TOC","2010-08-10"
"60023","ARMANCOURT","-","060003906","LONGUEUIL SAINTE MARIE RÉSEAU ARCBA","2021-01-01"
"61411","SAINT-JOUIN-DE-BLAVOU","-","061000426","PERVENCHERES","2010-10-14"
"63309","SAILLANT","-","063001675","SAILLANT","2010-09-16"
"69030","BRULLIOLES","en totalité","069000013","MONTS DU LYONNAIS","2010-09-07"
"71543","TOURNUS","-","071003953","TOURNUGEOIS","2020-09-28"
```

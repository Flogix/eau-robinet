# Dataset used

Ministère des Solidarités et de la Santé, « Résultats du contrôle sanitaire de l'eau distribuée commune par commune »,
data.gouv.fr, Licence Ouverte / Open Licence 2.0, last updated on 5 October 2026.

- Dataset page: https://www.data.gouv.fr/datasets/resultats-du-controle-sanitaire-de-leau-distribuee-commune-par-commune
- List of files (URL, size, date) through the API: https://www.data.gouv.fr/api/1/datasets/resultats-du-controle-sanitaire-de-leau-distribuee-commune-par-commune/
- Producer documentation (PDF, copy in `docs/eau-distrib-documentation.pdf`): https://www.data.gouv.fr/api/1/datasets/r/36afc708-42dc-4a89-b039-7fde6bcc83d8

Files used: the yearly national files `dis-2016.zip` to `dis-2026.zip` (2026 partial, samples up to 31 August 2026),
about 3 GB of zips. They are not included here: `make data` (or `.\make.ps1 data`) downloads them with a cache and rebuilds
`data/processed/`, the small tables read by the app, which are included. The size and SHA1 of every file used are recorded
in `data/processed/source_manifest.json`. Other sources (referentials, health and regulatory texts): `docs/sources.md`.

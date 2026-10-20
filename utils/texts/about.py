"""Page "About this project": author, open code and data, how to reproduce, sources and licences, tools."""

T = {
    "about.kicker": {"en": "Credits", "fr": "Crédits"},
    "about.title": {"en": "About this project", "fr": "À propos du projet"},
    "about.lede": {
        "en": "Au robinet is a data storytelling project made by Florian Giraud, student at EFREI Paris in the Data & AI "
              "track, in 2026.",
        "fr": "Au robinet est un projet de data storytelling réalisé par Florian Giraud, étudiant à l'EFREI Paris dans la "
              "filière Data & AI, en 2026."},
    "about.why": {
        "en": "The starting point was a simple question that everyone has asked at least once in front of a tap. The "
              "answer exists, in a public file of several million samples, but nobody reads it. The goal of this app is "
              "to make that file readable for anyone, without hiding what it cannot say.",
        "fr": "Le point de départ est une question simple que chacun s'est posée au moins une fois devant un robinet. La "
              "réponse existe, dans un fichier public de plusieurs millions de prélèvements, mais personne ne le lit. Le "
              "but de cette application est de rendre ce fichier lisible par tous, sans cacher ce qu'il ne peut pas dire."},
    "about.open.kicker": {"en": "Open by design", "fr": "Ouvert par principe"},
    "about.open.title": {"en": "The code and the data are public", "fr": "Le code et les données sont publics"},
    "about.open.text": {
        "en": "Everything is on GitHub, in a public repository: [github.com/Flogix/eau-robinet](https://github.com/Flogix/eau-robinet). "
              "Anyone can download the code and the processed data, reuse them, check every number of this app and redo "
              "the whole analysis. The processed tables (about 55 MB) are in the repository, so the app runs from a "
              "simple copy; the raw files (about 3 GB of archives) are downloaded by a script that keeps them in a cache.",
        "fr": "Tout est sur GitHub, dans un dépôt public : [github.com/Flogix/eau-robinet](https://github.com/Flogix/eau-robinet). "
              "Chacun peut télécharger le code et les données traitées, les réutiliser, vérifier chaque chiffre de cette "
              "application et refaire toute l'analyse. Les tables traitées (environ 55 Mo) sont dans le dépôt, si bien que "
              "l'application tourne à partir d'une simple copie ; les fichiers bruts (environ 3 Go d'archives) sont "
              "téléchargés par un script qui les garde en cache."},
    "about.reproduce": {
        "en": "To run the app on your computer: copy the repository with `git clone https://github.com/Flogix/eau-robinet.git`, "
              "install the dependencies with `pip install -r requirements.txt` (Python 3.12), then start it with "
              "`streamlit run app.py`. To rebuild every table from the raw files, run `make data`, or the PowerShell "
              "equivalent described in the README.",
        "fr": "Pour lancer l'application sur votre ordinateur : copiez le dépôt avec `git clone https://github.com/Flogix/eau-robinet.git`, "
              "installez les dépendances avec `pip install -r requirements.txt` (Python 3.12), puis lancez-la avec "
              "`streamlit run app.py`. Pour reconstruire toutes les tables depuis les fichiers bruts, lancez `make data`, "
              "ou l'équivalent PowerShell décrit dans le README."},
    "about.sources.kicker": {"en": "Sources and licences", "fr": "Sources et licences"},
    "about.sources.text": {
        "en": "The data comes from the French Ministry of Health, *Résultats du contrôle sanitaire de l'eau distribuée "
              "commune par commune*, published on data.gouv.fr under the Licence Ouverte 2.0 (Etalab open licence), last "
              "updated on 5 October 2026. This licence allows reuse, including commercial, provided the source and the "
              "date of update are cited. The geographic references come from geo.api.gouv.fr, INSEE, Cerema and Etalab, "
              "under the same licence. Every other figure, threshold and date shown in the app is listed with its link in "
              "[docs/sources.md](https://github.com/Flogix/eau-robinet/blob/main/docs/sources.md). The code of the app is "
              "released under the MIT licence ([LICENSE](https://github.com/Flogix/eau-robinet/blob/main/LICENSE)); the "
              "data, raw or processed, stays under the Licence Ouverte 2.0 of its producer.",
        "fr": "Les données viennent du ministère de la Santé, *Résultats du contrôle sanitaire de l'eau distribuée commune "
              "par commune*, publiées sur data.gouv.fr sous Licence Ouverte 2.0 (Etalab), mise à jour le 5 octobre 2026. "
              "Cette licence autorise la réutilisation, y compris commerciale, à condition de citer la source et la date "
              "de mise à jour. Les référentiels géographiques viennent de geo.api.gouv.fr, de l'INSEE, du Cerema et "
              "d'Etalab, sous la même licence. Tous les autres chiffres, seuils et dates de l'application sont listés avec "
              "leur lien dans [docs/sources.md](https://github.com/Flogix/eau-robinet/blob/main/docs/sources.md). Le code de "
              "l'application est publié sous licence MIT ([LICENSE](https://github.com/Flogix/eau-robinet/blob/main/LICENSE)) ; "
              "les données, brutes ou traitées, restent sous la Licence Ouverte 2.0 de leur producteur."},
    "about.dataset": {"en": "Open the dataset on data.gouv.fr", "fr": "Ouvrir le jeu de données sur data.gouv.fr"},
    "about.repo": {"en": "Open the GitHub repository", "fr": "Ouvrir le dépôt GitHub"},
    "about.sources.link": {"en": "Read the list of sources", "fr": "Lire la liste des sources"},
    "about.tools.kicker": {"en": "How it was built", "fr": "Comment c'est fait"},
    "about.tools": {
        "en": "Python, DuckDB and Parquet for the processing, pandas and Plotly for the analysis and the charts, "
              "Streamlit for the app, hosted on Streamlit Community Cloud, fpdf2 for the PDF report. Claude Code, an AI coding assistant made by "
              "Anthropic, was used to help write and test the code; the questions, the choices of method and the "
              "validation of every result are the author's. Typefaces: Fraunces and IBM Plex, under the SIL Open Font "
              "License.",
        "fr": "Python, DuckDB et Parquet pour le traitement, pandas et Plotly pour l'analyse et les graphiques, Streamlit "
              "pour l'application, hébergée sur Streamlit Community Cloud, fpdf2 pour le rapport PDF. Claude Code, un assistant de programmation par "
              "IA conçu par Anthropic, a aidé à écrire et tester le code ; les questions, les choix de méthode et la "
              "validation de chaque résultat sont ceux de l'auteur. Polices : Fraunces et IBM Plex, sous licence SIL Open "
              "Font License."},
    "about.disclaimer": {
        "en": "This app gives a teaching indicator, not a health opinion. For any question about your water, the reference "
              "is your regional health agency (ARS) and your water supplier.",
        "fr": "Cette application donne un indicateur pédagogique, pas un avis sanitaire. Pour toute question sur votre eau, "
              "la référence est votre agence régionale de santé (ARS) et votre distributeur d'eau."},
}

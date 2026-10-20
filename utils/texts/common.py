"""Shared strings: brand, navigation, sidebar filters, footer, badges, units."""

T = {
    # brand and navigation
    "brand.tagline": {"en": "Is my tap water good? An investigation into ten years of official tests.",
                      "fr": "Mon eau du robinet est-elle bonne ? Enquête sur dix ans de contrôles officiels."},
    "nav.home": {"en": "What's in my glass?", "fr": "Qu'y a-t-il dans mon verre ?"},
    "nav.reading": {"en": "How to read a water test", "fr": "Lire une analyse d'eau"},
    "nav.town": {"en": "The water of my town", "fr": "L'eau de ma commune"},
    "nav.compare": {"en": "Town against town", "fr": "Commune contre commune"},
    "nav.map": {"en": "The map of France", "fr": "La carte de France"},
    "nav.monitor": {"en": "What we look for, what we find", "fr": "Ce qu'on cherche, ce qu'on trouve"},
    "nav.quality": {"en": "Behind the numbers", "fr": "Les coulisses des chiffres"},
    "nav.conclusions": {"en": "What it all means", "fr": "Ce qu'il faut en retenir"},
    "nav.about": {"en": "About this project", "fr": "À propos du projet"},
    "nav.section.story": {"en": "The story", "fr": "Le récit"},
    "nav.section.explore": {"en": "Explore", "fr": "Explorer"},
    "nav.section.more": {"en": "Method and credits", "fr": "Méthode et crédits"},

    # town search (utils/town_search.py)
    "search.placeholder": {"en": "Type the name of a town", "fr": "Tapez le nom d'une commune"},
    "search.placeholder.current": {"en": "{town}: type to choose another town",
                                   "fr": "{town} : tapez pour choisir une autre commune"},
    # sidebar
    "side.lang": {"en": "Language", "fr": "Langue"},
    "side.author.logo": {"en": "EFREI Paris, engineering school", "fr": "EFREI Paris, école d'ingénieurs"},
    "side.author.program": {"en": "Data & AI, DAI group", "fr": "Data & AI, groupe DAI"},
    "side.author.course": {"en": "Data Analysis & Visualization", "fr": "Data Analysis & Visualization"},
    "side.author.coord": {"en": "coordinator: MATHEW Mano Joseph", "fr": "coordinateur : MATHEW Mano Joseph"},
    "side.filters": {"en": "Filters", "fr": "Filtres"},
    "side.intro": {
        "en": "These filters narrow the figures of this page to a period, a region or a kind of town. Only the "
              "filters that change something here are shown, and your choice is kept from one page to the next.",
        "fr": "Ces filtres restreignent les chiffres de cette page à une période, une région ou un type de commune. "
              "Seuls les filtres qui changent quelque chose ici sont affichés, et votre choix est gardé d'une page à "
              "l'autre."},
    "side.years": {"en": "Period (years)", "fr": "Période (années)"},
    "side.years.help": {
        "en": "Calendar years of the samples. 2026 only runs to 31 August 2026. The score of a town always uses the "
              "latest months, whatever the period.",
        "fr": "Années civiles des prélèvements. 2026 s'arrête au 31 août 2026. Le score d'une commune utilise toujours "
              "les derniers mois, quelle que soit la période."},
    "side.region": {"en": "Region", "fr": "Région"},
    "side.region.all": {"en": "All of France", "fr": "Toute la France"},
    "side.region.help": {"en": "Restricts the figures, the map and the rankings to one region.",
                         "fr": "Restreint les chiffres, la carte et les classements à une région."},
    "side.variable": {"en": "What the map shows", "fr": "Ce que montre la carte"},
    "side.variable.help": {
        "en": "Official conformity is the verdict of the health agency on each sample. For the other families we "
              "recomputed the verdict ourselves: a result above the threshold written next to it in the data.",
        "fr": "La conformité officielle est le verdict de l'agence de santé sur chaque prélèvement. Pour les autres "
              "familles, nous avons recalculé ce verdict : un résultat au-dessus du seuil écrit à côté de lui."},
    "side.ctype": {"en": "Kind of town", "fr": "Type de commune"},
    "side.ctype.help": {
        "en": "Urban or rural comes from the INSEE density grid, mountain from the Mountain Act list (Cerema). "
              "The Mediterranean coast is approximated by the coastal departments outside mountain areas.",
        "fr": "Urbain ou rural vient de la grille de densité de l'INSEE, montagne de la liste de la loi Montagne "
              "(Cerema). Le littoral méditerranéen est approché par les départements côtiers hors zones de montagne."},
    "side.disclaimer": {
        "en": "A teaching indicator, not a health opinion. The official opinion on your water is given by your "
              "regional health agency (ARS).",
        "fr": "Un indicateur pédagogique, pas un avis sanitaire. L'avis officiel sur votre eau est celui de votre "
              "agence régionale de santé (ARS)."},

    "var.bact_official": {"en": "Bacteria, official verdict", "fr": "Bactéries, verdict officiel"},
    "var.chem_official": {"en": "Chemistry, official verdict", "fr": "Chimie, verdict officiel"},
    "var.nitrates": {"en": "Nitrates", "fr": "Nitrates"},
    "var.pesticides": {"en": "Pesticides", "fr": "Pesticides"},
    "var.pfas": {"en": "PFAS (sum of 20)", "fr": "PFAS (somme de 20)"},
    "var.metals": {"en": "Metals (lead, arsenic…)", "fr": "Métaux (plomb, arsenic…)"},
    "var.disinfection_byproducts": {"en": "Disinfection by-products", "fr": "Sous-produits de désinfection"},
    "var.comfort": {"en": "Comfort indicators", "fr": "Indicateurs de confort"},
    "ctype.all": {"en": "All towns", "fr": "Toutes les communes"},
    "ctype.urban_dense": {"en": "Dense urban", "fr": "Urbain dense"},
    "ctype.urban_inter": {"en": "Intermediate urban", "fr": "Urbain intermédiaire"},
    "ctype.rural": {"en": "Rural", "fr": "Rural"},
    "ctype.mountain": {"en": "Mountain (Mountain Act)", "fr": "Montagne (loi Montagne)"},
    "ctype.med": {"en": "Mediterranean coast (approx.)", "fr": "Littoral méditerranéen (approx.)"},
    "period.partial": {"en": " (2026 partial)", "fr": " (2026 partielle)"},

    # INSEE density grid, 7 levels
    "dens7.1": {"en": "large urban centre", "fr": "grand centre urbain"},
    "dens7.2": {"en": "intermediate urban centre", "fr": "centre urbain intermédiaire"},
    "dens7.3": {"en": "small town", "fr": "petite ville"},
    "dens7.4": {"en": "urban belt", "fr": "ceinture urbaine"},
    "dens7.5": {"en": "rural town", "fr": "bourg rural"},
    "dens7.6": {"en": "dispersed rural", "fr": "rural à habitat dispersé"},
    "dens7.7": {"en": "very dispersed rural", "fr": "rural à habitat très dispersé"},

    # families and grades
    "fam.micro": {"en": "Bacteria", "fr": "Bactéries"},
    "fam.chem": {"en": "Health chemistry", "fr": "Chimie sanitaire"},
    "fam.comfort": {"en": "Comfort", "fr": "Confort"},
    "grade": {"en": "Grade", "fr": "Note"},
    "conf.high": {"en": "high", "fr": "élevée"},
    "conf.medium": {"en": "medium", "fr": "moyenne"},
    "conf.low": {"en": "low", "fr": "faible"},
    "badge.ok": {"en": "Good", "fr": "Bon"},
    "badge.limit": {"en": "Above limit", "fr": "Hors limite"},
    "badge.watch": {"en": "Watch", "fr": "À surveiller"},
    "badge.info": {"en": "Note", "fr": "À savoir"},
    "badge.unknown": {"en": "Not tested", "fr": "Non mesuré"},

    # sources and footer
    "common.source_short": {
        "en": "Source: Ministry of Health, sanitary control of tap water, data.gouv.fr (Licence Ouverte 2.0, 5 Oct 2026).",
        "fr": "Source : ministère de la Santé, contrôle sanitaire de l'eau, data.gouv.fr (Licence Ouverte 2.0, 05/10/2026)."},
    "common.partial2026": {"en": "2026: January to August", "fr": "2026 : janvier à août"},
    "common.year": {"en": "Year", "fr": "Année"},
    "footer.text": {
        "en": "Made by **[Florian Giraud](https://www.linkedin.com/in/florian-giraud-67883a291/)**, student at EFREI Paris (Data & AI), data storytelling project 2026. "
              "The code and the processed data are public on [GitHub](https://github.com/Flogix/eau-robinet): anyone "
              "can download them, reuse them and redo the analysis. Data: French Ministry of Health, Licence Ouverte 2.0; "
              "every other source is listed in [sources.md](https://github.com/Flogix/eau-robinet/blob/main/docs/sources.md).",
        "fr": "Réalisé par **[Florian Giraud](https://www.linkedin.com/in/florian-giraud-67883a291/)**, étudiant à l'EFREI Paris (Data & AI), projet de data storytelling 2026. "
              "Le code et les données traitées sont publics sur [GitHub](https://github.com/Flogix/eau-robinet) : chacun "
              "peut les télécharger, les réutiliser et refaire l'analyse. Données : ministère de la Santé, Licence Ouverte "
              "2.0 ; toutes les autres sources sont listées dans [sources.md](https://github.com/Flogix/eau-robinet/blob/main/docs/sources.md)."},
    # interpretation under a chart
    "an.seen": {"en": "What we see.", "fr": "Ce qu'on observe."},
    "an.why": {"en": "Why, probably.", "fr": "Pourquoi, probablement."},
    "an.limits": {"en": "Limits.", "fr": "Limites."},
}

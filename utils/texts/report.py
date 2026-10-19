"""Sentences of the rule-based "why" report (utils/score.why_report)."""

T = {
    "rep.bacteria": {"en": "bacteria", "fr": "bactéries"},
    "rep.on_date": {"en": " on {date}", "fr": " le {date}"},
    "rep.bact_none": {"en": "No bacteriological sample was taken in the last twelve months.",
                      "fr": "Aucun prélèvement bactériologique n'a été fait sur les douze derniers mois."},
    "rep.bact_ok": {"en": "All {n} bacteriological samples of the last twelve months were compliant.",
                    "fr": "Les {n} prélèvements bactériologiques des douze derniers mois étaient tous conformes."},
    "rep.bact_nc": {"en": "{nc} of the {n} bacteriological samples of the last twelve months were non-compliant "
                          "({pct}), because of {which}.",
                    "fr": "{nc} des {n} prélèvements bactériologiques des douze derniers mois étaient non conformes "
                          "({pct}), à cause de : {which}."},
    "rep.chem_exceed": {"en": "{lab}: {k} of {n} measurements went above the limit of {thr} {unit} in three years, "
                              "with a peak at {max} {unit}{date}.",
                        "fr": "{lab} : {k} mesures sur {n} ont dépassé la limite de {thr} {unit} en trois ans, "
                              "avec un pic à {max} {unit}{date}."},
    "rep.chem_close": {"en": "{lab}: highest value {max} {unit}{date}, more than half of the limit of {thr} {unit}.",
                       "fr": "{lab} : valeur la plus haute {max} {unit}{date}, plus de la moitié de la limite de "
                             "{thr} {unit}."},
    "rep.chem_close_p95": {"en": "{lab}: highest value {max} {unit}{date}, and values often above half of the limit "
                                 "of {thr} {unit}.",
                           "fr": "{lab} : valeur la plus haute {max} {unit}{date}, et des valeurs souvent au-dessus "
                                 "de la moitié de la limite de {thr} {unit}."},
    "rep.chem_ok": {"en": "No health-related substance came above half of its limit in three years.",
                    "fr": "Aucune substance à enjeu sanitaire n'a dépassé la moitié de sa limite en trois ans."},
    "rep.nitrates_ok": {"en": "Nitrates stayed at {max} {unit} at most, below the limit of {thr} {unit}.",
                        "fr": "Les nitrates sont restés à {max} {unit} au plus, sous la limite de {thr} {unit}."},
    "rep.pest_ok": {"en": "No pesticide above its limit in {n} samples, where {k} different substances were searched.",
                    "fr": "Aucun pesticide au-dessus de sa limite dans {n} prélèvements, où {k} substances différentes "
                          "ont été recherchées."},
    "rep.kind_indicative": {"en": "indicative value", "fr": "valeur indicative"},
    "rep.kind_reference": {"en": "quality reference", "fr": "référence de qualité"},
    "rep.comf_range": {"en": "{lab}: {k} of {n} measurements outside the expected range ({lo} to {hi} {unit}). "
                             "This is a comfort or treatment indicator, not a health limit.",
                       "fr": "{lab} : {k} mesures sur {n} hors de la plage attendue ({lo} à {hi} {unit}). "
                             "C'est un indicateur de confort ou de traitement, pas une limite sanitaire."},
    "rep.comf_exceed": {"en": "{lab}: {k} of {n} measurements above the {kind} of {thr} {unit}. "
                              "This is a comfort or treatment indicator, not a health limit.",
                        "fr": "{lab} : {k} mesures sur {n} au-dessus de la {kind} de {thr} {unit}. "
                              "C'est un indicateur de confort ou de traitement, pas une limite sanitaire."},
    "rep.indicative_exceed": {
        "en": "{lab}: {k} of {n} measurements above the 0.9 µg/L indicative value. Health authorities consider that "
              "this does not prevent drinking the water, but the water supplier must set up an action plan.",
        "fr": "{lab} : {k} mesures sur {n} au-dessus de la valeur indicative de 0,9 µg/L. Selon les autorités "
              "sanitaires, cela n'empêche pas de boire l'eau, mais le distributeur doit mettre en place un plan "
              "d'actions."},
    "rep.comf_close": {"en": "{lab}: highest value {max} {unit}, for a {kind} of {thr} {unit}.",
                       "fr": "{lab} : valeur la plus haute {max} {unit}, pour une {kind} de {thr} {unit}."},
    "rep.nonrel": {"en": "{lab} was found, at {max} µg/L at most. Health authorities judge this pesticide residue "
                         "\"non-relevant\" and compare it with a 0.9 µg/L indicative value, which it stays under.",
                   "fr": "{lab} a été détecté, à {max} µg/L au plus. Les autorités sanitaires jugent ce résidu de "
                         "pesticide « non pertinent » et le comparent à une valeur indicative de 0,9 µg/L, qu'il ne "
                         "dépasse pas."},
    "rep.hardness": {"en": "Hardness averages {v} °f. It only means more or less limescale and has no health limit.",
                     "fr": "La dureté est de {v} °f en moyenne. Elle ne dit que la quantité de calcaire et n'a pas de "
                           "limite sanitaire."},
    "rep.no_chem": {"en": "No health-related chemistry was measured in the last three years.",
                    "fr": "Aucune analyse de chimie sanitaire sur les trois dernières années."},
    "rep.no_nitrates": {"en": "Nitrates were not measured on this network in the last three years.",
                        "fr": "Les nitrates n'ont pas été mesurés sur ce réseau depuis trois ans."},
    "rep.no_pesticides": {"en": "Pesticides were not measured on this network in the last three years.",
                          "fr": "Les pesticides n'ont pas été mesurés sur ce réseau depuis trois ans."},
    "rep.no_pfas": {"en": "PFAS have not been measured on this network yet. They are part of the routine control only "
                          "since 1 January 2026.",
                    "fr": "Les PFAS n'ont pas encore été mesurés sur ce réseau. Ils ne font partie du contrôle "
                          "courant que depuis le 1er janvier 2026."},
    "rep.no_comfort": {"en": "No comfort indicator was measured in the last twelve months.",
                       "fr": "Aucun indicateur de confort n'a été mesuré sur les douze derniers mois."},
}

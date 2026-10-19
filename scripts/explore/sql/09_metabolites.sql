-- refqual / limitequal contenant 0,9 ou 0.9 µg/L
SELECT cdparametresiseeaux, any_value(libminparametre) lib, limitequal, refqual, min(annee_fichier) a1, max(annee_fichier) a2, count(*) n
FROM result WHERE refqual LIKE '%0,9 µg%' OR refqual LIKE '%0.9 µg%' OR limitequal LIKE '%0,9 µg%' OR limitequal LIKE '%0.9 µg%' GROUP BY ALL ORDER BY n DESC LIMIT 30;;
-- Métabolites métolachlore / chlorothalonil / chloridazone : codes, limites, références par année
SELECT cdparametresiseeaux, any_value(libminparametre) lib, annee_fichier, string_agg(DISTINCT coalesce(limitequal,'∅'), '|') lim, string_agg(DISTINCT coalesce(refqual,'∅'), '|') refq, count(*) n,
  count(*) FILTER (WHERE try_cast(valtraduite AS DOUBLE) > 0) quantif
FROM result WHERE libminparametre ILIKE '%tolachlor%' OR libminparametre ILIKE '%chlorothalonil%' OR libminparametre ILIKE '%chloridazon%'
GROUP BY cdparametresiseeaux, annee_fichier ORDER BY 1, 3;;
-- Tous les paramètres qui ont, une année, une limite puis plus de limite (codes "sans limite" voisins)
SELECT cdparametresiseeaux, any_value(libminparametre) lib, count(*) n, min(annee_fichier) a1, max(annee_fichier) a2, string_agg(DISTINCT coalesce(limitequal,'∅'), '|') lim
FROM result WHERE limitequal IS NULL AND cdunitereferencesiseeaux = 'µg/L' AND casparam IS NOT NULL
  AND libminparametre IN (SELECT DISTINCT libminparametre FROM result WHERE limitequal = '<=0,1 µg/L')
GROUP BY 1 ORDER BY n DESC LIMIT 30

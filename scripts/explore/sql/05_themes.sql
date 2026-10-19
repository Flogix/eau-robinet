-- PFAS : paramètres et 1re année de mesure
SELECT cdparametresiseeaux code, any_value(libminparametre) lib, min(annee_fichier) annee_1, count(*) n,
  count(*) FILTER (WHERE annee_fichier = 2026) n_2026, string_agg(DISTINCT limitequal, ' | ') limites
FROM result WHERE libminparametre ILIKE '%perfluor%' OR libminparametre ILIKE '%PFAS%' OR libminparametre ILIKE '%fluorotelom%' OR cdparametresiseeaux ILIKE 'PF%'
GROUP BY 1 ORDER BY n DESC LIMIT 40;;
-- Somme PFAS : mesures par année
SELECT annee_fichier, cdparametresiseeaux, any_value(libminparametre) lib, count(*) n, count(DISTINCT referenceprel) prel
FROM result WHERE libminparametre ILIKE '%somme%PFAS%' OR libminparametre ILIKE '%PFAS%somme%' OR libminparametre ILIKE '%total%PFAS%' GROUP BY ALL ORDER BY 1, 2;;
-- Microplastiques / particules ?
SELECT cdparametresiseeaux, any_value(libminparametre) lib, count(*) n FROM result
WHERE libminparametre ILIKE '%plasti%' OR libminparametre ILIKE '%microparticul%' OR libminparametre ILIKE '%particule%' GROUP BY 1 ORDER BY n DESC LIMIT 20;;
-- Paramètres distincts mesurés par année
SELECT annee_fichier annee, count(DISTINCT cdparametresiseeaux) n_param, count(DISTINCT cdparametresiseeaux) FILTER (WHERE limitequal IS NOT NULL) n_param_avec_limite FROM result GROUP BY 1 ORDER BY 1;;
-- Paramètres responsables des dépassements de limite : à partir des prélèvements C=N, quels paramètres dépassent ?
-- (approche simple : paramètres dont limitequal est de la forme '<=x unité' et valtraduite > x)
WITH r AS (
  SELECT annee_fichier, referenceprel, cdparametresiseeaux, libminparametre, limitequal,
         try_cast(valtraduite AS DOUBLE) v,
         try_cast(replace(regexp_extract(limitequal, '^<=\s*([0-9]+[.,]?[0-9]*)', 1), ',', '.') AS DOUBLE) lim
  FROM result WHERE limitequal LIKE '<=%' AND limitequal NOT LIKE '%et%')
SELECT annee_fichier annee, cdparametresiseeaux code, any_value(libminparametre) lib, count(DISTINCT referenceprel) prel_depassement
FROM r WHERE v > lim GROUP BY annee_fichier, cdparametresiseeaux QUALIFY row_number() OVER (PARTITION BY annee_fichier ORDER BY prel_depassement DESC) <= 8 ORDER BY annee, prel_depassement DESC;;
-- Références de qualité les plus dépassées (2025) — même approche simplifiée sur '<=x'
WITH r AS (
  SELECT referenceprel, cdparametresiseeaux, libminparametre, try_cast(valtraduite AS DOUBLE) v,
         try_cast(replace(regexp_extract(refqual, '^<=\s*([0-9]+[.,]?[0-9]*)', 1), ',', '.') AS DOUBLE) ref
  FROM result WHERE annee_fichier = 2025 AND refqual LIKE '<=%' AND refqual NOT LIKE '%et%')
SELECT cdparametresiseeaux code, any_value(libminparametre) lib, count(DISTINCT referenceprel) prel_depassement FROM r WHERE v > ref GROUP BY 1 ORDER BY 3 DESC LIMIT 12;;
-- Références dépassées 2026 vs 2025 (pour comprendre la hausse rc_N 2026)
WITH r AS (
  SELECT annee_fichier, referenceprel, cdparametresiseeaux, libminparametre, try_cast(valtraduite AS DOUBLE) v,
         try_cast(replace(regexp_extract(refqual, '^<=\s*([0-9]+[.,]?[0-9]*)', 1), ',', '.') AS DOUBLE) ref
  FROM result WHERE annee_fichier >= 2025 AND refqual LIKE '<=%' AND refqual NOT LIKE '%et%')
SELECT cdparametresiseeaux code, any_value(libminparametre) lib,
  count(DISTINCT referenceprel) FILTER (WHERE annee_fichier = 2025) d2025, count(DISTINCT referenceprel) FILTER (WHERE annee_fichier = 2026) d2026
FROM r WHERE v > ref GROUP BY 1 ORDER BY d2026 DESC LIMIT 12;;
-- Dureté / calcium / nitrates : codes
SELECT cdparametresiseeaux, any_value(libminparametre) lib, any_value(cdunitereferencesiseeaux) unite, count(*) n FROM result
WHERE annee_fichier = 2025 AND (libminparametre ILIKE '%nitrat%' OR libminparametre ILIKE 'titre hydrot%' OR libminparametre ILIKE 'calcium%' OR libminparametre ILIKE 'magn_sium%'
  OR libminparametre ILIKE 'plomb%' OR libminparametre ILIKE 'arsenic%' OR libminparametre ILIKE 'escherichia%' OR libminparametre ILIKE 'ent_rocoques%' OR libminparametre ILIKE '%total des pesticides%' OR libminparametre ILIKE '%chlorure de vinyl%')
GROUP BY 1 ORDER BY n DESC;;
-- Limitequal qui change dans le temps pour un même paramètre (exemples)
SELECT cdparametresiseeaux, any_value(libminparametre) lib, string_agg(DISTINCT annee_fichier::VARCHAR || ':' || coalesce(limitequal,'∅'), ' | ' ORDER BY annee_fichier::VARCHAR || ':' || coalesce(limitequal,'∅')) hist
FROM (SELECT DISTINCT annee_fichier, cdparametresiseeaux, libminparametre, limitequal FROM result WHERE cdparametresiseeaux IN ('NO3','PB','AS','ECOLI','PESTOT','CLVYL','SPFAS','PFAS20'))
GROUP BY 1

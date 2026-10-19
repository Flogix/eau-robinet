
-- Références de qualité les plus dépassées, 2025 vs 2026 (pour comprendre la hausse de rc_N en 2026)
WITH r AS (
  SELECT annee_fichier, referenceprel, cdparametresiseeaux, libminparametre, try_cast(valtraduite AS DOUBLE) v,
         try_cast(replace(regexp_extract(refqual, '^<=\s*([0-9]+[.,]?[0-9]*)', 1), ',', '.') AS DOUBLE) rq
  FROM result WHERE annee_fichier >= 2025 AND refqual LIKE '<=%' AND rqana <> 'N.M.')
SELECT cdparametresiseeaux code, any_value(libminparametre) lib,
  count(DISTINCT referenceprel) FILTER (WHERE annee_fichier = 2025) d2025, count(DISTINCT referenceprel) FILTER (WHERE annee_fichier = 2026) d2026
FROM r WHERE v > rq GROUP BY 1 ORDER BY d2026 DESC LIMIT 12;;
-- Paramètres clés : codes, unités (2025)
SELECT cdparametresiseeaux, any_value(libminparametre) lib, string_agg(DISTINCT cdunitereferencesiseeaux, '|') unite, count(*) n FROM result
WHERE annee_fichier = 2025 AND (libminparametre ILIKE '%nitrat%' OR libminparametre ILIKE 'titre hydrot%' OR libminparametre ILIKE 'calcium%' OR libminparametre ILIKE 'magn_sium%'
  OR libminparametre ILIKE 'plomb%' OR libminparametre ILIKE 'arsenic%' OR libminparametre ILIKE 'escherichia%' OR libminparametre ILIKE 'ent_rocoques%' OR libminparametre ILIKE '%total des pesticides%')
GROUP BY 1 ORDER BY n DESC;;
-- Historique des limites pour quelques paramètres clés
SELECT cdparametresiseeaux, annee_fichier, string_agg(DISTINCT coalesce(limitequal,'∅'), ' | ') limites, count(*) n
FROM result WHERE cdparametresiseeaux IN ('NO3','PB','AS','ECOLI','PESTOT','SPFAS','CLVYL') GROUP BY ALL ORDER BY 1, 2;;
-- Métabolites de pesticides : chlorothalonil R471811, ESA-métolachlore etc. (1re année et dépassements)
SELECT cdparametresiseeaux, any_value(libminparametre) lib, min(annee_fichier) annee_1, count(*) n, string_agg(DISTINCT limitequal, '|') limites
FROM result WHERE libminparametre ILIKE '%R471811%' OR libminparametre ILIKE '%chlorothalonil%' OR libminparametre ILIKE '%ESA%m_tolachlore%' OR libminparametre ILIKE '%OXA%m_tolachlore%'
GROUP BY 1 ORDER BY n DESC LIMIT 10;;
-- COM_UDI : clés (insee, cdreseau, quartier) répétées 2021-2024 — en quoi diffèrent-elles ?
WITH d AS (SELECT annee_fichier, inseecommune, cdreseau, quartier FROM com_udi GROUP BY ALL HAVING count(*) > 1)
SELECT c.* FROM com_udi c JOIN d USING (annee_fichier, inseecommune, cdreseau, quartier) ORDER BY annee_fichier, inseecommune LIMIT 12;;
-- PLV : couples (referenceprel, cdreseau) répétés (2025-2026)
WITH d AS (SELECT annee_fichier, referenceprel, cdreseau FROM plv GROUP BY ALL HAVING count(*) > 1)
SELECT p.annee_fichier, p.referenceprel, p.cdreseau, p.cdreseauamont, p.nomreseauamont, p.pourcentdebit FROM plv p JOIN d USING (annee_fichier, referenceprel, cdreseau) ORDER BY 1, 2
;;
-- Historique de la limite du chlorothalonil R471811 et des métabolites de la chloridazone
SELECT cdparametresiseeaux, annee_fichier, string_agg(DISTINCT coalesce(limitequal,'∅'), ' | ') limites, count(*) n FROM result WHERE cdparametresiseeaux IN ('R471811','CLDZ_D','CLDZ_MD','ESAMTC','CLTHALS') GROUP BY ALL ORDER BY 1, 2
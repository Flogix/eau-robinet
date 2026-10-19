-- Top 8 paramètres en dépassement de LIMITE par année (prélèvements distincts ; limites de forme '<=x')
WITH r AS (
  SELECT annee_fichier, referenceprel, cdparametresiseeaux, libminparametre,
         try_cast(valtraduite AS DOUBLE) v,
         try_cast(replace(regexp_extract(limitequal, '^<=\s*([0-9]+[.,]?[0-9]*)', 1), ',', '.') AS DOUBLE) lim
  FROM result WHERE limitequal LIKE '<=%' AND rqana NOT IN ('N.M.'))
SELECT annee_fichier annee, cdparametresiseeaux code, any_value(libminparametre) lib, count(DISTINCT referenceprel) prel_depassement
FROM r WHERE v > lim GROUP BY annee_fichier, cdparametresiseeaux
QUALIFY row_number() OVER (PARTITION BY annee_fichier ORDER BY count(DISTINCT referenceprel) DESC) <= 8 ORDER BY annee, prel_depassement DESC;;
-- Prélèvements avec au moins un dépassement de limite (recalculé) vs plvconformitechimique = N, par année
WITH r AS (
  SELECT annee_fichier, referenceprel, cdunitereferencesiseeaux u, try_cast(valtraduite AS DOUBLE) v,
         try_cast(replace(regexp_extract(limitequal, '^<=\s*([0-9]+[.,]?[0-9]*)', 1), ',', '.') AS DOUBLE) lim,
         cdparametresiseeaux IN ('ECOLI','STRF') OR limitequal LIKE '%n/(100mL)%' OR limitequal LIKE '%NPP%' AS micro
  FROM result WHERE limitequal LIKE '<=%' AND rqana <> 'N.M.'),
d AS (SELECT annee_fichier, referenceprel, bool_or(v > lim AND NOT micro) dep_chim, bool_or(v > lim AND micro) dep_micro FROM r GROUP BY ALL),
p AS (SELECT DISTINCT annee_fichier, referenceprel, plvconformitebacterio b, plvconformitechimique c FROM plv)
SELECT p.annee_fichier annee,
  count(*) FILTER (WHERE c = 'N') c_N, count(*) FILTER (WHERE dep_chim) recalc_chim, count(*) FILTER (WHERE c = 'N' AND dep_chim) les_deux_chim,
  count(*) FILTER (WHERE b = 'N') b_N, count(*) FILTER (WHERE dep_micro) recalc_micro, count(*) FILTER (WHERE b = 'N' AND dep_micro) les_deux_micro
FROM p LEFT JOIN d USING (annee_fichier, referenceprel) GROUP BY 1 ORDER BY 1;;
-- Références de qualité les plus dépassées, 2025 vs 2026 (pour comprendre la hausse de rc_N en 2026)
WITH r AS (
  SELECT annee_fichier, referenceprel, cdparametresiseeaux, libminparametre, try_cast(valtraduite AS DOUBLE) v,
         try_cast(replace(regexp_extract(refqual, '^<=\s*([0-9]+[.,]?[0-9]*)', 1), ',', '.') AS DOUBLE) ref
  FROM result WHERE annee_fichier >= 2025 AND refqual LIKE '<=%' AND rqana <> 'N.M.')
SELECT cdparametresiseeaux code, any_value(libminparametre) lib,
  count(DISTINCT referenceprel) FILTER (WHERE annee_fichier = 2025) d2025, count(DISTINCT referenceprel) FILTER (WHERE annee_fichier = 2026) d2026
FROM r WHERE v > ref GROUP BY 1 ORDER BY d2026 DESC LIMIT 12;;
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

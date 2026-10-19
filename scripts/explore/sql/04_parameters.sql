-- Top 40 paramètres les plus mesurés (2025, dernière année complète)
SELECT cdparametresiseeaux code, any_value(cdparametre) sandre, any_value(libminparametre) libelle, count(*) n,
  string_agg(DISTINCT cdunitereferencesiseeaux, ' | ') unites,
  string_agg(DISTINCT limitequal, ' | ') limites, string_agg(DISTINCT refqual, ' | ') references_q
FROM result WHERE annee_fichier = 2025 GROUP BY 1 ORDER BY n DESC LIMIT 40;;
-- Formats de limitequal (chiffres remplacés par 9), toutes années
SELECT regexp_replace(limitequal, '[0-9]+', '9', 'g') motif, count(*) n, any_value(limitequal) exemple, count(DISTINCT cdparametresiseeaux) n_param
FROM result WHERE limitequal IS NOT NULL GROUP BY 1 ORDER BY n DESC LIMIT 30;;
-- Formats de refqual
SELECT regexp_replace(refqual, '[0-9]+', '9', 'g') motif, count(*) n, any_value(refqual) exemple, count(DISTINCT cdparametresiseeaux) n_param
FROM result WHERE refqual IS NOT NULL GROUP BY 1 ORDER BY n DESC LIMIT 30;;
-- Part des lignes avec une limite / une référence
SELECT count(*) n, count(limitequal) avec_limite, count(refqual) avec_reference, count(*) FILTER (WHERE limitequal IS NOT NULL AND refqual IS NOT NULL) les_deux FROM result;;
-- Formats de rqana (paramètres quantitatifs)
SELECT regexp_replace(rqana, '[0-9]+', '9', 'g') motif, count(*) n, any_value(rqana) exemple, any_value(valtraduite) exemple_valtraduite
FROM result WHERE qualitparam = 'N' GROUP BY 1 ORDER BY n DESC LIMIT 30;;
-- Valeurs de rqana pour les paramètres qualitatifs
SELECT rqana, count(*) n FROM result WHERE qualitparam = 'O' GROUP BY 1 ORDER BY n DESC LIMIT 25;;
-- valtraduite : format, nulls, négatifs
SELECT count(*) n, count(valtraduite) non_null, count(*) FILTER (WHERE try_cast(valtraduite AS DOUBLE) IS NULL AND valtraduite IS NOT NULL) non_numerique,
  count(*) FILTER (WHERE try_cast(valtraduite AS DOUBLE) < 0) negatifs, count(*) FILTER (WHERE valtraduite LIKE '%,%') avec_virgule
FROM result;;
-- Paramètres négatifs (lesquels ?)
SELECT cdparametresiseeaux, any_value(libminparametre) lib, count(*) n, min(try_cast(valtraduite AS DOUBLE)) vmin FROM result WHERE try_cast(valtraduite AS DOUBLE) < 0 GROUP BY 1 ORDER BY n DESC LIMIT 10;;
-- Cohérence rqana '<x' -> valtraduite 0
SELECT count(*) n_inf, count(*) FILTER (WHERE try_cast(valtraduite AS DOUBLE) = 0) traduit_0 FROM result WHERE rqana LIKE '<%';;
-- Paramètres avec plusieurs unités
SELECT cdparametresiseeaux, any_value(libminparametre) lib, string_agg(DISTINCT cdunitereferencesiseeaux, ' | ') unites, count(DISTINCT cdunitereferencesiseeaux) nu
FROM result GROUP BY 1 HAVING nu > 1 ORDER BY nu DESC LIMIT 20;;
SELECT count(*) n_param_multi_unites FROM (SELECT cdparametresiseeaux FROM result GROUP BY 1 HAVING count(DISTINCT cdunitereferencesiseeaux) > 1);;
-- Unités les plus fréquentes
SELECT cdunitereferencesiseeaux, count(*) n FROM result GROUP BY 1 ORDER BY n DESC LIMIT 20

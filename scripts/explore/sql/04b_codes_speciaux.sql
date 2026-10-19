-- Codes spéciaux de rqana : valeurs de valtraduite réellement associées (même ligne)
SELECT CASE WHEN rqana IS NULL THEN '(vide)' WHEN regexp_matches(rqana, '^[0-9]') THEN 'nombre' WHEN rqana LIKE '<%' THEN '<x'
            WHEN rqana LIKE '>%' THEN '>x' WHEN rqana LIKE '-%' THEN '-x' ELSE rqana END classe,
  count(*) n, count(valtraduite) vt_non_null,
  min(try_cast(valtraduite AS DOUBLE)) vt_min, max(try_cast(valtraduite AS DOUBLE)) vt_max
FROM result WHERE qualitparam = 'N' GROUP BY 1 ORDER BY n DESC LIMIT 20;;
-- N.M. : quels paramètres, et pourquoi valtraduite non nulle ?
SELECT cdparametresiseeaux, any_value(libminparametre) lib, count(*) n, count(valtraduite) vt_non_null, min(valtraduite) vmin, max(valtraduite) vmax
FROM result WHERE rqana = 'N.M.' GROUP BY 1 ORDER BY n DESC LIMIT 10;;
-- N.M. par année
SELECT annee_fichier, count(*) n FROM result WHERE rqana = 'N.M.' GROUP BY 1 ORDER BY 1

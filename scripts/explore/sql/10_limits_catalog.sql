-- Paramètres avec une limite autre que 0,1/0,03 µg/L (hors pesticides typiques)
SELECT cdparametresiseeaux code, any_value(libminparametre) lib, string_agg(DISTINCT limitequal, '|') lim, count(*) n
FROM result WHERE limitequal IS NOT NULL AND replace(limitequal, ',', '.') NOT IN ('<=0.1 µg/L', '<=0.03 µg/L')
GROUP BY 1 ORDER BY n DESC;;
-- Limite 0,1 µg/L : libellés qui ne ressemblent pas à des pesticides (mots-clés)
SELECT cdparametresiseeaux code, any_value(libminparametre) lib, count(*) n FROM result
WHERE replace(limitequal, ',', '.') IN ('<=0.1 µg/L', '<=0.03 µg/L')
  AND (libminparametre ILIKE '%epichlor%' OR libminparametre ILIKE '%acrylam%' OR libminparametre ILIKE '%PFAS%' OR libminparametre ILIKE '%perfluor%'
       OR libminparametre ILIKE '%benzo%' OR libminparametre ILIKE '%hydrocarb%' OR libminparametre ILIKE '%HAP%' OR libminparametre ILIKE '%somme%' OR libminparametre ILIKE '%total%'
       OR libminparametre ILIKE '%chlorure%' OR libminparametre ILIKE '%bisphen%' OR libminparametre ILIKE '%microcyst%' OR libminparametre ILIKE '%tritium%')
GROUP BY 1 ORDER BY n DESC;;
-- Limite 0,1 µg/L : nb de paramètres et exemples au hasard
SELECT count(DISTINCT cdparametresiseeaux) FROM result WHERE replace(limitequal, ',', '.') IN ('<=0.1 µg/L', '<=0.03 µg/L');;
SELECT DISTINCT cdparametresiseeaux, libminparametre FROM result WHERE replace(limitequal, ',', '.') IN ('<=0.1 µg/L', '<=0.03 µg/L') USING SAMPLE 40 ROWS (reservoir, 42)

-- Valeurs manquantes PLV (toutes années)
SELECT column_name, null_percentage, approx_unique, min, max FROM (SUMMARIZE plv);;
-- Valeurs manquantes COM_UDI (toutes années)
SELECT column_name, null_percentage, approx_unique, min, max FROM (SUMMARIZE com_udi);;
-- Valeurs manquantes RESULT (toutes années)
SELECT column_name, null_percentage, approx_unique FROM (SUMMARIZE result);;
-- Formats heureprel
SELECT regexp_replace(heureprel, '[0-9]', '9', 'g') motif, count(*) n FROM plv GROUP BY 1 ORDER BY n DESC LIMIT 5;;
-- DROM : prélèvements par année
SELECT annee_fichier, count(DISTINCT referenceprel) FILTER (WHERE cddept = '971') gp, count(DISTINCT referenceprel) FILTER (WHERE cddept = '972') mq,
  count(DISTINCT referenceprel) FILTER (WHERE cddept = '973') gf, count(DISTINCT referenceprel) FILTER (WHERE cddept = '974') re, count(DISTINCT referenceprel) FILTER (WHERE cddept = '976') yt,
  count(DISTINCT cddept) n_dept
FROM plv GROUP BY 1 ORDER BY 1;;
-- PFAS (somme de 20) : prélèvements mesurés et > 0,1 µg/L par année
SELECT annee_fichier, count(DISTINCT referenceprel) prel, count(DISTINCT referenceprel) FILTER (WHERE try_cast(valtraduite AS DOUBLE) > 0.1) prel_sup_limite,
  count(DISTINCT referenceprel) FILTER (WHERE try_cast(valtraduite AS DOUBLE) > 0) prel_quantifie
FROM result WHERE cdparametresiseeaux = 'SPFAS' GROUP BY 1 ORDER BY 1;;
-- Communes témoins : UDI et nb de couples prélèvement-UDI en 2025
SELECT c.inseecommune, c.nomcommune, c.quartier, c.cdreseau, c.nomreseau,
  (SELECT count(*) FROM plv p WHERE p.annee_fichier = 2025 AND p.cdreseau = c.cdreseau) n_plv_2025,
  (SELECT count(DISTINCT inseecommune) FROM com_udi c2 WHERE c2.annee_fichier = 2025 AND c2.cdreseau = c.cdreseau) n_communes_udi
FROM com_udi c WHERE c.annee_fichier = 2025 AND c.inseecommune IN ('75056', '94076') ORDER BY 1, 4;;
-- Taille des UDI (nb de couples prélèvement-UDI en 2025) : distribution
SELECT CASE WHEN n < 5 THEN '1-4' WHEN n < 12 THEN '5-11' WHEN n < 50 THEN '12-49' WHEN n < 200 THEN '50-199' ELSE '200+' END classe, count(*) n_udi
FROM (SELECT cdreseau, count(*) n FROM plv WHERE annee_fichier = 2025 GROUP BY 1) GROUP BY 1 ORDER BY min(n);;
-- Communes : codes INSEE stables ? communes présentes en 2016 mais absentes en 2026 et inversement
SELECT
  (SELECT count(*) FROM (SELECT DISTINCT inseecommune FROM com_udi WHERE annee_fichier = 2016 EXCEPT SELECT DISTINCT inseecommune FROM com_udi WHERE annee_fichier = 2026)) dans_2016_pas_2026,
  (SELECT count(*) FROM (SELECT DISTINCT inseecommune FROM com_udi WHERE annee_fichier = 2026 EXCEPT SELECT DISTINCT inseecommune FROM com_udi WHERE annee_fichier = 2016)) dans_2026_pas_2016,
  (SELECT count(DISTINCT inseecommune) FROM com_udi) total_codes_distincts;;
-- UDI : stabilité des codes entre 2016 et 2026
SELECT
  (SELECT count(*) FROM (SELECT DISTINCT cdreseau FROM com_udi WHERE annee_fichier = 2016 INTERSECT SELECT DISTINCT cdreseau FROM com_udi WHERE annee_fichier = 2026)) udi_communes_2016_2026,
  (SELECT count(DISTINCT cdreseau) FROM com_udi) udi_total

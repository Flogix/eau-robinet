-- PLV : couple (referenceprel, cdreseau) répété
WITH d AS (SELECT referenceprel, cdreseau FROM plv GROUP BY ALL HAVING count(*) > 1)
SELECT p.* EXCLUDE (conclusionprel, ugelib, distrlib, moalib) FROM plv p JOIN d USING (referenceprel, cdreseau);;
-- PLV : un referenceprel -> combien d'UDI ? (distribution)
SELECT n_udi, count(*) n_ref FROM (SELECT referenceprel, count(DISTINCT cdreseau) n_udi FROM plv GROUP BY 1) GROUP BY 1 ORDER BY 1 LIMIT 15;;
-- PLV : lignes avec/sans installation amont
SELECT (cdreseauamont IS NOT NULL) AS amont, count(*) n, count(DISTINCT referenceprel) n_ref FROM plv GROUP BY 1;;
-- PLV : les attributs du prélèvement (date, conformités) sont-ils identiques entre lignes d'un même referenceprel ?
SELECT count(*) n_ref_multi,
  count(*) FILTER (WHERE nd > 1) ref_dates_diff,
  count(*) FILTER (WHERE nb > 1) ref_bact_diff,
  count(*) FILTER (WHERE nc > 1) ref_chim_diff
FROM (SELECT referenceprel, count(DISTINCT dateprel) nd, count(DISTINCT plvconformitebacterio) nb, count(DISTINCT plvconformitechimique) nc
      FROM plv GROUP BY 1 HAVING count(*) > 1);;
-- RESULT : clés et doublons
SELECT count(*) n,
  count(DISTINCT referenceprel) n_prel,
  count(DISTINCT (referenceprel, cdparametresiseeaux)) n_prel_param,
  count(DISTINCT (referenceprel, cdparametresiseeaux, insituana)) n_prel_param_insitu,
  count(DISTINCT (referenceprel, cdparametresiseeaux, insituana, referenceanl)) n_prel_param_insitu_anl
FROM result;;
-- RESULT : lignes strictement identiques
SELECT count(*) - (SELECT count(*) FROM (SELECT DISTINCT * FROM result)) AS doublons_exacts FROM result;;
-- RESULT : exemple de (referenceprel, param) répété
WITH d AS (SELECT referenceprel, cdparametresiseeaux FROM result GROUP BY ALL HAVING count(*) > 1 LIMIT 3)
SELECT referenceprel, cdparametresiseeaux, insituana, rqana, cdunitereferencesiseeaux, limitequal, refqual, valtraduite, referenceanl
FROM result JOIN d USING (referenceprel, cdparametresiseeaux) ORDER BY 1, 2;;
-- Intégrité : RESULT sans PLV, PLV sans RESULT
SELECT
  (SELECT count(DISTINCT referenceprel) FROM result WHERE referenceprel NOT IN (SELECT referenceprel FROM plv)) result_sans_plv,
  (SELECT count(DISTINCT referenceprel) FROM plv WHERE referenceprel NOT IN (SELECT referenceprel FROM result)) plv_sans_result;;
-- Intégrité : UDI de PLV absentes de COM_UDI, et inversement
SELECT
  (SELECT count(DISTINCT cdreseau) FROM plv) udi_plv,
  (SELECT count(DISTINCT cdreseau) FROM com_udi) udi_comudi,
  (SELECT count(DISTINCT cdreseau) FROM plv WHERE cdreseau NOT IN (SELECT cdreseau FROM com_udi)) udi_plv_sans_commune,
  (SELECT count(DISTINCT cdreseau) FROM com_udi WHERE cdreseau NOT IN (SELECT cdreseau FROM plv)) udi_comudi_sans_plv;;
-- COM_UDI : clés
SELECT count(*) n, count(DISTINCT inseecommune) n_communes, count(DISTINCT cdreseau) n_udi,
  count(DISTINCT (inseecommune, cdreseau)) n_commune_udi,
  count(DISTINCT (inseecommune, cdreseau, quartier)) n_commune_udi_quartier,
  count(*) - (SELECT count(*) FROM (SELECT DISTINCT * FROM com_udi)) doublons_exacts
FROM com_udi;;
-- COM_UDI : nb d'UDI par commune (distribution)
SELECT least(n_udi, 10) n_udi_plafonne_10, count(*) n_communes FROM (SELECT inseecommune, count(DISTINCT cdreseau) n_udi FROM com_udi GROUP BY 1) GROUP BY 1 ORDER BY 1;;
-- COM_UDI : nb de communes par UDI (distribution)
SELECT least(n_com, 20) n_communes_plafonne_20, count(*) n_udi FROM (SELECT cdreseau, count(DISTINCT inseecommune) n_com FROM com_udi GROUP BY 1) GROUP BY 1 ORDER BY 1;;
-- COM_UDI : valeurs de quartier les plus fréquentes
SELECT quartier, count(*) n FROM com_udi GROUP BY 1 ORDER BY n DESC LIMIT 12;;
-- COM_UDI : Paris / Lyon / Marseille / Villejuif
SELECT inseecommune, nomcommune, count(DISTINCT cdreseau) n_udi, count(*) n_lignes FROM com_udi
WHERE inseecommune LIKE '751%' OR inseecommune IN ('75056','69123','13055','94076') OR inseecommune LIKE '6938%' OR inseecommune LIKE '132%'
GROUP BY ALL ORDER BY 1 LIMIT 60;;
-- COM_UDI : formats des codes INSEE et debutalim
SELECT length(inseecommune) l, regexp_matches(inseecommune, '^[0-9][0-9AB][0-9]{3}$') ok, count(*) n FROM com_udi GROUP BY ALL;;
SELECT min(debutalim), max(debutalim), count(*) FILTER (WHERE try_strptime(debutalim, '%Y-%m-%d') IS NULL) non_parsable FROM com_udi;;
-- Départements gestionnaires (cddept) : nb de prélèvements
SELECT cddept, count(DISTINCT referenceprel) n_prel FROM plv GROUP BY 1 ORDER BY 1

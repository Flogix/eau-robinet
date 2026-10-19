-- Volumétrie et clés par année (PLV)
SELECT annee_fichier annee, count(*) lignes, count(DISTINCT referenceprel) prelevements,
  count(DISTINCT (referenceprel, cdreseau)) couples_prel_udi, count(DISTINCT cdreseau) udi,
  min(dateprel) dmin, max(dateprel) dmax,
  count(*) FILTER (WHERE year(try_strptime(dateprel, '%Y-%m-%d')) <> annee_fichier) dates_hors_annee,
  count(*) FILTER (WHERE try_strptime(dateprel, '%Y-%m-%d') IS NULL) dates_invalides,
  count(*) FILTER (WHERE cdreseauamont IS NOT NULL) lignes_amont
FROM plv GROUP BY 1 ORDER BY 1;;
-- Volumétrie et clés par année (RESULT)
SELECT annee_fichier annee, count(*) lignes, count(DISTINCT referenceprel) prelevements,
  count(DISTINCT cdparametresiseeaux) parametres,
  count(*) - count(DISTINCT (referenceprel, cdparametresiseeaux, insituana, referenceanl)) doublons_cle_complete,
  count(*) - count(DISTINCT (referenceprel, cdparametresiseeaux)) repetitions_prel_param
FROM result GROUP BY 1 ORDER BY 1;;
-- Volumétrie et clés par année (COM_UDI)
SELECT annee_fichier annee, count(*) lignes, count(DISTINCT inseecommune) communes, count(DISTINCT cdreseau) udi,
  count(*) - count(DISTINCT (inseecommune, cdreseau, quartier)) doublons_cle,
  count(*) FILTER (WHERE quartier IS NULL) quartier_null
FROM com_udi GROUP BY 1 ORDER BY 1;;
-- Intégrité par année
WITH p AS (SELECT DISTINCT annee_fichier, referenceprel FROM plv),
     r AS (SELECT DISTINCT annee_fichier, referenceprel FROM result),
     pu AS (SELECT DISTINCT annee_fichier, cdreseau FROM plv),
     cu AS (SELECT DISTINCT annee_fichier, cdreseau FROM com_udi)
SELECT y.annee_fichier annee,
  (SELECT count(*) FROM r WHERE r.annee_fichier = y.annee_fichier AND NOT EXISTS (SELECT 1 FROM p WHERE p.annee_fichier = r.annee_fichier AND p.referenceprel = r.referenceprel)) result_sans_plv,
  (SELECT count(*) FROM p WHERE p.annee_fichier = y.annee_fichier AND NOT EXISTS (SELECT 1 FROM r WHERE r.annee_fichier = p.annee_fichier AND r.referenceprel = p.referenceprel)) plv_sans_result,
  (SELECT count(*) FROM pu WHERE pu.annee_fichier = y.annee_fichier AND NOT EXISTS (SELECT 1 FROM cu WHERE cu.annee_fichier = pu.annee_fichier AND cu.cdreseau = pu.cdreseau)) udi_plv_sans_commune,
  (SELECT count(*) FROM cu WHERE cu.annee_fichier = y.annee_fichier AND NOT EXISTS (SELECT 1 FROM pu WHERE pu.annee_fichier = cu.annee_fichier AND pu.cdreseau = cu.cdreseau)) udi_commune_sans_plv
FROM (SELECT DISTINCT annee_fichier FROM plv) y ORDER BY 1;;
-- Un referenceprel apparaît-il dans plusieurs fichiers annuels ?
SELECT count(*) n_ref_multi_annees FROM (SELECT referenceprel FROM plv GROUP BY 1 HAVING count(DISTINCT annee_fichier) > 1);;
-- Conformité bactério (limites) par année, au niveau du prélèvement (referenceprel dédoublonné)
WITH u AS (SELECT DISTINCT annee_fichier, referenceprel, plvconformitebacterio b, plvconformitechimique c, plvconformitereferencebact rb, plvconformitereferencechim rc FROM plv)
SELECT annee_fichier annee, count(*) prel,
  count(*) FILTER (WHERE b='C') b_C, count(*) FILTER (WHERE b='N') b_N, count(*) FILTER (WHERE b='S') b_S, count(*) FILTER (WHERE b IS NULL) b_vide,
  count(*) FILTER (WHERE c='C') c_C, count(*) FILTER (WHERE c='N') c_N, count(*) FILTER (WHERE c='D') c_D, count(*) FILTER (WHERE c='S') c_S, count(*) FILTER (WHERE c IS NULL) c_vide,
  count(*) FILTER (WHERE rb='N') rb_N, count(*) FILTER (WHERE rc='N') rc_N
FROM u GROUP BY 1 ORDER BY 1;;
-- Autres valeurs éventuelles des colonnes de conformité (toutes années)
SELECT 'bacterio' col, plvconformitebacterio v, count(*) n FROM plv GROUP BY ALL
UNION ALL SELECT 'chimique', plvconformitechimique, count(*) FROM plv GROUP BY ALL
UNION ALL SELECT 'ref_bact', plvconformitereferencebact, count(*) FROM plv GROUP BY ALL
UNION ALL SELECT 'ref_chim', plvconformitereferencechim, count(*) FROM plv GROUP BY ALL ORDER BY 1, 3 DESC;;
-- qualitparam / insituana
SELECT qualitparam, insituana, count(*) n FROM result GROUP BY ALL ORDER BY n DESC

-- Exemples PLV 2026
SELECT * EXCLUDE (conclusionprel, ugelib, distrlib, moalib) FROM plv WHERE annee_fichier = 2026 USING SAMPLE 10 ROWS (reservoir, 42);;
-- Exemples RESULT 2026
SELECT * EXCLUDE (libmajparametre, libwebparametre) FROM result WHERE annee_fichier = 2026 USING SAMPLE 10 ROWS (reservoir, 42);;
-- Exemples COM_UDI 2026
SELECT * FROM com_udi WHERE annee_fichier = 2026 USING SAMPLE 10 ROWS (reservoir, 42);;
-- Valeurs distinctes des conformités PLV 2026
SELECT plvconformitebacterio b, plvconformitechimique c, plvconformitereferencebact rb, plvconformitereferencechim rc, count(*) n
FROM plv WHERE annee_fichier = 2026 GROUP BY ALL ORDER BY n DESC LIMIT 30;;
-- Plage de dates PLV 2026
SELECT min(dateprel), max(dateprel), count(DISTINCT dateprel), count(*) FILTER (WHERE try_strptime(dateprel, '%Y-%m-%d') IS NULL) AS dates_non_parsables FROM plv WHERE annee_fichier = 2026;;
-- Unicité referenceprel PLV 2026
SELECT count(*) n, count(DISTINCT referenceprel) n_distinct FROM plv WHERE annee_fichier = 2026;;
-- Lignes PLV entièrement dupliquées 2026
SELECT count(*) - (SELECT count(*) FROM (SELECT DISTINCT * FROM plv WHERE annee_fichier = 2026)) AS doublons_exacts FROM plv WHERE annee_fichier = 2026;;
-- referenceprel répétés dans PLV : sur quelles colonnes diffèrent-ils ?
WITH d AS (SELECT referenceprel FROM plv WHERE annee_fichier = 2026 GROUP BY 1 HAVING count(*) > 1)
SELECT count(*) n_lignes, count(DISTINCT referenceprel) n_ref,
       count(DISTINCT referenceprel || cdreseau) n_ref_reseau,
       count(DISTINCT referenceprel || coalesce(inseecommuneprinc,'')) n_ref_commune
FROM plv WHERE annee_fichier = 2026 AND referenceprel IN (SELECT * FROM d);;
-- Exemple de referenceprel répété
WITH d AS (SELECT referenceprel FROM plv WHERE annee_fichier = 2026 GROUP BY 1 HAVING count(*) > 1 LIMIT 2)
SELECT cddept, cdreseau, inseecommuneprinc, nomcommuneprinc, cdreseauamont, pourcentdebit, referenceprel, dateprel, plvconformitebacterio, plvconformitechimique
FROM plv WHERE annee_fichier = 2026 AND referenceprel IN (SELECT * FROM d) ORDER BY referenceprel;;
-- pourcentdebit formats
SELECT pourcentdebit, count(*) n FROM plv WHERE annee_fichier = 2026 GROUP BY 1 ORDER BY n DESC LIMIT 15;;
-- conclusionprel les plus fréquentes
SELECT left(conclusionprel, 140) c, count(*) n FROM plv WHERE annee_fichier = 2026 GROUP BY 1 ORDER BY n DESC LIMIT 15

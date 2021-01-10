SELECT * 
FROM filelist_dts

-- SELECT * 
-- FROM filelist_dts
-- LIMIT 10

SELECT DISTINCT originalpath, searchablepath
FROM taxonomyschema_generaldts
WHERE href_type = 'XBRLORG'
GROUP BY originalpath;

SET lc_messages TO 'en_US.UTF-8';



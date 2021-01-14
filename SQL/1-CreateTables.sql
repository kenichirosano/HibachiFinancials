-- SELECT *
-- FROM pg_database;

DROP TABLE filelist_DTS;
CREATE TABLE IF NOT EXISTS filelist_DTS (
	filePath 	VARCHAR(200),
	PRIMARY KEY (filePath)
);

DROP TABLE taxonomyschema_generaldts;
CREATE TABLE IF NOT EXISTS taxonomyschema_generaldts (
	filepath 			VARCHAR(255)
	,tag				VARCHAR(20)
	,id					VARCHAR(255)
	,roleURI			VARCHAR(20)
	,childElementDict	VARCHAR(20)
	,PRIMARY KEY (filePath)
);

DROP TABLE roletype_generaldts;
CREATE TABLE IF NOT EXISTS roletype_generaldts (
	filepath 		VARCHAR(255)
	,tag			VARCHAR(20)
	,id				VARCHAR(255)
	,type			VARCHAR(20)
	,role			VARCHAR(20)
	,arcrole		VARCHAR(20)
	,base			VARCHAR(20)
	,originalpath	VARCHAR(255)
	,fragment_id	VARCHAR(255)
	,href_type		VARCHAR(20)
	,searchablepath	VARCHAR(255)
	,PRIMARY KEY (filePath)
);
roletype_generaldts

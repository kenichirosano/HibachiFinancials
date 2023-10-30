use hibachi;

# This takes 2 minutes
UPDATE raw_LabelExtendedLink	a
JOIN		CommonDTS					b
ON			a.filePath = b.filePath
SET 		a.document_id = b.document_id; 

# For labelLinks
DROP TEMPORARY TABLE IF EXISTS temp_LabelLoc;
CREATE TEMPORARY TABLE temp_LabelLoc (
	linkbase_id_Num				INT UNSIGNED,
    document_id			VARCHAR(255),
    Extended_label					VARCHAR(255),
    Extended_searchablePath	VARCHAR(255),
    Extended_fragment_ID		VARCHAR(255),
    
    PRIMARY KEY (linkbase_id_Num),
    INDEX(Extended_label)
);
INSERT INTO temp_LabelLoc
SELECT 	linkbase_id_Num	,
				document_id,
				Extended_label		,
				Extended_searchablePath	,
				Extended_fragment_ID		
FROM raw_LabelExtendedLink	a
WHERE 	Extended_tag 		= 'loc';

DROP TEMPORARY TABLE IF EXISTS temp_LabelArc;
CREATE TEMPORARY TABLE temp_LabelArc (
	linkbase_id_Num		INT UNSIGNED,
    document_id				INT UNSIGNED,
    Extended_tag				VARCHAR(255),
    Extended_arcrole		VARCHAR(255),
    Extended_fromAttr		VARCHAR(255),
    Extended_toAttr			VARCHAR(255),
    
    PRIMARY KEY (linkbase_id_Num),
    INDEX(
		Extended_fromAttr,
        Extended_toAttr
    )
);
INSERT INTO temp_LabelArc
SELECT 	linkbase_id_Num	,
				document_id,
				Extended_tag			,
				Extended_arcrole	,
				Extended_fromAttr	,
				Extended_toAttr		
FROM	raw_LabelExtendedLink
WHERE Extended_tag = 'labelArc';

DROP TEMPORARY TABLE IF EXISTS temp_Label;
CREATE TEMPORARY TABLE temp_Label (
	linkbase_id_Num		INT UNSIGNED,
    document_id				INT UNSIGNED,
    Extended_label			VARCHAR(255),
    Extended_role				VARCHAR(255),
    Extended_lang			VARCHAR(255),
    Extended_content		TEXT,
    
    PRIMARY KEY (linkbase_id_Num),
    INDEX(Extended_label)
);
INSERT INTO temp_Label
SELECT 	linkbase_id_Num,
				document_id,
				Extended_label,
				Extended_role,
				Extended_lang,
				Extended_content		
FROM	raw_LabelExtendedLink
WHERE	Extended_tag = 'label'
AND		Extended_role = 'http://www.xbrl.org/2003/role/label'; # Only specifying the normal label

# Concept with Label (normal label) takes 15 seconds
DROP TABLE IF EXISTS CommonLabelLink;
CREATE TABLE CommonLabelLink (
	document_id												INT UNSIGNED,
    Extended_arcrole										VARCHAR(255),
    Extended_fragment_ID								VARCHAR(255),
    Extended_role												VARCHAR(255),
    Extended_lang											VARCHAR(255),
    Extended_content										TEXT,
    
    PRIMARY KEY (
		document_id,
		Extended_fragment_ID,
        Extended_role,
		Extended_lang
    ),
    INDEX(
		Extended_fragment_ID
    )
);
INSERT INTO CommonLabelLink
SELECT  arc.document_id,
				arc.Extended_arcrole,
                loc.Extended_fragment_ID,
   				Extended_role,
				Extended_lang,
                label.Extended_content
FROM	temp_LabelArc	arc
JOIN 	temp_LabelLoc	loc
ON		arc.document_id 			= loc.document_id
AND	arc.Extended_fromAttr	= loc.Extended_label
JOIN	temp_Label			label
ON		arc.document_id				= label.document_id
AND	arc.Extended_toAttr		= label.Extended_label;


DROP TABLE IF EXISTS CommonConceptLabel;
CREATE TABLE CommonConceptLabel (
	name					VARCHAR(255) NOT NULL,
    id							VARCHAR(255),
    periodType			VARCHAR(255),
    balance				VARCHAR(255),
    type						VARCHAR(255),
    lang						VARCHAR(255),
    content				TEXT,
    
    PRIMARY KEY (
		name,
        id,
		lang
    ),
    INDEX(name)
);
TRUNCATE TABLE CommonConceptLabel;
INSERT INTO CommonConceptLabel
SELECT	DISTINCT 
				Concept.name,
                Concept.id,
                Concept.periodType,
                Concept.balance,
                Concept.type,
                LabelLink.Extended_lang,
                LabelLink.Extended_content
FROM	commonLabelLink 	LabelLink
JOIN 	CommonConcept	Concept
ON		Extended_fragment_ID 		= id;

select * 
from CommonConceptLabel
where lang = 'ja';






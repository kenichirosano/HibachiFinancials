USE hibachi;

# This takes 2 minutes
UPDATE CalculationExtendedLink	a
JOIN		CommonDTS					b
ON			a.filePath = b.filePath
SET 		a.document_id = b.document_id; 

# <loc> only
DROP TEMPORARY TABLE IF EXISTS temp_CalculationLoc_to;
CREATE TEMPORARY TABLE temp_CalculationLoc_to (
	linkbase_id_Num				INT UNSIGNED,
    document_id						VARCHAR(255),
    linkbaseLink_role				VARCHAR(255),    
    Extended_label					VARCHAR(255),
    Extended_searchablePath	VARCHAR(255),
    Extended_fragment_ID		VARCHAR(255),
    
    PRIMARY KEY (linkbase_id_Num),
    INDEX(Extended_label)
);
INSERT INTO temp_CalculationLoc_to
SELECT 	linkbase_id_Num,
				document_id,
				linkbaseLink_role,
                Extended_label,
				Extended_searchablePath,
				Extended_fragment_ID		
FROM CalculationExtendedLink	a
WHERE 	Extended_tag 		= 'loc';

DROP TEMPORARY TABLE IF EXISTS temp_CalculationLoc_from;
CREATE TEMPORARY TABLE temp_CalculationLoc_from (
	linkbase_id_Num				INT UNSIGNED,
    document_id						VARCHAR(255),
    linkbaseLink_role				VARCHAR(255),
    Extended_label					VARCHAR(255),
    Extended_searchablePath	VARCHAR(255),
    Extended_fragment_ID		VARCHAR(255),
    
    PRIMARY KEY (linkbase_id_Num),
    INDEX(Extended_label)
);
INSERT INTO temp_CalculationLoc_from
SELECT 	linkbase_id_Num,
				document_id,
                linkbaseLink_role,
				Extended_label,
				Extended_searchablePath,
				Extended_fragment_ID		
FROM CalculationExtendedLink	a
WHERE 	Extended_tag 		= 'loc';


# <calculationArc> only
DROP TEMPORARY TABLE IF EXISTS temp_CalculationArc;
CREATE TEMPORARY TABLE temp_CalculationArc (
	linkbase_id_Num				INT UNSIGNED,
    document_id						INT UNSIGNED,
    linkbaseLink_role				VARCHAR(255), 
    Extended_fromAttr				VARCHAR(255),
    Extended_toAttr					VARCHAR(255),
    Extended_weight				VARCHAR(255),
    Extended_orderAttr				FLOAT,
   
    
    PRIMARY KEY (linkbase_id_Num),
    INDEX(
		Extended_fromAttr,
        Extended_toAttr
    )
);
INSERT INTO temp_CalculationArc
SELECT 	linkbase_id_Num,
				document_id,
				linkbaseLink_role,
				Extended_fromAttr,
				Extended_toAttr,
                Extended_weight,
                Extended_orderAttr
FROM	CalculationExtendedLink
WHERE Extended_tag = 'calculationArc';

DROP TABLE IF EXISTS CommonCalculationLink;
CREATE TABLE CommonCalculationLink (
	document_id								INT UNSIGNED,
    linkbaseLink_role						VARCHAR(255),
    Extended_weight						VARCHAR(255),
    Extended_orderAttr						FLOAT,
    Summation_searchablePath		VARCHAR(255),
    Summation_fragment_ID			VARCHAR(255),
    Numeric_searchablePath			VARCHAR(255),
    Numeric_fragment_ID					VARCHAR(255),
    
    PRIMARY KEY (
		document_id,
		linkbaseLink_role,
        Summation_fragment_ID,
        Numeric_fragment_ID
    ),
    INDEX(
		Summation_searchablePath,
		Summation_fragment_ID,
        Numeric_searchablePath,
        Numeric_fragment_ID
    )
);
INSERT INTO CommonCalculationLink
SELECT  	arc.document_id,
					arc.linkbaseLink_role,
                    arc.Extended_weight,
                    arc.Extended_orderAttr,
					f.Extended_searchablePath,
					f.Extended_fragment_ID,
                    t.Extended_searchablePath,
					t.Extended_fragment_ID
FROM 		temp_CalculationArc	arc
LEFT JOIN	temp_CalculationLoc_from	f 
ON 				arc.Extended_fromAttr	= f.Extended_label
AND			arc.document_id				= f.document_id
AND			arc.linkbaseLink_role		= f.linkbaseLink_role
LEFT JOIN	temp_CalculationLoc_to		t 
ON 				arc.Extended_toAttr		= t.Extended_label
AND			arc.document_id				= t.document_id
AND			arc.linkbaseLink_role		= t.linkbaseLink_role;

select * from CommonCalculationLink order by linkbaseLink_role, Extended_orderAttr;

DROP TABLE IF EXISTS CommonConceptCalculation;
CREATE TABLE CommonConceptCalculation (
	name						VARCHAR(255) NOT NULL,
    id								VARCHAR(255),
    periodType				VARCHAR(255),
    balance					VARCHAR(255),
    type							VARCHAR(255),
    linkbaseLink_role	VARCHAR(255),
    preferredLabel			VARCHAR(255),
    orderAttr					TEXT,
    
    PRIMARY KEY (
		name,
        id
    ),
    INDEX(name)
);
TRUNCATE TABLE CommonConceptCalculation;
INSERT IGNORE INTO CommonConceptCalculation
SELECT	Concept.name,
                Concept.id,
                Concept.periodType,
                Concept.balance,
                Concept.type,
				CalculationLink.linkbaseLink_role,
                CalculationLink.Extended_preferredLabel,
                CalculationLink.Extended_orderAttr
FROM	CommonCalculationLink 	CalculationLink
JOIN 	Concept								Concept
ON		Extended_searchablePath	= filePath
AND	Extended_fragment_ID 		= id 
limit 10;







USE hibachi;

DROP TABLE IF EXISTS InstanceFiles;
CREATE TABLE IF NOT EXISTS InstanceFiles(
	documentSet_id 		INT UNSIGNED NOT NULL AUTO_INCREMENT,
	edinetCode 				VARCHAR(255),
    filingDate 				DATE,
    fiscalYear				DATE,
    documentType 		ENUM('Yuho','Tanshin'),
    repFileName 			VARCHAR(255),
    accountingMethod	VARCHAR(20),
    amendmentFlag		VARCHAR(20),
               	
    PRIMARY KEY(documentSet_id)             	
    ,CONSTRAINT unique_DocumentSet UNIQUE (edinetCode, filingDate, documentType, repFileName)
);

DROP TABLE IF EXISTS Context;
CREATE TABLE IF NOT EXISTS Context(
	documentSet_id 		INT UNSIGNED NOT NULL,
	id 							VARCHAR(255),
	identifier 					VARCHAR(255),
	instant 					VARCHAR(20),
	forever 					ENUM('True') DEFAULT NULL,
	startDate 				VARCHAR(20),
	endDate 					VARCHAR(20),
	segment 					VARCHAR(255),
	scenario 					CHAR(4),
	dimension 				VARCHAR(255),
	member 					VARCHAR(255),
	
	PRIMARY KEY (documentSet_id, id),
    INDEX(id)
);

DROP TABLE IF EXISTS Unit;
CREATE TABLE IF NOT EXISTS Unit(
	documentSet_id int unsigned not null,
	id 						VARCHAR(255),
	singleMeasure 	VARCHAR(255),
	divide 					VARCHAR(255),
	unitNumerator 	VARCHAR(255),
	unitDenominator 	VARCHAR(255),
		
	PRIMARY KEY (
		documentSet_id, 
        id
    )
);

DROP TABLE IF EXISTS Instance;
CREATE TABLE IF NOT EXISTS Instance(
	documentSet_id 	INT UNSIGNED NOT NULL,
	tag 						VARCHAR(255) 	NOT NULL,
	value 					BIGINT,
	unitRef 				VARCHAR(255),
	contextRef 			VARCHAR(255),
	precisionAttr 		VARCHAR(255), 
	decimals 				VARCHAR(255), 
	
	PRIMARY KEY (
		documentSet_id, 
        tag, 
        unitRef,
        contextRef
    ),
    INDEX(tag)
);

SELECT	a.contextRef,
                a.tag,
				a.value,
                a.decimals,
                b.instant,
                startDate,
                endDate
FROM Instance	a
JOIN	Context	b
ON		a.contextRef = b.id
AND	a.documentSet_id = b.documentSet_id;


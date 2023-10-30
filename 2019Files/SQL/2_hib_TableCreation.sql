use hibachi;

DROP TABLE IF EXISTS CommonDTS;
CREATE TABLE CommonDTS(
	document_id 	INT UNSIGNED NOT NULL AUTO_INCREMENT,
    filePath			VARCHAR(150),
    
	PRIMARY KEY(document_id),
    INDEX(filePath)
);

DROP TABLE IF EXISTS CommonDTSRelationShip;
CREATE TABLE CommonDTSRelationShip(
	parent_file		VARCHAR(150),
    child_file 			VARCHAR(150),
    relationship		VARCHAR(20),
    
	CONSTRAINT unique_CommonDTSRelationShip UNIQUE (parent_file, child_file, relationship)
);

/*-------------------------------------- Linkbase ------------------------------------------*/
/*
DROP TABLE IF EXISTS raw_CommonExtendedLink;
CREATE TABLE raw_CommonExtendedLink(
	linkbase_id_Num				INT UNSIGNED NOT NULL AUTO_INCREMENT,
	filePath 								VARCHAR(255),
	linkbaseLink_tag					VARCHAR(255),		-- labelLink, referenceLink, presentationLink, calculationLink, definitionLink
	linkbaseLink_role 				VARCHAR(255),
	Extended_tag 						VARCHAR(255),
	Extended_role 					VARCHAR(255),
	Extended_arcrole 				VARCHAR(255),
	Extended_label 					VARCHAR(255),
	Extended_lang 					VARCHAR(255),
	Extended_fromAttr 				VARCHAR(255),
	Extended_toAttr 					VARCHAR(255),
	Extended_preferredLabel 	VARCHAR(255),  	-- <presentationArc>
	Extended_weight 				VARCHAR(255),     -- <calculationArc>
	Extended_orderAttr 			VARCHAR(255),
	Extended_originalPath 		VARCHAR(255),
	Extended_searchablePath 	VARCHAR(180),
	Extended_fragment_ID 		VARCHAR(255),
	Extended_content 				TEXT,
	Extended_useAttr 				ENUM ('optional','prohibited') DEFAULT NULL,
	Extended_priority 				INT,
    
	PRIMARY KEY (linkbase_id_Num)
);*/

DROP TABLE IF EXISTS raw_LabelExtendedLink;
CREATE TABLE raw_LabelExtendedLink(
	linkbase_id_Num				INT UNSIGNED NOT NULL AUTO_INCREMENT,
    document_id						INT UNSIGNED,
	filePath 								VARCHAR(255),
	linkbaseLink_tag					VARCHAR(255),		-- labelLink, referenceLink, presentationLink, calculationLink, definitionLink
	linkbaseLink_role 				VARCHAR(255),
	Extended_tag 						VARCHAR(255),
	Extended_role 					VARCHAR(255),
	Extended_arcrole 				VARCHAR(255),
	Extended_label 					VARCHAR(255),
	Extended_lang 					VARCHAR(255),
	Extended_fromAttr 				VARCHAR(255),
	Extended_toAttr 					VARCHAR(255),
	Extended_preferredLabel 	VARCHAR(255),  	-- <presentationArc>
	Extended_weight 				VARCHAR(255),     -- <calculationArc>
	Extended_orderAttr 			VARCHAR(255),
	Extended_originalPath 		VARCHAR(255),
	Extended_searchablePath 	VARCHAR(180),
	Extended_fragment_ID 		VARCHAR(255),
	Extended_content 				TEXT,
	Extended_useAttr 				ENUM ('optional','prohibited') DEFAULT NULL,
	Extended_priority 				INT,
    
	PRIMARY KEY (linkbase_id_Num)
);

DROP TABLE IF EXISTS raw_PresentationExtendedLink;
CREATE TABLE raw_PresentationExtendedLink(
	linkbase_id_Num				INT UNSIGNED NOT NULL AUTO_INCREMENT,
    document_id						INT UNSIGNED,
	filePath 								VARCHAR(255),
	linkbaseLink_tag					VARCHAR(255),		-- labelLink, referenceLink, presentationLink, calculationLink, definitionLink
	linkbaseLink_role 				VARCHAR(255),
	Extended_tag 						VARCHAR(255),
	Extended_role 					VARCHAR(255),
	Extended_arcrole 				VARCHAR(255),
	Extended_label 					VARCHAR(255),
	Extended_lang 					VARCHAR(255),
	Extended_fromAttr 				VARCHAR(255),
	Extended_toAttr 					VARCHAR(255),
	Extended_preferredLabel 	VARCHAR(255),  	-- <presentationArc>
	Extended_weight 				VARCHAR(255),     -- <calculationArc>
	Extended_orderAttr 			VARCHAR(255),
	Extended_originalPath 		VARCHAR(255),
	Extended_searchablePath 	VARCHAR(180),
	Extended_fragment_ID 		VARCHAR(255),
	Extended_content 				TEXT,
	Extended_useAttr 				ENUM ('optional','prohibited') DEFAULT NULL,
	Extended_priority 				INT,
    
	PRIMARY KEY (linkbase_id_Num)
);

DROP TABLE IF EXISTS raw_CalculationExtendedLink;
CREATE TABLE raw_CalculationExtendedLink(
	linkbase_id_Num				INT UNSIGNED NOT NULL AUTO_INCREMENT,
    document_id						INT UNSIGNED,
	filePath 								VARCHAR(255),
	linkbaseLink_tag					VARCHAR(255),		-- labelLink, referenceLink, presentationLink, calculationLink, definitionLink
	linkbaseLink_role 				VARCHAR(255),
	Extended_tag 						VARCHAR(255),
	Extended_role 					VARCHAR(255),
	Extended_arcrole 				VARCHAR(255),
	Extended_label 					VARCHAR(255),
	Extended_lang 					VARCHAR(255),
	Extended_fromAttr 				VARCHAR(255),
	Extended_toAttr 					VARCHAR(255),
	Extended_preferredLabel 	VARCHAR(255),  	-- <presentationArc>
	Extended_weight 				VARCHAR(255),     -- <calculationArc>
	Extended_orderAttr 			VARCHAR(255),
	Extended_originalPath 		VARCHAR(255),
	Extended_searchablePath 	VARCHAR(180),
	Extended_fragment_ID 		VARCHAR(255),
	Extended_content 				TEXT,
	Extended_useAttr 				ENUM ('optional','prohibited') DEFAULT NULL,
	Extended_priority 				INT,
    
	PRIMARY KEY (linkbase_id_Num)
);


DROP TABLE IF EXISTS raw_CommonRoleType;
CREATE TABLE IF NOT EXISTS raw_CommonRoleType(
    roleType_id_Num 				INT unsigned NOT NULL AUTO_INCREMENT,
	filePath 								VARCHAR(255),
    roleType_tag 						VARCHAR(255),
    roleType_id 						VARCHAR(255), #optional
	roleType_roleURI 				VARCHAR(255),	#MUST This is equal to @role attribute of extended links
	roleType_arcroleURI 			VARCHAR(255),
	roleType_cyclesAllowed 		VARCHAR(255),
	roleTypeChild_tag 				VARCHAR(255),
    roleTypeChild_content 		VARCHAR(255),

	PRIMARY KEY (roleType_id_Num)
);

/*------------------------------- Concept -----------------------------------------*/
DROP TABLE IF EXISTS raw_CommonConcept;
CREATE TABLE raw_CommonConcept (
	filePath 					VARCHAR(255),
    name 						VARCHAR(255) NOT NULL, # Equals to instance's element tag (5.1.1)
	substitutionGroup 	VARCHAR(255) NOT NULL,
	id 							VARCHAR(255),
	periodType 				VARCHAR(255),
	balance 					VARCHAR(255),
	type 						VARCHAR(255),
	           	
	PRIMARY KEY(
		filePath, 
		name
    ),
	CONSTRAINT unique_Concept unique(filePath, id)
);
# Table 5: Correct signage in an XBRL instance
# balance="credit" & Positive => Credit
# balance="credit" & Negative => Debit
# balance="debit" & Positive => Debit
# balance="debit" & Negative => Credit


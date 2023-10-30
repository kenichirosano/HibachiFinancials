use financials;

/*-------------------------------------- Dropping the tables -------------------------------*/
DROP TABLE IF EXISTS ConceptWithLabel;
DROP TABLE IF EXISTS DocumentHasTaxonomySchema;
DROP TABLE IF EXISTS TaxonomySchema;
DROP TABLE IF EXISTS DocumentHasLinkbase;
DROP TABLE IF EXISTS PresentationLinkTreePath; 	# Created for presentation link
DROP TABLE IF EXISTS PresentationOrder;				# Created for presentation link
DROP TABLE IF EXISTS ExtendedLink;
DROP TABLE IF EXISTS LinkbaseLink;
DROP TABLE IF EXISTS Linkbase;
DROP TABLE IF EXISTS DocumentHasRoleRef;
DROP TABLE IF EXISTS RoleRef;
DROP TABLE IF EXISTS Context;
DROP TABLE IF EXISTS Unit;
DROP TABLE IF EXISTS DocumentHasConcept;
DROP TABLE IF EXISTS Concept;
DROP TABLE IF EXISTS DocumentHasRoletype;
DROP TABLE IF EXISTS RoletypeChild;
DROP TABLE IF EXISTS Roletype;
DROP TABLE IF EXISTS footnoteExtendedLink;
DROP TABLE IF EXISTS footnoteLink;
DROP TABLE IF EXISTS Instance;
DROP TABLE IF EXISTS DocumentSet;

/*-------------------------------------- Creating the tables -------------------------------*/
CREATE TABLE IF NOT EXISTS DocumentSet(
	documentSet_id 		INT UNSIGNED NOT NULL AUTO_INCREMENT,
	edinetCode 				VARCHAR(255),
    filingDate 				DATE,
    documentType 		ENUM('Yuho','Tanshin'),
    repFileName 			VARCHAR(255),
               	
    PRIMARY KEY(documentSet_id)             	
    -- ,FOREIGN KEY (edinetCode) REFERENCES EdinetCode(edinetCode)
    ,CONSTRAINT unique_DocumentSet UNIQUE (edinetCode, filingDate, documentType, repFileName)
);

CREATE TABLE IF NOT EXISTS Context(
	documentSet_id 		INT UNSIGNED NOT NULL,
	id 							VARCHAR(255),
	edinetCode 				VARCHAR(255),
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
	FOREIGN KEY (documentSet_id) REFERENCES documentSet(DocumentSet_id)	
);
CREATE INDEX contextID_idx on Context(id);


/*-------------------------------------- Unit ------------------------------------------*/
CREATE TABLE IF NOT EXISTS Unit(
	documentSet_id int unsigned not null,
	id varchar(255),
	singleMeasure varchar(255),
	divide varchar(255),
	unitNumerator varchar(255),
	unitDenominator varchar(255),
		
	PRIMARY KEY (documentSet_id, id),
	FOREIGN KEY (documentSet_id) REFERENCES documentSet(DocumentSet_id)	
);

/*-------------------------------------- Taxonomy Schema ------------------------------------------*/
CREATE TABLE IF NOT EXISTS TaxonomySchema(
	taxonomyInternal_id int unsigned not null AUTO_INCREMENT,
	searchablePath varchar(180),

	PRIMARY KEY (taxonomyInternal_id)
    ,constraint unique_TaxonomySchema unique(searchablePath)
);

/*------------------------- Many to Many Relation between DocumentSet and TaxonomySchema -------------------------*/
CREATE TABLE IF NOT EXISTS DocumentHasTaxonomySchema(
	tag varchar(255)
	,documentSet_id int unsigned not null
    ,taxonomyInternal_id int unsigned not null
    
    ,CONSTRAINT primary key(documentSet_id, taxonomyInternal_id)
    ,CONSTRAINT foreign key (documentSet_id) REFERENCES DocumentSet(documentSet_id)
    ,CONSTRAINT foreign key (taxonomyInternal_id) REFERENCES TaxonomySchema(taxonomyInternal_id)
);

/*-------------------------------------- Linkbases ------------------------------------------*/
CREATE TABLE IF NOT EXISTS Linkbase(
	linkbaseInternal_id int unsigned NOT NULL AUTO_INCREMENT,
	tag varchar(255),
	base varchar(255),
	currentPath varchar(255),
    generalLinkbase ENUM('General','Specific'), # Differentiate the general / company specific one
	
	PRIMARY KEY (linkbaseInternal_id),
    CONSTRAINT unique_Linkbase unique(tag, currentPath)
);

CREATE TABLE IF NOT EXISTS DocumentHasLinkbase(
	documentSet_id int unsigned not null,
    linkbaseInternal_id int unsigned not null,
    
    CONSTRAINT primary key (documentSet_id, linkbaseInternal_id)
    ,CONSTRAINT foreign key (documentSet_id) REFERENCES DocumentSet(documentSet_id)
    ,CONSTRAINT foreign key (linkbaseInternal_id) REFERENCES Linkbase(linkbaseInternal_id)
);

CREATE TABLE IF NOT EXISTS LinkbaseLink(
	linkbaseInternal_id int unsigned not null
	,linkbaseLinkInternal_id int unsigned NOT NULL AUTO_INCREMENT
	,tag varchar(255)
	,id varchar(255)
	,type varchar(255)
	,role varchar(255)
	,base varchar(255)
	
	,PRIMARY KEY (linkbaseLinkInternal_id)
	,FOREIGN KEY (linkbaseInternal_id) REFERENCES Linkbase(linkbaseInternal_id)
    ,CONSTRAINT unique_LinkbaseLink unique (linkbaseInternal_id, tag, role)
    /* In MySQL, treat LinkbaseLink in the same file as the same linkbase 
    for the sake of avoiding trouble in fetching foreign key id for ExtendedLink. */
);

CREATE TABLE IF NOT EXISTS ExtendedLink(
	linkbaseLinkInternal_id int unsigned not null,
    ExtendedLink_id int unsigned not null auto_increment,
	tag varchar(255),
	type varchar(255),
	role varchar(255),
	arcrole varchar(255),
	label varchar(255),
	lang varchar(255),
	fromAttr varchar(255),
	toAttr varchar(255),
	preferredLabel varchar(255),  /*<presentationArc> only*/
	weight varchar(255),          /*<calculationArc> only*/
	orderAttr varchar(255),
	originalPath varchar(255),
	searchablePath varchar(180),
	fragment_ID varchar(255),
	content text,
	useAttr enum ('optional','prohibited') default null,
	priority int,
	
	PRIMARY KEY (ExtendedLink_id)
	,FOREIGN KEY (linkbaseLinkInternal_id) REFERENCES LinkbaseLink(linkbaseLinkInternal_id)
    ,CONSTRAINT unique_ExtendedLink unique (linkbaseLinkInternal_id, tag, label, lang)
);
CREATE INDEX extendedLink_label_idx on ExtendedLink(label);	
/*------------------------------------------ End of linkbases -----------------------------------------------*/

CREATE TABLE IF NOT EXISTS RoleRef(
	roleRefInternal_id int unsigned NOT NULL AUTO_INCREMENT
	,tag varchar(255)
	,type varchar(255)
	,originalPath varchar(255)
	,searchablePath varchar(180)
    ,fragment_ID varchar(255)
	,roleURI varchar(255)
	,arcroleURI varchar(255)
	,currentPath varchar(255)
	
	,PRIMARY KEY (roleRefInternal_id)
    ,CONSTRAINT unique_RoleRef unique(roleURI, arcroleURI, currentPath)
);

CREATE TABLE IF NOT EXISTS DocumentHasRoleRef(
	documentSet_id int unsigned not null,
    roleRefInternal_id int unsigned not null,
    
    primary key (documentSet_id, roleRefInternal_id)
    ,foreign key (documentSet_id) REFERENCES DocumentSet(documentSet_id)
    ,foreign key (roleRefInternal_id) REFERENCES RoleRef(roleRefInternal_id)
);

/*------------------------------- Concept -----------------------------------------*/
CREATE TABLE Concept (
				conceptInternal_id INT unsigned NOT NULL AUTO_INCREMENT,
				name varchar(255) NOT NULL, # Equals to instance's element tag (5.1.1)
				substitutionGroup varchar(255) NOT NULL,
				id varchar(255),
				periodType varchar(255),
				balance varchar(255),
				type varchar(255),
				currentPath varchar(255),
                generalConcept ENUM('General','Specific'), # Differentiate the general / company specific one
               	
               	PRIMARY KEY(conceptInternal_id)
                ,CONSTRAINT unique_Concept unique(id, currentPath)
);
/* -------------------- XBRL Specification -----------------
Table 5: Correct signage in an XBRL instance
balance="credit" & Positive => Credit
balance="credit" & Negative => Debit
balance="debit" & Positive => Debit
balance="debit" & Negative => Credit
*/

/*---------------------------------- Relationship between DocumentSet and Concept -----------------------------------------*/
CREATE TABLE DocumentHasConcept(
	documentSet_id int unsigned not null,
    conceptInternal_id int unsigned not null,
    
    CONSTRAINT primary key (documentSet_id, conceptInternal_id)
    ,CONSTRAINT foreign key (documentSet_id) REFERENCES DocumentSet(documentSet_id)
    ,CONSTRAINT foreign key (conceptInternal_id) REFERENCES Concept(conceptInternal_id)
);


/*---------------------------------- Instance and footnotes -----------------------------------------*/
CREATE TABLE IF NOT EXISTS Instance(
	documentSet_id INT unsigned NOT NULL,
	tag varchar(255) NOT NULL,
	value bigint,
	unitRef varchar(255),
	contextRef varchar(255),
	precisionAttr varchar(255), 
	decimals varchar(255), 
	
	CONSTRAINT primary key (documentSet_id, tag, contextRef, unitRef),
	FOREIGN KEY (documentSet_id) REFERENCES DocumentSet(documentSet_id)
);

/* --------------------------------------------- Roletype ------------------------------------------------*/
CREATE TABLE IF NOT EXISTS Roletype(
    roleTypeInternal_id int unsigned NOT NULL AUTO_INCREMENT
	,tag varchar(255)
    ,id varchar(255)
	,roleURI varchar(255)
	,arcroleURI varchar(255)
	,cyclesAllowed varchar(255)
	,currentPath varchar(255)
	
	,CONSTRAINT primary key (roleTypeInternal_id)
    ,CONSTRAINT unique_RoleType unique(roleURI, arcroleURI, currentPath)
);

CREATE TABLE IF NOT EXISTS DocumentHasRoletype(
	documentSet_id int unsigned not null,
    roleTypeInternal_id int unsigned not null,
    
    primary key (documentSet_id, roleTypeInternal_id)
    ,foreign key (documentSet_id) REFERENCES DocumentSet(documentSet_id)
    ,foreign key (roleTypeInternal_id) REFERENCES Roletype(roleTypeInternal_id)
);

CREATE TABLE IF NOT EXISTS RoletypeChild(
	roleTypeInternal_id int unsigned not null
    ,roleTypeChildInternal_id int unsigned NOT NULL AUTO_INCREMENT
	,tag varchar(255)
    ,content varchar(255)
	
	,PRIMARY KEY (roleTypeChildInternal_id)
	,FOREIGN KEY (roleTypeInternal_id) REFERENCES Roletype(roleTypeInternal_id)
    # This table has lots of duplicate rows. However, since each linked to RoleType table rows, no need for unique constraint.
);

/* -------------------------------------------- footnote -------------------------------------------- */
CREATE TABLE IF NOT EXISTS FootnoteLink(
	documentSet_id INT unsigned NOT NULL
    ,footnoteLinkInternal_id int unsigned NOT NULL AUTO_INCREMENT
	,tag varchar(255)
	,type varchar(255)
	,role varchar(255)
	
	,primary key (footnoteLinkInternal_id)
	,FOREIGN KEY (documentSet_id) REFERENCES DocumentSet(documentSet_id)
);

CREATE TABLE IF NOT EXISTS FootnoteExtendedLink(
	footnoteLinkInternal_id int unsigned not null
    ,footnoteExtendedLinkInternal_id int unsigned NOT NULL AUTO_INCREMENT
	,footnoteID varchar(255)
    ,footnoteLinkRole varchar(255)
    ,footnoteRole varchar(255)
	,tag varchar(255)
	,type varchar(255)
	,role varchar(255)
	,arcrole varchar(255)
	,label varchar(255)
	,lang varchar(255)
	,fromAttr varchar(255)
	,toAttr varchar(255)
	,originalPath varchar(255)
	,searchablePath varchar(180)
	,fragment_ID varchar(255)
    ,content varchar(255)
	
	,PRIMARY KEY (footnoteExtendedLinkInternal_id)
	,FOREIGN KEY (footnoteLinkInternal_id) REFERENCES FootnoteLink(footnoteLinkInternal_id)
);


# This is for presentation order
DROP TABLE IF exists PresentationLinkTreePath;
CREATE TABLE IF NOT EXISTS PresentationLinkTreePath (
	documentSet_id int unsigned not null
    ,ancestorConcept_id int unsigned not null
    ,descendantConcept_id int unsigned not null
    ,orderNumber int
    ,role varchar(255)
    
    ,primary key (documentSet_id, ancestorConcept_id, descendantConcept_id, orderNumber, role)
);

# This is for presentation order
DROP TABLE IF exists PresentationOrder;
CREATE TABLE IF NOT EXISTS PresentationOrder (
	documentSet_id int unsigned not null
    ,role varchar(255)
    ,ancestorConcept_id int unsigned not null
    ,descendantConcept_id int unsigned not null
    ,orderNumber int not null
    ,deapth int unsigned not null
    ,orderInThisDocument int unsigned not null
    
    ,primary key (documentSet_id, role, ancestorConcept_id, descendantConcept_id, orderNumber, deapth)
);










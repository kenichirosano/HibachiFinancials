USE hibachi;

# This takes 2 minutes
UPDATE raw_PresentationExtendedLink	a
JOIN		CommonDTS						b
ON			a.filePath = b.filePath
SET 		a.document_id = b.document_id; 

# check if there's duplicates
/*
select * from PresentationExtendedLink a
join PresentationExtendedLink b
using(document_id,extended_tag,extended_label)
where a.linkbase_id_Num != b.linkbase_id_Num;
*/

DROP TEMPORARY TABLE IF EXISTS CommonPresentationLoc;
CREATE TEMPORARY TABLE CommonPresentationLoc (
	linkbaseLink_role				VARCHAR(255),
	Extended_label					VARCHAR(255),
    Extended_searchablePath	VARCHAR(255),
    Extended_fragment_ID		VARCHAR(255),
    
    PRIMARY KEY (
		linkbaseLink_role,
        Extended_label,
        Extended_searchablePath,
        Extended_fragment_ID
    )
);
INSERT INTO CommonPresentationLoc
SELECT 	DISTINCT
				linkbaseLink_role,
				Extended_label,
				Extended_searchablePath,
				Extended_fragment_ID		
FROM raw_PresentationExtendedLink	a
WHERE 	Extended_tag 		= 'loc';

DROP TABLE IF EXISTS CommonPresentationArc;
CREATE TABLE CommonPresentationArc (
	id											INT UNSIGNED NOT NULL AUTO_INCREMENT,
    linkbaseLink_role				VARCHAR(255), 
    Extended_fromAttr				VARCHAR(255),
    Extended_toAttr					VARCHAR(255),
    Extended_preferredLabel	VARCHAR(255),
    Extended_orderAttr				FLOAT,
    Extended_priority 				INT,
    
    PRIMARY KEY(id)
);
INSERT INTO CommonPresentationArc (
	linkbaseLink_role,
	Extended_fromAttr,
	Extended_toAttr,
    Extended_preferredLabel,
	Extended_orderAttr,
	Extended_priority
)
SELECT 	DISTINCT
				linkbaseLink_role,
				Extended_fromAttr,
				Extended_toAttr,
				Extended_preferredLabel,
				Extended_orderAttr,
				CASE
					WHEN Extended_priority IS NULL THEN 0
					ELSE 	Extended_priority
				END
FROM	raw_PresentationExtendedLink
WHERE Extended_tag = 'presentationArc';

# This represents the order of all of the common concepts (own id, parent id,depth, order)
DROP TABLE IF EXISTS CommonPresentationOrder;
CREATE TABLE CommonPresentationOrder (
	parent_id		INT,
    id					INT UNSIGNED NOT NULL,
    depth 			INT,
    orderNo		INT,
    
    PRIMARY KEY(
		parent_id,
        id
    )
);
# Insert the root presentation arcs
INSERT INTO CommonPresentationOrder
SELECT 	-1,
				id,
                0,
				1
FROM (	
	SELECT 	id, 
					linkbaseLink_role				AS role,
                    Extended_preferredLabel,
					Extended_fromAttr				AS parent
	FROM 	CommonPresentationArc
	WHERE 	Extended_orderAttr = 1
) a
LEFT JOIN	(
	SELECT 	DISTINCT 
					linkbaseLink_role		AS role,
					Extended_toAttr			AS child
	FROM 	CommonPresentationArc
) b
ON		a.role = b.role
AND	a.parent = b.child
WHERE b.child IS NULL; 

# insert the 1st child tree presentation arcs (This is done in python.)
/*
DELETE FROM CommonPresentationOrder WHERE depth > 0;
INSERT INTO CommonPresentationOrder
SELECT	DISTINCT
				parent.id,
                child.id,
                1,
                child.Extended_orderAttr
FROM (
	SELECT	a.id,
					linkbaseLink_role,
					Extended_toAttr
	FROM	CommonPresentationOrder	a
	JOIN	CommonPresentationArc		b
	ON		a.id = b.id
    WHERE a.depth = 0
) parent
JOIN CommonPresentationArc child
ON		parent.linkbaseLink_role = child.linkbaseLink_role
AND	parent.Extended_toAttr 	= child.Extended_fromAttr;
*/

# List of the root presentation arcs
SELECT	b.linkbaseLink_role,
				b.Extended_fromAttr,
                b.Extended_preferredLabel,
                c.Extended_SearchablePath,
                c.Extended_fragment_ID,
                e.*
FROM CommonPresentationOrder	a
JOIN	CommonPresentationArc		b ON a.id = b.id 
LEFT JOIN	CommonPresentationLoc		c 
ON		b.linkbaseLink_role = c.linkbaseLink_role
AND	b.Extended_fromAttr = c.Extended_label
LEFT JOIN	CommonConceptLabel			e
ON		c.Extended_fragment_ID		= e.id
where depth = 0 ;

SELECT max(depth) FROM CommonPresentationOrder;

SELECT	DISTINCT 
				child0.id, child0.depth, child0.orderNo,
				child1.id, child1.depth, child1.orderNo,
                child2.id, child2.depth, child2.orderNo,
                child3.id, child3.depth, child3.orderNo,
                child4.id, child4.depth, child4.orderNo,
                child5.id, child5.depth, child5.orderNo,
                child6.id, child6.depth, child6.orderNo,
                child7.id, child7.depth, child7.orderNo
FROM	CommonPresentationOrder			child0
JOIN	CommonPresentationOrder	child1
ON		child0.id = child1.parent_id 
JOIN	CommonPresentationOrder	child2
ON		child1.id = child2.parent_id 
JOIN	CommonPresentationOrder	child3
ON		child2.id = child3.parent_id
JOIN	CommonPresentationOrder	child4
ON		child3.id = child4.parent_id
JOIN	CommonPresentationOrder	child5
ON		child4.id = child5.parent_id
JOIN	CommonPresentationOrder	child6
ON		child5.id = child6.parent_id
JOIN	CommonPresentationOrder	child7
ON		child6.id = child7.parent_id 
WHERE 	
child0.depth = 0 
AND child2.depth = 2
AND child3.depth = 3
AND child4.depth = 4
AND child5.depth = 5
AND child6.depth = 6
AND child7.depth = 7
ORDER BY	child0.id,
					child1.orderNo,
					child2.orderNo,
                    child3.orderNo,
                    child4.orderNo,
                    child5.orderNo,
                    child6.orderNo,
                    child7.orderNo;


DROP TEMPORARY TABLE IF EXISTS temp_PresentationArc_root;
CREATE TEMPORARY TABLE temp_PresentationArc_root (
	linkbase_id_Num				INT UNSIGNED,
    document_id						INT UNSIGNED,
    linkbaseLink_role				VARCHAR(255), 
    Extended_fromAttr				VARCHAR(255),
    Extended_toAttr					VARCHAR(255),
    Extended_preferredLabel	VARCHAR(255),
    Extended_orderAttr				FLOAT,
    
    
    PRIMARY KEY (linkbase_id_Num),
    INDEX(
		Extended_fromAttr,
        Extended_toAttr
    )
);
INSERT INTO temp_PresentationArc_root
SELECT 	linkbase_id_Num,
				document_id,
				linkbaseLink_role,
				Extended_fromAttr,
				Extended_toAttr,
                Extended_preferredLabel,
                Extended_orderAttr
FROM	raw_PresentationExtendedLink
WHERE Extended_tag = 'presentationArc'
AND 		Extended_orderAttr = 1;

# Get the presentation arc that are not in "toAttr", which means the presentation arc is root
DROP TABLE IF EXISTS PresentationLinkRoot;
CREATE TEMPORARY TABLE PresentationLinkRoot(
	linkbaseLink_role				VARCHAR(255), 
    Extended_fromAttr				VARCHAR(255),
    Extended_toAttr					VARCHAR(255),
    Extended_preferredLabel	VARCHAR(255),
    Extended_orderAttr				FLOAT,
    roleType_id 						VARCHAR(255),
	roleTypeChild_content 		VARCHAR(255),
   
    PRIMARY KEY (
		linkbaseLink_role,
        Extended_fromAttr,
        Extended_toAttr
    ),
    INDEX(
		Extended_fromAttr,
        Extended_toAttr
    )
);
INSERT IGNORE INTO PresentationLinkRoot
SELECT	linkbaseLink_role,
				Extended_fromAttr,
				Extended_toAttr,
				Extended_preferredLabel,
				Extended_orderAttr,
				roleType_id,
				roleTypeChild_content 
FROM temp_presentationarc_root
JOIN 	commonroletype 
ON linkbaseLink_role = roleType_roleURI
WHERE Extended_fromAttr NOT IN
(
	SELECT a.Extended_fromAttr
	FROM (
	SELECT 		linkbase_id_Num,
						document_id,
						linkbaseLink_role,
						Extended_fromAttr
	FROM	temp_presentationarc_a
	) a
	JOIN (
		SELECT 	DISTINCT
						document_id,
						linkbaseLink_role,
						Extended_toAttr
		FROM temp_presentationarc_b
	) b	
	#ON		a.document_id			= b.document_id
	#AND	a.linkbaseLink_role 	= b.linkbaseLink_role
	ON	a.Extended_fromAttr	= b.Extended_toAttr
);



select * 
FROM	temp_presentationarc_root 
JOIN	commonroletype ON linkbaseLink_role = roleType_roleURI 
WHERE roleTypeChild_tag = 'definition'
limit 10;

# Concept with Label (normal label) takes 15 seconds
DROP TABLE IF EXISTS CommonPresentationLink;
CREATE TABLE CommonPresentationLink (
	document_id												INT UNSIGNED,
    Extended_fragment_ID								VARCHAR(255),
    linkbaseLink_role										VARCHAR(255),
    Extended_preferredLabel							VARCHAR(255),
    Extended_orderAttr										FLOAT,
    
    PRIMARY KEY (
		document_id,
		Extended_fragment_ID,
        linkbaseLink_role,
        Extended_orderAttr
    ),
    INDEX(
		Extended_fragment_ID
    )
);
INSERT INTO CommonPresentationLink
SELECT  arc.document_id,
                loc.Extended_fragment_ID,
   				arc.linkbaseLink_role,
                arc.Extended_preferredLabel,
                arc.Extended_orderAttr
FROM	temp_PresentationArc	arc
JOIN 	temp_PresentationLoc	loc
ON		arc.document_id 			= loc.document_id
AND	arc.Extended_toAttr	= loc.Extended_label;


DROP TABLE IF EXISTS CommonConceptPresentation;
CREATE TABLE CommonConceptPresentation (
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
TRUNCATE TABLE CommonConceptPresentation;
INSERT IGNORE INTO CommonConceptPresentation
SELECT	Concept.name,
                Concept.id,
                Concept.periodType,
                Concept.balance,
                Concept.type,
				PresentationLink.linkbaseLink_role,
                PresentationLink.Extended_preferredLabel,
                PresentationLink.Extended_orderAttr
FROM	CommonPresentationLink 	PresentationLink
JOIN 	CommonConcept				Concept
ON		Extended_fragment_ID 		= id;








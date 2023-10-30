USE financials;

# Classify Concept table into General and Specific
UPDATE Concept
SET generalConcept = 'General'
WHERE currentPath like 'dtr/%'
and generalConcept is Null;

UPDATE Concept
SET generalConcept = 'General'
WHERE currentPath like 'taxonomy/%'
and generalConcept is Null;

UPDATE Concept
SET generalConcept = 'General'
WHERE currentPath like '2003/%'
and generalConcept is Null;

UPDATE Concept
SET generalConcept = 'General'
WHERE currentPath like '2005/%'
and generalConcept is Null;

UPDATE Concept
SET generalConcept = 'General'
WHERE currentPath like '2006/%'
and generalConcept is Null;

# Classify Linkbase table into General and Specific
UPDATE Linkbase
SET generalLinkbase = 'General'
WHERE currentPath like 'taxonomy/%'
and generalLinkbase is Null;

UPDATE Linkbase
SET generalLinkbase = 'Specific'
WHERE currentPath like 'financials/%'
and generalLinkbase is Null;

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Combine Concept and Label
DROP TABLE IF exists ConceptWithLabel;
CREATE TABLE IF NOT EXISTS ConceptWithLabel (
	conceptInternal_id int(10) unsigned,
    label_j text,
    label_e text,
	name varchar(255),
    id varchar(255),
	periodType varchar(255),
    balance varchar(255),
    type varchar(255),
    currentPath varchar (255),
    generalConcept enum('General','Specific')
    
    ,primary key (conceptInternal_id)
);
INSERT INTO ConceptWithLabel
SELECT 
			a.conceptInternal_id
            ,label_j.content # adding a label here
            ,null
			,a.name # this is equal to the tag in Instance
            ,a.id
            ,a.periodType
            ,a.balance
            ,a.type
            ,a.currentPath
            ,a.generalConcept
FROM Concept a 
LEFT JOIN ExtendedLink loc on a.id = loc.fragment_ID and a.currentPath = loc.searchablePath
LEFT JOIN ExtendedLink labelArc_j on loc.linkbaselinkInternal_id = labelArc_j.linkbaselinkInternal_id and loc.label = labelArc_j.fromAttr
LEFT JOIN ExtendedLink label_j on labelArc_j.linkbaselinkInternal_id = label_j.linkbaselinkInternal_id and labelArc_j.toAttr = label_j.label
WHERE loc.tag = 'loc'
and labelArc_j.tag='labelArc' 
and label_j.tag = 'label' and label_j.role = 'http://www.xbrl.org/2003/role/label' and label_j.lang = 'ja'
and a.generalConcept = 'General';

DROP TEMPORARY TABLE IF EXISTS tempConceptWithLabel_E;
CREATE TEMPORARY TABLE IF NOT EXISTS tempConceptWithLabel_E (
	conceptInternal_id int(10) unsigned,
    label_e text
    
    ,primary key (conceptInternal_id)
);
INSERT INTO tempConceptWithLabel_E
SELECT 	a.conceptInternal_id
				,label_e.content
FROM Concept a 
LEFT JOIN ExtendedLink loc on a.id = loc.fragment_ID and a.currentPath = loc.searchablePath
LEFT JOIN ExtendedLink labelArc_e on loc.linkbaselinkInternal_id = labelArc_e.linkbaselinkInternal_id and loc.label = labelArc_e.fromAttr
LEFT JOIN ExtendedLink label_e on labelArc_e.linkbaselinkInternal_id = label_e.linkbaselinkInternal_id and labelArc_e.toAttr = label_e.label
WHERE loc.tag = 'loc' 
and labelArc_e.tag='labelArc' 
and label_e.tag = 'label' and label_e.role = 'http://www.xbrl.org/2003/role/label' and label_e.lang = 'en'
and a.generalConcept = 'General';
            
UPDATE  ConceptWithLabel X
LEFT JOIN tempConceptWithLabel_E Y ON X.conceptInternal_id = Y.conceptInternal_id
SET X.label_e = Y.label_e;
# select * from ConceptWithLabel;


# -------------------------------------------------------------- Create temp tables with a specified documentSet_id to work on a single document -------------------------------------------
# Create temprary table for Concept with a specified documentSet_id
DROP TEMPORARY TABLE IF EXISTS tempConceptForDocumentSet;
CREATE TEMPORARY TABLE tempConceptForDocumentSet(
	documentSet_id int,
    conceptInternal_id int,
    label_j text,
    label_e text,
    name varchar(255) ,
    id varchar(255),
    periodType varchar(255),
    balance varchar(255),
    currentPath varchar(255),
    generalConcept  ENUM('General','Specific'),
    
    Primary Key (documentSet_id, conceptInternal_id)
);
INSERT INTO tempConceptForDocumentSet
SELECT	b.documentSet_id,
				a.conceptInternal_id,
                a.label_j,
                a.label_e,
                a.name,
                a.id,
                a.periodType,
                a.balance,
                currentPath,
                generalConcept
FROM ConceptWithLabel a
JOIN DocumentHasConcept b ON a.conceptInternal_id = b.conceptInternal_id;
#WHERE b.documentSet_id = @documentSet_idNum;
# Select * from tempConceptForDocumentSet

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Calculate the values 
DROP TABLE IF EXISTS InstanceWithConcepts;
CREATE TABLE InstanceWithConcepts(
			documentSet_id int unsigned not null,
            conceptInternal_id int,
			label_j text,
            label_e text,
			value bigint,
			decimals varchar(255),
			unitRef varchar(255),
            singleMeasure varchar(255),
			contextRef varchar(255),
            instant varchar(20),
           	startDate varchar(20),
			endDate varchar(20), 
			generalConcept enum('General','Specific'),
			
            PRIMARY KEY(documentSet_id, conceptInternal_id, contextRef)
);
insert into InstanceWithConcepts
select	Instance.documentSet_id,
            tempConcept.conceptInternal_id,
            tempConcept.label_j,
            tempConcept.label_e,
            Instance.value,
            Instance.decimals,
			Instance.unitRef,
            Unit.singleMeasure,
			Instance.contextRef,
			Context.instant,
			Context.startDate,
			Context.endDate,
            tempConcept.generalConcept
from Instance
join tempConceptForDocumentSet tempConcept 
on Instance.tag = tempConcept.name and Instance.documentSet_id = tempConcept.documentSet_id
join Context 
on Instance.contextRef = Context.id and Instance.documentSet_id = Context.documentSet_id
join Unit
on Instance.unitRef = Unit.id and Instance.documentSet_id = Unit.documentSet_id
where Instance.contextRef in ('CurrentYearInstant', 'CurrentYearDuration','Prior1YearDuration','Prior1YearInstant')
and Context.scenario is NULL; # Consolidated statements are wher scenario in Context table is null
#and Instance.documentSet_id = @documentSet_idNum
#select * from InstanceWithConcepts;






use financials;

-- for tableau
ALTER SCHEMA `financials`  DEFAULT COLLATE utf8_bin;
ALTER TABLE `financials`.`EdinetCode` CONVERT TO CHARACTER SET UTF8MB3;

show databases;
SHOW CHARACTER SET;
show tables;
SELECT default_character_set_name FROM information_schema.SCHEMATA WHERE schema_name = "financials";
SHOW FIELDS FROM concept;

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Playing around presentation
select 
            t1.role,
			t1.ancestorConcept_id,
            t1.descendantConcept_id,
            t1.orderNumber,
            t2.role,
            t2.ancestorConcept_id,
            t2.descendantConcept_id,
            t2.orderNumber,
            t3.role,
            t3.ancestorConcept_id,
            t3.descendantConcept_id,
            t3.orderNumber
from PresentationLinkTreePath t1
left join PresentationLinkTreePath t2 on t1.descendantConcept_id = t2.ancestorConcept_id and t1.documentSet_id = t2.documentSet_id
left join PresentationLinkTreePath t3 on t2.descendantConcept_id = t3.ancestorConcept_id and t2.documentSet_id = t3.documentSet_id
where t1.ancestorConcept_id not in (select descendantConcept_id from PresentationLinkTreePath)
and t1.documentSet_id = 1
and t1.role = 'http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_ConsolidatedBalanceSheet'
order by t1.role, t1.ancestorConcept_id, t1.orderNumber, t2.role, t2.orderNumber, t3.role, t3.orderNumber;


/********************************************* For calculation link **********************************************/
DROP TEMPORARY TABLE IF EXISTS tempCalculationArcFrom;
CREATE TEMPORARY TABLE tempCalculationArcFrom
select
	a.*
    ,b.tag
    ,b.fromAttr
	,b.toAttr
    ,b.weight
    ,b.orderAttr
from tempLoc a join ExtendedLink b 
on a.label = b.fromAttr
and a.linkbaseLinkInternal_id = b.linkbaseLinkInternal_id 
where b.tag = 'calculationArc';
CREATE INDEX tempCalculationArcFrom_idx on tempCalculationArcFrom(toAttr);

select * from ExtendedLink where linkbaseLinkInternal_id = 79;
select * from LinkbaseLink where tag = 'labelLink';
select * from tempLoc;
select * from tempCalculationArcFrom;

DROP TEMPORARY TABLE IF EXISTS tempCalculationArcTo;
CREATE TEMPORARY TABLE tempCalculationArcTo
select * from tempCalculationArcFrom;
CREATE INDEX tempCalculationArcTo_idx on tempCalculationArcTo(label);

select a.contextRef, a.instant, a.value ,a.label, a.linkbaseLinkInternal_id, sum(b.value) 
from tempCalculationArcFrom a
join tempLoc b
on a.toAttr = b.label and a.linkbaseLinkInternal_id = b.linkbaseLinkInternal_id
group by a.contextRef, a.instant, a.value, a.label, a.linkbaseLinkInternal_id;

DROP TEMPORARY TABLE IF EXISTS tempCalc;
CREATE TEMPORARY TABLE tempCalc
select
	a.contextRef
    ,a.fromAttr
	,sum(b.value)
    ,count(b.toAttr)
from tempCalculationArc a 
join ExtendedLink b on a.toAttr = b.label and a.linkbaseLinkInternal_id = b.linkbaseLinkInternal_id
where b.tag = 'loc'
group by a.contextRef, a.fromAttr;


# ------------------------------------------------------------------------- EdinetCode -------------------------------------------------

# Number of the listed companies by the industry
select listed, industry, count(distinct EdinetCode) AS 'No. of Company'
from EdinetCode 
where listed = '上場'
group by listed, industry
order by count(distinct EdinetCode) desc;

select * from edinetcode
where listed like '上場';

# ------------------------------------------------------------------------- DocumentSet -------------------------------------------------
SELECT * from DocumentSet;
SELECT * from TaxonomySchema;

SELECT * from linkbase;
select * from DocumentHasTaxonomySchema;

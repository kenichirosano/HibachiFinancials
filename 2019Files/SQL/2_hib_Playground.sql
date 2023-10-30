USE hibachi;


show tables;
-- for tableau
ALTER SCHEMA `hibachi`  DEFAULT COLLATE utf8_bin;
ALTER TABLE `hibachi`.`CommonDTSRelationShip_temp` CONVERT TO CHARACTER SET UTF8MB3;


SELECT * FROM Instance;
SELECT distinct type FROM CommonConceptLabel;
SELECT * FROM CommonConceptLabel;

SELECT * 
FROM	Instance							a
JOIN	CommonConceptLabel	b
ON 		a.tag = b.name;

select * from LabelExtendedLink;
select * from PresentationExtendedLink;
select * from CalculationExtendedLink;




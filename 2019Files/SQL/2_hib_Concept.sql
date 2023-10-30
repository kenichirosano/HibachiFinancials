USE hibachi;

DROP TABLE IF EXISTS CommonConcept;
CREATE TABLE CommonConcept (
    name 						VARCHAR(255) NOT NULL, # Equals to instance's element tag (5.1.1)
	substitutionGroup 	VARCHAR(255) NOT NULL,
	id 							VARCHAR(255),						#Equals to linkbase fragment ID
	periodType 				VARCHAR(255),
	balance 					VARCHAR(255),
	type 						VARCHAR(255),
	           	
	PRIMARY KEY(name),
    INDEX(id)
);
INSERT IGNORE INTO CommonConcept
SELECT	name,
				substitutionGroup,
				id,
                periodType,
                balance,
                type
FROM 	raw_CommonConcept
GROUP BY name,
					substitutionGroup,
					id,
					periodType,
					balance,
					type;

select	a.name,
			a.substitutionGroup,
            a.id,
            a.periodType,
            a.balance,
            a.type,
            b.lang,
            b.content
from CommonConcept			a
join	CommonConceptLabel	b
on	a.name = b.name
AND	a.id = b.id;




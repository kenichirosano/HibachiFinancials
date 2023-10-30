USE hibachi;

/*
Note on April 3, 2019
Checked the common <roleType> - <usedOn> elements all and none had content in itself.
You can ignore <usedOn> for a while.

SELECT 	DISTINCT roleType_tag
FROM raw_CommonRoleType;

SELECT 	*
FROM 	raw_CommonRoleType
WHERE 	roleType_arcroleURI IS NOT NULL
OR			roleType_cyclesAllowed IS NOT NULL;

Note on April 6, 2019
Checked commonDTS has only roleType as role type tag.
Checked all the roleType_arcroleURI, roleType_cyclesAllowed are null.
you can ignore them for a while
*/

DROP TABLE IF EXISTS CommonRoleType;
CREATE TABLE IF NOT EXISTS CommonRoleType(
    roleType_id 						VARCHAR(255),
	roleType_roleURI 				VARCHAR(255),
	roleTypeChild_content 		VARCHAR(255),

	PRIMARY KEY (
		roleType_id,
        roleType_roleURI
    )
);
INSERT IGNORE INTO CommonRoleType
SELECT 	DISTINCT
				roleType_id,
				roleType_roleURI,
                roleTypeChild_content
FROM 	raw_CommonRoleType
WHERE 	roleTypeChild_tag = 'definition';

select * from CommonRoleType;

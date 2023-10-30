use financials;

/* --------------------------------- Assumptions --------------------------------- */
SET @documentSet_idNum = 3;

# Find what role is reported in the document
DROP TEMPORARY TABLE IF EXISTS tempRoleURI;
CREATE TEMPORARY TABLE tempRoleURI
select f.name
		, b.roleTypeInternal_id
		, a.roleURI
        , c.tag
        , c.content
from RoleRef a
join RoleType b on a.searchablePath = b.currentPath 
and a.fragment_ID = b.id
and a.roleURI = b.roleURI
join RoletypeChild c on b.roleTypeInternal_id = c.roleTypeInternal_id
join DocumentHasRoleRef d on a.roleRefInternal_id = d.roleRefInternal_id
join DocumentSet e on d.documentSet_id = e.documentSet_id
join EdinetCode f on e.edinetCode = f.edinetCode
where e.documentSet_id = @documentSet_idNum
and c.tag = 'definition';

SELECT * FROM tempRoleURI WHERE content IN (
	'連結貸借対照表',
    '連結損益計算書',
    '連結キャッシュ・フロー計算書　間接法',
    '連結キャッシュ・フロー計算書　直接法'
);





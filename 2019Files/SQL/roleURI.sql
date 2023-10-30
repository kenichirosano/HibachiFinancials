USE Financials;

# ------------------------------------------------ Set the variables here -----------------------------------------
SET @selectLang = 'ja';

SET @roleURI = 'http://www.xbrl.org/2003/role/label'; #標準ラベル @role attribute in <label>
DROP TEMPORARY TABLE IF EXISTS tempRoleURIListToBeSelected;
CREATE TEMPORARY TABLE tempRoleURIListToBeSelected(
	roleURI varchar(255)
);
INSERT INTO tempRoleURIListToBeSelected SELECT '連結貸借対照表';
INSERT INTO tempRoleURIListToBeSelected SELECT '連結損益計算書';
INSERT INTO tempRoleURIListToBeSelected SELECT '連結キャッシュ・フロー計算書　間接法';
INSERT INTO tempRoleURIListToBeSelected SELECT '連結キャッシュ・フロー計算書　直接法';
INSERT INTO tempRoleURIListToBeSelected SELECT '注記番号';
# select * from tempRoleURIListToBeSelected;
# select * from RoleRef;

# Find what role is reported in the document
DROP TEMPORARY TABLE IF EXISTS tempRoleURIForDocumentSet;
CREATE TEMPORARY TABLE tempRoleURIForDocumentSet
select	f.name
			,b.roleTypeInternal_id
			,a.roleURI
			,c.tag
			,c.content
from RoleRef a
join RoleType b on a.searchablePath = b.currentPath and a.fragment_ID = b.id and a.roleURI = b.roleURI
join RoletypeChild c on b.roleTypeInternal_id = c.roleTypeInternal_id
join DocumentHasRoleRef d on a.roleRefInternal_id = d.roleRefInternal_id
join DocumentSet e on d.documentSet_id = e.documentSet_id
join EdinetCode f on e.edinetCode = f.edinetCode
where e.documentSet_id = @documentSet_idNum
and c.tag = 'definition'
and c.content IN (select * from tempRoleURIListToBeSelected);
select * from tempRoleURIForDocumentSet;

# 
Select distinct role from PresentationOrder 
where role = 'http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_ConsolidatedBalanceSheet';


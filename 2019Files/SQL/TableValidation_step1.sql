use financials;

/*  
1. Create temp table to store the number of taxonomy schema is linked to the document.
	This table only contains edinetCode/DocumentSet tables info (ticker, english name, filingDate)..
	2. Update the temp table
    3. Show the results
*/

SET SQL_SAFE_UPDATES = 0; # To allow updating without primary key

/* -- Step 1. Create temp table to store the number of taxonomy schema is linked to the document. */
DROP TEMPORARY TABLE IF EXISTS tempStats;
CREATE TEMPORARY TABLE tempStats(
	ticker int unsigned not null,
    nameEnglish varchar(100),
    nameJapanese varchar(100),
    documentSet_id int unsigned not null,
    filingDate date,
    taxonomy int,
    concept int,
    linkbase int,
    linkbaseLink int,
    extendedLink int,
    roleRef int,
    roleType int,
    
    primary key (documentSet_id)
);

insert into tempStats
select left (b.ticker, 4),
		 b.nameEnglish,
        b.name,
        a.documentSet_id,
		a.filingDate,
		count(c.taxonomyInternal_id),
        null,
        null,
        null,
        null,
        null,
        null
from DocumentSet a
join EdinetCode b
	on a.edinetCode = b.edinetCode
join DocumentHasTaxonomySchema c
	on a.documentSet_id = c.documentSet_id
group by c.documentSet_id;


# -- Step 2. Update the tempStats table with the stats
update tempStats x
join (
		select	a.documentSet_id
				,count(c.conceptInternal_id) as concept
		from DocumentSet a
		join DocumentHasConcept c
			on a.documentSet_id = c.documentSet_id
		group by a.documentSet_id
) y on x.documentSet_id = y.documentSet_id
set x.concept = y.concept;

update tempStats x
join (
	select	a.documentSet_id
			,count(c.linkbaseInternal_id) as linkbase
	from DocumentSet a
	join DocumentHasLinkbase c
		on a.documentSet_id = c.documentSet_id
	group by a.documentSet_id
) y on x.documentSet_id = y.documentSet_id
set x.linkbase = y.linkbase;

update tempStats x
join (
	select 	a.documentSet_id
			,count(d.linkbaseLinkInternal_id) as linkbaseLink
	from DocumentSet a
	join DocumentHasLinkbase c on a.documentSet_id = c.documentSet_id
	join LinkbaseLink d on c.linkbaseInternal_id = d.linkbaseInternal_id
	group by a.documentSet_id
) y on x.documentSet_id = y.documentSet_id
set x.linkbaseLink = y.linkbaseLink;

update tempStats x
join (
		select a.documentSet_id
				, count(distinct e.extendedLink_id) as extendedLink
		from DocumentSet a
		join DocumentHasLinkbase c on a.documentSet_id = c.documentSet_id
		join LinkbaseLink d on c.linkbaseInternal_id = d.linkbaseInternal_id
		join ExtendedLink e on d.linkbaseLinkInternal_id = e.linkbaseLinkInternal_id
		group by a.documentSet_id
) y on x.documentSet_id = y.documentSet_id
set x.extendedLink = y.extendedLink;

update tempStats x
join (
		select a.documentSet_id
				, count(c.roleRefInternal_id) as roleRef
		from DocumentSet a
		join DocumentHasRoleRef c
			on a.documentSet_id = c.documentSet_id
		group by a.documentSet_id
) y on x.documentSet_id = y.documentSet_id
set x.roleRef = y.roleRef;

update tempStats x
join (
		select a.documentSet_id
				, count(c.roleTypeInternal_id) as roleType
		from DocumentSet a
		join DocumentHasRoletype c
			on a.documentSet_id = c.documentSet_id
		group by a.documentSet_id
) y on x.documentSet_id = y.documentSet_id
set x.roleType = y.roleType;


/* ----------------------- Step 3. Showing the results  -----------------------------*/
select * from tempStats;



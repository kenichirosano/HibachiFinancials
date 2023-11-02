Data Taxonomy Set (DTS) is divided into 2.

Common file - path [directory + filename] (which is unique) Common files under taxonomy directory.
Special file - name + path (which makes it unique) Xbrl and other files that are downloaded from EDINET.

Common DTS can be updated all at once.
Get and read all the files under taxonomy directory CommonDTSList (unique_id, path)

Get the relationship of all the files under taxonomy directory
The relationships are 'import','include','linkbaseRef'. CommonDTSRelationship (parentfile_id, childfile_id, relationship)

Special files are imported when the process is run.

Linkbases are categorized into 3 layers.
1.Linkbase element 2.LinkbaseLink 3.ExtendedLink

While they are defined as linkbase in XBRL specification, hibachi treats them seperately.
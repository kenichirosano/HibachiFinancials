# HibachiFinancials is a program to read Edinet XBRL and transform the data into PostgreSQL written in Python.

- Data Taxonomy Set (DTS) is divided into 2.
1. Common  file - path [directory + filename] (which is unique)
    Common files under taxonomy directory.
2. Special file -  name + path (which makes it unique)
    Xbrl and other files that are downloaded from EDINET.

- Common DTS can be updated all at once.
1. Get and read all the files under taxonomy directory
    CommonDTSList (unique_id, path)
2. Get the relationship of all the files under taxonomy directory
   The relationships are 'import','include','linkbaseRef'.
    CommonDTSRelationship (parentfile_id, childfile_id, relationship)

    Special files are imported when the process is run.

- Linkbases are categorized into 3 layers.
1.Linkbase
    <Linkbase> element
2.LinkbaseLink
    <labelLink>, <presentationLink>, <calculationLink>, <definitionLink>
3.ExtendedLink
    <loc>

    While <roleRef> and <arcroleRef> are defined as linkbase in XBRL specification, hibachi treats them seperately. 


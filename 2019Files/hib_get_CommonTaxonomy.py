# -*- coding: utf-8 -*-
import os
import sys
import hib_connectMySQL
import hib_Linkbase             as Linkbase
import hib_Concept              as Concept
import hi_Roletype              as Roletype
import hib_RoleType_WrSQL       as RoleType_WrSQL
import hi__EXT_ETtree           as hi_EXT_ET
import hi_TaxonomySchema_Class  as TaxonomySchema
import hi_RoleRef_Class         as RoleRef

# Switch
switch_DTS      = 0 # or 1
switch_Linkbase = 0 # or 1
switch_Role     = 1 # or 1
switch_Concept  = 0

# DTS is consisted of TaxonomySchema, Linkbase, FootnoteLink, Roletype classes.
list_of_DTS      = []
list_of_Concept  = []
list_of_Linkbase = []
list_of_Role     = []

# Connect to MySQL
connection_to_Database  = hib_connectMySQL.connectToMySQL()
cursor_for_SQL          = connection_to_Database.cursor()

# Get all the common DTS files (files under taxonomy directory)
commonDTSFilePath   = []
tableName           = 'commonDTS'
query_to_SELECT     = 'SELECT filePath FROM ' \
                    + tableName \
                    + ';'
cursor_for_SQL.execute(query_to_SELECT)
rowsFromSQL = cursor_for_SQL.fetchall()
for row in rowsFromSQL:
    commonDTSFilePath.append(row[0])

# Get the extention of the file name and process accordingly
for name_of_CurrentFile in commonDTSFilePath:
    extension_of_CurrentFile = os.path.splitext(name_of_CurrentFile)[1] #Get the extention of the file it is reading

    #------------------------------------------- If the file is XSD file (schema file) ---------------------------------------------
    if extension_of_CurrentFile == '.xsd':
        try:
            root_ElementTree = hi_EXT_ET.etree_parse_remove_NS(name_of_CurrentFile)

            if root_ElementTree != None:

                if switch_DTS == 1:
                    XBRL_schema_Tags = ['import','include','linkbaseRef']

                    for empty_Var, temp_tagName in enumerate(XBRL_schema_Tags):

                        for temp_schema_ElementTree in root_ElementTree.iter(temp_tagName):
                            temp_TaxonomySchema_instance = TaxonomySchema.TaxonomySchema(name_of_CurrentFile, temp_schema_ElementTree) # Use TaxonomySchema class
                            list_of_DTS.append([name_of_CurrentFile, temp_TaxonomySchema_instance.searchablePath, temp_tagName])

                if switch_Concept == 1:
                    for temp_concept_ElementTree in root_ElementTree.iter('element'):
                        substitutionGroup = temp_concept_ElementTree.get('substitutionGroup') # Specification 4.6
                        if substitutionGroup: # If the element has substitutionGroup attritube
                            if (('item' in substitutionGroup) or ('tuple' in substitutionGroup)):
                                list_of_Concept.append(Concept.Concept(name_of_CurrentFile, temp_concept_ElementTree))

                if switch_Linkbase == 1:
                    # 5.2.1 <linkbase>
                    for linkbase_ElementTree in root_ElementTree.iter('linkbase'):
                        temp_Linkbase_instance = Linkbase.Linkbase(name_of_CurrentFile, linkbase_ElementTree)
                        list_of_Linkbase.append(temp_Linkbase_instance)

                if switch_Role == 1:
                    # 5.1.3 <roleType>, 5.1.4 <arcroleType>
                    for schema_ElementTree in root_ElementTree.iter('schema'):
                        for annotation_ElementTree in schema_ElementTree.findall('annotation'):
                            for appinfo_ElementTree in annotation_ElementTree.findall('appinfo'):

                                XBRL_roleType_Tags = ['roleType','arcroleType']
                                for empty_Var, temp_tagName in enumerate(XBRL_roleType_Tags):
                                    for temp_roleType_ElementTree in appinfo_ElementTree.findall(temp_tagName): #
                                        temp_Roletype_instance = Roletype.Roletype(name_of_CurrentFile, temp_roleType_ElementTree)
                                        list_of_Role.append(temp_Roletype_instance)

                                XBRL_roleRef_Tags = ['roleRef', 'arcroleRef']
                                for empty_Var, temp_tagName in enumerate(XBRL_roleRef_Tags):
                                    for temp_roleRef_ElementTree in appinfo_ElementTree.findall(temp_tagName): #
                                        temp_RoleRef_instance = RoleRef.RoleRef(name_of_CurrentFile, temp_roleRef_ElementTree)
                                        list_of_Role.append(temp_RoleRef_instance)

        except:
            print ('Error in reading:', name_of_CurrentFile, sys.exc_info()[0], sys.exc_info()[1])
            list_of_ErrorURLs.append(name_of_CurrentFile)

    #------------------------------------------- If the file is XML file (linkbase file) ---------------------------------------------
    elif extension_of_CurrentFile == '.xml':
        try:
            root_ElementTree = hi_EXT_ET.etree_parse_remove_NS(name_of_CurrentFile) #Parse the xbrl ingnoring namespace

            if root_ElementTree != None:

                if root_ElementTree.tag in ('linkbase'):
                    if switch_Linkbase == 1:
                        temp_Linkbase_instance = Linkbase.Linkbase(name_of_CurrentFile, root_ElementTree)
                        list_of_Linkbase.append(temp_Linkbase_instance)

                # Search for the linkbase elements under the linkbase path of //xsd:schema/xsd:annotation/xsd:appinfo/
                elif root_ElementTree.tag in ('schema'):
                    for annotation_ElementTree in root_ElementTree.findall('annotation'):
                        for appinfo_ElementTree in annotation_ElementTree.findall('appinfo'):

                            if switch_Linkbase == 1:
                                for linkbase_ElementTree in appinfo_ElementTree.findall('linkbase'):
                                    temp_Linkbase_instance = Linkbase.Linkbase(name_of_CurrentFile, linkbase_ElementTree)
                                    list_of_Linkbase.append(temp_Linkbase_instance)

                            if switch_Role == 1:
                                # 5.1.3 <roleType>, 5.1.4 <arcroleType>
                                XBRL_roleType_Tags = ['roleType','arcroleType']
                                for empty_Var, temp_tagName in enumerate(XBRL_roleType_Tags):
                                    for taxonomySchemaElement in appinfo_ElementTree.findall(temp_tagName): #Search for <'roleType','arcroleType'> element (specification 4.2)
                                        temp_Roletype_instance = Roletype.Roletype(name_of_CurrentFile, taxonomySchemaElement)
                                        list_of_Role.append(temp_Roletype_instance) # Add to the list

                                XBRL_roleRef_Tags = ['roleRef', 'arcroleRef']
                                for empty_Var, temp_tagName in enumerate(XBRL_roleRef_Tags):
                                    for temp_roleRef_ElementTree in appinfo_ElementTree.findall(temp_tagName): #Search for <'roleType','arcroleType'> element (specification 4.2)
                                        temp_roleRef_instance = RoleRef.RoleRef(name_of_CurrentFile, temp_roleRef_ElementTree)
                                        list_of_Role.append(temp_roleRef_instance) # Add to the list

        except:
            print ('Error in reading:', name_of_CurrentFile, sys.exc_info()[0], sys.exc_info()[1])
            list_of_ErrorURLs.append(name_of_CurrentFile)

    else:
        print ('Not XBRL, XSD or XML:', name_of_CurrentFile)

# Overwrite the DTS info into SQL
if switch_DTS == 1:
    # Insert the common DTS relationships into MySQL
    tableName       = 'CommonDTSRelationShip'
    # Delete all the record in CommonDTSRelationShip first before running query
    cursor_for_SQL.execute('TRUNCATE TABLE ' + tableName)
    connection_to_Database.commit()

    for record in list_of_DTS:
        #print(record)
        query_to_SELECT = 'INSERT INTO ' \
                        + tableName \
                        + ' (parent_file, child_file, relationship) VALUES (%s,%s,%s);'
        cursor_for_SQL.execute(query_to_SELECT, record)
    connection_to_Database.commit()

# Insert the concepts into MySQL
if switch_Concept == 1:
    Concept.writeInSQL(list_of_Concept, connection_to_Database)

# Insert the linkbases into MySQL
if switch_Linkbase == 1:
    Linkbase.writeInSQL(list_of_Linkbase, connection_to_Database)

# Insert the roleType into MySQL
if switch_Role == 1:
    RoleType_WrSQL.writeInSQL(list_of_Role, connection_to_Database)

'''
3.1 Overview of XBRL taxonomies
When a linkbase is not embedded in a taxonomy schema, the taxonomy schema MUST contain a <linkbaseRef> to point to the linkbase document.

3.5 XLink in XBRL
There are attributes that are permitted by the XML Schema syntax constraints but are not documented or given any specific semantics.
Examples include the @xlink:show and the @xlink:actuate attributes.

3.5.2 The <linkbase> element
While the syntax for Concepts is defined in Taxonomy Schemas, the semantics of those concepts are defined in XBRL Linkbases.
Linkbases are Extended Links or they are elements that contain extended links.

4.3 The <linkbaseRef> element in XBRL instances
In an XBRL Instance, the <linkbaseRef> element identifies a Linkbase that becomes part of the DTS supporting that XBRL instance.

4.3.1 The @xlink:type attribute MUST occur and MUST have the fixed content "simple".
4.3.2 The @xlink:href attribute MUST occur
'''

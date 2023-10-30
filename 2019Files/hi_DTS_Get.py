# -*- coding: utf-8 -*-
import os
import sys
import hi_TaxonomySchema_Class as TaxonomySchema
import hi_Linkbase_Class as Linkbase
import hi_RoleRef_Class as RoleRef
import hi_FootnoteLink as FootnoteLink
import hi_Roletype as Roletype
import hi__EXT_ETtree as hi_EXT_ET
import hi__EXT_XLink as hi_EXT_XL
import hi__EXT_SQL as hi_EXT_SQL

def getDTSPath(name_of_CurrentFile, list_of_DTS, connection_to_Database, list_of_ErrorURLs):
    ''' Get all the DTS file pathes and store them in list_of_DTS.
        DTS is consisted of TaxonomySchema, Linkbase, FootnoteLink, Roletype classes.
    '''
    Extension_of_CurrentFile = os.path.splitext(name_of_CurrentFile)[1] #Get the extention of the file it is reading
    tableName_in_SQL    = 'TaxonomySchema'

    #------------------------------------------- If the file is .xbrl file (instance file) ----------------------------------------------
    if Extension_of_CurrentFile == '.xbrl':
        try:
            root_ElementTree = hi_EXT_ET.etree_parse_remove_NS(name_of_CurrentFile)

            if root_ElementTree.tag == 'xbrl':

                for schemaRef_ElementTree in root_ElementTree.iter('schemaRef'): #Search for <schemaRef> element (specification 4.2)
                    temp_TaxonomySchema_instance = TaxonomySchema.TaxonomySchema(name_of_CurrentFile, schemaRef_ElementTree)

                    # To read only unique links, check if the link is unique and doesn't have FID
                    if hi_EXT_XL.isUniquePath(list_of_DTS, temp_TaxonomySchema_instance.searchablePath):
                        #if hi_EXT_SQL.existsInSQL(connection_to_Database, tableName_in_SQL, temp_TaxonomySchema_instance.searchablePath) == None: # If unique and not in SQL
                        list_of_DTS.append(temp_TaxonomySchema_instance) # Add to the DTS list
                        getDTSPath(temp_TaxonomySchema_instance.searchablePath, list_of_DTS, connection_to_Database, list_of_ErrorURLs) # If no FID, parse the linked file

                # 4.3 <linkbaseRef>
                for linkbaseRef_ElementTree in root_ElementTree.iter('linkbaseRef'):
                    temp_TaxonomySchema_instance = TaxonomySchema.TaxonomySchema(name_of_CurrentFile, linkbaseRef_ElementTree)

                    if hi_EXT_XL.isUniquePath(list_of_DTS, temp_TaxonomySchema_instance.searchablePath):
                        #if hi_EXT_SQL.existsInSQL(connection_to_Database, tableName_in_SQL, temp_TaxonomySchema_instance.searchablePath) == None:
                        list_of_DTS.append(temp_TaxonomySchema_instance) #Add to the DTS list
                        getDTSPath(temp_TaxonomySchema_instance.searchablePath, list_of_DTS, connection_to_Database, list_of_ErrorURLs)

                # 4.4 <roleRef>, 4.5 <arcroleRef>
                XBRL_roleRef_Tags = ['roleRef', 'arcroleRef']
                for empty_Var, temp_XBRL_tagName in enumerate(XBRL_roleRef_Tags):
                    for temp_RoleRef_ElementTree in root_ElementTree.iter(temp_XBRL_tagName):
                        temp_RoleRef_instance = RoleRef.RoleRef(name_of_CurrentFile, temp_RoleRef_ElementTree)
                        list_of_DTS.append(temp_RoleRef_instance)

                # 4.11 <footnoteLink>
                for footnoteLink_ElementTree in root_ElementTree.iter('footnoteLink'):
                    temp_FootnoteLink_instance = FootnoteLink.FootnoteLink(name_of_CurrentFile, footnoteLink_ElementTree)
                    list_of_DTS.append(temp_FootnoteLink_instance)

        except:
            print ('Errro in reading:', name_of_CurrentFile, sys.exc_info()[0], sys.exc_info()[1])
            list_of_ErrorURLs.append(name_of_CurrentFile)

    #------------------------------------------- If the file is XSD file (schema file) ---------------------------------------------
    elif Extension_of_CurrentFile == '.xsd':
        try:
            root_ElementTree = hi_EXT_ET.etree_parse_remove_NS(name_of_CurrentFile)

            if root_ElementTree != None:
                XBRL_schema_Tags = ['import','include','linkbaseRef']

                for empty_Var, temp_XBRL_tagName in enumerate(XBRL_schema_Tags):

                    for temp_schema_ElementTree in root_ElementTree.iter(temp_XBRL_tagName):
                        temp_TaxonomySchema_instance = TaxonomySchema.TaxonomySchema(name_of_CurrentFile, temp_schema_ElementTree)

                        if hi_EXT_XL.isUniquePath(list_of_DTS, temp_TaxonomySchema_instance.searchablePath):
                            #if hi_EXT_SQL.existsInSQL(connection_to_Database, tableName_in_SQL, temp_TaxonomySchema_instance.searchablePath) == None:
                            list_of_DTS.append(temp_TaxonomySchema_instance)
                            getDTSPath(temp_TaxonomySchema_instance.searchablePath, list_of_DTS, connection_to_Database, list_of_ErrorURLs)

                # 5.2.1 <linkbase>
                for linkbase_ElementTree in root_ElementTree.iter('linkbase'):
                    temp_Linkbase_instance = Linkbase.Linkbase(name_of_CurrentFile, linkbase_ElementTree)
                    list_of_DTS.append(temp_Linkbase_instance)

                # 5.1.3 <roleType>, 5.1.4 <arcroleType>
                for schema_ElementTree in root_ElementTree.iter('schema'):
                    for annotation_ElementTree in schema_ElementTree.findall('annotation'):
                        for appinfo_ElementTree in annotation_ElementTree.findall('appinfo'):

                            XBRL_roleType_Tags = ['roleType','arcroleType']
                            for empty_Var, temp_XBRL_tagName in enumerate(XBRL_roleType_Tags):
                                for temp_roleType_ElementTree in appinfo_ElementTree.findall(temp_XBRL_tagName): #
                                    temp_Roletype_instance = Roletype.Roletype(name_of_CurrentFile, temp_roleType_ElementTree)
                                    list_of_DTS.append(temp_Roletype_instance)

                            XBRL_roleRef_Tags = ['roleRef', 'arcroleRef']
                            for empty_Var, temp_XBRL_tagName in enumerate(XBRL_roleRef_Tags):
                                for temp_roleRef_ElementTree in appinfo_ElementTree.findall(temp_XBRL_tagName): #
                                    temp_RoleRef_instance = RoleRef.RoleRef(name_of_CurrentFile, temp_roleRef_ElementTree)
                                    list_of_DTS.append(temp_RoleRef_instance)

        except:
            print ('Error in reading:', name_of_CurrentFile, sys.exc_info()[0], sys.exc_info()[1])
            list_of_ErrorURLs.append(name_of_CurrentFile)
    #------------------------------------------- If the file is XML file (linkbase file) ---------------------------------------------
    elif Extension_of_CurrentFile == '.xml':
        try:
            root_ElementTree = hi_EXT_ET.etree_parse_remove_NS(name_of_CurrentFile) #Parse the xbrl ingnoring namespace

            if root_ElementTree != None:

                if root_ElementTree.tag in ('linkbase'):
                    temp_Linkbase_instance = Linkbase.Linkbase(name_of_CurrentFile, root_ElementTree)
                    list_of_DTS.append(temp_Linkbase_instance)

                # Search for the linkbase elements under the linkbase path of //xsd:schema/xsd:annotation/xsd:appinfo/
                elif root_ElementTree.tag in ('schema'):
                    for annotation_ElementTree in root_ElementTree.findall('annotation'):
                        for appinfo_ElementTree in annotation_ElementTree.findall('appinfo'):

                            for linkbase_ElementTree in appinfo_ElementTree.findall('linkbase'):
                                temp_Linkbase_instance = Linkbase.Linkbase(name_of_CurrentFile, linkbase_ElementTree)
                                list_of_DTS.append(temp_Linkbase_instance)

                            # 5.1.3 <roleType>, 5.1.4 <arcroleType>
                            XBRL_roleType_Tags = ['roleType','arcroleType']
                            for empty_Var, temp_XBRL_tagName in enumerate(XBRL_roleType_Tags):
                                for taxonomySchemaElement in appinfo_ElementTree.findall(temp_XBRL_tagName): #Search for <schemaRef> element (specification 4.2)
                                    temp_Roletype_instance = Roletype.Roletype(name_of_CurrentFile, taxonomySchemaElement)
                                    list_of_DTS.append(temp_Roletype_instance) # Add to the list

                            XBRL_roleRef_Tags = ['roleRef', 'arcroleRef']
                            for empty_Var, temp_XBRL_tagName in enumerate(XBRL_roleRef_Tags):
                                for temp_roleRef_ElementTree in appinfo_ElementTree.findall(temp_XBRL_tagName): #Search for <schemaRef> element (specification 4.2)
                                    temp_roleRef_instance = RoleRef.RoleRef(name_of_CurrentFile, temp_roleRef_ElementTree)
                                    list_of_DTS.append(temp_roleRef_instance) # Add to the list

        except:
            print ('Error in reading:', name_of_CurrentFile, sys.exc_info()[0], sys.exc_info()[1])
            list_of_ErrorURLs.append(name_of_CurrentFile)

    else:
        print ('Not XBRL, XSD or XML:', name_of_CurrentFile)


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

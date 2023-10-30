# -*- coding: utf-8 -*-
import sys
import hi__EXT_XLink_Ext    as EXT_XL_Ext
import hi_XmlElement_Class as hi_XmlElement

class Linkbase(hi_XmlElement.XmlElement):
    #Class of each linkbase (<linkbase>, <roleRef>, <roleType> or <arcroleType>)
    def __init__(self, fileName, element):
        super(Linkbase, self).__init__(fileName, element)
        self.childElementList = assign_linkbaseElementDictList(fileName, element)

def assign_linkbaseElementDictList(fileName, linkbase_ElementTree):
    '''Get child elements and create a list containing the elements.'''

    # Switch
    switch_LabelLink        = 0 # or 1
    switch_ReferenceLink    = 0 # or 1
    switch_PresentationLink = 1 # or 1
    switch_CalculationLink  = 1 # or 1
    switch_DefinitionLink   = 0 # or 1

    list_of_LinkbaseElementDict = []
    if linkbase_ElementTree.tag == 'linkbase':
        linkbaseLinkElementDict = {
            'tag'       :None
            ,'type'     :None # 3.5.3.2 MUST have "extended"
            ,'id'       :None
            ,'role'     :None
            ,'base'     :None
            ,'childList':None
        }
        extendedLinkElementDict = {
            'tag'            :None
            ,'type'          :None # "locator", "resource"
            ,'role'          :None
            ,'arcrole'       :None
            ,'label'         :None
            ,'lang'          :None
            ,'from'          :None
            ,'to'            :None
            ,'preferredLabel':None
            ,'weight'        :None
            ,'order'         :None
            ,'originalPath'  :None # This is @href
            ,'searchablePath':None # This is modified @href
            ,'content'       :None
            ,'use'           :None
            ,'priority'      :None
            ,'fragment_ID'   :None
        }
        list_of_ChildElementDicts = []

        # 5.2.2 <labelLink>
        if  switch_LabelLink        == 1:
            for labelLink_ElementTree in linkbase_ElementTree.findall('labelLink'):
                labelLink_ElementDict = linkbaseLinkElementDict.copy()
                labelLink_ElementDict = EXT_XL_Ext.returnElementAsDict(labelLink_ElementTree, labelLink_ElementDict)
                list_of_ChildElementDicts = EXT_XL_Ext.returnChildElementListOfDict(fileName, labelLink_ElementTree, ['loc','label','labelArc'], extendedLinkElementDict)
                labelLink_ElementDict['childList'] = list_of_ChildElementDicts
                list_of_LinkbaseElementDict.append(labelLink_ElementDict)

        # 5.2.3 <referenceLink>
        if  switch_ReferenceLink    == 1 :
            for referenceLink_ElementTree in linkbase_ElementTree.findall('referenceLink'):
                referenceLinkElementDict = linkbaseLinkElementDict.copy()
                referenceLinkElementDict = EXT_XL_Ext.returnElementAsDict(referenceLink_ElementTree, referenceLinkElementDict)
                list_of_ChildElementDicts = EXT_XL_Ext.returnChildElementListOfDict(fileName, referenceLink_ElementTree, ['loc', 'reference', 'referenceArc'], extendedLinkElementDict)
                referenceLinkElementDict['childList'] = list_of_ChildElementDicts
                list_of_LinkbaseElementDict.append(referenceLinkElementDict)

        # 5.2.4 <presentationLink>
        if  switch_PresentationLink == 1:
            for presentationLink_ElementTree in linkbase_ElementTree.findall('presentationLink'):
                presentationLinkElementDict = linkbaseLinkElementDict.copy()
                presentationLinkElementDict = EXT_XL_Ext.returnElementAsDict(presentationLink_ElementTree, presentationLinkElementDict)
                list_of_ChildElementDicts = EXT_XL_Ext.returnChildElementListOfDict(fileName, presentationLink_ElementTree, ['loc', 'presentationArc'], extendedLinkElementDict)
                presentationLinkElementDict['childList'] = list_of_ChildElementDicts
                list_of_LinkbaseElementDict.append(presentationLinkElementDict)

        # 5.2.5 <calculationLink>
        if  switch_CalculationLink  == 1:
            for calculationLink_ElementTree in linkbase_ElementTree.findall('calculationLink'):
                calculationLinkElementDict = linkbaseLinkElementDict.copy()
                calculationLinkElementDict = EXT_XL_Ext.returnElementAsDict(calculationLink_ElementTree, calculationLinkElementDict)
                list_of_ChildElementDicts = EXT_XL_Ext.returnChildElementListOfDict(fileName, calculationLink_ElementTree, ['loc', 'calculationArc'], extendedLinkElementDict)
                calculationLinkElementDict['childList'] = list_of_ChildElementDicts
                list_of_LinkbaseElementDict.append(calculationLinkElementDict)

        # 5.2.6 <definitionLink>
        if  switch_DefinitionLink   == 1:
            for definitionLink_ElementTree in linkbase_ElementTree.findall('definitionLink'):
                definitionLinkElementDict = linkbaseLinkElementDict.copy()
                definitionLinkElementDict = EXT_XL_Ext.returnElementAsDict(definitionLink_ElementTree, definitionLinkElementDict)
                list_of_ChildElementDicts = EXT_XL_Ext.returnChildElementListOfDict(fileName, definitionLink_ElementTree, ['loc', 'definitionArc'], extendedLinkElementDict)
                definitionLinkElementDict['childList'] = list_of_ChildElementDicts
                list_of_LinkbaseElementDict.append(definitionLinkElementDict)

    return list_of_LinkbaseElementDict

'''
5.2 Taxonomy linkbases
Extended Links MUST be held in an [XLINK] document container, which MUST be a <linkbase> element located either:
1. among the set of nodes identified by the XPath [XPath 1.0] path "//xsd:schema/xsd:annotation/xsd:appinfo/*" in the Taxonomy Schema; or
2. at the root element of a separate document.
'''

def writeInSQL(listOfLinkbases, connection_to_Database):
    cursor_for_SQL = connection_to_Database.cursor()
    #cursor_for_SQL.execute('TRUNCATE TABLE ' + 'LabelExtendedLink')
    #cursor_for_SQL.execute('TRUNCATE TABLE ' + 'PresentationExtendedLink')
    #cursor_for_SQL.execute('TRUNCATE TABLE ' + 'CalculationExtendedLink')
    connection_to_Database.commit()

    for linkbase in listOfLinkbases:

        if linkbase.__class__.__name__ == 'Linkbase':

            for linkbaseLinkElementDict in linkbase.childElementList:

                tableName = ''
                if linkbaseLinkElementDict['tag'] == 'labelLink':
                    tableName = 'raw_LabelExtendedLink'
                    print('Inserting label Linkbases.')
                elif linkbaseLinkElementDict['tag'] == 'presentationLink':
                    tableName = 'raw_PresentationExtendedLink'
                    print('Inserting presentation Linkbases.')
                elif linkbaseLinkElementDict['tag'] == 'calculationLink':
                    tableName = 'raw_CalculationExtendedLink'
                    print('Inserting calculation Linkbases.')
                else:
                    break

                for extendtedLinkDict in linkbaseLinkElementDict['childList']:
                    values_for_CommonExtendedLink = []
                    try:
                        print('This is at each linkbase.')
                        sql = 'INSERT INTO ' + tableName \
                            + ' ('\
                            + 'filePath, '\
                            + 'linkbaseLink_tag, '\
                            + 'linkbaseLink_role, '\
                            + 'Extended_tag, '\
                            + 'Extended_role, ' \
                            + 'Extended_arcrole,'\
                            + 'Extended_label, '\
                            + 'Extended_lang, '\
                            + 'Extended_fromAttr, '\
                            + 'Extended_toAttr, '\
                            + 'Extended_preferredLabel, '\
                            + 'Extended_weight, '\
                            + 'Extended_orderAttr, '\
                            + 'Extended_originalPath, '\
                            + 'Extended_searchablePath, '\
                            + 'Extended_fragment_ID, '\
                            + 'Extended_content, '\
                            + 'Extended_useAttr, '\
                            + 'Extended_priority) '\
                            + 'VALUES (%s,%s,%s,%s,'\
                            + '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'  #22
                        values = [
                            linkbase.currentPath                        # filePath
                            ,linkbaseLinkElementDict['tag']             # linkbase_tag
                            ,linkbaseLinkElementDict['role']            #
                            ,extendtedLinkDict['tag']                   # Extended_tag
                            ,extendtedLinkDict['role']                  # "resource" role only
                            ,extendtedLinkDict['arcrole']               # "arc"      role only
                            ,extendtedLinkDict['label']                 #
                            ,extendtedLinkDict['lang']                  #
                            ,extendtedLinkDict['from']                  #
                            ,extendtedLinkDict['to']                    #
                            ,extendtedLinkDict['preferredLabel']        #
                            ,extendtedLinkDict['weight']                # Extended_weight
                            ,extendtedLinkDict['order']                 # Extended_orderAttr
                            ,extendtedLinkDict['originalPath']          #
                            ,extendtedLinkDict['searchablePath']        #
                            ,extendtedLinkDict['fragment_ID']           #
                            ,extendtedLinkDict['content']               #
                            ,extendtedLinkDict['use']                   #
                            ,extendtedLinkDict['priority']              #
                        ]
                        cursor_for_SQL.execute(sql, values)
                        # Update the document_id (of filepath) column

                    except:
                        connection_to_Database.rollback()
                        print(sys.exc_info(), 'Error occurred in writing CommonExtendedLink', linkbase.currentPath)

                    connection_to_Database.commit()

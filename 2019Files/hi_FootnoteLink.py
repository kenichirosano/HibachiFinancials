# -*- coding: utf-8 -*-
import hi__EXT_XLink_Ext as EXT_XL_Ext
import hi_XmlElement_Class as hi_XmlElement
import sys

class FootnoteLink(hi_XmlElement.XmlElement):
    #Class of <footnoteLink> element
    def __init__(self, fileName, element):
        super(FootnoteLink, self).__init__(fileName, element)
        self.childElementList = assign_footnoteLinkElementDictList(fileName, element)

def assign_footnoteLinkElementDictList(fileName, footnoteLinkElement):
    '''
    Get child elements of <footnoteLink> element and create a list containing them.
    <footnoteLink> element has <loc>, <footnote> and <footnoteArc> element
    '''
    footnoteExtendedLinkElementDict = {
        'footnoteID'        :None
        ,'footnoteLinkRole' :None
        ,'footnoteRole'     :None
        ,'tag'              :None
        ,'type'             :None
        ,'role'             :None
        ,'arcrole'          :None
        ,'label'            :None
        ,'lang'             :None
        ,'from'             :None
        ,'to'               :None
        ,'originalPath'     :None
        ,'searchablePath'   :None
        ,'fragment_ID'      :None
        ,'content'          :None
    }
    listOfChildElements = EXT_XL_Ext.returnChildElementListOfDict(fileName, footnoteLinkElement, 'loc', footnoteExtendedLinkElementDict)
    listOfChildElements.extend(EXT_XL_Ext.returnChildElementListOfDict(fileName, footnoteLinkElement, 'footnoteArc', footnoteExtendedLinkElementDict))
    listOfChildElements.extend(EXT_XL_Ext.returnChildElementListOfDict(fileName, footnoteLinkElement, 'footnote', footnoteExtendedLinkElementDict))
    return listOfChildElements

def writeInMySQL(documentSetID, listOfDTS, connection_to_Database):
    '''Method to write <footnoteLink> element in SQL'''

    for footnoteLink in listOfDTS:

        if footnoteLink.__class__.__name__ == 'FootnoteLink':
            try:
                cursor_for_SQL = connection_to_Database.cursor()
                tableName = 'footnoteLink'
                sql = 'INSERT INTO ' \
                    + tableName \
                    + ' (documentSet_id, tag, type, role) VALUES (%s,%s,%s,%s);'
                values = [
                    documentSetID
                    ,footnoteLink.tag
                    ,footnoteLink.type
                    ,footnoteLink.role
                ]
                cursor_for_SQL.execute(sql, values)

                cursor_for_SQL.execute("SELECT LAST_INSERT_ID();")
                footnoteLinkInternal_idNum = cursor_for_SQL.fetchall()

                for extendtedLinkDict in footnoteLink.childElementList:
                    tableName = 'footnoteExtendedLink'
                    sql = 'INSERT INTO ' + tableName \
                        + ' (footnoteLinkInternal_id, footnoteID, footnoteLinkRole, footnoteRole, tag, type, role, arcrole, label, lang,' \
                        + ' fromAttr, toAttr, originalPath, searchablePath, fragment_ID, content)' \
                        + ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
                    values = [
                        footnoteLinkInternal_idNum
                        ,extendtedLinkDict['footnoteID']
                        ,extendtedLinkDict['footnoteLinkRole']
                        ,extendtedLinkDict['footnoteRole']
                        ,extendtedLinkDict['tag']
                        ,extendtedLinkDict['type']
                        ,extendtedLinkDict['role']
                        ,extendtedLinkDict['arcrole']
                        ,extendtedLinkDict['label']
                        ,extendtedLinkDict['lang']
                        ,extendtedLinkDict['from']
                        ,extendtedLinkDict['to']
                        ,extendtedLinkDict['originalPath']
                        ,extendtedLinkDict['searchablePath']
                        ,extendtedLinkDict['fragment_ID']
                        ,extendtedLinkDict['content']
                    ]
                    cursor_for_SQL.execute(sql, values)

                connection_to_Database.commit()

            except:
                connection_to_Database.rollback()
                print (sys.exc_info(), 'footnoteLink')

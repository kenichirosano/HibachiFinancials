# -*- coding: utf-8 -*-
import sys
import xml.dom
import xml.dom.minidom
import hi__EXT_ETtree       as hi_EXT_ET
import hi_XmlElement_Class  as hi_XmlElement
import pymysql

class Instance(hi_XmlElement.XmlElement):
    '''Class of each instance defined in DTS (taxonomy schema files)'''

    def __init__(self, fileName, instanceElement):
        super(Instance, self).__init__(fileName, instanceElement)
        self.tag        = hi_EXT_ET.removeNSfromText(instanceElement.tag)
        self.value      = instanceElement.text
        self.contextRef = instanceElement.get('contextRef')
        self.unitRef    = instanceElement.get('unitRef')
        self.precision  = instanceElement.get('precision')
        self.decimals   = instanceElement.get('decimals')

def getDocumentSet(root_ElementTree, fileName):
    # Return a dictionay containing edinet code and filing date.

    list_of_EdinetCode = []
    dict_of_DocumentSet = {
        'edinetCode'    :None
        ,'filingDate'   :None
        ,'documentType' :'Yuho'
        ,'repFileName'  :fileName
    }

    # Get edinet code only if the file has only 1 edinet code
    # Edinet code is stored in <identifier> element in the form of [Edinet code]-[追番]
    for identifier_ElementTree in root_ElementTree.iter('identifier'):
        list_of_EdinetCode.append(identifier_ElementTree.text.split("-")[0])

    if len(set(list_of_EdinetCode)) == 1:
        dict_of_DocumentSet['edinetCode'] = list_of_EdinetCode[0]

    else:
        print ('Error: Multiple Edinet Codes.')
        return None

    # Get filingDate
    for context_ElementTree in root_ElementTree.findall('context'):

        if context_ElementTree.get('id') == 'FilingDateInstant':

            for period_ElementTree in context_ElementTree.findall('period'):

                for instant_ElementTree in period_ElementTree.findall('instant'):
                    dict_of_DocumentSet['filingDate'] = instant_ElementTree.text

    return dict_of_DocumentSet

def writeDocumentSetToSQL(dictOfDocumentSet, db):
    # Try to write the basic file info about the file in SQL.
    # If the file is already in the database, return null to stop the parsing process.

    cursor_for_SQL  = db.cursor()
    try:
        # Get and return document id automatically generated by SQL
        tableName_in_SQL    = 'InstanceFiles'
        temp_Query_holder   = 'SELECT documentSet_id FROM ' + tableName_in_SQL + ' '\
                            + 'WHERE edinetCode = %s '\
                            + 'AND filingDate = %s AND repFileName = %s;'
        values_for_Where    = [
            dictOfDocumentSet['edinetCode']
            ,dictOfDocumentSet['filingDate']
            ,dictOfDocumentSet['repFileName']
        ]
        cursor_for_SQL.execute(temp_Query_holder, values_for_Where)
        DocumentSet_id_in_SQL       = cursor_for_SQL.fetchall()

        # If the document has documentID DocumentSet, return Null and the error code
        if DocumentSet_id_in_SQL:
            return(None, 0)

        # Else if the document is not registered in DocumentSet, insert in DocumentSet and return the newly created id
        else:
            temp_Query_holder   = 'INSERT INTO ' + tableName_in_SQL \
                                + ' (edinetCode, filingDate, documentType, repFileName) VALUES (%s,%s,%s,%s);'
            values_to_Insert = [
                dictOfDocumentSet['edinetCode']
                ,dictOfDocumentSet['filingDate']
                ,dictOfDocumentSet['documentType']
                ,dictOfDocumentSet['repFileName']
            ]
            cursor_for_SQL.execute(temp_Query_holder, values_to_Insert)

            # Get and return document id automatically generated by SQL
            temp_Query_holder   = 'SELECT documentSet_id FROM ' + tableName_in_SQL \
                                + ' WHERE edinetCode = %s AND filingDate = %s AND repFileName = %s;'
            values_for_Where = [
                dictOfDocumentSet['edinetCode']
                ,dictOfDocumentSet['filingDate']
                ,dictOfDocumentSet['repFileName']
            ]
            cursor_for_SQL.execute(temp_Query_holder, values_for_Where)
            DocumentSet_id_in_SQL = cursor_for_SQL.fetchall()

            db.commit()
            return(True, DocumentSet_id_in_SQL)

    # if error ocurred, dont read the document
    except:
        db.rollback()
        print(sys.exc_info()[0])
        print ('Error in reading:', dictOfDocumentSet['repFileName'], sys.exc_info()[0], sys.exc_info()[1])
        return(None, 1)

def getInstance(instanceFileName, listOfInstances):
    # Method of getting all the instances.
    listOfInstanceElements = []

    # Return namespace URI. To parth with namespace of 'xmlns:jppfs_cor' to get JFSA instances.
    xml_dom = xml.dom.minidom.parse(instanceFileName) # parse by DOM
    # Get financial statements' namespace URI
    list_financials_NameSpace_URI = []
    list_financials_NameSpace_URI.append(xml_dom.getElementsByTagNameNS('*','xbrl')[0].getAttribute('xmlns:jppfs_cor')) #財務諸表本表タクソノミの語彙スキーマ
    list_financials_NameSpace_URI.append(xml_dom.getElementsByTagNameNS('*','xbrl')[0].getAttribute('xmlns:jpigp_cor')) #国際会計基準タクソノミの語彙スキーマ
    # Parse the xbrl
    root = hi_EXT_ET.etree_parse_with_NS(instanceFileName)

    # Get the list of instance elements that have the specified name space in the tag
    listOfInstanceElements = []
    for nameSpace_URI in list_financials_NameSpace_URI:
        listOfInstanceElements.append(hi_EXT_ET.returnListOfInstanceElements_with_SpecifiedNameSpace(instanceFileName, nameSpace_URI))

    # Put the Instance class objects one by one to the list
    for instanceElement in listOfInstanceElements:
        listOfInstances.append(Instance(instanceFileName, instanceElement))

def writeInSQL(documentSetID, listOfInstance, connection_to_Database):

    cursor_for_SQL = connection_to_Database.cursor()
    tableName = 'Instance'
    sql = 'DELETE FROM '\
        + tableName\
        + ' WHERE documentSet_id=%s;'
    cursor_for_SQL.execute(sql, documentSetID)

    for instance in listOfInstance:
        try:
            query_to_Insert = 'INSERT INTO ' \
                            + tableName \
                            + ' (' \
                            + 'documentSet_id,' \
                            + 'tag,' \
                            + 'value,' \
                            + 'contextRef,' \
                            + 'unitRef,' \
                            + 'precisionAttr,' \
                            + 'decimals) ' \
                            + 'VALUES (%s,%s,%s,%s,%s,%s,%s);'
            values_to_Insert = [
                documentSetID
                ,instance.tag
                ,instance.value
                ,instance.contextRef
                ,instance.unitRef
                ,instance.precision
                ,instance.decimals
            ]
            cursor_for_SQL.execute(query_to_Insert, values_to_Insert)
            connection_to_Database.commit()

        except:
            connection_to_Database.rollback()
            print (sys.exc_info(), 'Instance Value:', instance.value)

'''
XBRL instances are XML fragments with root element, <xbrl>

1.4 Terminology (non-normative except where otherwise noted)
An item contains the value of the simple fact and a reference to the context (and unit for numeric items) needed to correctly interpret that fact.
When items occur as children of a tuple, they must also be interpreted in light of the other items and tuples that are children of the same tuple.
There are numeric items and non-numeric items, with numeric items being required to document their measurement accuracy and units of measurement.

4.6.4 The @precision attribute (optional)
The @precision attribute MUST be a non-negative integer or the string "INF" that conveys the arithmetic precision of a measurementsself.

'''

# -*- coding: utf-8 -*-
import hi_XmlElement_Class as hi_XmlElement
import sys

class Roletype(hi_XmlElement.XmlElement):
    #Class of <footnoteLink> element
    def __init__(self, fileName, element):
        super(Roletype, self).__init__(fileName, element)
        self.roleURI = element.get('roleURI') # 5.1.3 <roleType>, <roleRef>
        self.arcroleURI = element.get('arcroleURI') # 5.1.4 <arcroleType>
        self.cyclesAllowed = element.get('cyclesAllowed') # for <arcroleURI>
        self.childElementDict = assign_roleTypeElementDict(fileName, element)

def assign_roleTypeElementDict(fileName, element):
    '''
    Get child elements of <roleType> or <arcroleType> element and create a list containing them.
    <roleType> element has <definition>, <usedOn> element
    '''
    roleTypeChildElementDict = { 'definition':None, 'usedOn':None }
    for key in roleTypeChildElementDict.keys():
        for element in element.findall(key):
            roleTypeChildElementDict[key] = element.text
    return roleTypeChildElementDict

def writeInMySQL(documentSetID, listOfDTS, connection_to_Database):

    for roleType in listOfDTS:
        if roleType.__class__.__name__ == 'Roletype':
            try:
                cursor_for_SQL = connection_to_Database.cursor()
                tableName = 'Roletype'
                if roleType.tag == 'roleType':
                    tempQueryText   = 'SELECT roleTypeInternal_id FROM ' + tableName \
                                        + ' WHERE tag = %s and roleURI = %s and currentPath = %s;'
                    valuesForTempQueryText    = [
                        roleType.tag
                        ,roleType.roleURI
                        ,roleType.currentPath
                    ]
                elif roleType.tag == 'arcroleType':
                    tempQueryText   = 'SELECT roleTypeInternal_id FROM ' + tableName \
                                        + ' WHERE tag = %s and arcroleURI = %s and currentPath = %s;'
                    valuesForTempQueryText    = [
                        roleType.tag
                        ,roleType.arcroleURI
                        ,roleType.currentPath
                    ]
                cursor_for_SQL.execute(tempQueryText, valuesForTempQueryText)
                existsInSQL = cursor_for_SQL.fetchall()
                connection_to_Database.commit()

                if not existsInSQL:
                    try:
                        # Save <roleType> or <arcroleType> to SQL
                        cursor_for_SQL = connection_to_Database.cursor()
                        sql = 'INSERT INTO ' + tableName + ' (tag, id, roleURI, arcroleURI, cyclesAllowed, currentPath) VALUES (%s,%s,%s,%s,%s,%s);'
                        values = [roleType.tag, roleType.id, roleType.roleURI, roleType.arcroleURI, roleType.cyclesAllowed, roleType.currentPath]
                        cursor_for_SQL.execute(sql, values)
                        if roleType.tag == 'roleType':
                            tempQueryText   = 'SELECT roleTypeInternal_id FROM ' + tableName \
                                                + ' WHERE tag = %s and roleURI = %s and currentPath = %s;'
                            valuesForTempQueryText    = [
                                roleType.tag
                                ,roleType.roleURI
                                ,roleType.currentPath
                            ]
                        elif roleType.tag == 'arcroleType':
                            tempQueryText   = 'SELECT roleTypeInternal_id FROM ' + tableName \
                                                + ' WHERE tag = %s and arcroleURI = %s and currentPath = %s;'
                            valuesForTempQueryText    = [
                                roleType.tag
                                ,roleType.arcroleURI
                                ,roleType.currentPath
                            ]
                        cursor_for_SQL.execute(tempQueryText, valuesForTempQueryText)
                        roleTypeInternal_idNum = cursor_for_SQL.fetchall()
                        if roleTypeInternal_idNum:
                            # Save child elements of <roleType> <arcroleType>, (<definition>, <unsedOn>)
                            tableName = 'RoletypeChild'
                            for key in roleType.childElementDict.keys():
                                sql = 'INSERT INTO ' + tableName + ' (roleTypeInternal_id, tag, content)' + ' VALUES (%s,%s,%s);'
                                values = [roleTypeInternal_idNum, key, roleType.childElementDict[key]]
                                cursor_for_SQL.execute(sql, values)

                        connection_to_Database.commit()

                    except:
                        connection_to_Database.rollback()
                        print (sys.exc_info(), 'Roletype')

            except:
                connection_to_Database.rollback()
                print (sys.exc_info(), 'Error Occurred in select statement for RoleType table.')

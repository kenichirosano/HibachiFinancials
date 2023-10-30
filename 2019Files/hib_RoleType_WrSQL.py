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

def writeInSQL(list_of_RoleType, connection_to_Database):

    # Truncate the table before inserting
    tableName       = 'raw_CommonRoleType'
    cursor_for_SQL = connection_to_Database.cursor()
    cursor_for_SQL.execute('TRUNCATE TABLE ' + tableName)
    connection_to_Database.commit()

    for roleType in list_of_RoleType:
        if roleType.__class__.__name__ == 'Roletype':
            try:
                sql = 'INSERT INTO ' + tableName \
                    + ' ('\
                    + 'filePath, '\
                    + 'roleType_tag, '\
                    + 'roleType_id, '\
                    + 'roleType_roleURI, '\
                    + 'roleType_arcroleURI, '\
                    + 'roleType_cyclesAllowed, '\
                    + 'roleTypeChild_tag, '\
                    + 'roleTypeChild_content '\
                    + ') '\
                    + 'VALUES (%s,%s,%s,%s,%s,%s,%s,%s);'
                for key in roleType.childElementDict.keys():
                    valuesForTempQueryText = [
                        roleType.currentPath,
                        roleType.tag,
                        roleType.id,
                        roleType.roleURI,
                        roleType.arcroleURI,
                        roleType.cyclesAllowed,
                        key,
                        roleType.childElementDict[key]
                    ]
                    cursor_for_SQL.execute(sql, valuesForTempQueryText)
                    connection_to_Database.commit()

            except:
                connection_to_Database.rollback()
                print (sys.exc_info(), 'Error Occurred in select statement for CommonRoleType table.')

'''
The <roleType> element describes the custom role type by defining the @roleURI of the role type,
declaring the elements that the role type may be used on,
and providing a human-readable definition of the role type.

Note on April 3, 2019
Checked the common <roleType> - <usedOn> elements all and none had content in itself.
You can ignore <usedOn> for a while.
'''

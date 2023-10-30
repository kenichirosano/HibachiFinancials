# -*- coding: utf-8 -*-
import sys

def writeInMySQL(documentSetID, listOfDTS, connection_to_Database):

    for roleRef in listOfDTS:

        if roleRef.__class__.__name__ == 'RoleRef':
            try:
                cursor_for_SQL = connection_to_Database.cursor()
                tableName = 'RoleRef'
                sql = 'INSERT INTO ' + tableName \
                    + ' (tag, type, originalPath, searchablePath, currentPath, roleURI, arcroleURI, fragment_ID) ' \
                    + 'VALUES (%s,%s,%s,%s,%s,%s,%s,%s);'
                values = [
                    roleRef.tag
                    ,roleRef.type
                    ,roleRef.originalPath
                    ,roleRef.searchablePath
                    ,roleRef.currentPath
                    ,roleRef.roleURI
                    ,roleRef.arcroleURI
                    ,roleRef.fragment_ID
                ]
                cursor_for_SQL.execute(sql, values)
                connection_to_Database.commit()

            except:
                connection_to_Database.rollback()
                print (sys.exc_info(), 'roleRef', roleRef.currentPath)

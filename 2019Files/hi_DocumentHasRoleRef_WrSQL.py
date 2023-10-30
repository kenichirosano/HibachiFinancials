# -*- coding: utf-8 -*-
import sys

def writeInMySQL(documentSetID, listOfDTS, connection_to_Database):

    for roleRef in listOfDTS:
        if roleRef.__class__.__name__ == 'RoleRef':
            try: # Tie roleRef to document by searching unique roleRef by tag, roleURI and currentPath
                cursor_for_SQL = connection_to_Database.cursor()
                tableName_in_SQL    = 'RoleRef'
                if roleRef.tag == 'roleRef':
                    temp_Query_holder   = 'SELECT roleRefInternal_id FROM ' + tableName_in_SQL \
                                        + ' WHERE tag = %s and roleURI = %s and currentPath = %s;'
                    values_for_Where    = [
                        roleRef.tag
                        ,roleRef.roleURI
                        ,roleRef.currentPath
                    ]
                elif roleRef.tag == 'arcroleRef':
                    temp_Query_holder   = 'SELECT roleRefInternal_id FROM ' + tableName_in_SQL \
                                        + ' WHERE tag = %s and arcroleURI = %s and currentPath = %s;'
                    values_for_Where    = [
                        roleRef.tag
                        ,roleRef.arcroleURI
                        ,roleRef.currentPath
                    ]
                cursor_for_SQL.execute(temp_Query_holder, values_for_Where)
                roleRefInternal_idNum = cursor_for_SQL.fetchone()

                if roleRefInternal_idNum:
                    tableName_in_SQL = 'DocumentHasRoleRef'
                    query_to_Insert = 'INSERT INTO ' + tableName_in_SQL + ' (documentSet_id, roleRefInternal_id) VALUES (%s,%s);'
                    values_to_Insert = [
                        documentSetID
                        ,roleRefInternal_idNum
                    ]
                    cursor_for_SQL.execute(query_to_Insert, values_to_Insert)
                    connection_to_Database.commit()
                else:
                    print ('roleRefInternal_idNum is Null for ', roleRef.tag, roleRef.roleURI, roleRef.arcroleURI, roleRef.currentPath)

            except:
                connection_to_Database.rollback()
                print (sys.exc_info(), 'Erro Occurred in DocumentHasRoleRef', roleRef.currentPath)

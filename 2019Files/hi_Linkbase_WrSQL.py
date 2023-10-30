# -*- coding: utf-8 -*-
import sys

def writeInMySQL(documentSetID, listOfDTS, connection_to_Database):
    '''Get the <linkbase> from DTS in python and save to SQL database.'''
    for linkbase in listOfDTS:
        if linkbase.__class__.__name__ == 'Linkbase':
            try:
                cursor_for_SQL = connection_to_Database.cursor()
                tableName    = 'Linkbase'
                tempQueryText   = 'SELECT linkbaseInternal_id FROM ' + tableName \
                                    + ' WHERE tag = %s and currentPath = %s;'
                valuesForTempQueryText    = [ linkbase.tag, linkbase.currentPath]
                cursor_for_SQL.execute(tempQueryText, valuesForTempQueryText)
                existsInSQL = cursor_for_SQL.fetchall()
                connection_to_Database.commit()

                '''If the element didn't exist in SQL, save to SQL.'''
                if not existsInSQL:
                    try:
                        cursor_for_SQL = connection_to_Database.cursor()
                        sql = 'INSERT INTO ' + tableName \
                            + ' (tag, base, currentPath) ' \
                            + 'VALUES (%s,%s,%s);'
                        values = [linkbase.tag, linkbase.base, linkbase.currentPath]
                        cursor_for_SQL.execute(sql, values)
                        connection_to_Database.commit()

                    except:
                        connection_to_Database.rollback()
                        print (sys.exc_info(), 'Linkbase', linkbase.currentPath)

            except:
                connection_to_Database.rollback()
                print (sys.exc_info(), 'Error Occurred in select statement for Linkbase table.')

            '''Tie linkbase to document by searching unique linkbase'''
            try:
                cursor_for_SQL = connection_to_Database.cursor()
                temp_Query_holder   = 'SELECT linkbaseInternal_id FROM ' + tableName \
                                    + ' WHERE tag = %s and currentPath = %s;'
                values_for_Where    = [ linkbase.tag, linkbase.currentPath]
                cursor_for_SQL.execute(temp_Query_holder, values_for_Where)
                linkbaseInternal_idNum = cursor_for_SQL.fetchone()

                if linkbaseInternal_idNum:
                    tableName_in_SQL = 'DocumentHasLinkbase'
                    query_to_Insert = 'INSERT INTO ' + tableName_in_SQL + ' (documentSet_id, linkbaseInternal_id) VALUES (%s,%s);'
                    values_to_Insert = [ documentSetID, linkbaseInternal_idNum]
                    cursor_for_SQL.execute(query_to_Insert, values_to_Insert)
                else:
                    print ('linkbaseInternal_id is null with ', linkbase.tag, linkbase.currentPath)

                connection_to_Database.commit()

            except:
                connection_to_Database.rollback()
                print (sys.exc_info(), 'Error Occurred in DocumentHasLinkbase', linkbase.currentPath)

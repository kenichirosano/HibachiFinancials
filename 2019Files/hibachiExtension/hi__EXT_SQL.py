# -*- coding: utf-8 -*-
import sys

def existsInSQL(connection_to_Database, tableName_in_SQL, searchablePath):
    '''
    Check if the searchable path already exists in SQL database.
    '''
    if tableName_in_SQL == 'TaxonomySchema':

        try:
            cursor_for_SQL = connection_to_Database.cursor()
            #tableName_in_SQL    = 'TaxonomySchema'
            temp_Query_holder   = 'SELECT * FROM ' + tableName_in_SQL + ' WHERE searchablePath = %s;'
            values_for_Where    = [searchablePath]

            cursor_for_SQL.execute(temp_Query_holder, values_for_Where)
            returnValuesFromSQL = cursor_for_SQL.fetchall()
            connection_to_Database.commit()
            if returnValuesFromSQL:
                return True
            else:
                return None
        except:
            print (sys.exc_info(), 'Error Occurred in searching existing TaxonomySchema.')
            return None

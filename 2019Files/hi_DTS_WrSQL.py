# -*- coding: utf-8 -*-
import sys

def writeInMySQL(documentSetID, list_of_DTS, connection_to_Database):
    '''Get the TaxonomySchema from list of DTS in python and save to SQL'''

    for taxonomySchema in list_of_DTS:
        if taxonomySchema.__class__.__name__ == 'TaxonomySchema':
            try:
                cursor_for_SQL = connection_to_Database.cursor()
                tableName    = 'TaxonomySchema'
                tempQueryText   = 'SELECT * FROM ' + tableName \
                                + ' WHERE searchablePath = %s;'
                valuesForTempQueryText    = [taxonomySchema.searchablePath]

                cursor_for_SQL.execute(tempQueryText, valuesForTempQueryText)
                existsInSQL = cursor_for_SQL.fetchall()
                connection_to_Database.commit()

                if not existsInSQL:
                    try:
                        cursor_for_SQL = connection_to_Database.cursor()
                        tableName_in_SQL = 'TaxonomySchema'
                        query_to_Insert = 'INSERT INTO ' + tableName_in_SQL + \
                        ' (searchablePath)' + \
                        ' VALUES (%s);'
                        values_to_Insert = [taxonomySchema.searchablePath]
                        cursor_for_SQL.execute(query_to_Insert, values_to_Insert)
                        connection_to_Database.commit()

                    except: # If the taxonomy schema is not new, don't write in SQL
                        connection_to_Database.rollback()
                        print (sys.exc_info(), 'Error occurred in writing TaxonomySchema.')

            except: # If the taxonomy schema is not new, don't write in SQL
                connection_to_Database.rollback()
                print (sys.exc_info(), 'Error occurred in select statement for TaxonomySchema table.')

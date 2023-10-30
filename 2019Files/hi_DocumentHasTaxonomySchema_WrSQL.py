# -*- coding: utf-8 -*-
import sys

def writeInMySQL(documentSetID, list_of_DTS, connection_to_Database):

    # SAVE simple linked taxonomy schemas to SQL
    for taxonomySchema in list_of_DTS:

        if taxonomySchema.__class__.__name__ == 'TaxonomySchema':
            try:
                # Save the fact this document has this taxonomy schema
                cursor_for_SQL = connection_to_Database.cursor()
                tableName_in_SQL    = 'TaxonomySchema'
                temp_Query_holder   = 'SELECT taxonomyInternal_id FROM ' + tableName_in_SQL \
                                    + ' WHERE searchablePath = %s;'
                values_for_Where    = [taxonomySchema.searchablePath]
                cursor_for_SQL.execute(temp_Query_holder, values_for_Where)
                taxonomyInternal_idNum = cursor_for_SQL.fetchall()

                if taxonomyInternal_idNum:
                    tableName_in_SQL    = 'DocumentHasTaxonomySchema'
                    query_to_Insert     = 'INSERT INTO ' + tableName_in_SQL \
                                        + '(tag, documentSet_id, taxonomyInternal_id)' \
                                        + ' VALUES (%s,%s,%s);'
                    values_to_Insert = [
                        taxonomySchema.tag
                        ,documentSetID
                        ,taxonomyInternal_idNum
                    ]
                    cursor_for_SQL.execute(query_to_Insert, values_to_Insert)
                    #cursor_for_SQL.close()
                    connection_to_Database.commit()
                else:
                    print ('taxonomyInternal_idNum is Null for ', taxonomySchema.searchablePath)

            except:
                connection_to_Database.rollback()
                print (sys.exc_info(), 'Error at Document has TaxonomySchema.')

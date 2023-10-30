def writeInMySQL(documentSetID, listOfConcepts, connection_to_Database):
    ''' Write Concepts in SQL '''

    for concept in listOfConcepts:
        # Write the concept in listOfConcepts to SQL database

        '''Check first if the concept exists in SQL database.'''
        try:
            cursor_for_SQL = connection_to_Database.cursor()
            tableName    = 'Concept'
            temp_Query_holder   = 'SELECT * FROM ' + tableName \
                                + ' WHERE name = %s and id = %s and currentPath = %s;'
            values_for_Where    = [concept.name, concept.id, concept.currentPath]

            cursor_for_SQL.execute(temp_Query_holder, values_for_Where)
            existsInSQL = cursor_for_SQL.fetchall()
            connection_to_Database.commit()

            if not existsInSQL:
                try:
                    # Write concepts in the list to SQL dataabse
                    cursor_for_SQL = connection_to_Database.cursor()
                    queryText = 'INSERT INTO ' + tableName \
                        + ' (name, substitutionGroup, id, periodType, balance, type, currentPath) VALUES (%s,%s,%s,%s,%s,%s,%s);'
                    valuesForQueryText = [
                        concept.name
                        ,concept.substitutionGroup
                        ,concept.id
                        ,concept.periodType
                        ,concept.balance
                        ,concept.type
                        ,concept.currentPath
                    ]
                    cursor_for_SQL.execute(queryText, valuesForQueryText)
                    connection_to_Database.commit()
                except:
                    connection_to_Database.rollback()
                    print (sys.exc_info())
        except: # If the taxonomy schema is not new, don't write in SQL
            connection_to_Database.rollback()
            print (sys.exc_info(), 'Error occurred in select statement for Concept table.')

        try :
            tableName_in_SQL    = 'Concept'
            temp_Query_holder   = 'SELECT conceptInternal_id FROM ' + tableName_in_SQL \
                                + ' WHERE name = %s and id = %s and currentPath = %s;'
            values_for_Where    = [ concept.name, concept.id, concept.currentPath]
            cursor_for_SQL.execute(temp_Query_holder, values_for_Where)
            conceptInternal_idNum = cursor_for_SQL.fetchone()

            if conceptInternal_idNum:
                sql = 'INSERT INTO DocumentHasConcept (documentSet_id, conceptInternal_id) VALUES (%s,%s);'
                values = [documentSetID, conceptInternal_idNum]
                cursor_for_SQL.execute(sql, values)
            else:
                print ('conceptInternal_id was null with ', concept.name, concept.id, concept.currentPath)

            connection_to_Database.commit()

        except:
            connection_to_Database.rollback()
            print (sys.exc_info(), 'Error Occurred in DocumentHasConcept', concept.currentPath)

# -*- coding: utf-8 -*-
import sys

def writeInMySQL(documentSetID, listOfInstance, connection_to_Database):

    for instance in listOfInstance:
        try:
            cursor_for_SQL = connection_to_Database.cursor()
            tableName = 'Instance'
            query_to_Insert = 'INSERT INTO ' \
                            + tableName \
                            + ' (documentSet_id, tag, value, contextRef, unitRef, precisionAttr, decimals) VALUES (%s,%s,%s,%s,%s,%s,%s);'
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

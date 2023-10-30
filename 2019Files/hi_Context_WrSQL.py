# -*- coding: utf-8 -*-
import sys

def writeToSQL(documentSetID, list_of_Contexts, connection_to_Database):

    #SAVE simple linked taxonomy schema sql
    for context in list_of_Contexts:
        try:
            cursor_for_SQL = connection_to_Database.cursor()
            tableName_in_SQL = 'Context'
            temp_Query_Text  = 'INSERT INTO ' + tableName_in_SQL + \
            ' (documentSet_id, id, edinetCode, identifier, instant, forever, startDate, endDate, segment,scenario, dimension, member)' + \
            ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
            values_to_Insert = [
                documentSetID
                ,context['id']
                ,context['edinetCode']
                ,context['identifier']
                ,context['instant']
                ,context['forever']
                ,context['startDate']
                ,context['endDate']
                ,context['segment']
                ,context['scenario']
                ,context['dimension']
                ,context['member']
            ]
            cursor_for_SQL.execute(temp_Query_Text, values_to_Insert)
            connection_to_Database.commit()

        except:
            connection_to_Database.rollback()
            print (sys.exc_info())

import sys

def writeToSQL(documentSetID, listOfUnits, connection_to_Database):

    #SAVE simple linked taxonomy schema sql
    for context in listOfUnits:
        try:
            cursor_for_SQL = connection_to_Database.cursor()
            tableName_in_SQL = 'Unit'
            temp_query_Text  = 'INSERT INTO ' + tableName_in_SQL + \
            '  (documentSet_id, id, singleMeasure, divide, unitNumerator, unitDenominator)' + \
            'VALUES (%s,%s,%s,%s,%s,%s);'
            values_to_Insert = [
                documentSetID
                ,context['id']
                ,context['singleMeasure']
                ,context['divide']
                ,context['unitNumerator']
                ,context['unitDenominator']
            ]
            cursor_for_SQL.execute(temp_query_Text,values_to_Insert)
            connection_to_Database.commit()

        except:
            connection_to_Database.rollback()
            print (sys.exc_info())

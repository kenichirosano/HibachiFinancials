# -*- coding: utf-8 -*-
import sys

def getUnit(root_ElementTree):

    list_of_Units = []
    for unit_ElementTree in root_ElementTree.findall('unit'):
        dict_of_Unit = {
            'id'                :None
            ,'singleMeasure'    :None
            ,'divide'           :None
            ,'unitNumerator'    :None
            ,'unitDenominator'  :None
        }
        dict_of_Unit['id'] = unit_ElementTree.get('id')

        for divide_ElementTree in unit_ElementTree.findall('divide'):
            dict_of_Unit['divide'] = 'True'

            for unitNumerator_ElementTree in divide_ElementTree.findall('unitNumerator'):

                for measure_ElementTree in unitNumerator_ElementTree.findall('measure'):
                    dict_of_Unit['unitNumerator']   = measure_ElementTree.text

            for unitDenominator_ElementTree in divide_ElementTree.findall('unitDenominator'):

                for measure_ElementTree in unitNumerator_ElementTree.findall('measure'):
                    dict_of_Unit['unitDenominator'] = measure_ElementTree.text

        for measure_ElementTree in unit_ElementTree.findall('measure'):
            dict_of_Unit['singleMeasure'] = 'True'
            dict_of_Unit['measure']       = measure_ElementTree.text

        list_of_Units.append(dict_of_Unit)

    return list_of_Units

'''
< 4.8 The <unit> element >
The content of the <unit> element MUST be either a simple unit of measure expressed
with a single <measure> element or a ratio of products of units of measure,
with the ratio represented by the <divide> element
and the numerator and denominator products both represented by a sequence of <measure> elements.
< 4.8.1 The @id attribute >
The @id attribute identifies the Unit so that it may be referenced by <item> elements.
'''

def writeToSQL(documentSetID, listOfUnits, connection_to_Database):
    #SAVE units in instance file

    cursor_for_SQL  = connection_to_Database.cursor()
    tableName= 'Unit'

    # Truncate first
    sql = 'DELETE FROM '\
        + tableName\
        + ' WHERE documentSet_id = %s;'
    cursor_for_SQL.execute(sql,documentSetID)
    connection_to_Database.commit()

    for context in listOfUnits:
        try:
            temp_query_Text = 'INSERT INTO ' + tableName \
                            + ' (' \
                            + 'documentSet_id,' \
                            + 'id,' \
                            + 'singleMeasure,' \
                            + 'divide,' \
                            + 'unitNumerator,' \
                            + 'unitDenominator)' \
                            + 'VALUES (%s,%s,%s,%s,%s,%s);'
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

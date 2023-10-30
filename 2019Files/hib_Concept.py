import sys
import hi_XmlElement_Class as hi_XmlElement

class Concept(hi_XmlElement.XmlElement):
    ''' Class of each concept defined in DTS (taxonomy schema files)
        5.1.1 Concept definitions
        All element names MUST be unique within a given taxonomy schema.'''

    def __init__(self, fileName, element):
        super(Concept, self).__init__(fileName, element)
        self.substitutionGroup  = element.get('substitutionGroup')
        self.name               = element.get('name')
        self.periodType         = element.get('periodType')
        self.balance            = element.get("balance")

def writeInSQL(listOfConcepts, connection_to_Database):
    ''' Write Concepts in SQL '''

    tableName = 'raw_CommonConcept'
    cursor_for_SQL = connection_to_Database.cursor()

    # Truncate the records in the table before inserting the data.
    cursor_for_SQL.execute('TRUNCATE TABLE ' + tableName)

    for concept in listOfConcepts:
        try:
            queryText = 'INSERT INTO ' + tableName \
                + ' ('\
                + 'filePath,'\
                + 'name,'\
                + 'substitutionGroup,'\
                + 'id,'\
                + 'periodType,'\
                + 'balance,'\
                + 'type '\
                + ') '\
                + 'VALUES (%s,%s,%s,%s,%s,%s,%s);'
            values = [
                concept.currentPath,
                concept.name,
                concept.substitutionGroup,
                concept.id,
                concept.periodType,
                concept.balance,
                concept.type
            ]
            cursor_for_SQL.execute(queryText, values)
            connection_to_Database.commit()

        except:
            connection_to_Database.rollback()
            print (sys.exc_info(), 'Error Occurred in writing concepts.', concept.currentPath)

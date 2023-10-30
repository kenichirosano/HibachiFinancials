import hi_XmlElement_Class as hi_XmlElement

class Concept(hi_XmlElement.XmlElement):
    '''Class of each concept defined in DTS (taxonomy schema files)'''

    def __init__(self, fileName, element):
        super(Concept, self).__init__(fileName, element)
        self.substitutionGroup = element.get('substitutionGroup')
        self.name = element.get('name')
        self.periodType = element.get('periodType')
        self.balance = element.get("balance")

'''
5.1.1 Concept definitions
All element names MUST be unique within a given taxonomy schema.
'''

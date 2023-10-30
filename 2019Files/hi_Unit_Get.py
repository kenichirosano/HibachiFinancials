# -*- coding: utf-8 -*-

def getUnit(root_ElementTree):

    list_of_Units = []
    for unit_ElementTree in root_ElementTree.findall('unit'):
        dict_of_Unit = {
            'id':None
            ,'singleMeasure':None
            ,'divide':None
            ,'unitNumerator':None
            ,'unitDenominator':None
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

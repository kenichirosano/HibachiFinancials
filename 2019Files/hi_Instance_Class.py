# -*- coding: utf-8 -*-
import hi__EXT_ETtree as hi_EXT_ET
import hi_XmlElement_Class as hi_XmlElement

class Instance(hi_XmlElement.XmlElement):
    '''Class of each instance defined in DTS (taxonomy schema files)'''

    def __init__(self, fileName, instanceElement):
        super(Instance, self).__init__(fileName, instanceElement)
        self.tag = hi_EXT_ET.removeNSfromText(instanceElement.tag)
        self.value = instanceElement.text
        self.contextRef = instanceElement.get('contextRef')
        self.unitRef = instanceElement.get('unitRef')
        self.precision = instanceElement.get('precision')
        self.decimals = instanceElement.get('decimals')

'''
1.4 Terminology (non-normative except where otherwise noted)
An item contains the value of the simple fact and a reference to the context (and unit for numeric items) needed to correctly interpret that fact.
When items occur as children of a tuple, they must also be interpreted in light of the other items and tuples that are children of the same tuple.
There are numeric items and non-numeric items, with numeric items being required to document their measurement accuracy and units of measurement.

4.6.4 The @precision attribute (optional)
The @precision attribute MUST be a non-negative integer or the string "INF" that conveys the arithmetic precision of a measurementsself.

'''

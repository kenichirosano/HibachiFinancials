# -*- coding: utf-8 -*-
import hi__EXT_XLink_Ext as EXT_XL_Ext
import hi_XmlElement_Class as hi_XmlElement

class RoleRef(hi_XmlElement.XmlElement):
    #Class of each linkbase (<linkbase>, <roleRef>, <roleType> or <arcroleType>)
    def __init__(self, fileName, element):
        super(RoleRef, self).__init__(fileName, element)
        self.roleURI = element.get('roleURI') #<roleRef>
        self.arcroleURI = element.get('arcroleURI')

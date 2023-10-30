# -*- coding: utf-8 -*-
import hi__EXT_XLink as hi_EXT_XL
import hi_XmlElement_Class

class TaxonomySchema(hi_XmlElement_Class.XmlElement):

    def __init__(self, name_of_CurrentFile, taxonomy_ElementTree):
        super(TaxonomySchema, self).__init__(name_of_CurrentFile, taxonomy_ElementTree)
        self.originalPath = hi_EXT_XL.getOriginalPath(taxonomy_ElementTree)
        self.fragment_ID = hi_EXT_XL.split_Fragment_ID(self.originalPath)[1]
        self.href_type, self.searchablePath = hi_EXT_XL.createSearchablePath(name_of_CurrentFile, self.originalPath) #Check original path type and get new path

    def hasJFSApath(self): #Return True if the link contains JFSA link path
        if (self.href_type == 'JFSA'):
            return True
        else:
            return False

    def hasFragmentID(self): #Return True if the link contains JFSA link fragment identifier
        if (hi_EXT_XL.split_Fragment_ID(self.originalPath)[1]):
            return True #If it doesn't contain hash
        else:
            return False

    def isFragmentID_only(self): #Return True if the path is only fragment ID
        if (self.href_type == 'FIDONLY'):
            return True
        else:
            return False

'''
5.1.3 Defining custom role types - the <roleType> element
The <roleType> element MUST be located among the set of nodes identified by the [XPath 1.0] path "//xsd:schema/xsd:annotation/xsd:appinfo/*".
The value of the @roleURI attribute identifies the @xlink:role attribute value that is being defined.
5.1.4 Defining custom arc role types - the arcroleType element
The <arcroleType> element MUST be among the set of nodes identified by the [XPath 1.0] path "//xsd:schema/xsd:annotation/xsd:appinfo/*".
The value of the @arcroleURI identifies the @xlink:arcrole attribute value that is being defined.
'''

# -*- coding: utf-8 -*-
import hi__EXT_ETtree as hi_EXT_ET
import hi__EXT_XLink as hi_EXT_XL

class XmlElement(object):

    def __init__(self, fileName, element):
        self.tag            = element.tag # Element name
        self.id             = element.get('id')
        self.type           = element.get('type')
        self.role           = element.get('role')
        self.arcrole        = element.get('arcrole') #For <linkbaseRef> element (4.3.3) (Must be http://www.w3.org/1999/xlink/properties/linkbase)
        self.base           = element.get('base') #For <linkbaseRef> element (4.3.5)
        self.originalPath   = hi_EXT_XL.getOriginalPath(element) # Original value of URI
        self.fragment_ID    = hi_EXT_XL.split_Fragment_ID(self.originalPath)[1] # Get fragment ID
        self.currentPath    = fileName # The file xlink is referred to from
        self.href_type, self.searchablePath = hi_EXT_XL.createSearchablePath(fileName, self.originalPath) #Check original path type and get new path

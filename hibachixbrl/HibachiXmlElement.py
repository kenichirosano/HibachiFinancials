from hibachixbrl import HibachiXLink

class XmlElement(object):
    def __init__(self, fileName, element):
        # Make sure the attributes in lower cases (hustles when saved in PostgreSQL)
        self.tag            = element.tag # Element name
        self.id             = element.get('id')
        self.type           = element.get('type')
        self.role           = element.get('role')
        
        #For <linkbaseRef> element (4.3.3) (Must be http://www.w3.org/1999/xlink/properties/linkbase)
        self.arcrole        = element.get('arcrole') 

        #For <linkbaseRef> element (4.3.5)
        self.base           = element.get('base') 

        # Original value of URI
        self.originalpath   = HibachiXLink.getoriginalpath(element) 

        # Get fragment ID
        self.fragment_id    = HibachiXLink.split_fragment_id(self.originalpath)[1] 

        #Check original path type and get new path
        self.href_type, self.searchablepath, self.href = HibachiXLink.createsearchablepath(fileName, self.originalpath) 

        #self.currentPath    = fileName # The file xlink is referred to from


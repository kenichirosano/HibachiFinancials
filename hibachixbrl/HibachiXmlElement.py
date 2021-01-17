from hibachixbrl import HibachiXLink

class XmlElement(object):
    def __init__(self, fileName, element):
        # Make sure the attributes in lower cases (hustles when saved in PostgreSQL)
        self.tag            = element.tag # Element name
        self.id             = element.get('id')
        self.type           = element.get('type')
        self.role           = element.get('role')
        self.arcrole        = element.get('arcrole') #For <linkbaseRef> element (4.3.3) (Must be http://www.w3.org/1999/xlink/properties/linkbase)
        self.base           = element.get('base') #For <linkbaseRef> element (4.3.5)
        self.originalpath   = HibachiXLink.getoriginalpath(element) # Original value of URI
        self.fragment_id    = HibachiXLink.split_fragment_id(self.originalpath)[1] # Get fragment ID
        #self.currentPath    = fileName # The file xlink is referred to from
        self.href_type, self.searchablepath, self.href = HibachiXLink.createsearchablepath(fileName, self.originalpath) #Check original path type and get new path

class TaxonomySchema(XmlElement):

    def __init__(self, name_of_CurrentFile, taxonomy_ElementTree):
        super(TaxonomySchema, self).__init__(name_of_CurrentFile, taxonomy_ElementTree)
        self.originalpath = HibachiXLink.getoriginalpath(taxonomy_ElementTree)
        self.fragment_id = HibachiXLink.split_fragment_id(self.originalpath)[1]
        #Check original path type and get new path
        self.href_type, self.searchablepath, self.href = HibachiXLink.createsearchablepath(name_of_CurrentFile, self.originalpath) 
        #<roleRef>
        self.roleURI = taxonomy_ElementTree.get('roleURI')
        #<arcroleRef>
        self.arcroleURI = taxonomy_ElementTree.get('arcroleURI')

    def hasJFSApath(self): #Return True if the link contains JFSA link path
        if (self.href_type == 'JFSA'):
            return True
        else:
            return False

    def hasFragmentID(self): #Return True if the link contains JFSA link fragment identifier
        if (HibachiXLink.split_fragment_id(self.originalpath)[1]):
            return True #If it doesn't contain hash
        else:
            return False

    def isFragmentID_only(self): #Return True if the path is only fragment ID
        if (self.href_type == 'FIDONLY'):
            return True
        else:
            return False


class Linkbase(XmlElement):
    #Class of each linkbase (<linkbase>, <roleRef>, <roleType> or <arcroleType>)
    def __init__(self, fileName, element):
        super(Linkbase, self).__init__(fileName, element)
        self.childElementList = assign_linkbaseElementDictList(fileName, element)

def assign_linkbaseElementDictList(fileName, linkbase_ElementTree):
    '''Get child elements and create a list containing the elements.'''

    list_of_LinkbaseElementDict = []
    if linkbase_ElementTree.tag == 'linkbase':
        linkbaseLinkElementDict = {
            'tag'       :None
            ,'type'     :None
            ,'id'       :None
            ,'role'     :None
            ,'base'     :None
            ,'childList':None
        }
        extendedLinkElementDict = {
            'tag'            :None
            ,'type'          :None
            ,'role'          :None
            ,'arcrole'       :None
            ,'label'         :None
            ,'lang'          :None
            ,'from'          :None
            ,'to'            :None
            ,'preferredLabel':None
            ,'weight'        :None
            ,'order'         :None
            ,'originalPath'  :None
            ,'content'       :None
            ,'use'           :None
            ,'priority'      :None
            ,'fragment_ID'   :None
            ,'searchablePath':None
        }

        # 5.2.2 <labelLink>
        for labelLink_ElementTree in linkbase_ElementTree.findall('labelLink'):
            labelLink_ElementDict = linkbaseLinkElementDict.copy()
            labelLink_ElementDict = HibachiXLink.returnElementAsDict(labelLink_ElementTree, labelLink_ElementDict)
            # Get the child element with specific tags
            list_of_ChildElementDicts = HibachiXLink.returnChildElementListOfDict(fileName, labelLink_ElementTree, ['loc','label','labelArc'], extendedLinkElementDict)
            labelLink_ElementDict['childList'] = list_of_ChildElementDicts
            list_of_LinkbaseElementDict.append(labelLink_ElementDict)

        # 5.2.3 <referenceLink>
        for referenceLink_ElementTree in linkbase_ElementTree.findall('referenceLink'):
            referenceLinkElementDict = linkbaseLinkElementDict.copy()
            referenceLinkElementDict = HibachiXLink.returnElementAsDict(referenceLink_ElementTree, referenceLinkElementDict)
            # Get the child element with specific tags
            list_of_ChildElementDicts = HibachiXLink.returnChildElementListOfDict(fileName, referenceLink_ElementTree, ['loc','label','labelArc'], extendedLinkElementDict)
            referenceLinkElementDict['childList'] = list_of_ChildElementDicts
            list_of_LinkbaseElementDict.append(referenceLinkElementDict)

        # 5.2.4 <presentationLink>
        for presentationLink_ElementTree in linkbase_ElementTree.findall('presentationLink'):
            presentationLinkElementDict = linkbaseLinkElementDict.copy()
            presentationLinkElementDict = HibachiXLink.returnElementAsDict(presentationLink_ElementTree, presentationLinkElementDict)
            # Get the child element with specific tags 5.2.4.1 <loc>, 5.2.4.2 <presentationArc>
            list_of_ChildElementDicts = HibachiXLink.returnChildElementListOfDict(fileName, presentationLink_ElementTree,['loc','presentationArc'], extendedLinkElementDict)
            presentationLinkElementDict['childList'] = list_of_ChildElementDicts
            list_of_LinkbaseElementDict.append(presentationLinkElementDict)

        # 5.2.5 <calculationLink>
        for calculationLink_ElementTree in linkbase_ElementTree.findall('calculationLink'):
            calculationLinkElementDict = linkbaseLinkElementDict.copy()
            calculationLinkElementDict = HibachiXLink.returnElementAsDict(calculationLink_ElementTree, calculationLinkElementDict)
            # Get the child element with specific tags
            list_of_ChildElementDicts = HibachiXLink.returnChildElementListOfDict(fileName, calculationLink_ElementTree,['loc','calculationArc'], extendedLinkElementDict)
            calculationLinkElementDict['childList'] = list_of_ChildElementDicts
            list_of_LinkbaseElementDict.append(calculationLinkElementDict)

        # 5.2.6 <definitionLink>
        for definitionLink_ElementTree in linkbase_ElementTree.findall('definitionLink'):
            definitionLinkElementDict = linkbaseLinkElementDict.copy()
            definitionLinkElementDict = HibachiXLink.returnElementAsDict(definitionLink_ElementTree, definitionLinkElementDict)
            # Get the child element with specific tags
            list_of_ChildElementDicts = HibachiXLink.returnChildElementListOfDict(fileName, definitionLink_ElementTree, ['loc','definitionArc'], extendedLinkElementDict)
            definitionLinkElementDict['childList'] = list_of_ChildElementDicts
            list_of_LinkbaseElementDict.append(definitionLinkElementDict)

    return list_of_LinkbaseElementDict


# class RoleRef(XmlElement):
#     #Class of each linkbase (<linkbase>, <roleRef>, <roleType> or <arcroleType>)
#     def __init__(self, fileName, element):
#         super(RoleRef, self).__init__(fileName, element)
#         self.roleURI = element.get('roleURI') #<roleRef>
#         self.arcroleURI = element.get('arcroleURI')

class Roletype(XmlElement):
    #Class of <footnoteLink> element
    def __init__(self, fileName, element):
        super(Roletype, self).__init__(fileName, element)
        self.roleURI = element.get('roleURI') # 5.1.3 <roleType>, <roleRef>
        self.arcroleURI = element.get('arcroleURI') # 5.1.4 <arcroleType>
        self.cyclesAllowed = element.get('cyclesAllowed') # for <arcroleURI>
        self.childElementDict = assign_roleTypeElementDict(fileName, element)

def assign_roleTypeElementDict(fileName, element):
    '''
    Get child elements of <roleType> or <arcroleType> element and create a list containing them.
    <roleType> element has <definition>, <usedOn> element
    '''
    roleTypeChildElementDict = { 'definition':None, 'usedOn':None }
    for key in roleTypeChildElementDict.keys():
        for element in element.findall(key):
            roleTypeChildElementDict[key] = element.text
    return roleTypeChildElementDict


'''
5.1.3 Defining custom role types - the <roleType> element
The <roleType> element MUST be located among the set of nodes identified by the [XPath 1.0] path "//xsd:schema/xsd:annotation/xsd:appinfo/*".
The value of the @roleURI attribute identifies the @xlink:role attribute value that is being defined.
5.1.4 Defining custom arc role types - the arcroleType element
The <arcroleType> element MUST be among the set of nodes identified by the [XPath 1.0] path "//xsd:schema/xsd:annotation/xsd:appinfo/*".
The value of the @arcroleURI identifies the @xlink:arcrole attribute value that is being defined.
'''

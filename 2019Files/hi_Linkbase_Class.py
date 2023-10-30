# -*- coding: utf-8 -*-
import hi__EXT_XLink_Ext as EXT_XL_Ext
import hi_XmlElement_Class as hi_XmlElement

class Linkbase(hi_XmlElement.XmlElement):
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
        list_of_ChildElementDicts = []

        # 5.2.2 <labelLink>
        for labelLink_ElementTree in linkbase_ElementTree.findall('labelLink'):
            labelLink_ElementDict = linkbaseLinkElementDict.copy()
            labelLink_ElementDict = EXT_XL_Ext.returnElementAsDict(labelLink_ElementTree, labelLink_ElementDict)
            list_of_ChildElementDicts = EXT_XL_Ext.returnChildElementListOfDict(fileName, labelLink_ElementTree, 'loc', extendedLinkElementDict)
            list_of_ChildElementDicts.extend(EXT_XL_Ext.returnChildElementListOfDict(fileName, labelLink_ElementTree, 'label', extendedLinkElementDict))
            list_of_ChildElementDicts.extend(EXT_XL_Ext.returnChildElementListOfDict(fileName, labelLink_ElementTree, 'labelArc', extendedLinkElementDict))
            labelLink_ElementDict['childList'] = list_of_ChildElementDicts
            list_of_LinkbaseElementDict.append(labelLink_ElementDict)

        # 5.2.3 <referenceLink>
        for referenceLink_ElementTree in linkbase_ElementTree.findall('referenceLink'):
            referenceLinkElementDict = linkbaseLinkElementDict.copy()
            referenceLinkElementDict = EXT_XL_Ext.returnElementAsDict(referenceLink_ElementTree, referenceLinkElementDict)
            list_of_ChildElementDicts = EXT_XL_Ext.returnChildElementListOfDict(fileName, referenceLink_ElementTree, 'loc', extendedLinkElementDict)
            list_of_ChildElementDicts.extend(EXT_XL_Ext.returnChildElementListOfDict(fileName, referenceLink_ElementTree, 'reference', extendedLinkElementDict))
            list_of_ChildElementDicts.extend(EXT_XL_Ext.returnChildElementListOfDict(fileName, referenceLink_ElementTree, 'referenceArc', extendedLinkElementDict))
            referenceLinkElementDict['childList'] = list_of_ChildElementDicts
            list_of_LinkbaseElementDict.append(referenceLinkElementDict)

        # 5.2.4 <presentationLink>
        for presentationLink_ElementTree in linkbase_ElementTree.findall('presentationLink'):
            presentationLinkElementDict = linkbaseLinkElementDict.copy()
            presentationLinkElementDict = EXT_XL_Ext.returnElementAsDict(presentationLink_ElementTree, presentationLinkElementDict)
            list_of_ChildElementDicts = EXT_XL_Ext.returnChildElementListOfDict(fileName, presentationLink_ElementTree, 'loc', extendedLinkElementDict)
            list_of_ChildElementDicts.extend(EXT_XL_Ext.returnChildElementListOfDict(fileName, presentationLink_ElementTree, 'presentationArc', extendedLinkElementDict))
            presentationLinkElementDict['childList'] = list_of_ChildElementDicts
            list_of_LinkbaseElementDict.append(presentationLinkElementDict)

        # 5.2.5 <calculationLink>
        for calculationLink_ElementTree in linkbase_ElementTree.findall('calculationLink'):
            calculationLinkElementDict = linkbaseLinkElementDict.copy()
            calculationLinkElementDict = EXT_XL_Ext.returnElementAsDict(calculationLink_ElementTree, calculationLinkElementDict)
            list_of_ChildElementDicts = EXT_XL_Ext.returnChildElementListOfDict(fileName, calculationLink_ElementTree, 'loc', extendedLinkElementDict)
            list_of_ChildElementDicts.extend(EXT_XL_Ext.returnChildElementListOfDict(fileName, calculationLink_ElementTree, 'calculationArc', extendedLinkElementDict))
            calculationLinkElementDict['childList'] = list_of_ChildElementDicts
            list_of_LinkbaseElementDict.append(calculationLinkElementDict)

        # 5.2.6 <definitionLink>
        for definitionLink_ElementTree in linkbase_ElementTree.findall('definitionLink'):
            definitionLinkElementDict = linkbaseLinkElementDict.copy()
            definitionLinkElementDict = EXT_XL_Ext.returnElementAsDict(definitionLink_ElementTree, definitionLinkElementDict)
            list_of_ChildElementDicts = EXT_XL_Ext.returnChildElementListOfDict(fileName, definitionLink_ElementTree, 'loc', extendedLinkElementDict)
            list_of_ChildElementDicts.extend(EXT_XL_Ext.returnChildElementListOfDict(fileName, definitionLink_ElementTree, 'definitionArc', extendedLinkElementDict))
            definitionLinkElementDict['childList'] = list_of_ChildElementDicts
            list_of_LinkbaseElementDict.append(definitionLinkElementDict)

    return list_of_LinkbaseElementDict

'''
5.2 Taxonomy linkbases
Extended Links MUST be held in an [XLINK] document container, which MUST be a <linkbase> element located either:
1. among the set of nodes identified by the XPath [XPath 1.0] path "//xsd:schema/xsd:annotation/xsd:appinfo/*" in the Taxonomy Schema; or
2. at the root element of a separate document.
'''

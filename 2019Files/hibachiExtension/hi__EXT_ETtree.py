# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import sys

def etree_parse_remove_NS(file_name):
    '''Remove namespace for all the elements and attibutes'''

    try:
        it = ET.iterparse(file_name) #parse
        for _, element in it:
            if '}' in element.tag:
                element.tag = element.tag.split('}', 1)[1]  # strip all namespaces
                for at in list(element.attrib.keys()): # strip namespaces of attributes too. User list!
                    if '}' in at:
                        newat = at.split('}', 1)[1]
                        element.attrib[newat] = element.attrib[at]
                        del element.attrib[at]
        root = it.root
        return root #Return root tree

    except:
        print ('Error when parsing', sys.exc_info()[0], sys.exc_info()[1])

def returnListOfInstanceElements_with_SpecifiedNameSpace(file_name, nameSpaceSpecified):
    '''Return etree with specified namespace for all the elements and attibutes'''

    listOfInstanceElements = []
    try:
        it = ET.iterparse(file_name) #parse
        for _, element in it:
            if '}' in element.tag:
                elementNamespace = (element.tag.split('{', 1)[1]).split('}',1)[0]
                if elementNamespace == nameSpaceSpecified:
                    listOfInstanceElements.append(element)
        return listOfInstanceElements

    except:
        print ('Error when parsing', sys.exc_info()[0], sys.exc_info()[1])

#Parse without removing namespaces
def etree_parse_with_NS(file_name):

    try:
        root = ET.parse(file_name)# parse
        return root # Return root tree

    except:
        print ('Error when parsing', sys.exc_info()[0],  sys.exc_info()[1])
        listOfErrorURLs = file_name

def removeNSfromText(text):
    #Remove namespace from text

    if '}' in text:
        text = text.split('}', 1)[1]  # get text after namespace
    return text #Return text without namespace

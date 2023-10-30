# -*- coding: utf-8 -*-
import sys
import hi_Instance_Class as Instance
import hi__EXT_ETtree as hi_EXT_ET
import xml.dom
import xml.dom.minidom

def getInstance(instanceFileName, listOfConcepts, listOfInstances):
    '''Method of getting all the instances from DTS'''

    financials_URI = get_Financials_NS_URI(instanceFileName) # Get financial statements' namespace URI
    root = hi_EXT_ET.etree_parse_with_NS(instanceFileName) # Parse the xbrl
    for concept in listOfConcepts: # For all concept
        elementNameToSearch = '{' + financials_URI + '}' + concept.name
        for instanceElement in root.iter(elementNameToSearch): # Find element
            listOfInstances.append(Instance.Instance(instanceFileName, instanceElement))

def get_Financials_NS_URI(instanceFileName):
    '''Get financial statements' namespace URI'''

    xml_dom = xml.dom.minidom.parse(instanceFileName) # parse by DOM
    ''' Return namespace URI.
        Parth with namespace of 'xmlns:jppfs_cor' to get JFSA instances.'''
    return xml_dom.getElementsByTagNameNS('*','xbrl')[0].getAttribute('xmlns:jppfs_cor')

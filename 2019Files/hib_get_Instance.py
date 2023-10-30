# -*- coding: utf-8 -*-
import os
import sys
import hib_connectMySQL
import hi__EXT_ETtree       as hi_EXT_ET
import hi_XmlElement_Class  as hi_XmlElement
import hib_Instance         as Instance
import hib_Unit             as Unit
import hib_Context          as Context

fileName_List_to_Read = [
    'financials/jpcrp030000-asr-001_E00288-000_2018-03-31_01_2018-07-02.xbrl'
]

# switches
switch_unit     = 1
switch_context  = 1
switch_instance = 1

# Connect to MySQL
connection_to_Database  = hib_connectMySQL.connectToMySQL()

for fileName_to_Read in fileName_List_to_Read:

    listOfInstance = []
    root_ElementTree = hi_EXT_ET.etree_parse_remove_NS(fileName_to_Read)
    resultFromDocumentSet = Instance.writeDocumentSetToSQL(Instance.getDocumentSet(root_ElementTree, fileName_to_Read),connection_to_Database)

    if (os.path.splitext(fileName_to_Read)[1])  == '.xbrl':
        documentSet_id = resultFromDocumentSet[1]
        try:
            # Get unit
            if switch_unit == 1:
                Unit.writeToSQL(documentSet_id, Unit.getUnit(root_ElementTree), connection_to_Database)

            # Get context
            if switch_context == 1:
                Context.writeToSQL(documentSet_id, Context.getContext(root_ElementTree), connection_to_Database)

            # Get Instance
            if switch_instance == 1:
                Instance.getInstance(fileName_to_Read, listOfInstance) #Get all instance
                Instance.writeInSQL(documentSet_id, listOfInstance, connection_to_Database)

        except:
            print ('Error in reading:', fileName_to_Read, sys.exc_info()[0], sys.exc_info()[1])

connection_to_Database.close()

# -*- coding: utf-8 -*-

# ------------------- The process of reading xbrl document Set -------------------
# 1. Get Context, DocumentSet info
# 2. Get DTS including linkbase
# 3. Get Concept using DTS list
# 4. Get Instance using Concept list

# ------------------- Hibachi Financials Moducles -------------------------
import hi__EXT_ETtree                       as hi_EXT_ET
import hi_DTS_Get                           as getDTS
import hi_Concept_Get                       as getConcept
import hi_Instance_Get                      as getInstance
import hi_FootnoteLink                      as FootnoteLink
import hi_Roletype                          as Roletype
import hi_Context_Get                       as getContext
import hi_DocumentSet_Get                   as getDocumentSet
import hi_Unit_Get                          as getUnit
import hi_DTS_WrSQL                         as writeToSQLDTS
import hi_DocumentHasTaxonomySchema_WrSQL   as writeToSQLDocumentHasTaxonomySchema
import hi_DocumentHasRoleRef_WrSQL          as writeToSQLDocumentHasRoleRef
import hi_Linkbase_WrSQL                    as writeToSQLLinkbase
import hi_LinkbaseLink_WrSQL                as writeToSQLLinkbaseLink
import hi_RoleRef_WrSQL                     as writeToSQLRoleRef
import hi_Concept_WrSQL                     as writeToSQLConcept
import hi_Instance_WrSQL                    as writeToSQLInstance
import hi_Context_WrSQL                     as writeToSQLContext
import hi_DocumentSet_WrSQL                 as writeToSQLDocumentSet    # Check if the document is new and write in SQL
import hi_Unit_WrSQL                        as writeToSQLUnit
import hi_removeReadFiles                   as removeReadFiles          # Function to avoid reading the same file again

# ------------------- Common Modules ----------------------------------------
import os       # To split the path and get the extention
import time     # To calculate the program time
import pymysql  # To handle MySQL

# -------------------- Program Starts From Here --------------------------------------------------------
# Set the file path & name to open
fileName_List_to_Read = [
    'jpcrp030000-asr-001_E03606-000_2019-03-31_01_2019-06-27.xbrl' #UFJ
]
listOferrorURLs = [] # List to hold URLs that are failed to be parsed
listOfEndTimes  = [] # List to hold times that took at each step
# inputCommand = str(raw_input('What do you like to do?')) # Get the input
start_time = round(time.time(),2) # To calculate the process time, get the current time

#--------------------------------------------- Get DTS ----------------------------------------
for fileName_to_Read in fileName_List_to_Read:

    if (os.path.splitext(fileName_to_Read)[1])  == '.xbrl':

        listOfDTS       = [] # List to hold DTS, Data Taxonomy Set
        listOfLinkbase  = [] # List to hold linkbase
        listOfConcepts  = [] # List to hold concept
        listOfInstance  = [] # List to hold instance

        '''Read the xbrl files and save the unique data to SQL database.'''
        # document set
        root_ElementTree = hi_EXT_ET.etree_parse_remove_NS(fileName_to_Read)
        resultFromDocumentSet = writeToSQLDocumentSet.writeToSQL(getDocumentSet.getDocumentSet(root_ElementTree, fileName_to_Read))
        listOfEndTimes.append(round(time.time(),2))

        # ------------------------------------------- If the document is already read, don't read the document ------------------------------
        if resultFromDocumentSet[0]:
            connection_to_Database = pymysql.connect(
                host        = "localhost"
                ,user       = "root"
                ,passwd     = "stufsno1"
                ,db         = "financials"
                ,use_unicode= True
                ,charset    = "utf8"
            )
            #connection_to_Database.set_character_set('utf8')
            documentSet_id = resultFromDocumentSet[1]

            # unit
            writeToSQLUnit.writeToSQL(documentSet_id, getUnit.getUnit(root_ElementTree), connection_to_Database)
            listOfEndTimes.append(round(time.time(),2))

            # context
            writeToSQLContext.writeToSQL(documentSet_id, getContext.getContext(root_ElementTree), connection_to_Database)
            listOfEndTimes.append(round(time.time(),2))

            # **************** Get DTS (Discoverable Taxonomy Set) ****************
            getDTS.getDTSPath(fileName_to_Read, listOfDTS, connection_to_Database, listOferrorURLs)
            # Remove the files that are already read from DTS list
            removeReadFiles.returnOnlyFilesToBeRead(listOfDTS, connection_to_Database)
            writeToSQLDTS.writeInMySQL(documentSet_id, listOfDTS, connection_to_Database)
            listOfEndTimes.append(round(time.time(),2))

            # Roletype
            Roletype.writeInMySQL(documentSet_id, listOfDTS, connection_to_Database)
            listOfEndTimes.append(round(time.time(),2))

            # Linkbase
            writeToSQLLinkbase.writeInMySQL(documentSet_id, listOfDTS, connection_to_Database)
            writeToSQLLinkbaseLink.writeInMySQL(documentSet_id, listOfDTS, connection_to_Database)
            listOfEndTimes.append(round(time.time(),2))

            # RoleRef
            writeToSQLRoleRef.writeInMySQL(documentSet_id, listOfDTS, connection_to_Database)
            listOfEndTimes.append(round(time.time(),2))

            # Concept
            getConcept.getConcept_OnPython(listOfDTS,listOfConcepts) #Get all concept
            writeToSQLConcept.writeInMySQL(documentSet_id, listOfConcepts, connection_to_Database)
            listOfEndTimes.append(round(time.time(),2))

            # Instance
            getInstance.getInstance(fileName_to_Read, listOfConcepts, listOfInstance) #Get all instance
            writeToSQLInstance.writeInMySQL(documentSet_id, listOfInstance, connection_to_Database)
            listOfEndTimes.append(round(time.time(),2))

            # FootNote
            FootnoteLink.writeInMySQL(documentSet_id, listOfDTS, connection_to_Database)
            listOfEndTimes.append(round(time.time(),2))

            ''' Save the relatioship between documentSet and taxonomy schema & linkbases.'''
            # DocumentHasTaxonomySchema
            writeToSQLDocumentHasTaxonomySchema.writeInMySQL(documentSet_id, listOfDTS, connection_to_Database)
            listOfEndTimes.append(round(time.time(),2))

            # DocumentHasRoleRef
            writeToSQLDocumentHasRoleRef.writeInMySQL(documentSet_id, listOfDTS, connection_to_Database)
            listOfEndTimes.append(round(time.time(),2))

            connection_to_Database.close()

        elif resultFromDocumentSet[1] == 0:
            print('Document wasn\'t read because the same document is already in the SQL database.')

        elif resultFromDocumentSet[1] == 1:
            print('Error occurred in reading the file.')

# Display URLs that cannot be read
for errorURL in listOferrorURLs:
    print ('Error occurred in reading: '), errorURL

# Calculate the process time
stepCounter = 0
for eachTime in listOfEndTimes:
    if stepCounter == 0: processTime = eachTime - start_time
    else: processTime = eachTime - listOfEndTimes[stepCounter-1]
    stepCounter += 1
    print (stepCounter,('took'), ("%.2f" % processTime), ('seconds.'))
print ('This program took', ("%.2f" % (round(time.time(),2) - start_time)), 'seconds in total.')

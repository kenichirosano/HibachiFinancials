# -*- coding: utf-8 -*-
import sys

def writeInMySQL(documentSetID, listOfDTS, connection_to_Database):

    for linkbase in listOfDTS:

        if linkbase.__class__.__name__ == 'Linkbase':
            try: # Fetch linkbaseInternal_id from Linkbase table to match linkbaselink
                cursor_for_SQL = connection_to_Database.cursor()
                tableName_in_SQL    = 'Linkbase'
                temp_Query_holder   = 'SELECT linkbaseInternal_id FROM ' + tableName_in_SQL \
                                    + ' WHERE tag = %s and currentPath = %s;'
                values_for_Where    = [
                    linkbase.tag
                    ,linkbase.currentPath
                ]
                cursor_for_SQL.execute(temp_Query_holder, values_for_Where)
                linkbaseInternal_idNum = cursor_for_SQL.fetchone()
                connection_to_Database.commit()
                #print linkbaseInternal_idNum

                for linkbaseLinkElementDict in linkbase.childElementList:
                    cursor_for_SQL = connection_to_Database.cursor()
                    tableName = 'LinkbaseLink'
                    sql = 'INSERT IGNORE INTO ' + tableName \
                        + ' (linkbaseInternal_id, id, tag, type, role, base) VALUES (%s,%s,%s,%s,%s,%s);'
                    values = [
                        linkbaseInternal_idNum
                        ,linkbaseLinkElementDict['id']
                        ,linkbaseLinkElementDict['tag']
                        ,linkbaseLinkElementDict['type']
                        ,linkbaseLinkElementDict['role']
                        ,linkbaseLinkElementDict['base']
                    ]
                    cursor_for_SQL.execute(sql, values)
                    linkbaseLinkInternal_idNum = cursor_for_SQL.lastrowid
                    #linkbaseLinkInternal_idNum = cursor_for_SQL.fetchall()
                    #print linkbaseLinkInternal_idNum

                    if linkbaseLinkInternal_idNum:
                        for extendtedLinkDict in linkbaseLinkElementDict['childList']:
                            try:
                                tableName = 'ExtendedLink'
                                sql = 'INSERT IGNORE INTO ' + tableName \
                                    + ' (linkbaseLinkInternal_id, tag, type, role, arcrole, label, lang, fromAttr,' \
                                    + ' toAttr, preferredLabel, weight, orderAttr, originalPath, searchablePath, fragment_ID, content, useAttr, priority)' \
                                    + ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
                                values = [
                                    linkbaseLinkInternal_idNum
                                    ,extendtedLinkDict['tag']
                                    ,extendtedLinkDict['type']
                                    ,extendtedLinkDict['role']
                                    ,extendtedLinkDict['arcrole']
                                    ,extendtedLinkDict['label']
                                    ,extendtedLinkDict['lang']
                                    ,extendtedLinkDict['from']
                                    ,extendtedLinkDict['to']
                                    ,extendtedLinkDict['preferredLabel']
                                    ,extendtedLinkDict['weight']
                                    ,extendtedLinkDict['order']
                                    ,extendtedLinkDict['originalPath']
                                    ,extendtedLinkDict['searchablePath']
                                    ,extendtedLinkDict['fragment_ID']
                                    ,extendtedLinkDict['content']
                                    ,extendtedLinkDict['use']
                                    ,extendtedLinkDict['priority']
                                ]
                                cursor_for_SQL.execute(sql, values)

                            except:
                                connection_to_Database.rollback()
                                print (sys.exc_info(), 'Error occurred in ExtendedLink', 'linkbaselink_id was', linkbaseLinkInternal_idNum, linkbaseInternal_idNum, linkbaseLinkElementDict['tag'], linkbase.currentPath)

                    else:
                        print ('linkbaseLinkInternal_id is Null with ', linkbaseInternal_idNum, extendtedLinkDict['tag'], extendtedLinkDict['role'], linkbase.tag, linkbase.role)

                        connection_to_Database.commit()

            except:
                connection_to_Database.rollback()
                print(sys.exc_info(), 'Error occurred in LinkbaseLink', linkbase.currentPath)

# -*- coding: utf-8 -*-
import pymysql
import sys

connection_to_Database = pymysql.connect(
    host        = "localhost"
    ,user       = "root"
    ,passwd     = "stufsno1"
    ,db         = "financials"
    ,use_unicode= True
    ,charset    = "utf8"
)
documentSet_idNum = 1

try: #Insert into PresentationLinkTreePath table the combination of parent and child ids
    cursor_for_SQL  = connection_to_Database.cursor()
    tempQueryText   = 'INSERT INTO PresentationLinkTreePath'\
                    +' SELECT   e.documentSet_id'\
                    +		    ',ParentConcept.conceptInternal_id'\
                    +		    ',ChildConcept.conceptInternal_id'\
                    +		    ',preArc.orderAttr'\
                    +		    ',c.role'\
                    +' FROM Concept ParentConcept'\
                    +' LEFT JOIN ExtendedLink ParentLoc on ParentConcept.id = ParentLoc.fragment_ID and ParentConcept.currentPath = ParentLoc.searchablePath'\
                    +' LEFT JOIN ExtendedLink preArc on preArc.fromAttr = ParentLoc.label and preArc.linkbaseLinkInternal_id = ParentLoc.linkbaseLinkInternal_id'\
                    +' LEFT JOIN ExtendedLink ChildLoc on preArc.toAttr = ChildLoc.label and preArc.linkbaseLinkInternal_id = ChildLoc.linkbaseLinkInternal_id'\
                    +' LEFT JOIN Concept ChildConcept on ChildConcept.id = ChildLoc.fragment_ID and ChildConcept.currentPath = ChildLoc.searchablePath'\
                    +' LEFT JOIN LinkbaseLink c on ChildLoc.linkbaseLinkInternal_id = c.linkbaseLinkInternal_id'\
                    +' LEFT JOIN Linkbase d on c.linkbaseInternal_id = d.linkbaseInternal_id'\
                    +' LEFT JOIN DocumentHasLinkbase e on d.linkbaseInternal_id = e.linkbaseInternal_id'\
                    +' WHERE preArc.tag = "presentationArc" and ChildLoc.tag= "loc" and ParentLoc.tag = "loc"'\
                    +' and ParentConcept.substitutionGroup = "xbrli:item" and ChildConcept.substitutionGroup = "xbrli:item"'
    cursor_for_SQL.execute(tempQueryText)
    connection_to_Database.commit()

except:
    connection_to_Database.rollback()
    print('Couldn\'t insert into PresentationLinkTreePath table.')
    print(sys.exc_info())

try:
    tableName = 'PresentationLinkTreePath'
    tempAliasCounter    = str(1)
    tempAliasCounterNext= str(int(tempAliasCounter) + 1)
    cursor_for_SQL = connection_to_Database.cursor()
    tempQueryTextSelect = 'SELECT' \
                        + ' t' + tempAliasCounter + '.role' \
                        + ', t' + tempAliasCounter + '.ancestorConcept_id' \
                        + ', t' + tempAliasCounter + '.descendantConcept_id' \
                        + ', t' + tempAliasCounter + '.orderNumber'
    tempQueryTextFrom   = ' FROM ' + tableName + ' t' + tempAliasCounter
    tempQueryTextWhere  = ' WHERE t1.documentSet_id = %s and t1.ancestorConcept_id not in (select distinct descendantConcept_id from PresentationLinkTreePath)'
    tempQueryTextOrder  = ' ORDER BY' \
                        + ' t' + tempAliasCounter + '.role' \
                        + ', t' + tempAliasCounter + '.ancestorConcept_id' \
                        + ', t' + tempAliasCounter + '.orderNumber'

    while True:
        # Join the next 'PresentationLinkTreePath' table
        tempQueryTextSelect +=', t' + tempAliasCounterNext + '.role' \
                            + ', t' + tempAliasCounterNext + '.ancestorConcept_id' \
                            + ', t' + tempAliasCounterNext + '.descendantConcept_id' \
                            + ', t' + tempAliasCounterNext + '.orderNumber'
        tempQueryTextFrom   += ' LEFT JOIN ' + tableName + ' t' + tempAliasCounterNext \
                            + ' ON'  + ' t' + tempAliasCounter + '.descendantConcept_id = t' + tempAliasCounterNext + '.ancestorConcept_id' \
                            + ' AND' + ' t' + tempAliasCounter + '.documentSet_id = t' + tempAliasCounterNext + '.documentSet_id'
        tempQueryTextOrder  +=', t' + tempAliasCounterNext + '.role' \
                            + ', t' + tempAliasCounterNext + '.orderNumber'
        tempQueryText       = tempQueryTextSelect + tempQueryTextFrom + tempQueryTextWhere + tempQueryTextOrder
        valuesForTempQueryText    = [documentSet_idNum]
        cursor_for_SQL.execute(tempQueryText, valuesForTempQueryText)
        resultFromQuery = cursor_for_SQL.fetchall()

        # Check if the result of the query has at least one descendant by joining a new table
        lastColumn = list()
        for result in resultFromQuery:
            lastColumn.append(result[int(tempAliasCounterNext)*3]) # The position of the last column increases by every 3 column
        if lastColumn.count(None) == len(lastColumn):
            print('The number of column is :', tempAliasCounterNext)
            break

        #Save the query that had at least one number in the last column
        tempAliasCounter        = str(int(tempAliasCounter) + 1)
        tempAliasCounterNext    = str(int(tempAliasCounter) + 1)
        resultFromQueryBefore   = resultFromQuery

    ListOfOrderedID = list()
    for resultRow in resultFromQueryBefore:
        numberOfJoinedTable = int(len(resultRow)/4)
        for columenMultiple in range(0, numberOfJoinedTable):
            headerPosition = columenMultiple * 4 # 0, 4, 8, 12
            for columenMultiple_2nd in range(columenMultiple, numberOfJoinedTable): # 0, 4, 8, 12
                eachOrderDictionary = {
                    'role'                          :None
                    ,'ancestorConceptInternal_id'   :None
                    ,'descendantConceptInternal_id' :None
                    ,'deapth'                       :None
                    ,'orderNumber'                  :None
                }
                headerPosition2nd = columenMultiple_2nd * 4
                if resultRow[headerPosition2nd] != None:
                    eachOrderDictionary['role']                         = resultRow[headerPosition]
                    eachOrderDictionary['ancestorConceptInternal_id']   = resultRow[headerPosition+1]
                    eachOrderDictionary['descendantConceptInternal_id'] = resultRow[headerPosition2nd+2]
                    eachOrderDictionary['orderNumber']                  = resultRow[headerPosition2nd+3]
                    eachOrderDictionary['deapth']                       = columenMultiple_2nd
                    ListOfOrderedID.append(eachOrderDictionary)

                else:
                    break

    #print(ListOfOrderedID,len(ListOfOrderedID))

    rowNumberForOrderedID = 0
    for insertID in ListOfOrderedID:
        tempQueryText           = 'INSERT IGNORE INTO PresentationOrder SELECT'\
                                + ' %s, %s, %s, %s, %s, %s, %s;'
        valuesForTempQuery      = [documentSet_idNum,
                                    insertID['role'],
                                    insertID['ancestorConceptInternal_id'],
                                    insertID['descendantConceptInternal_id'],
                                    insertID['orderNumber'],
                                    insertID['deapth'],
                                    rowNumberForOrderedID
                                ]
        rowNumberForOrderedID   += 1
        cursor_for_SQL.execute(tempQueryText, valuesForTempQuery)
    connection_to_Database.commit()

except:
    connection_to_Database.rollback()
    print(sys.exc_info())

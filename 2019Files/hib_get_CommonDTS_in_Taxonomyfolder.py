# -*- coding: utf-8 -*-
import os
import sys
import hib_connectMySQL # connect to MySQL

# Get all the paths of the common DTS files under "taxonomy" folder
commonDTSList = []
for path, subDirectories, fileNames in os.walk('taxonomy'):
    for fileName in fileNames: # by doing this, only the path with file name will be included
        commonDTSList.append(path + '/' + fileName)
print(commonDTSList)

try:
    # Connect to MySQL
    connection_to_Database = hib_connectMySQL.connectToMySQL()
    cursor_for_SQL = connection_to_Database.cursor()
    # Insert the file paths of common DTS
    tableName = 'commonDTS'
    cursor_for_SQL.execute('TRUNCATE TABLE ' + tableName + ';') # Delete all the records before running this
    for commondDTSFilePath in commonDTSList:
        query_to_Insert = 'INSERT INTO ' \
                        + tableName \
                        + ' (filePath) VALUES (%s);'
        cursor_for_SQL.execute(query_to_Insert, commondDTSFilePath)
    connection_to_Database.commit()

except:
    connection_to_Database.rollback()
    print (sys.exc_info())

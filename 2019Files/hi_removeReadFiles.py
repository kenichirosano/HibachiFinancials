import sys

# Get the list of file names that are already read and revmore them from DTS list
def returnOnlyFilesToBeRead(listOfDTS, connection_to_Database):
    try:
        cursorForSQL        = connection_to_Database.cursor()
        tableName           = 'TaxonomySchema'
        sql                 = 'SELECT searchablePath FROM ' + tableName
        cursorForSQL.execute(sql)
        filesAlreadyRead    = cursorForSQL.fetchone()
        connection_to_Database.commit()
        # Check if the file name in DTS list is already parsed before
        # and if so, delete from DTS list
        for fileName in listOfDTS:
            if filesAlreadyRead:
                if fileName in filesAlreadyRead:
                    listOfDTS.remove[fileName]

    except:
        connection_to_Database.rollback()
        print(sys.exc_info(), 'Error occurred in ParsedFiles.')

'''
# Save the file name that are read in the process to SQL permanently
def registerReadFiles(listOfDTS, connection_to_Database):
    try:
        cursorForSQL        = connection_to_Database.cursor()
        tableName           = 'ParsedFiles'
        for fileNameAlreadyRead in listOfDTS:
            sql     = 'INSERT IGNORE INTO ' + tableName \
                    + ' (filename)' \
                    + ' VALUES(%s);'
            values  = [fileNameAlreadyRead]
            cursorForSQL.execute(sql, values)
        connection_to_Database.commit()

    except:
        connection_to_Database.rollback()
        print(sys.exc_info(), 'Error occurred in ParsedFiles.')
*/
'''

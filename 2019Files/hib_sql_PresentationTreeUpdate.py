import os
import sys
import hib_connectMySQL

# Connect to MySQL
connection_to_Database  = hib_connectMySQL.connectToMySQL()
cursor_for_SQL = connection_to_Database.cursor()

tableName = 'CommonPresentationOrder'
#cursor_for_SQL.execute('TRUNCATE TABLE ' + tableName)

insertCommand = 0
selectCommand = 1

if insertCommand == 1:
    try:
        depth        = 0
        affectedRows = 1
        while affectedRows > 0: # keep doing this until no row is affected
            query_to_Insert = 'INSERT INTO ' + tableName + ' '\
                            + 'SELECT '\
                            + 'DISTINCT '\
                            + 'parent.id, ' \
                            + 'child.id, ' \
                            + str(depth +1) + ', ' \
                            + 'child.Extended_orderAttr ' \
                            + 'FROM ( '\
                                + 'SELECT	a.id, '\
        					    + 'linkbaseLink_role, '\
        					    + 'Extended_toAttr '\
        	                    + 'FROM	CommonPresentationOrder	a '\
        	                    + 'JOIN	CommonPresentationArc		b '\
        	                    + 'ON		a.id = b.id '\
                                + 'WHERE a.depth = ' + str(depth) + ' '\
                            + ') parent '\
                            + 'JOIN CommonPresentationArc child '\
                            + 'ON   parent.linkbaseLink_role = child.linkbaseLink_role '\
                            + 'AND  parent.Extended_toAttr 	 = child.Extended_fromAttr;'
            affectedRows = cursor_for_SQL.execute(query_to_Insert) # execute and get the number of affected rows
            depth += 1 # increase the depth
            connection_to_Database.commit()

    except:
        connection_to_Database.rollback()
        print (sys.exc_info(),sys.exc_info()[0],'Depth is',depth)

# Show the presentation order by adding the maximum depth
if selectCommand == 1:
    try:
        getMaxQuery     = 'SELECT max(depth) FROM ' + tableName + ';'
        cursor_for_SQL.execute(getMaxQuery)
        maxDepth        = cursor_for_SQL.fetchall()[0][0]
        query_to_Insert = 'SELECT '\
                        + 'DISTINCT '\
        # list all the columns to show
        query_to_Insert = query_to_Insert\
                        + 'child0.id'\
                        + ',child0.depth'\
                        + ',child0.orderNo '
        for depth in range(1, maxDepth + 1):
            query_to_Insert = query_to_Insert\
                            + ',child'+ str(depth)+'.id'\
                            + ',child'+ str(depth)+'.depth '\
                            + ',child'+ str(depth)+'.orderNo '
        query_to_Insert = query_to_Insert\
                        + 'FROM ' + tableName + ' child0 '\
        # list all tables to join
        for depth in range(1, maxDepth + 1):
            query_to_Insert = query_to_Insert\
                            + 'LEFT JOIN ' + tableName + ' child' + str(depth) + ' '\
                            + 'ON child' + str(depth-1) + '.id ' + '=' + ' child' + str(depth) + '.parent_id ' #child0.id = child2.parent_id
        query_to_Insert = query_to_Insert\
                        + 'WHERE child0.depth = 0 '
        # list all conditions of where
        for depth in range(1, maxDepth + 1):
            query_to_Insert = query_to_Insert\
                            + 'AND ' + 'child' + str(depth)+'.depth = ' + str(depth) + ' '      # AND child1.depth = 1
        query_to_Insert = query_to_Insert\
                        + 'ORDER BY child0.orderNo'
        # orders
        for depth in range(1, maxDepth + 1):
            query_to_Insert = query_to_Insert\
                            + ', child' + str(depth)+'.orderNo'
        query_to_Insert = query_to_Insert\
                        + ';'
        cursor_for_SQL.execute(query_to_Insert) # execute and get the number of affected rows
        print(query_to_Insert)
        queryResults = cursor_for_SQL.fetchall()
        print(queryResults)
        for record in queryResults:
            print(record)
        connection_to_Database.commit()

    except:
        connection_to_Database.rollback()
        print(query_to_Insert)
        print (sys.exc_info(),sys.exc_info()[0],maxDepth)

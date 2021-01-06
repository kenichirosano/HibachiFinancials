# -*- coding: utf-8 -*-
# Pull all the file pathes from PotgreSQL
from config import config
import psycopg2 # Connector to Postgres
import pandas as pd

# Create the conenction and select all the file pathes
def generalDTSPathes():
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)
        
        sqlquery = 'SELECT * FROM filelist_dts'
        return pd.read_sql_query(sqlquery, connection)
        
    except (Exception, psycopg2.Error) as error:
        raise(error)
        
    finally:
        # Close the database connection
        if(connection):
            try:
                #cursor.close()
                connection.close()
                print("Connection is closed.")
            except (Exception, psycopg2.Error) as error:
                raise(error)

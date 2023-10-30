import pymysql  # To handle MySQL

def connectToMySQL():
    connection_to_Database = pymysql.connect(
        host        = "localhost"
        ,user       = "root"
        ,passwd     = "stufsno1"
        ,db         = "financials"
        ,use_unicode= True
        ,charset    = "utf8"
    )
    return connection_to_Database

import pandas as pd
import pyodbc


'''
Supporting functions
'''


def connectdb(config):
    # Connect
    if config['ts_localpush_bool']:
        db_conn_server = config['localserver']
        db_conn_database = config['localdatabase']
        db_conn_driver = '{ODBC Driver 17 for SQL Server}'
        conn = pyodbc.connect('DRIVER=' + db_conn_driver +
                              ';SERVER=' + db_conn_server +
                              ';DATABASE=' + db_conn_database +
                              ';Trusted_Connection=yes;')
    else:
        db_conn_server = config['azureserver']
        db_conn_database = config['azuredatabase']
        db_conn_username = config['azureusername']
        db_conn_password = '{' + config['azurepassword'] + '}'
        db_conn_driver = '{ODBC Driver 17 for SQL Server}'
        conn = pyodbc.connect('DRIVER=' + db_conn_driver +
                              ';SERVER=tcp:' + db_conn_server +
                              ';PORT=1433' +
                              ';DATABASE=' + db_conn_database +
                              ';UID=' + db_conn_username +
                              ';PWD=' + db_conn_password)
        conn.timeout = 0
    cursor = conn.cursor()
    return cursor, conn

def disconnectdb(cursor, conn):
    cursor.close()
    conn.close()



''''
Get column information

'''

def getcolumnnames(cursor, tablename, schema):
    query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '%s' AND TABLE_NAME = '%s'" % (schema, tablename)
    cursor.execute(query)
    tablecol = [i[0] for i in cursor.fetchall()]
    return tablecol


def getcolumntypes(cursor, tablename, schema):
    query = "SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '%s' AND TABLE_NAME = '%s'" % (schema, tablename)
    cursor.execute(query)
    tablecoltype = [i[0] for i in cursor.fetchall()]
    return tablecoltype


'''
Push queries

'''

def pushquery(cursor, dataframe, tablename, schema, tablecol):
    # Prep dynamic query
    COLUMN_query = '{0}{1}{2}'.format("( ", ", ".join(tablecol), " )")
    VALUES_query = '{0}{1}{2}'.format("( ", ", ".join(["?" for i in range(0, len(dataframe.columns))]), " )")
    TABLE_COLUMNS = '%s.%s %s' % (schema, tablename, COLUMN_query)
    query = f"INSERT INTO {TABLE_COLUMNS} VALUES %s" % VALUES_query
    # Commit dynamic query
    cursor.setinputsizes([(pyodbc.SQL_WVARCHAR, 0, 0)])
    cursor.fast_executemany = True
    cursor.executemany(query, dataframe.values.tolist())
    cursor.commit()





'''
Run

'''


def runpush(config, tablename, schema, dataframe):
    # Prepare connection
    cursor, conn = connectdb(config)


    # Get DB columns names
    tablecol = getcolumnnames(cursor, tablename, schema)

    # Test that the width of the df correspond to the target table
    assert \
        len(tablecol) == len(dataframe.columns), \
        "The number of columns between the target DB table (%i) " \
        "and dataframe (%i) to push does not match." \
        % (len(tablecol), len(dataframe.columns))


    # Connect and push the data
    pushquery(cursor, dataframe, tablename, schema, tablecol)

    # Disconnect
    disconnectdb(cursor, conn)

    print(f'{len(dataframe)} rows inserted in the {tablename} table')





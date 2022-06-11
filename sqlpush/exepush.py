'''
Install requirements:
- pandas
- pyodbc
'''


import pandas as pd
from config import *
import sqlstd


def looppush(config, tables_dict):
    for table in tables_dict:  # this loops across the different tables you would like to push to
        print("Process for table", tables_dict[table]['TableName'], "in database", config['localdatabase'], "on server", args.localserver, ": started.")
        i = 0
        while i < len(tables_dict[table]['Dataframe']):  # this loop is used for the batch size
            print("Rows %i to %i for %s being processed. Total table length is %i" % (i, min(i+config['batchsize'], len(tables_dict[table]['Dataframe'])), table, len(tables_dict[table]['Dataframe'])))
            # Prepare function arguments
            tablename = tables_dict[table]['TableName']
            schema = tables_dict[table]['Schema']
            dataframe = tables_dict[table]['Dataframe'].iloc[i:min(i+config['batchsize'],len(tables_dict[table]['Dataframe'])) , :].copy(deep=True)
            # Prepare dataframe format
            dataframe = dataframe.astype(object).where(pd.notnull(dataframe), None)
            # Run push
            sqlstd.runpush(config, tablename, schema, dataframe)
            # Increment for batch
            i += config['batchsize']
        print("Push successfully executed for table", tables_dict[table]['TableName'], ".")


# Get dataframe(s) to be pushed
df = pd.read_csv(inputfilepath, index_col=None, encoding="ISO-8859-1", low_memory=False)

# Specify database structure and associated input data dataframe
tables_dict = {'belgiumaddresses': {  # arbitrary name for the table to push to
                    'TableName': 'belgium_addresses',  # database table name
                    'Schema': 'dbo',  # database table schema, ex: 'dwh', 'temp', 'prod'...
                    'Dataframe': df
                    }}

# Run push
looppush(config, tables_dict)


'''
Install requirements:
- pandas
- pyodbc
'''

import pandas as pd
from config import *
import sqlstd
from add_flood_factor import *


def looppush(config, tables_dict):
    for table in tables_dict:  # this loops across the different tables you would like to push to
        print("\nProcess for table", tables_dict[table]['TableName'], "in database", config['localdatabase'], "on server", args.localserver, ": started.")
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
# addresses
print("Importing all belgian addresses...")
df = pd.read_csv(inputfilepath, index_col=None, encoding="ISO-8859-1", low_memory=False).drop('address_id', axis = 1)
print(f"{len(df)} rows imported")
df = df.drop_duplicates()
print(f"{len(df)} unique addresses")
df["address_id"] = [i for i in range(1, len(df) +1)]
df = df[['address_id', 'EPSG:31370_x', 'EPSG:31370_y', 'EPSG:4326_lat', 'EPSG:4326_lon',
         'box_number', 'house_number', 'municipality_id', 'municipality_name_de',
         'municipality_name_fr', 'municipality_name_nl', 'postcode',
         'postname_fr', 'postname_nl', 'street_id', 'streetname_de',
         'streetname_fr', 'streetname_nl', 'region_code', 'status']]

# flooding risks
df_risk = add_risk_factor(df)
df_risk = df_risk[['address_id', 'risk_level', 'alea_type', 'map_object_id', 'map_local_id', 'map_src_file']] 

# Specify database structure and associated input data dataframe
tables_dict = {'belgiumaddresses': {  # arbitrary name for the table to push to
                    'TableName': 'belgium_addresses',  # database table name
                    'Schema': 'dbo',  # database table schema, ex: 'dwh', 'temp', 'prod'...
                    'Dataframe': df
                    },
               'flooding_risk': {  # arbitrary name for the table to push to
                    'TableName': 'flooding_risk',  # database table name
                    'Schema': 'dbo',  # database table schema, ex: 'dwh', 'temp', 'prod'...
                    'Dataframe': df_risk
                    }}

# Run push
looppush(config, tables_dict)


import argparse

config = {}

parser = argparse.ArgumentParser()
parser.add_argument('localserver', type=str)
parser.add_argument('localdatabase', type=str)
parser.add_argument('inputfilepath', type=str)
#args = parser.parse_args()

# Settings for local filepath
inputfilepath = 'belgium_addresses.csv'

# Push types
config['batchsize'] = 500000  # batch size of data pushed (number of rows), reduce to avoid database timeout error
config['ts_localpush_bool'] = True  # False to push to cloud database, True to push to local SQL Server

# Settings local database for SQL Server
config.update({'localserver': "BE3097427W2",
               'localdatabase': 'Flood_factor'})

# Settings cloud database
config.update({'azureserver': 'myserver',
               'azuredatabase': 'mydatabase',
               'azureusername': 'myusername',
               'azurepassword': 'mypassword'})




import argparse

config = {}

# Settings for local filepath
inputfilepath = "belgium_addresses.csv"
floodingmap = "BE_flooding_map.zip"

# name of the coordinates columns
x_coordinate = "EPSG:31370_x"
y_coordinate = "EPSG:31370_y"

# coordinates system used in flooding risk map
crs = "EPSG:31370"

# Push types
config['batchsize'] = 500000  # batch size of data pushed (number of rows), reduce to avoid database timeout error
config['ts_localpush_bool'] = True  # False to push to cloud database, True to push to local SQL Server

# Settings local database for SQL Server
parser = argparse.ArgumentParser()
parser.add_argument('localserver', type=str)
args = parser.parse_args()
config.update({'localserver': args.localserver,
               'localdatabase': 'Flood_factor'})

# Settings cloud database
config.update({'azureserver': 'myserver',
               'azuredatabase': 'mydatabase',
               'azureusername': 'myusername',
               'azurepassword': 'mypassword'})




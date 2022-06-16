import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
from config import *
from sqlstd import connectdb
import os


def add_risk_factor() :
    data_folder = os.path.abspath(os.path.join(os.path.join(os.getcwd(), ".."), "data"))
    print("Load flooding map...")
    risk_map = gpd.read_file(os.path.join(data_folder, 'BE_flooding_map.zip'))

    # get addresses from database
    df_addresses = pd.read_sql_query('SELECT EPSG_31370_x, EPSG_31370_y, address_id, region_code FROM dbo.belgium_addresses', con = conn)
    print(f"{len(df_addresses)} rows imported from database")
    
    crs = 'EPSG:31370' # coordinate reference system used
    geometry = [Point(xy) for xy in zip(df_addresses['EPSG_31370_x'], df_addresses['EPSG_31370_y'])]
    gdf = gpd.GeoDataFrame(df_addresses, crs = crs, geometry = geometry)

    # join addresses to flooding risk map
    # find points with flooding risks
    risk_gdf = gpd.sjoin(gdf, risk_map, op = "within") # return only points in flooding map
    print(f"{len(risk_gdf)} addresses in flooding risk zones")
    
    # merge the result to the initial dataframe
    res = pd.merge(gdf, risk_gdf[['EPSG_31370_x', 'EPSG_31370_y', 'address_id', 'region_code',
                                  'RISK_LEVEL', 'TYPEALEA', "OBJECTID", "LOCALID", "TYPEALEA", 'src_file']],
                   on = ['EPSG_31370_x', 'EPSG_31370_y'], how = 'left')
    res.RISK_LEVEL = res.RISK_LEVEL.fillna("No risk")
    print(f"{len(res)} rows returned after join")

    # push the resulting data into the database
    # to do

    return df_addresses, res

    
if __name__ == "__main__" :

    cursor, conn = connectdb(config) # done only once in final script

    df_addresses, res = add_risk_factor()
    

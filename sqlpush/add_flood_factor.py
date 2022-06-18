import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
from config import *


    
def add_risk_factor(df_addresses) :
    print("\nImporting flooding risk map...")
    risk_map = gpd.read_file(floodingmap)
   
    geometry = [Point(xy) for xy in zip(df_addresses[x_coordinate], df_addresses[y_coordinate])]
    gdf = gpd.GeoDataFrame(df_addresses, crs = crs, geometry = geometry)

    # join addresses to flooding risk map
    # find points with flooding risks
    print("Joining risk map to addresses...")
    print(f"{len(gdf)} addresses in geodataframe")
    risk_gdf = gpd.sjoin(gdf, risk_map, op = "within") # return only points in flooding map
    print(f"{len(risk_gdf)} addresses in flooding risk zones")
    risk_gdf = risk_gdf[[x_coordinate, y_coordinate, 'RISK_LEVEL', 'TYPEALEA', "OBJECTID", "LOCALID", 'src_file']]
    risk_gdf.columns = [x_coordinate, y_coordinate, 'risk_level', 'alea_type', "map_object_id", "map_local_id", 'map_src_file']
    
    # merge the result to the initial dataframe
    res = pd.merge(gdf, risk_gdf,
                   on = [x_coordinate, y_coordinate], how = 'left')
    res.risk_level = res.risk_level.fillna("No risk")
    res = res.drop("geometry", axis = 1)
    
    print(f"{len(res)} rows returned after join")

    return res

    
if __name__ == "__main__" :
    from sqlstd import connectdb
    import os

    cursor, conn = connectdb(config) # done only once in final script
    data_folder = os.path.abspath(os.path.join(os.path.join(os.getcwd(), ".."), "data"))
    print("Load flooding map...")

    # get addresses from database
    df_addresses = pd.read_sql_query('SELECT * FROM dbo.belgium_addresses', con = conn)

    res = add_risk_factor(df_addresses)
    

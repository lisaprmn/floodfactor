import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
from config import *


    
def add_risk_factor(df_addresses) :
    print("\nImporting flooding risk map...")
    risk_map = gpd.read_file(floodingmap)

    # import addresses
    # for some rows, the x, y coordinates are missing -> sepzarate in different dataframes
    df_ok = df_addresses[df_addresses[x_coordinate] != 0]
    print(f"{len(df_ok)} rows with correct coordinates")
    geometry = [Point(xy) for xy in zip(df_ok[x_coordinate], df_ok[y_coordinate])]
    gdf_ok = gpd.GeoDataFrame(df_ok, crs = crs, geometry = geometry)

    # for the other rows, take the latitude and longitude and reproject in right coordinates system
    df_lon_lat = df_addresses[df_addresses[x_coordinate] == 0]
    print(f"{len(df_lon_lat)} rows without {crs} coordinates. use longitude and latitude instead")
    geometry = [Point(xy) for xy in zip(df_lon_lat['EPSG:4326_lon'], df_lon_lat['EPSG:4326_lat'])]
    gdf_lon_lat = gpd.GeoDataFrame(df_lon_lat, crs = "EPSG:4326", geometry = geometry).to_crs(crs)

    # append geodataframes together
    gdf = pd.concat([gdf_ok, gdf_lon_lat], axis = 0)

    # join addresses to flooding risk map
    # find points with flooding risks
    print("Joining risk map to addresses...")
    print(f"{len(gdf)} addresses in geodataframe")
    risk_gdf = gpd.sjoin(gdf, risk_map, op = "within") # returns only points in flooding map
    print(f"{len(risk_gdf)} addresses in flooding risk zones")
    risk_gdf = risk_gdf[[x_coordinate, y_coordinate, 'RISK_LEVEL', 'TYPEALEA', "OBJECTID", "LOCALID", 'src_file']]
    risk_gdf.columns = [x_coordinate, y_coordinate, 'risk_level', 'alea_type', "map_object_id", "map_local_id", 'map_src_file']
    
    # merge the result to the initial dataframe
    res = pd.merge(gdf, risk_gdf,
                   on = [x_coordinate, y_coordinate], how = 'left')
    res.risk_level = res.risk_level.fillna("No risk")
    
    print(f"{len(res)} rows returned after join")

    return res

    
if __name__ == "__main__" :
    from sqlstd import connectdb
    import os

    data_folder = os.path.abspath(os.path.join(os.path.join(os.getcwd(), ".."), "data"))
    print("Load flooding map...")

    # get addresses
    df_addresses = pd.read_csv(inputfilepath, index_col=None, encoding="ISO-8859-1", low_memory=False).drop('address_id', axis = 1)

    res = add_risk_factor(df_addresses)
    

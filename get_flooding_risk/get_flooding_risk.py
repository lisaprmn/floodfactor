import geopandas as gpd
from shapely.geometry import Point, Polygon
import pandas as pd
import os


def add_risk_to_df(df, risk_map) :
    # add geometry
    crs = 'EPSG:4326' # coordinate reference system used for lon / lat
    geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
    gdf = gpd.GeoDataFrame(df, crs = crs, geometry = geometry)
    
    # put in coordinates system used by belgian maps
    gdf = gdf.to_crs(epsg = 31370)

    # find points with flooding risks
    risk_gdf = gpd.sjoin(gdf, risk_map, op = "within") # return only points in flooding map

    # merge the result to the initial dataframe
    res = pd.merge(gdf, risk_gdf[['lat', 'lon', 'FLOOD_RISK', 'TYPEALEA', 'src_file']], on = ['lat', 'lon'], how = 'left')
    test.FLOOD_RISK = test.FLOOD_RISK.fillna("No risk")
    
    return res, risk_gdf


def get_risk_from_coordinates(lat, lon, risk_map) :
    print(f"\nadd flood factor for lat: {lat}, lon: {lon}")
    df = pd.DataFrame([[lat, lon]], columns = ["lat", "lon"])
    gdf, risk_gdf = add_risk_to_df(df, risk_map)

    if len(risk_gdf) == 0:
        risk = "No risk"
    else:
        risk = "Flooding Risk"

    print(risk)

    return gdf, risk


if __name__ == "__main__" :
    # a few tests on the functions above:
    
    data_folder = os.path.abspath(os.path.join(os.path.join(os.getcwd(), ".."), "data"))
    flooding_map = gpd.read_file(os.path.join(data_folder, 'BE_flooding_map.zip'))

    # single address: give coordinates
    lat = 50.85015136702573
    lon = 4.339041499920154

    gdf_1_point, gdf_1_point_risk, risk_1_point = get_risk_from_coordinates(lat, lon, flooding_map)
    print("geometries df:", gdf_1_point)

    # multiple addresses: give a dataframe with coordinates in columns 'lat' and 'lon'
    df = pd.DataFrame([[50.85015136702573, 4.339041499920154],
                       [51.194859, 4.344027],
                       [51.067459, 4.184039],
                       [50.921634, 4.704236]], columns = ["lat", "lon"])
    
    gdf, risk_gdf = add_risk_to_df(df, flooding_map)

import geopandas as gpd
import pandas as pd
import os


def add_risk_to_df(df, risk_map) :
    # add geometry
    gdf = gpd.GeoDataFrame(df)
    
    # put in right coordinates system
    gdf["geometry"] = gpd.points_from_xy(df.lat, df.lon, z = None, crs = None)

    # link to risk map
    risk_gdf = gpd.sjoin(gdf, risk_map, op = "within")
    
    return gdf, risk_gdf


def get_risk_from_coordinates(lat, lon, risk_map) :
    print(f"\nadd flood factor for lat: {lat}, lon: {lon}")
    df = pd.DataFrame([[lat, lon]], columns = ["lat", "lon"])
    gdf, risk_gdf = add_risk(df, risk_map)

    if len(risk_gdf) == 0:
        risk = "No risk"
    else:
        risk = "Flooding Risk"

    print(risk)

    return gdf, risk_gdf, risk


if __name__ == "__main__" :
    data_folder = os.path.abspath(os.path.join(os.path.join(os.getcwd(), ".."), "data"))
    flooding_map = gpd.read_file(os.path.join(data_folder, 'BE_flooding_map.zip'))

    # single address: give coordinates
    lat = 50.85015136702573
    lon = 4.339041499920154

    gdf_1_point, gdf_1_point_risk, risk_1_point = get_risk_from_coordinates(lat, lon, flooding_map)
    print("geometries df:", gdf_1_point)
    print("risk:", gdf_1_point_risk)

    # multiple addresses: give a dataframe with coordinates in columns 'lat' and 'lon'
    lat = [50.85015136702573]
    df = pd.DataFrame([[lat, lon]], columns = ["lat", "lon"])

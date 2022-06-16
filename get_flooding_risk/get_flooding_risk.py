import geopandas as gpd
from shapely.geometry import Point, Polygon
import pandas as pd
import os


def add_risk_to_df(df, risk_map) :
    # add geometry
    crs = 'EPSG:31370' # coordinate reference system used for lon / lat
    geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
    gdf = gpd.GeoDataFrame(df, crs = crs, geometry = geometry)

    # find points with flooding risks
    risk_gdf = gpd.sjoin(gdf, risk_map, op = "within") # return only points in flooding map

    # merge the result to the initial dataframe
    res = pd.merge(gdf, risk_gdf[['lat', 'lon', 'FLOOD_RISK', 'TYPEALEA', 'src_file']], on = ['lat', 'lon'], how = 'left')
    res.FLOOD_RISK = res.FLOOD_RISK.fillna("No risk")
    
    return res, risk_gdf


def plot_map_points_at_risk(flooding_map, risk_gdf, title, img_name) :
    print("\nPreparing map...")
    # append both geodataframes together
    res = pd.merge(flooding_map[[]], risk_gdf[['FLOOD_RISK', 'TYPEALEA', 'geometry', 'src_file']])
    
    # need to find out here how to use the RGB column without making the legend disappear
    gdf.plot(figsize = (24, 16), column = gdf.FLOOD_RISK, label = gdf.FLOOD_RISK, legend = True)
    plt.xlabel(gdf.crs.axis_info[0].name + ', ' + gdf.crs.axis_info[0].unit_auth_code + " - " + gdf.crs.axis_info[0].unit_name)
    plt.ylabel(gdf.crs.axis_info[1].name + ', ' + gdf.crs.axis_info[1].unit_auth_code + " - " + gdf.crs.axis_info[1].unit_name)
    plt.title(title)

    img_name = os.path.join(img_folder, img_name)
    plt.savefig(img_name)
    print(f"\nMap saved to {img_name}")
    #plt.show()


if __name__ == "__main__" :
    # a few tests on the functions above:
    
    data_folder = os.path.abspath(os.path.join(os.path.join(os.getcwd(), ".."), "data"))
    flooding_map = gpd.read_file(os.path.join(data_folder, 'BE_flooding_map.zip'))

    # single address: give coordinates
    # lat = 50.85015136702573
    # lon = 4.339041499920154

    # gdf_1_point, risk_1_point = get_risk_from_coordinates(lat, lon, flooding_map)
    # print("geometries df:", gdf_1_point)

    # multiple addresses: give a dataframe with coordinates in columns 'lat' and 'lon'
    """
    df = pd.DataFrame([[50.85015136702573, 4.339041499920154],
                       [51.194859, 4.344027],
                       [51.067459, 4.184039],
                       [50.921634, 4.704236]], columns = ["lat", "lon"])
    
    gdf, risk_gdf = add_risk_to_df(df, flooding_map)
    print(risk_gdf)
    """

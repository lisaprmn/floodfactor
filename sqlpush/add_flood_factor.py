import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
from config import *
from datetime import datetime as DT


    
def add_risk_factor(df_addresses, plot_addresses = False) :
    """
    add the risk factor from the map to a dataframe containing coordinate columns
    input: the dataframe with coordinates
    config: name of the coordinate columns, geographical referential used
    """
    
    print(f"\n{DT.now()} - Import flooding risk map")
    risk_map = gpd.read_file(floodingmap)

    # import addresses
    # for some rows, the x, y coordinates are missing -> sepzarate in different dataframes
    df_ok = df_addresses[df_addresses[x_coordinate] != 0]
    print(f"{len(df_ok)} rows with {crs} coordinates")
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
    print(f"\n{DT.now()} - Join risk map to addresses...")
    print(f"{len(gdf)} addresses in geodataframe")
    risk_gdf = gpd.sjoin(gdf, risk_map, op = "within") # returns only points in flooding map
    risk_gdf = risk_gdf[[x_coordinate, y_coordinate, 'RISK_LEVEL', 'TYPEALEA', "OBJECTID", "LOCALID", 'src_file']]
    risk_gdf.columns = [x_coordinate, y_coordinate, 'risk_level', 'alea_type', "map_object_id", "map_local_id", 'map_src_file']
    
    # merge the result to the initial dataframe
    res = pd.merge(gdf, risk_gdf,
                   on = [x_coordinate, y_coordinate], how = 'left').drop_duplicates()
    res.risk_level = res.risk_level.fillna("no risk")
    
    print(f"{len(res)} rows returned after joining with flooding risk map:")
    print(res.risk_level.value_counts())

    # plot the addresses, colored ny risk level
    if plot_addresses == True :
        from matplotlib import pyplot as plt
        print(f"\n{DT.now()} - Plot addresses map")
        # need to find out here how to use the RGB column without making the legend disappear
        res.plot(figsize = (24, 16), column = res.risk_level, label = res.risk_level, legend = True)
        plt.xlabel(res.crs.axis_info[0].name + ', ' + res.crs.axis_info[0].unit_auth_code + " - " + res.crs.axis_info[0].unit_name)
        plt.ylabel(res.crs.axis_info[1].name + ', ' + res.crs.axis_info[1].unit_auth_code + " - " + res.crs.axis_info[1].unit_name)
        plt.title("Addresses in database colored by risk level")

        img_name = os.path.join(img_folder, "addresses.png")
        plt.savefig(img_name)
        print(f"\nMap saved to {img_name}")
        #plt.show()

    return res


def get_risk_from_coordinates(lon, lat, plot_map = False) :

    # import flooding risk map
    print(f"\n{DT.now()} - Import flooding risk map")
    risk_map = gpd.read_file(floodingmap)

    # convert coordinates to belgian system
    df = pd.DataFrame([[lat, lon]], columns = ['lat', 'lon'])
    geometry = [Point(xy) for xy in zip(df.lon, df.lat)]
    gdf = gpd.GeoDataFrame(df, crs = "EPSG:4326", geometry = geometry).to_crs(crs)
    
    # search on the map
    risk_gdf = gpd.sjoin(gdf, risk_map, op = "within")

    res = ""
    if len(risk_gdf) == 0 :
        res = "no risk" # no shape found in risk map
    else :
        alea = risk_gdf.TYPEALEA.values[0]
        lvl = risk_gdf.RISK_LEVEL.values[0]
        res = f"{lvl} risk"

        if len(alea) > 1 :
            res = f"{lvl} risk of type: {alea}"
            
    return gdf, risk_gdf, res



if __name__ == "__main__" :
    from sqlstd import connectdb
    import os

    lat = 50.850164895152545
    lon = 4.3390629560555265

    # gdf, risk_gdf, res = get_risk_from_coordinates(lon, lat, plot_map = False)
    
    # get addresses
    df_addresses = pd.read_csv(inputfilepath, index_col=None, encoding="ISO-8859-1", low_memory=False).drop('address_id', axis = 1)

    res = add_risk_factor(df_addresses, plot_addresses = True)
    

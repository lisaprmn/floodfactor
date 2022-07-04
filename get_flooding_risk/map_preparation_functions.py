import os
import shutil
import tempfile
from pathlib import Path
import pandas as pd
import numpy as np
import geopandas as gpd
from matplotlib import pyplot as plt
from config import *



def import_maps(folder) :
    """
    a function that imports all map files in a folder and append them together
    the files must be either shapefiles or other in a geographical data format, readable by geopandas
    """
    
    print(f"\nImport data from {folder}")
    res = gpd.GeoDataFrame()
    for root, dirs, files in os.walk(folder):
        for file_name in files:
            file_path = os.path.join(folder, file_name)
            flood_map = gpd.read_file(file_path)
            flood_map['src_file'] = file_name
            print(f"\ncolumns available for {file_name}")
            print(list(flood_map.columns))

            res = pd.concat([res, flood_map], axis = 0)
    return res


def plot_map(gdf, title, img_name, show_image = False) :
    """
    a function to plot a geodataframe
    the coordinates are given in column "geometry" (default geopandas behavior)
    the map takes a long time to be plotted
    """
    print("\nPreparing map...")
    # need to find out here how to use the RGB column without making the legend disappear
    gdf.plot(figsize = (24, 16), column = gdf.RISK_LEVEL, label = gdf.RISK_LEVEL, legend = True)
    plt.xlabel(gdf.crs.axis_info[0].name + ', ' + gdf.crs.axis_info[0].unit_auth_code + " - " + gdf.crs.axis_info[0].unit_name)
    plt.ylabel(gdf.crs.axis_info[1].name + ', ' + gdf.crs.axis_info[1].unit_auth_code + " - " + gdf.crs.axis_info[1].unit_name)
    plt.title(title)

    img_name = os.path.join(img_folder, img_name)
    plt.savefig(img_name)
    print(f"\nMap saved to {img_name}")

    if show_image == True :
        plt.show()



def export_map(input_map, output_file_name) :

    file_path = os.path.join(data_folder, 'output_file_name')
    print(f"\nDataset being saved to {file_path}...")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        print(f"outputting in temp directory {temp_dir}")
        input_map.drop(labels = ["RGB"], axis = 1).to_file(filename = temp_dir, driver = 'ESRI Shapefile')
        archiveFile = shutil.make_archive(file_path, 'zip', temp_dir)
        shutil.rmtree(temp_dir)


def map_wallonia() :
    """
    import the 5 files for Wallonia
    append files together
    """
    
    print("\nImport data for Wallonia")
    ALEA_Wallonie_folder = os.path.join(data_folder, "Wallonie", "ALEA_Wallonie")

    Wallonie_ALEA_map = import_maps(ALEA_Wallonie_folder)
    Wallonie_ALEA_map.RGB = Wallonie_ALEA_map.RGB.apply(lambda x: tuple(np.array(x.split(",")).astype(float)/255))

    # print some info
    print(f"\nCoordinates system used\n{Wallonie_ALEA_map.crs.to_string}")
    print(f"\n---- CODEALEA\n{Wallonie_ALEA_map[['CODEALEA', 'VALEUR', 'RGB']].value_counts()}")
    print(f"\n---- TYPEALEA\n{Wallonie_ALEA_map.TYPEALEA.value_counts()}")
    print(f"\n---- CLASSEMENT\n{Wallonie_ALEA_map.CLASSEMENT.value_counts()}")
    print(f"\n---- STATUS\n{Wallonie_ALEA_map.STATUS.value_counts()}")
    print(f"\n---- DECISION\n{Wallonie_ALEA_map.DECISION.value_counts()}")
    print(f"\n---- MILLESIME\n{Wallonie_ALEA_map.MILLESIME.value_counts()}")

    # select and rename relevant columns for Wallonia
    WALLONIE_selection = Wallonie_ALEA_map[["OBJECTID", "LOCALID", "TYPEALEA", "VALEUR", "RGB", "geometry", "src_file"]]
    WALLONIE_selection.columns = ["OBJECTID", "LOCALID", "TYPEALEA", "RISK_LEVEL", "RGB", "geometry", "src_file"]

    return WALLONIE_selection




def map_flanders() :
    
    print("\nImport data for Flanders")
    VLAANDEREN_Overstromingsgevoelige_gebieden_2017_file = os.path.join(data_folder, "Vlaanderen", "Overstromingsgevoelige_gebieden_2017_(Watertoets)_correctie_13_07_2017_GewVLA_Shape", "shapefile")
    VLAANDEREN_Overstromingsgevoelige_gebieden_2017 = gpd.read_file(VLAANDEREN_Overstromingsgevoelige_gebieden_2017_file)
    VLAANDEREN_Overstromingsgevoelige_gebieden_2017["src_file"] = "Overstromingsgevoelige_gebieden_2017_(Watertoets)_correctie_13_07_2017_GewVLA_Shape"

    # print some info
    print(f"\nCoordinates system used\n{VLAANDEREN_Overstromingsgevoelige_gebieden_2017.crs.to_string}")
    print(f"\n---- EFFECTIVE vs. POSSIBLE DANGER\n{VLAANDEREN_Overstromingsgevoelige_gebieden_2017[['OVSTRGV', 'LBLOVSTRGV', 'DEFOVSTRGV']].value_counts()}")
    dic = {1 : (0.2, 0.2, 0.2),
           2 : (0.6, 0.6, 0.6)}
    VLAANDEREN_Overstromingsgevoelige_gebieden_2017["RGB"] = VLAANDEREN_Overstromingsgevoelige_gebieden_2017.OVSTRGV.map(dic)

    # select and rename relevant columns for Flanders
    VLAANDEREN_selection = VLAANDEREN_Overstromingsgevoelige_gebieden_2017[["OIDN", "UIDN", "DEFOVSTRGV", "RGB", "geometry", "src_file"]]
    VLAANDEREN_selection.columns = ["OBJECTID", "LOCALID", "RISK_LEVEL", "RGB", "geometry", "src_file"]

    return VLAANDEREN_selection

def map_brussels() :
    print("import data for Brussels")
    bxl_file = os.path.join(data_folder, "Brussels", "NaturalRiskZones_HazardArea.gml")
    bxl_map = gpd.read_file(bxl_file)
    bxl_map['src_file'] = "NaturalRiskZones_HazardArea.gml"

    for c in ['description', 'beginLifeSpanVersion', 'determinationMethod', 'namespace', 'likelihoodOfOccurrence', 'magnitudeOrIntensity'] :
        print(f"\n--> values for column {c}:")
        print(bxl_map[c].value_counts())

    return bxl_map


if __name__ == "__main__" :
    # WALLONIE_selection = map_wallonia()
    # VLAANDEREN_selection = map_flanders()
    bxl_map = map_brussels()

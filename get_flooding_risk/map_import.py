import os
import shutil
import tempfile
from pathlib import Path
import pandas as pd
import geopandas as gpd
import numpy as np
from matplotlib import pyplot as plt


data_folder = os.path.abspath(os.path.join(os.path.join(os.getcwd(), ".."), "data"))
img_folder = os.path.abspath(os.path.join(os.path.join(os.getcwd(), ".."), "img"))


# WALLONIA
print("\nImport data for Wallonia")
ALEA_Wallonie_folder = os.path.join(data_folder, "Wallonie", "ALEA_Wallonie")

def import_maps(folder) :
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


# FLANDERS
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

#VLAANDEREN_Overstromingsgebieden_2020_file = os.path.join(data_folder, "Vlaanderen", "Overstromingsgebieden_en_oeverzones_2020_01_GewVLA_Shapefile", "shapefile")
#VLAANDEREN_Overstromingsgebieden_2020 = gpd.read_file(VLAANDEREN_Overstromingsgebieden_2020_file)


# put all datasets together (the choice of input dataset can vary)
# keep only "common" columns
print("\nPut all data on one map")

# select and rename relevant columns for Wallonia
WALLONIE_selecion = Wallonie_ALEA_map[["OBJECTID", "LOCALID", "TYPEALEA", "CODEALEA", "VALEUR", "RGB", "geometry", "src_file"]]
WALLONIE_selecion.loc[:, "FLOOD_RISK"] = WALLONIE_selecion.loc[:, "VALEUR"]

# select and rename relevant columns for Flanders
VLAANDEREN_selection = VLAANDEREN_Overstromingsgevoelige_gebieden_2017[["OIDN", "UIDN", "DEFOVSTRGV", "RGB", "geometry", "src_file"]]
VLAANDEREN_selection.columns = ["OBJECTID", "LOCALID", "TYPEALEA", "RGB", "geometry", "src_file"]
VLAANDEREN_selection.loc[:, "FLOOD_RISK"] = VLAANDEREN_selection.loc[:, "TYPEALEA"]

# concatenate datasets and export to shapefile
whole_map = pd.concat([WALLONIE_selecion, VLAANDEREN_selection], axis = 0)
whole_map["RGB_STR"] = whole_map["RGB"].apply(lambda x : str(x[0]) + "," + str(x[1]) + "," + str(x[2]))


# export to .zip file
file_name = os.path.join(data_folder, 'BE_flooding_map')
print(f"\nDataset being saved to {file_name}...")

with tempfile.TemporaryDirectory() as temp_dir:
    temp_dir = Path(temp_dir)
    print(f"outputting in temp directory {temp_dir}")
    whole_map.drop(labels = ["RGB"], axis = 1).to_file(filename = temp_dir, driver = 'ESRI Shapefile')
    archiveFile = shutil.make_archive(file_name, 'zip', temp_dir)
    shutil.rmtree(temp_dir)

"""
# export to shapefile
file_name = os.path.join(data_folder, 'BE_flooding_map.shp')
whole_map.drop(labels = ["RGB"], axis = 1).to_file(file_name)
print(f"\nDataset saved to {file_name}")

# export to json file
file_name = os.path.join(data_folder, 'BE_flooding_map.geojson')
whole_map.drop(labels = ["RGB"], axis = 1).to_file(file_name, driver = "GeoJSON")
print(f"\nDataset saved to {file_name}")
"""

def plot_map(gdf, title, img_name) :
    print("\nPreparing map...")
    # need to find out here how to use the RGB column without making the legend disappear
    gdf.plot(figsize = (24, 16), column = gdf.FLOOD_RISK, label = gdf.FLOOD_RISK, legend = True)
    plt.xlabel(gdf.crs.axis_info[0].name + ', ' + gdf.crs.axis_info[0].unit_auth_code + " - " + gdf.crs.axis_info[0].unit_name)
    plt.ylabel(gdf.crs.axis_info[1].name + ', ' + gdf.crs.axis_info[1].unit_auth_code + " - " + gdf.crs.axis_info[1].unit_name)
    plt.title(title)

    img_name = os.path.join(img_folder, img_name)
    plt.savefig(img_name)
    print(f"\nMap saved to {img_name}")
    #plt.show()

plot_map(whole_map, "Flood map - Wallonie & Vlaanderen", "BE_flooding_map.png")

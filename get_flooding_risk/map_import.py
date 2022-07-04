import os
import shutil
import tempfile
from pathlib import Path
import pandas as pd
import geopandas as gpd
import numpy as np
from matplotlib import pyplot as plt
from config import *


# import separate maps
WALLONIE_selection = map_wallonia()
LAANDEREN_selection = map_flanders()

# concatenate datasets and export to shapefile
print("\nPut all data on one map")

whole_map = pd.concat([WALLONIE_selecion, VLAANDEREN_selection], axis = 0)
whole_map["RGB_STR"] = whole_map["RGB"].apply(lambda x : str(x[0]) + "," + str(x[1]) + "," + str(x[2]))

# translate columns to standard terms
whole_map.TYPEALEA = whole_map.TYPEALEA.map(type_alea_dic)
whole_map.RISK_LEVEL = whole_map.RISK_LEVEL.map(risk_level_dic)

# add a synthetic column for the risk, with 1 row / point



# export to .zip file
file_name = os.path.join(data_folder, 'BE_flooding_map')
print(f"\nDataset being saved to {file_name}...")

with tempfile.TemporaryDirectory() as temp_dir:
    temp_dir = Path(temp_dir)
    print(f"outputting in temp directory {temp_dir}")
    whole_map.drop(labels = ["RGB"], axis = 1).to_file(filename = temp_dir, driver = 'ESRI Shapefile')
    archiveFile = shutil.make_archive(file_name, 'zip', temp_dir)
    shutil.rmtree(temp_dir)

# export plotted map for verifications
plot_map(whole_map, "Flood map - Wallonie & Vlaanderen", "BE_flooding_map.png")

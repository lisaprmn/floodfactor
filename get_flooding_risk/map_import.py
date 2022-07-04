import os
import pandas as pd
import geopandas as gpd
import numpy as np
from matplotlib import pyplot as plt
from config import *


if __name__ == "__main__" :
    # import separate maps
    WALLONIE_map = map_wallonia()
    LAANDEREN_map = map_flanders()
    BXL_map = map_brussels()

    # concatenate datasets and export to shapefile
    print("\nPut all data on one map")

    whole_map = pd.concat([WALLONIE_map, VLAANDEREN_map], axis = 0)
    whole_map["RGB_STR"] = whole_map["RGB"].apply(lambda x : str(x[0]) + "," + str(x[1]) + "," + str(x[2]))

    # translate risk columns to standard terms
    whole_map.TYPEALEA = whole_map.TYPEALEA.map(type_alea_dic)
    whole_map.RISK_LEVEL = whole_map.RISK_LEVEL.map(risk_level_dic)

    # add a synthetic column for the risk, with 1 row / geometry



    # export to .zip file
    export_map(whole_map, 'BE_flooding_map')

    # export plotted map to image for verifications
    plot_map(whole_map, "Flood map - Wallonie & Vlaanderen", "BE_flooding_map.png")

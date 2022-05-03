"""Assignment script using GIS Practical 2 from module EGM711.

 Practical 2 aims to focus on displaying. collating, creating and querying data in ArcGIS.
 Topics include:
 Adding, symbolising and navigating spatial data
 Clipping large datasets to an area of interest
 Accessing linked attribute data
 Creating a points shapefile from tabular data
 Accessing and selecting attribute and spatial data through attribute and locational queries
 Creating a Digital Terrain Model"""

# Import modules required for the practical.
#
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import rasterio as rio
import numpy as np
#
        
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

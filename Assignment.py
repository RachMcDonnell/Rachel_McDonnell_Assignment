# GIS Practical 2 Script.

# Import modules required for the practical.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import geopandas as gpd
 from shapely.geometry import Point, LineString, Polygon
import matplotlib.pyplot as plt
 from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import rasterio as rio

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

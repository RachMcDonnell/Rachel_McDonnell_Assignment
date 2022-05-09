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

import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import rasterio as rio
import numpy as np

# Exercise 1: Copying practical data and adding and symbolising data

# Download Practical 2 data from the data files folder and load data here:
outline = gpd.read_file('data_files/NI_outline.shp')
roads = gpd.read_file('data_files/NI_roads.shp')
settlements_poly = gpd.read_file('data_files/settlements_poly.shp')
gazeteer = gpd.read_file('data_files/Gazeteer.shp')
binevenagh_250k = rio.open('data_files/Binevenagh_250k.tif')

# Add NI_Outline and NI_Roads layers to current map:
# create a figure of size 10x10 (representing the page size in inches)
myFig = plt.figure(figsize=(10, 10))

myCRS = ccrs.UTM(29)  # create a Universal Transverse Mercator reference system to transform our data.

ax = plt.axes(projection=ccrs.Mercator())  # finally, create an axes object in the figure, using a Mercator
# projection, where we can actually plot our data.

#  add the outline of Northern Ireland using cartopy's ShapelyFeature
outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='k', facecolor='w')

xmin, ymin, xmax, ymax = outline.total_bounds
ax.add_feature(outline_feature)  # add the features we've created to the map.

#  add the NI_Roads using cartopy's ShapelyFeature
Roads = ShapelyFeature(roads['geometry'], myCRS, edgecolor='k', facecolor='w')

# get the number of unique road classes we have in the dataset
road_class = len(roads.Road_class.unique())
print('Number of unique features: {}'.format(road_class))


def clip_to_study_area(name):
    # Use a breakpoint in the code line below to debug your script.

    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


"""Clips layers to the Study Area.

 Each layer must be clipped to the 'Study Area' Shapefile"""

# Exercise 2 Clipping Map Layers:
study_area = gpd.read_file('data_files/study_area_box.shp')  # Add map layer called Study Area Box

# Check both layers are the same CRS
assert isinstance(roads.crs, object)
print(study_area.crs == roads.crs)
# Clip roads layer to the Study Area Box
roads_clip = gpd.clip(roads, study_area)

if __name__ == '__main__':
    print_hi('PyCharm')
# Exercise 3 Creating and applying a layer file
# Exercise 4 Obtaining Map layers online and clipping them to the study area
# Exercise 5 Symbolising Quantities
# Exercise 6 Creating and displaying point data and saving to a shapefile (Track Centre)
# Exercise 7 Displaying point data and saving to a shapefile (Buildings)
# Exercise 8 Selecting Features from within the attribute table
# Exercise 9 Selecting Features from within the map
# Exercise 10 Selecting Features by attribute
# Exercise 11 Selecting Features by location
# Exercise 12 Impact of scale on accuracy and detail
# Exercise 13 Raster and the impact of resolution (DTM)
# Exercise 14 Create a Map Layout


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

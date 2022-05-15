"""Assignment script using an excerpt from EGM711 GIS Practical 2.

 Practical 2 aims to focus on displaying. collating, creating and querying data in ArcGIS.
 Topics include:
 Adding, symbolising and navigating spatial data
 Clipping large datasets to an area of interest
 Creating a points shapefile from tabular data
 Accessing and selecting attribute and spatial data through attribute and locational queries
 Creating a Digital Terrain Model
 Creating a map layout"""

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

# Part 1: Copying practical data and adding and symbolising data

# Download Practical 2 data from the data files folder and load data here:
outline = gpd.read_file('data_files/NI_outline.shp')
roads = gpd.read_file('data_files/NI_roads.shp')
settlements_poly = gpd.read_file('data_files/settlements_poly.shp')
gazeteer = gpd.read_file('data_files/Gazeteer.shp')
binevenagh_250k = rio.open('data_files/Binevenagh_250k.tif')
study_area = gpd.read_file('data_files/study_area_box.shp')

# Part 2 :Add Layers to current map and updating symbology:

# create a figure of size 10x10 (representing the page size in inches)
myFig = plt.figure(figsize=(10, 10))

myCRS = ccrs.UTM(29)  # create a Universal Transverse Mercator reference system to transform our data.

ax = plt.axes(projection=ccrs.Mercator())  # finally, create an axes object in the figure, using a Mercator
# projection, where we can actually plot our data.

#  add the outline of Northern Ireland using cartopy's ShapelyFeature with a black outline
outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='k', facecolor='w')
ax.add_feature(outline_feature)  # add the features we've created to the map.

# Add Study Area Box, Display it with a wide outline and no fill colour:
study_area_outline = ShapelyFeature(study_area['geometry'], myCRS, edgecolor='black', facecolor='none', linewidth=1)
xmin, ymin, xmax, ymax = study_area.total_bounds
ax.add_feature(study_area_outline) # add the features we've created to the map.

# using the boundary of the shapefile features, zoom the map to our area of interest
ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS)  # because total_bounds gives output as xmin, ymin, xmax, ymax,
# but set_extent takes xmin, xmax, ymin, ymax, we re-order the coordinates here.

#  add the NI_Roads using cartopy's ShapelyFeature
Roads = ShapelyFeature(roads['geometry'], myCRS, edgecolor='k', facecolor='w')

# Display the Roads Layer by Road Class and modify the symbols for each type of road:
road_class = len(roads.Road_class.unique())  # get the number of unique road classes we have in the dataset
print('Number of unique features: {}'.format(road_class))

# Pick Colours for individual road classes
road_colours = ['gray', 'red', 'gold', 'blue', 'purple', 'green', 'lime', 'cyan']

# Get a list of unique names for road classes:
road_class_names = list(roads.Road_class.unique())
print(road_class_names)

# next, add the road classes to the map using the colors that we've picked.
# here, we're iterating over the unique values in the 'Road_class' field.
# we're also setting the edge color to be black, with a line width of 0.5 pt.

for i, name in enumerate(road_class_names):
    feat = ShapelyFeature(roads['geometry'][roads['Road_class'] == name], myCRS,
                          edgecolor=road_colours[i],
                          facecolor='none',
                          linewidth=1,
                          alpha=0.25)
    ax.add_feature(feat)

plt.show()

"""Clips layers to the Study Area.

 Each layer must be clipped to the 'Study Area' Shapefile"""


# Part 3: Clipping Map Layers to the study area:
def clip_to_study_area(name):
    clipped = gpd.clip(name,study_area)
    clipped_gdf=gpd.Geodataframe(pd.clipped)

# Check both layers are the same CRS
assert isinstance(roads.crs, object)
print(study_area.crs == roads.crs)

# Clip roads layer to the Study Area Box
roads_clipped = roads.clip(study_area_outline)
ax.add_feature(roads_clipped)
plt.show()



# Exercise 3 Creating and applying a layer file
# Exercise 4 Obtaining Map layers online and clipping them to the study area
# Exercise 5 Symbolising Quantities (census data)
# Exercise 6 Creating and displaying point data and saving to a shapefile (Track Centre)
# Exercise 7 Displaying point data and saving to a shapefile (Buildings)
# Adding and displaying a raster
# Exercise 14 Create a Map Layout


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

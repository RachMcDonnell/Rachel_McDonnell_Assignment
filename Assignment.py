"""Assignment script using an excerpt from EGM711 GIS Practical 2.

 Produce a map showing the key features of the area surrounding a proposed motorbike track in Binevenagh.

 Topics include:
 Adding, symbolising and navigating spatial data
 Clipping large datasets to an area of interest
 Creating a points shapefile from tabular data
 Creating a map layout illustrating the general context and environment of the surrounding area including:
    -Roads
    -Buildings
    -Settlements
    -Motorbike Track
    -Rivers
    -Areas of outstanding Natural Beauty (AONB'S)
    -Areas of Special Scientific Interest (ASSI's)
    -Background Raster Mapping"""

# Import modules required for the practical.

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

# Part 1: Load practical data

# Download Practical 2 data from the data files folder and load data here:
outline = gpd.read_file('data_files/NI_outline.shp')
roads = gpd.read_file('data_files/NI_roads.shp')
settlements_poly = gpd.read_file('data_files/settlements_poly.shp')
gazeteer = gpd.read_file('data_files/Gazeteer.shp')
binevenagh_250k = rio.open('data_files/Binevenagh_250k.tif')
study_area = gpd.read_file('data_files/study_area_box.shp')
AONB_boundary = gpd.read_file('data_files/AONB.shp')
ASSI_boundary = gpd.read_file('data_files/ASSI.shp')
Buildings = gpd.read_file('data_files/Binevenagh Pointer.dbf')

# Part 2 :Add data to map and adding and symbolising data:

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

# Add the AONB layer using cartopy's ShapelyFeature. AONB shows the boundaries of Areas of outstanding natural beauty
AONB_boundary= ShapelyFeature(AONB_boundary['geometry'], myCRS, edgecolor='tan', facecolor='tan', linewidth=1,)
ax.add_feature(AONB_boundary) # add the features we've created to the map

# Add the ASSI layer using cartopy's ShapelyFeature. ASSI shows the boundaries of Areas of Special Scientific Interest
ASSI_boundary = ShapelyFeature(ASSI_boundary['geometry'], myCRS, edgecolor='sandybrown', facecolor='sandybrown', linewidth=1,)
ax.add_feature(ASSI_boundary) # add the features we've created to the map

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
# we're also setting the edge color to be black, with a line width of 1pt.

for i, name in enumerate(road_class_names):
    feat = ShapelyFeature(roads['geometry'][roads['Road_class'] == name], myCRS,
                          edgecolor=road_colours[i],
                          facecolor='none',
                          linewidth=1,
                          alpha=0.25)
    ax.add_feature(feat)

# Add the settlements_poly layer using cartopy's ShapelyFeature. Settlments_poly shows the boundaries of built up areas.
Settlements = ShapelyFeature(settlements_poly['geometry'], myCRS, edgecolor='darkolivegreen', facecolor='green')
ax.add_feature(Settlements) # add the features we've created to the map
plt.show()

# Part 4 Creating and displaying point data (Track Centre)
Track_centre = Point(638049.7221,6112938.0385)
print(Track_centre)

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



# Part 5 Displaying point data from a database (Buildings)


# Part 6 Adding and displaying a raster for Background mapping
# Part 7 Creating a map:
# Adding legends
# Adding scale bar
# Add labels





# See PyCharm help at https://www.jetbrains.com/help/pycharm/

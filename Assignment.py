"""Assignment script using an excerpt from EGM711 GIS Practical 2.

 Produce a map showing the key features of the area surrounding a proposed motorbike track in Binevenagh.

 Topics include:
 Adding, symbolising and navigating spatial data
 Displaying polygon data and editing symbology
 Displaying point data and editing symbology
 Creating a map layout illustrating the general context and environment of the surrounding area including:
    -Roads
    -Settlements Boundaries (Towns)
    -Settlement Points (Towns & villages)
    -Buildings
    -Motorbike Track itself
    -Areas of outstanding Natural Beauty (AONB'S)
    -Areas of Special Scientific Interest (ASSI's)"""

# Import modules required for the practical.

import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
from pandas import DataFrame
from shapely.geometry import Point, LineString, Polygon
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib.lines import Line2D
import numpy as np


# generate matplotlib handles to create a legend of the features we put in our map.
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

# create a scale bar of length 20km in the upper part of the map
# adapted this question: https://stackoverflow.com/q/32333870
# answered by SO user Siyh: https://stackoverflow.com/a/35705477

def scale_bar(ax, location=(0.95, 0.95)):
    llx0, llx1, lly0, lly1 = ax.get_extent(ccrs.PlateCarree())
    sbllx = (llx1 + llx0) / 2
    sblly = lly0 + (lly1 - lly0) * location[1]

    tmc = ccrs.TransverseMercator(sbllx, sblly)
    x0, x1, y0, y1 = ax.get_extent(tmc)
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    plt.plot([sbx, sbx - 20000], [sby, sby], color='k', linewidth=9, transform=tmc)
    plt.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=6, transform=tmc)
    plt.plot([sbx-10000, sbx - 20000], [sby, sby], color='w', linewidth=6, transform=tmc)

    plt.text(sbx, sby-1000, '20 km', transform=tmc, fontsize=8)
    plt.text(sbx-12500, sby-1000, '10 km', transform=tmc, fontsize=8)
    plt.text(sbx-20500, sby-1000, '0 km', transform=tmc, fontsize=8)

# Part 1: Adding, symbolising and navigating spatial data

# Load Practical_2 data from the data_files folder:
outline = gpd.read_file('data_files/NI_outline.shp')
roads = gpd.read_file('data_files/NI_roads.shp')
settlements_poly = gpd.read_file('data_files/settlements_poly.shp')
study_area = gpd.read_file('data_files/study_area_box.shp')
AONB_boundary = gpd.read_file('data_files/AONB.shp')
ASSI_boundary = gpd.read_file('data_files/ASSI.shp')
Buildings = gpd.read_file('data_files/Binevenagh_buildings.shp')
Track_centre = gpd.read_file('data_files/track_centre.shp')
Binevenagh_gazeteer = gpd.read_file('data_files/Binevenagh_Gazeteer.shp')

# Part 2 : Displaying polygon data and editing symbology

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
ax.add_feature(study_area_outline)  # add the features we've created to the map.

# using the boundary of the shapefile features, zoom the map to our area of interest
ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS)  # because total_bounds gives output as xmin, ymin, xmax, ymax,
# but set_extent takes xmin, xmax, ymin, ymax, we re-order the coordinates here.

# Add the AONB layer using cartopy's ShapelyFeature. AONB shows the boundaries of Areas of outstanding natural beauty
AONB_boundary = ShapelyFeature(AONB_boundary['geometry'], myCRS, edgecolor='tan', facecolor='tan', linewidth=0.5, )
ax.add_feature(AONB_boundary)  # add the features we've created to the map

# Add the ASSI layer using cartopy's ShapelyFeature. ASSI shows the boundaries of Areas of Special Scientific Interest
ASSI_boundary = ShapelyFeature(ASSI_boundary['geometry'], myCRS, edgecolor='sandybrown', facecolor='sandybrown',
                               linewidth=0.5, )
ax.add_feature(ASSI_boundary)  # add the features we've created to the map

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

for i, row in Binevenagh_gazeteer.iterrows():
    x, y = row.geometry.x, row.geometry.y  # get the x,y location for each town
    plt.text(x, y, row['NAME'].title(), fontsize=8, transform=myCRS)  # use plt.text to place a label at x,y

# Add the settlements_poly layer using cartopy's ShapelyFeature. This layer shows the boundaries of built-up areas.
Settlements = ShapelyFeature(settlements_poly['geometry'], myCRS, edgecolor='green', facecolor='green')
ax.add_feature(Settlements)  # add the features we've created to the map

# Part 3  Displaying point data and editing symbology

# Add Track_centre to map:
# This layer shows the location of the Motorbike track.
# ShapelyFeature creates a polygon, so for point data we can just use ax.plot()
# Set marker size to 6 to create a large point on the map and set marker symbol as Diamond
Track_Centre = ax.plot(Track_centre.geometry.x, Track_centre.geometry.y, 'D', color='red', ms=6, transform=myCRS)

# Add Buildings to map:
# This layer is derived from a pointer database of addresses of every building in Northern Ireland
# Default colour left as black, set marker size to 3 as to not obscure other point data.
Buildings = ax.plot(Buildings.geometry.x, Buildings.geometry.y, '.', color='black', ms=3, transform=myCRS)

# Add Binevenagh_gazeteer to map:
# This layer displays point location of built-up areas plus smaller villages not included in the Settlements_poly layer
# Set marker symbol to triangle, marker size to 7, and colour to blue
Binevenagh_gazeteer = ax.plot(Binevenagh_gazeteer.geometry.x, Binevenagh_gazeteer.geometry.y, '^', color='blue', ms=7,
                              transform=myCRS)

# Part 4 Creating a map layout:
# Adding legends

# generate a list of handles for the roads dataset
roads_handle = generate_handles(roads.Road_class.unique(), road_colours, alpha=0.25)

# generate handles for the Settlements dataset
settlements_handle = generate_handles(['Settlements'], ['green'])

# generate marker for the Buildings dataset
buildings_handle = [Line2D([],[],marker='.', color='black', ms=7)]

# generate marker for the Track_centre dataset
track_handle = [Line2D([0],[0],marker='D', color='red', ms=6)]

# generate handles for the Areas of Natural Beauty dataset
aonb_handle = generate_handles(['AONB'], ['tan'])

# generate handles for the Areas of Special Scientific Interest dataset
assi_handle = generate_handles(['ASSI'], ['sandybrown'])

# generate marker for the Gazeteer (Towns & Villages) dataset
gazeteer_handle = [Line2D([],[],marker='^', color='mediumblue', ms=7)]

# ax.legend() takes a list of handles and a list of labels corresponding to the objects you want to add to the legend
handles = roads_handle + settlements_handle + buildings_handle + track_handle + aonb_handle + assi_handle + gazeteer_handle
labels = road_class_names + ['Settlements', 'Buildings', 'Track', 'AONB', 'ASSI', 'Towns_and_Villages']

leg = ax.legend(handles, labels, title='Legend', title_fontsize=9,
                fontsize=7, loc='lower right', frameon=True, framealpha=1)

# Add a scale bar
scale_bar(ax)

plt.show()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

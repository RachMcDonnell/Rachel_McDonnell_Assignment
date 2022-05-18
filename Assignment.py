"""Assignment script using exercise 14. from EGM711 Principles of GIS Practical 2.

 Produce a map showing the key features of the area surrounding the proposed motorbike track in Binevenagh.

 Topics include:
 Adding, symbolising and navigating spatial data
 Displaying polygon data and editing symbology
 Displaying point data and editing symbology
 Creating a map layout-
    Illustrate the general context and environment of the surrounding area including:
    -Roads
    -Settlement Boundaries (Towns)
    -Settlement Points (Towns & villages)
    -Buildings
    -Motorbike Track
    -Areas of Outstanding Natural Beauty (AONB'S)
    -Areas of Special Scientific Interest (ASSI's)"""

# 1.Import modules

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

# 2. Create Functions

"""The 'generate_handles' function will generate legend items required when creating a legend for the map layout.

Each data file (map layer) plotted to the map layout will require a legend item to represent it. This function will 
generate labels and colours for each legend item. 

len returns the number of items in a list, in this case len(colors) will generate a list of colours which can be used 
in the legend.
For eg: to generate a legend item for the buildings dataset : 

 buildings_handle = [Line2D([],[],marker='.', color='black', ms=7)]

 will generate a point (.) symbol to represent the buildings in black, and with marker size (ms) of 7"""


# create a scale bar of length 20km in the upper part of the map
# adapted this question: https://stackoverflow.com/q/32333870
# answered by SO user Siyh: https://stackoverflow.com/a/35705477

def scale_bar(ax, location=(0.95, 0.95)):
    # Get the limits of the axis in lat long
    llx0, llx1, lly0, lly1 = ax.get_extent(ccrs.PlateCarree())

    # Centre the scale bar or choose a location eg [1]:
    sbllx = (llx1 + llx0) / 2
    sblly = lly0 + (lly1 - lly0) * location[1]

    tmc = ccrs.TransverseMercator(sbllx, sblly)
    # Get the extent of the plotted area in coordinates in metres:
    x0, x1, y0, y1 = ax.get_extent(tmc)

    # Turn the specified scalebar location into coordinates in metres:
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    # Calculates the scale bar length:
    plt.plot([sbx, sbx - 20000], [sby, sby], color='k', linewidth=9, transform=tmc)
    plt.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=6, transform=tmc)
    plt.plot([sbx - 10000, sbx - 20000], [sby, sby], color='w', linewidth=6, transform=tmc)

    plt.text(sbx, sby - 1000, '20 km', transform=tmc, fontsize=8)
    plt.text(sbx - 12500, sby - 1000, '10 km', transform=tmc, fontsize=8)
    plt.text(sbx - 20500, sby - 1000, '0 km', transform=tmc, fontsize=8)


"""The 'scale_bar' function will produce a custom scale bar for the map layout which will be created the end of the 
script. 

    ax is the axes to draw the scalebar on,    
    location is center of the scalebar in axis coordinates.
    (ie. 0.5 is the middle of the plot)."""

# Adding, symbolising and navigating spatial data

# 3. Load data from the data_files folder:
outline = gpd.read_file('data_files/NI_outline.shp')
roads = gpd.read_file('data_files/NI_roads.shp')
settlements_poly = gpd.read_file('data_files/settlements_poly.shp')
study_area = gpd.read_file('data_files/study_area_box.shp')
AONB_boundary = gpd.read_file('data_files/AONB.shp')
ASSI_boundary = gpd.read_file('data_files/ASSI.shp')
Buildings = gpd.read_file('data_files/Binevenagh_buildings.shp')
Track_centre = gpd.read_file('data_files/track_centre.shp')
Binevenagh_gazeteer = gpd.read_file('data_files/Binevenagh_Gazeteer.shp')

# 4. Displaying polygon data and editing symbology

# create a figure of size 10x10 (representing the page size in inches)
myFig = plt.figure(figsize=(10, 10))

myCRS = ccrs.UTM(29)  # create a Universal Transverse Mercator reference system to transform our data.

ax = plt.axes(projection=ccrs.Mercator())  # finally, create an axes object in the figure, using a Mercator
# projection, where we can actually plot our data.

# Add the outline of Northern Ireland using cartopy's ShapelyFeature with a black outline
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
print(road_class_names)  # Allows us to see the list of road class types and decide how many colours to choose for
# each class

# next, add the road classes to the map using the colors that we've picked.
# here, we're iterating over the unique values in the 'Road_class' field.
# we're also setting the edge color to the chosen colours, with a line width of 1pt.

for i, name in enumerate(road_class_names):
    feat = ShapelyFeature(roads['geometry'][roads['Road_class'] == name], myCRS,
                          edgecolor=road_colours[i],
                          facecolor='none',
                          linewidth=1,
                          alpha=0.25)
    ax.add_feature(feat) # Add the features we have created to the map

# Add labels to the Gazeteer layer , (works when done at this point)
for i, row in Binevenagh_gazeteer.iterrows():
    x, y = row.geometry.x, row.geometry.y  # get the x,y location for each town or village
    plt.text(x, y, row['NAME'].title(), fontsize=8, transform=myCRS)  # use plt.text to place a label at x,y

# Add the settlements_poly layer using cartopy's ShapelyFeature. This layer shows the boundaries of built-up areas.
Settlements = ShapelyFeature(settlements_poly['geometry'], myCRS, edgecolor='green', facecolor='green')
ax.add_feature(Settlements)  # add the features we've created to the map

# 5. Displaying point data and editing symbology

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

# 6. Creating a map layout:

# Adding a legend to the map layout:
# Generate a list of handles for all datasets plotted to the map using the def function 'generate_handles':
# generate a list of handles for each road class using road colours chosen previously
roads_handle = generate_handles(roads.Road_class.unique(), road_colours, alpha=0.25)

# generate handles for the Settlements dataset. Choose the same colour as the layer plotted to map.
settlements_handle = generate_handles(['Settlements'], ['green'])

# generate marker for the Buildings dataset. Choose the same colour as the layer plotted to map.
buildings_handle = [Line2D([],[], marker='.', color='black', ms=7)]

# generate marker for the Track_centre dataset. Choose the same colour as the layer plotted to map.
track_handle = [Line2D([0], [0], marker='D', color='red', ms=6)]

# generate handles for the Areas of Natural Beauty dataset. Choose the same colour as the layer plotted to map.
aonb_handle = generate_handles(['AONB'], ['tan'])

# generate handles for the Areas of Special Scientific Interest dataset. Choose the same colour as the layer plotted
# to map.
assi_handle = generate_handles(['ASSI'], ['sandybrown'])

# generate marker for the Gazeteer (Towns & Villages) dataset. Choose the same colour as the layer plotted to map.
gazeteer_handle = [Line2D([], [], marker='^', color='blue', ms=7)]

# ax.legend() takes a list of handles and a list of labels corresponding to the objects you want to add to the legend
handles = roads_handle + settlements_handle + buildings_handle + track_handle + aonb_handle + assi_handle + gazeteer_handle
labels = road_class_names + ['Settlements', 'Buildings', 'Track', 'AONB', 'ASSI', 'Towns_and_Villages']

#Plot the legend
leg = ax.legend(handles, labels, title='Legend', title_fontsize=9,
                fontsize=7, loc='lower right', frameon=True, framealpha=1)

# Plot the scale bar
scale_bar(ax)

plt.show()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

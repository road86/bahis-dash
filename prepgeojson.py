# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 14:16:22 2023

@author: yoshka
"""

import pandas as pd
import json, glob
from shapely.geometry import shape, Point

#debug
# sourcepath = 'C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/newbahis_geo_cluster.csv'
# path3= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM3_simplified.geojson" #495 Upazila
# upadata = "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/upadata.geojson"
# path2= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM2_simplified.geojson"
# distdata = "c:/users/yoshka/documents/github/bahis-dash/geodata/distdata.geojson"
# path1= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM1_simplified.geojson"
# divdata = "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/divdata.geojson"

geofilename = glob.glob('exported_data/newbahis_geo_cluster*.csv')[-1]   # the available geodata from the bahis project
path3= "geodata/geoBoundaries-BGD-ADM3_simplified.geojson" #495 Upazila
upadata = "geodata/upadata.geojson"
path2= "geodata/geoBoundaries-BGD-ADM2_simplified.geojson"
distdata = "geodata/distdata.geojson"
path1= "geodata/geoBoundaries-BGD-ADM1_simplified.geojson"
divdata = "geodata/divdata.geojson"

geodata = pd.read_csv(geofilename)
geodata = geodata.drop(geodata[(geodata['loc_type']==1) | (geodata['loc_type']==2) | (geodata['loc_type']==4) | (geodata['loc_type']==5)].index)

with open(path3) as f:
    data = json.load(f)

for i in range(len(geodata)):
    point = Point(geodata['longitude'].iloc[i], geodata['latitude'].iloc[i])
    for feature in data['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
    #        print ('Found polygon:', feature['properties']['shapeName'])
    #        feature['properties']['newname']=geodata['name'].iloc[1]
            feature['properties']['upazilanumber']=geodata['value'].iloc[i]
            feature['properties']['ccheck_upaname']=geodata['name'].iloc[i]

manual=['Bandarban Sadar', 'Bijoynagar', 'Galachipa', 'Haim Char', 'Kalukhali', 'Kamarkhanda', 'Mehendiganj', 'Naikhongchhari', 'Paba', 'Ramu', 'Saltha', 'Tazumuddin', 'Zianagar']

for i in range(len(manual)):
    for feature in data['features']:
        if feature['properties']['shapeName']==manual[i]:
            feature['properties']['upazilanumber']=int(geodata[geodata['name']==manual[i].upper()]['value'])
            feature['properties']['ccheck_upaname']=str(geodata[geodata['name']==manual[i].upper()]['name'].values[0])


## first by names, except for doublings, then locations (causing naming problems)
#tmp=geodata[(geodata['name'].duplicated()) & (geodata['loc_type']==3)]['name']
#tmp2=geodata[geodata['name'].isin(tmp)==False]['name']

# for i in range(len(geodata)):
#     if (geodata.iloc[i]['name'] in tmp) == False:
#         for feature in data['features']:
#             if feature['properties']['shapeName']==geodata.iloc[i]['name'].title():
#                 feature['properties']['upazilanumber']=int(geodata.iloc[i]['value'])
#                 feature['properties']['ccheck_upaname']=str(geodata.iloc[i]['name'])
#     elif (geodata.iloc[i]['name'] in tmp) == True:
#         point = Point(geodata['longitude'].iloc[i], geodata['latitude'].iloc[i])
#         for feature in data['features']:
#             polygon = shape(feature['geometry'])
#             if polygon.contains(point):
#                 feature['properties']['upazilanumber']=geodata['value'].iloc[i]
#                 feature['properties']['ccheck_upaname']=geodata['name'].iloc[i]




json.dump(data, open(upadata, 'w') , default=str)


geodata = pd.read_csv(geofilename)
geodata = geodata.drop(geodata[(geodata['loc_type']==1) | (geodata['loc_type']==3) | (geodata['loc_type']==4) | (geodata['loc_type']==5)].index)

with open(path2) as f:
    data = json.load(f)

for i in range(len(geodata)):
    point = Point(geodata['longitude'].iloc[i], geodata['latitude'].iloc[i])
    for feature in data['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
    #        print ('Found polygon:', feature['properties']['shapeName'])
    #        feature['properties']['newname']=geodata['name'].iloc[1]
            feature['properties']['districtnumber']=geodata['value'].iloc[i]
            feature['properties']['ccheck_distname']=geodata['name'].iloc[i]

json.dump(data, open(distdata, 'w') , default=str)



geodata = pd.read_csv(geofilename)
geodata = geodata.drop(geodata[(geodata['loc_type']==2) | (geodata['loc_type']==3) | (geodata['loc_type']==4) | (geodata['loc_type']==5)].index)

with open(path1) as f:
    data = json.load(f)

for i in range(len(geodata)):
    point = Point(geodata['longitude'].iloc[i], geodata['latitude'].iloc[i])
    for feature in data['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
    #        print ('Found polygon:', feature['properties']['shapeName'])
    #        feature['properties']['newname']=geodata['name'].iloc[1]
            feature['properties']['divnumber']=geodata['value'].iloc[i]
            feature['properties']['ccheck_divname']=geodata['name'].iloc[i]

json.dump(data, open(divdata, 'w') , default=str)


# for items in data['features']:
#     if 'upazilanumber' not in items['properties']:
#         print(items['properties']['shapeName'])

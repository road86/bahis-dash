# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 14:16:22 2023

@author: yoshka
"""

import pandas as pd
import json
from shapely.geometry import shape, Point

sourcepath = 'C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/'
geofilename = sourcepath + 'newbahis_geo_cluster.csv'   # the available geodata from the bahis project
path3= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM3_simplified.geojson" #495 Upazila

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
            

json.dump(data, open("C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/upadata.geojson", 'w') , default=str)
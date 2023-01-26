# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 07:48:29 2023

@author: yoshka
"""

# Import necessary libraries 
import dash
from dash import html, dcc, Input, Output


# sourcepath = 'C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/'
# geofilename = sourcepath + 'newbahis_geo_cluster.csv'   # the available geodata from the bahis project
# sourcefilename =sourcepath + 'preped_data2.csv'   
# bahis_sd = pd.read_csv(sourcefilename)

# path0= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM0_simplified.geojson" #1 Nation # found shapefiles from the data.humdata.org
# path1= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM1_simplified.geojson" #8 Division
# path2= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM2_simplified.geojson" #64 District
# path3= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM3_simplified.geojson" #495 Upazila
# path4= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM4_simplified.geojson" #4562 Union

# def fetchsourcedata():
#     bahis_sd = pd.read_csv(sourcefilename) 
#     bahis_sd['basic_info_division'] = pd.to_numeric(bahis_sd['basic_info_division'])
#     bahis_sd['basic_info_district'] = pd.to_numeric(bahis_sd['basic_info_district'])
#     bahis_sd['basic_info_upazila'] = pd.to_numeric(bahis_sd['basic_info_upazila'])
#     bahis_sd['basic_info_date'] = pd.to_datetime(bahis_sd['basic_info_date'])
#     return bahis_sd
# bahis_sourcedata= fetchsourcedata()

dash.register_page(__name__)

#app = Dash(__name__)
layout = html.Div([
    dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown'),
    html.Div(id='dd-output-container')
])


@dash.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    return f'You have selected {value}'


# if __name__ == '__main__':
#     app.run_server(debug=True)
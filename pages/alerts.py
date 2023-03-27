# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 20:20:17 2023

@author: yoshka
"""

# Import necessary libraries 
import dash
from dash import dcc, html, callback #Dash, #dash_table, dbc 
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
import json, os
from datetime import datetime, timedelta


#### make second table with non responders and color empty ones per time period set  1.5h extra
pd.options.mode.chained_assignment = None

#dash.register_page(__name__) #, path='/')

sourcepath = 'exported_data/'
geofilename = sourcepath + 'newbahis_geo_cluster.csv'   # the available geodata from the bahis project
sourcefilename =sourcepath + 'preped_data2.csv'   
# path0= "geodata/geoBoundaries-BGD-ADM0_simplified.geojson" #1 Nation # found shapefiles from the data.humdata.org
# path1= "geodata/geoBoundaries-BGD-ADM1_simplified.geojson" #8 Division
# path2= "geodata/geoBoundaries-BGD-ADM2_simplified.geojson" #64 District
# path3= "geodata/geoBoundaries-BGD-ADM3_simplified.geojson" #495 Upazila
# path4= "geodata/geoBoundaries-BGD-ADM4_simplified.geojson" #4562 Union
path1= "geodata/divdata.geojson" #8 Division
path2= "geodata/distdata.geojson" #64 District
path3= "geodata/upadata.geojson" #495 Upazila

def fetchsourcedata():
    bahis_sd=[]
    bahis_sdtmp = pd.read_csv(sourcefilename) 
    bahis_sdtmp['basic_info_date'] = pd.to_datetime(bahis_sdtmp['basic_info_date'])
#    print(bahis_sdtmp)
#    bahis_sd = pd.to_numeric(bahis_sdtmp['basic_info_upazila']).dropna().astype(int)
    bahis_sd = bahis_sdtmp
    return bahis_sd
bahis_sourcedata= fetchsourcedata()

#print(bahis_sourcedata)
mask4w=(bahis_sourcedata['basic_info_date']> datetime.now()-timedelta(weeks=4)) & (bahis_sourcedata['basic_info_date'] < datetime.now())
tmp_4wdata=bahis_sourcedata.loc[mask4w]   
mask8w=(bahis_sourcedata['basic_info_date']> datetime.now()-timedelta(weeks=8)) & (bahis_sourcedata['basic_info_date'] < datetime.now())
tmp_8wdata=bahis_sourcedata.loc[mask8w]   
mask12w=(bahis_sourcedata['basic_info_date']> datetime.now()-timedelta(weeks=12)) & (bahis_sourcedata['basic_info_date'] < datetime.now())
tmp_12wdata=bahis_sourcedata.loc[mask12w]   
  ####################  
  
def fetchgeodata():
    return pd.read_csv(geofilename)
bahis_geodata= fetchgeodata()


upas=bahis_geodata[bahis_geodata['loc_type']==3]
upas=upas[['value', 'name']]
upas['name']=upas['name'].str.title()
upas['name']=upas['name'].astype('string')
reps= bahis_sourcedata[['basic_info_date', 'basic_info_upazila']]
upas['dyn']=16

for i in range(12, 1,-2):
    mask=(reps['basic_info_date']> datetime.now()-timedelta(weeks=i)) & (reps['basic_info_date'] < datetime.now())
    reps=reps.loc[mask]   
    upas['dyn'][upas['value'].isin(reps['basic_info_upazila'].astype(int).unique())]= i #upas['dyn']+1
    

def open_data(path):
    with open(path) as f:
        data = json.load(f)
        return data

def plot_map(path, loc, sub_bahis_sourcedata, title, pname, splace, variab, labl, theme):
#     subDist=bahis_geodata[(bahis_geodata["loc_type"]==loc)]  
#     reports = sub_bahis_sourcedata[title].value_counts().to_frame()
#     #reports.index = reports.index.astype(int)
#     reports[pname] = reports.index
#     reports.index = reports.index.astype(int)
#     reports= reports.loc[reports[pname] != 'nan']    
    data = open_data(path)

#     for i in range(reports.shape[0]):
#         #reports[pname].iloc[i] = subDist.loc[subDist['value']==int(reports[pname].iloc[i]),'name'].iloc[0]
#         reports[pname].iloc[i] = subDist[subDist['value']==reports.index[i]]['name'].values[0] ###still to work with the copy
#     reports[pname]=reports[pname].str.title()  
# #    reports.set_index(pname)                 
#     for i in data['features']:
#         i['id']= i['properties']['shapeName'].replace(splace,"")
    reports=upas
    reports.set_index('value')
    reports.index.name = 'Index'
    colorscales = [
    ((0.0, '#636efa'), (1.0, '#636efa')),
    ((0.0, '#EF553B'), (1.0, '#EF553B')),
    ((0.0, '#00cc96'), (1.0, '#00cc96'))
]
    
    fig = px.choropleth_mapbox(reports['dyn'], geojson=data, locations=reports['name'], color=reports['dyn'], #pnameupazilaname, color='dyn', # titlebasicinfoupazila,
                            featureidkey="properties.shapeName",
                            # color_discrete_map={'0':'#fffcfc',
                            #             '1':'#636efa',
                            #             '2':'#636efa',
                            #             '3':'#EF553B',
                            #             '4':'#00cc96'},
 #                           color_continuous_scale="YlOrBr",
                           # colorscale=colorscales[i],
                            hover_data=[reports.name, reports.value],
                            range_color=(0, reports['dyn'].max()),
                            mapbox_style="carto-positron",
                            zoom=6.4, center = {"lat": 23.7, "lon": 90.3},
                            opacity=0.5,
                            template=template_from_url(theme),
                            title='Title'
                            #labels={variab:labl}
                          )
    fig.update_layout(autosize=True, margin={"r":0,"t":0,"l":0,"b":0}, width=760 , height=800) #, coloraxis_showscale= False) #width= 1000, height=600, 
    fig.update_layout(
            coloraxis_colorbar=dict(
                title="last week reported",
                #tickvals=[0, 1, 2, 3,4,5,6,7,8,9,10,11,12],
                # ticktext=[
                #     "No measures", 
                #     "Recommend closing",
                #     "Require closing (only some levels)",
                #     "Require closing all levels",
                #     "vier","Blubb","7","8","9","10","11","12","1"
                # ],
            )
        )    
    return fig


header = html.H4(
    "BAHIS dashboard", className="bg-primary text-white p-2 mb-2 text-center"
)

row = html.Div(
    [ dbc.Row(
            [   
                dbc.Col([
                    dbc.Row([dbc.Card(dcc.Graph(
                                    id='AMap',
#                                    figure=figMap
                                    ), body=True)])
                     ], width=5
                    ),
            ]
        ),
    ]
)

theme_colors = [
    "primary",
    "secondary",
    "success",
    "warning",
    "danger",
    "info",
    "light",
    "dark",
    "link",
]

layout = dbc.Container(
    [
#        html.Div("Preselect local/server"),
        row,
        dbc.Row(
            [
                dbc.Col(
                    [
                        ThemeChangerAIO(aio_id="theme")
                    ],
                    width=4,
                ),
            ]
        ),
    ],
    fluid=True,
    className="dbc",
)

@callback(
    Output ('AMap', 'figure'),
    Input ('AMap', 'clickData'),    
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
)
def update_whatever(geoTile, theme):   #cRReport, start_date, end_date, cRDisease, cRDivision, cRDistrict, cRUpazila, theme):   
   

    if geoTile is not None:
        print(geoTile['points'][0]['location'])

    path=path3
    loc=3
    title='basic_info_upazila'
    pname='upazilaname'
    splace=' Upazila'
    variab='upazila'
    labl='Incidences per upazila'
    
    Rfig = plot_map(path, loc, bahis_sourcedata, title, pname, splace, variab, labl, theme)


    return Rfig









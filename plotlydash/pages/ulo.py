# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 07:48:14 2023

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
import json  

pd.options.mode.chained_assignment = None

dash.register_page(__name__) #, path='/')

sourcepath = 'C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/'
geofilename = sourcepath + 'newbahis_geo_cluster.csv'   # the available geodata from the bahis project
sourcefilename =sourcepath + 'preped_data2.csv'   
path0= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM0_simplified.geojson" #1 Nation # found shapefiles from the data.humdata.org
path1= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM1_simplified.geojson" #8 Division
path2= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM2_simplified.geojson" #64 District
path3= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM3_simplified.geojson" #495 Upazila
path4= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM4_simplified.geojson" #4562 Union


def fetchsourcedata():
    bahis_sd=[]
    bahis_sdtmp = pd.read_csv(sourcefilename) 
    bahis_sd = pd.to_numeric(bahis_sdtmp['basic_info_upazila']).dropna().astype(int)
    return bahis_sd
bahis_sourcedata= fetchsourcedata()

def fetchgeodata():
    return pd.read_csv(geofilename)
bahis_geodata= fetchgeodata()
print(bahis_geodata)

def fetchDivisionlist():   
    ddDivlist=bahis_geodata[(bahis_geodata["loc_type"]==1)]['name'].str.capitalize()
    ddDivlist.name='Division'
    ddDivlist=ddDivlist.sort_values()
    return ddDivlist.tolist()
ddDivlist=fetchDivisionlist()

def fetchDistrictlist(SelDiv):   
    DivNo= bahis_geodata.loc[(bahis_geodata['name'].str.capitalize()==SelDiv) & (bahis_geodata['loc_type']==1),'value'].values[0]
    ddDislist=bahis_geodata[bahis_geodata['parent']==DivNo]['name'].str.capitalize()
    ddDislist.name='District'
    ddDislist=ddDislist.sort_values()
    return ddDislist.tolist()

def fetchUpazilalist(SelDis):   
    DisNo= bahis_geodata.loc[(bahis_geodata['name'].str.capitalize()==SelDis) & (bahis_geodata['loc_type']==2),'value'].values[0]
    ddUpalist=bahis_geodata[bahis_geodata['parent']==DisNo]['name'].str.capitalize()
    ddUpalist.name='Upazila'
    ddUpalist=ddUpalist.sort_values()
    return ddUpalist.tolist()


ddDivision = html.Div(
    [
        dbc.Label("Select Division"),
        dcc.Dropdown(
            ddDivlist,
            id="cUDivision",
            clearable=True,
        ),
    ],
    className="mb-4",
)

ddDistrict = html.Div(
    [
        dbc.Label("Select District"),
        dcc.Dropdown(
            id="cUDistrict",
            clearable=True,
        ),
    ],
    className="mb-4",
)

ddUpazila = html.Div(
    [
        dbc.Label("Select Upazila"),
        dcc.Dropdown(
            id="cUUpazila",
            clearable=True,
        ),
    ],
    className="mb-4",
)


def open_data(path):
    with open(path) as f:
        data = json.load(f)
        return data

def plot_map(path, loc, sub_bahis_sourcedata, title, pname, splace, variab, labl, theme):
    subDist=bahis_geodata[(bahis_geodata["loc_type"]==loc)]  
#    reports = sub_bahis_sourcedata[title].value_counts().to_frame()
    reports = sub_bahis_sourcedata.value_counts().to_frame()
    #reports.index = reports.index.astype(int)
    reports[pname] = reports.index
    reports.index = reports.index.astype(int)
    reports= reports.loc[reports[pname] != 'nan']    
    data = open_data(path)

    for i in range(reports.shape[0]):
        #reports[pname].iloc[i] = subDist.loc[subDist['value']==int(reports[pname].iloc[i]),'name'].iloc[0]
        reports[pname].iloc[i] = subDist[subDist['value']==reports.index[i]]['name'].values[0] ###still to work with the copy
    reports[pname]=reports[pname].str.title()  
#    reports.set_index(pname)                 
    for i in data['features']:
        i['id']= i['properties']['shapeName'].replace(splace,"")
    
    fig = px.choropleth_mapbox(reports, geojson=data, locations=pname, color=title,
#                            featureidkey="Cmap",
                            color_continuous_scale="YlOrBr",
                            range_color=(0, reports[title].max()),
                            mapbox_style="carto-positron",
                            zoom=6.4, center = {"lat": 23.7, "lon": 90.3},
                            opacity=0.5,
                            template=template_from_url(theme),
                            labels={variab:labl}
                          )
    fig.update_layout(autosize=True, margin={"r":0,"t":0,"l":0,"b":0}, width=760 , height=800) #, coloraxis_showscale= False) #width= 1000, height=600, 
    return fig

header = html.H4(
    "BAHIS dashboard", className="bg-primary text-white p-2 mb-2 text-center"
)

row = html.Div(
    [ dbc.Row(
            [   dbc.Col(
                    [dbc.Card([ddDivision, ddDistrict, ddUpazila], body=True)
                     ], width=2),
                dbc.Col([
                    dbc.Row([dbc.Card(dcc.Graph(
                                    id='CUMap',
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

#app.layout = dbc.Container(
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

#@app.callback(
@callback(
    Output ('cUUpazila', 'options'),
    Input ('cUDistrict', 'value')
    )
def set_Upalist(cDistrict):  
    ddUpalist=None
    if cDistrict is None:
        ddUpalist="",
        #raise PreventUpdate
    else:
        ddUpalist=fetchUpazilalist(cDistrict)
    return ddUpalist

#@app.callback(
@callback(
        Output ('cUDistrict', 'options'),
        Input ('cUDivision', 'value')
        )
def set_Dislist(cDivision):  
    ddDislist=None
    if cDivision is None:
        ddDislist="",
        #raise PreventUpdate
    else:
        ddDislist=fetchDistrictlist(cDivision)
    return ddDislist

#@app.callback(
@callback(
    Output ('CUMap', 'figure'),
    
    #Output ('RepG2', 'figure'),
    
    #Input("cReport", 'value'),
    Input('CUMap', 'clickData'),    
    Input("cUDivision",'value'),
    Input("cUDistrict",'value'),
    Input("cUUpazila",'value'),
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
)
def update_whatever(geoTile, cUDivision, cUDistrict, cUUpazila, theme):   #cRReport, start_date, end_date, cRDisease, cRDivision, cRDistrict, cRUpazila, theme):   
   

    if geoTile is not None:
        print(geoTile['points'][0]['location'])


    if not cUUpazila:
        if not cUDistrict:
            if not cUDivision:
                path=path3
                loc=3
                title='basic_info_upazila'
                pname='upazilaname'
                splace=' Upazila'
                variab='upazila'
                labl='Incidences per upazila'
            else:
                path=path3
                loc=3
                title='basic_info_upazila'
                pname='upazilaname'
                splace=' Upazila'
                variab='upazila'
                labl='Incidences per upazila'
        else:
            path=path3
            loc=3
            title='basic_info_upazila'
            pname='upazilaname'
            splace=' Upazila'
            variab='Upazila'
            labl='Incidences per Upazila'
    else:
        path=path3
        loc=3
        title='basic_info_upazila'
        pname='upazilaname'
        splace=' Upazila'
        variab='upazila'
        labl='Incidences per upazila'
    
    Rfig = plot_map(path, loc, bahis_sourcedata, title, pname, splace, variab, labl, theme)


    return Rfig

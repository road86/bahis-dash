# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 07:48:14 2023

@author: yoshka
"""

# Import necessary libraries 
import dash
from dash import dcc, html, callback #Dash, #dash_table, dbc 
import plotly.express as px
import dash_bootstrap_components as dbc #dbc deprecationwarning
import pandas as pd
from dash.dependencies import Input, Output
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
import json  

pd.options.mode.chained_assignment = None

dash.register_page(__name__) #, path='/') for entry point probably

sourcepath = 'C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/'
geofilename = sourcepath + 'newbahis_geo_cluster.csv'   # the available geodata from the bahis project
sourcefilename =sourcepath + 'preped_data2.csv'   
path0= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM0_simplified.geojson" #1 Nation # found shapefiles from the data.humdata.org
path1= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM1_simplified.geojson" #8 Division
path2= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM2_simplified.geojson" #64 District
path3= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM3_simplified.geojson" #495 Upazila
# path4= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM4_simplified.geojson" #4562 Union

# only one path is necessary, remove rest potentially

### consider time mask at a later stage, currently only upa selection is focus

def fetchsourcedata():  # count reports / delete variable sdtmp
    bahis_sd=[]
    bahis_sdtmp = pd.read_csv(sourcefilename) 
    bahis_sd = pd.to_numeric(bahis_sdtmp['basic_info_upazila']).dropna().astype(int)
    del bahis_sdtmp
    return bahis_sd
bahis_sourcedata= fetchsourcedata() # later numbers are accumulated for number of reports, maybe accumulate here already.

def fetchgeodata():  
    geodata = pd.read_csv(geofilename)
    geodata = geodata.drop(geodata[(geodata['loc_type']==4) | (geodata['loc_type']==5)].index)
    return geodata
bahis_geodata= fetchgeodata()


def fetchDivisionlist():   #### fetched names; make detour via numbers for all div, dis and upa,
    ddDivlist=bahis_geodata[(bahis_geodata["loc_type"]==1)][['value', 'name']] #.str.capitalize()
    ddDivlist['name']=ddDivlist['name'].str.capitalize()
    ddDivlist=ddDivlist.rename(columns={'name':'Division'})
    ddDivlist=ddDivlist.sort_values(by=['Division'])
    diccc=ddDivlist.to_dict('records')
    return diccc #.tolist()
#    return ddDivlist #.tolist()
ddDivlist=fetchDivisionlist()
#diccc=ddDivlist.to_dict('records')

def fetchDistrictlist(SelDiv):   
#    DivNo= bahis_geodata.loc[(bahis_geodata['name'].str.capitalize()==SelDiv) & (bahis_geodata['loc_type']==1),'value'].values[0]
    DivNo=SelDiv
#    ddDislist=bahis_geodata[bahis_geodata['parent']==DivNo]['name'].str.capitalize()
    ddDislist=bahis_geodata[bahis_geodata['parent']==DivNo][['value','name']] #.str.capitalize()
    ddDislist['name']=ddDislist['name'].str.capitalize()
    ddDislist=ddDislist.rename(columns={'name':'District'})   
#    ddDislist.name='District'
    ddDislist=ddDislist.sort_values(by=['District'])
    diccc=ddDislist.to_dict('records')
    return diccc #.tolist()
#    return ddDislist #.tolist()

def fetchUpazilalist(SelDis):   
#    DisNo= bahis_geodata.loc[(bahis_geodata['name'].str.capitalize()==SelDis) & (bahis_geodata['loc_type']==2),'value'].values[0]
    DisNo=SelDis
    ddUpalist=bahis_geodata[bahis_geodata['parent']==DisNo][['value','name']] #.str.capitalize()
    ddUpalist['name']=ddUpalist['name'].str.capitalize()
    ddUpalist=ddUpalist.rename(columns={'name':'Upazila'})     
#    ddUpalist.name='Upazila'
    ddUpalist=ddUpalist.sort_values(by=['Upazila'])
    diccc=ddUpalist.to_dict('records')
    return diccc #tolist()
#    return ddUpalist #tolist()


## dropdowns encode numbers, somehow hide them

ddDivision = html.Div(
    [
        dbc.Label("Select Division"),
        dcc.Dropdown(
            options=[{'label': i['Division'], 'value': i['value']} for i in ddDivlist],
            #options={'label':ddDivlist['Division'], 'value':ddDivlist['value']},
            #value=ddDivlist['Division'],
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
    subDist=bahis_geodata[(bahis_geodata["loc_type"]==loc)]  # select (here) upazila level (results in 545 values)
#    reports = sub_bahis_sourcedata[title].value_counts().to_frame()
    reports = sub_bahis_sourcedata.value_counts().to_frame() #(results in 492 values, what about the rest, plot the rest where there is nothing)
    reports[pname] = reports.index
    reports.index = reports.index.astype(int)   # upazila name
    reports= reports.loc[reports[pname] != 'nan']    # unknown reason for now. does this have to be beore reports in sub_bahis_sourcedata?
    data = open_data(path)

    for i in range(reports.shape[0]): # go through all upazila report values
        #reports[pname].iloc[i] = subDist.loc[subDist['value']==int(reports[pname].iloc[i]),'name'].iloc[0]
        reports[pname].iloc[i] = subDist[subDist['value']==reports.index[i]]['name'].values[0] ###still to work with the copy , this goes with numbers and nnot names
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

# header = html.H4(
#     "BAHIS dashboard", className="bg-primary text-white p-2 mb-2 text-center"
# ) # included iin navbar

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

# #@app.callback(
# @callback(
#     Output ('cUUpazila', 'options'),
#     Input ('cUDistrict', 'value')
#     )
# def set_Upalist(cUDistrict):  
#     ddUpalist=None
#     if cUDistrict is None:
#         a="", #ddUpalist="",
#         #raise PreventUpdate
#     else:
#         ddUpalist=fetchUpazilalist(cUDistrict)
#         a=[{'label': i['Upazila'], 'value': i['value']} for i in ddUpalist] 
#     return a   
# #    return ddUpalist

# #@app.callback(
# @callback(
#         Output ('cUDistrict', 'options'),
# #        Output ('cUUpazila', 'options'),
#         Input ('cUDivision', 'value')
#         )
# def set_Dislist(cUDivision):  
#     ddDislist=None
#     b="",
#     if cUDivision is None:
#         a="", #ddDislist="",
#         #raise PreventUpdate
#     else:
#         ddDislist=fetchDistrictlist(cUDivision)
#         a = [{'label': i['District'], 'value': i['value']} for i in ddDislist]
#     return a, b 
#     #return ddDislist

#@app.callback(
@callback(
        Output ('cUDistrict', 'options'),
        Output ('cUUpazila', 'options'),
        Input ('cUDivision', 'value'),
        Input ('cUDistrict', 'value')
        )
def set_DisnUpalist(cUDivision, cUDistrict):  
    ddDislist=None
    ddUpalist=None
 

    if cUDivision is None:
        a="", 
        b="",
        #raise PreventUpdate
    else:
        ddDislist=fetchDistrictlist(cUDivision)
        a = [{'label': i['District'], 'value': i['value']} for i in ddDislist]
        if cUDistrict is None:
            b="", 
            #raise PreventUpdate
        else:
            ddUpalist=fetchUpazilalist(cUDistrict)
            b=[{'label': i['Upazila'], 'value': i['value']} for i in ddUpalist] 
    return a, b 
    #return ddDislist

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
        print(geoTile)


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

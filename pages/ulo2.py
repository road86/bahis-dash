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
import json  
from datetime import date
from plotly.subplots import make_subplots
#from shapely.geometry import shape, Point

pd.options.mode.chained_assignment = None

dash.register_page(__name__) #, path='/') for entry point probably

sourcepath = 'C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/'
geofilename = sourcepath + 'newbahis_geo_cluster.csv'   # the available geodata from the bahis project
dgfilename = sourcepath + 'Diseaselist.csv'   # disease grouping info
sourcefilename =sourcepath + 'preped_data2.csv'   
#path0= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM0_simplified.geojson" #1 Nation # found shapefiles from the data.humdata.org
#path1= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM1_simplified.geojson" #8 Division
#path2= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM2_simplified.geojson" #64 District
#path3= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM3_simplified.geojson" #495 Upazila
path3= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/upadata.geojson" #495 Upazila
# path4= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM4_simplified.geojson" #4562 Union

# only one path is necessary, remove rest potentially

### consider time mask at a later stage, currently only upa selection is focus

bahis_sdtmp = pd.read_csv(sourcefilename) 
bahis_sdtmp['basic_info_date'] = pd.to_datetime(bahis_sdtmp['basic_info_date'])
    
def fetchsourcedata():  # count reports / delete variable sdtmp
    bahis_sd=[]
    bahis_sdtmp = pd.read_csv(sourcefilename) 
    bahis_sd = pd.to_numeric(bahis_sdtmp['basic_info_upazila']).dropna().astype(int)
#    del bahis_sdtmp
    return bahis_sd
bahis_sourcedata= fetchsourcedata() # later numbers are accumulated for number of reports, maybe accumulate here already.

def fetchdisgroupdata():
    bahis_dgdata= pd.read_csv(dgfilename)
    bahis_dgdata= bahis_dgdata[['species', 'name', 'id', 'Disease type']]  
    bahis_dgdata= bahis_dgdata[['name', 'Disease type']]
    bahis_dgdata= bahis_dgdata.dropna() 
    return bahis_dgdata
bahis_dgdata= fetchdisgroupdata()

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


start_date=min(bahis_sdtmp['basic_info_date']).date()
end_date=max(bahis_sdtmp['basic_info_date']).date()
start_date=date(2021, 1, 1)

def date_subset(sdate, edate):
    dates=[sdate, edate]
    tmask= (bahis_sdtmp['basic_info_date']>= pd.to_datetime(dates[0])) & (bahis_sdtmp['basic_info_date'] <= pd.to_datetime(dates[1]))
    return bahis_sdtmp.loc[tmask]

ddDivision = html.Div(
    [
        dbc.Label("Select Division"),
        dcc.Dropdown(
            options=[{'label': i['Division'], 'value': i['value']} for i in ddDivlist],
            #options={'label':ddDivlist['Division'], 'value':ddDivlist['value']},
            #value=ddDivlist['Division'],
            id="cU2Division",
            clearable=True,
        ),
    ],
    className="mb-4",
)

ddDistrict = html.Div(
    [
        dbc.Label("Select District"),
        dcc.Dropdown(
            id="cU2District",
            clearable=True,
        ),
    ],
    className="mb-4",
)

ddUpazila = html.Div(
    [
        dbc.Label("Select Upazila"),
        dcc.Dropdown(
            id="cU2Upazila",
            clearable=True,
        ),
    ],
    className="mb-4",
)


def open_data(path):
    with open(path) as f:
        data = json.load(f)
        
        # # upazilanumber
        # for i in range(len(bahis_geodata)):
        #     point = Point(bahis_geodata['longitude'].iloc[i], bahis_geodata['latitude'].iloc[i])
        #     for feature in data['features']:
        #         polygon = shape(feature['geometry'])
        #         if polygon.contains(point):
        #     #        print ('Found polygon:', feature['properties']['shapeName'])
        #             feature['properties']['upazilanumber']=bahis_geodata['value'].iloc[i]
        #             feature['properties']['ccheck_upaname']=bahis_geodata['name'].iloc[i]
        
    return data

def plot_map(path, loc, sub_bahis_sourcedata, title, pname, splace, variab, labl):
    subDist=bahis_geodata[(bahis_geodata["loc_type"]==loc)]  # select (here) upazila level (results in 545 values -> comes from Dhaka and Chittagon and islands in the SW)
    reports = sub_bahis_sourcedata.value_counts().to_frame() #(results in 492 values, what about the rest, plot the rest where there is nothing)
    reports['upazilanumber'] = reports.index
    reports.index = reports.index.astype(int)   # upazila name
    reports['upazilanumber'] = reports['upazilanumber'].astype(int)
    reports= reports.loc[reports['upazilanumber'] != 'nan']    # unknown reason for now. does this have to be beore reports in sub_bahis_sourcedata?
    data = open_data(path)

    reports[pname] = reports.index
    for i in range(reports.shape[0]): # go through all upazila report values
        reports[pname].iloc[i] = subDist[subDist['value']==reports.index[i]]['name'].values[0] ###still to work with the copy , this goes with numbers and nnot names
    reports[pname]=reports[pname].str.title()  
    
    reports.set_index('upazilanumber')                 
        
    fig = px.choropleth_mapbox(reports, geojson=data, locations='upazilanumber', color=title,
                            featureidkey='properties.upazilanumber',
#                            featureidkey="Cmap",
                            color_continuous_scale="YlOrBr",
                            range_color=(0, reports[title].max()),
                            mapbox_style="carto-positron",
                            zoom=6.4, center = {"lat": 23.7, "lon": 90.3},
                            opacity=0.5,
                            labels={'upazila':labl}, 
                            hover_name='upazilaname'
                          )
    fig.update_layout(autosize=True, coloraxis_showscale=False, margin={"r":0,"t":0,"l":0,"b":0}, height=750) #, width=760 , height=800, ) #, coloraxis_showscale= False) #width= 1000, height=600, 
    return fig


layout =  html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col(ddDivision), dbc.Col(ddDistrict), dbc.Col(ddUpazila)
                        ]),
                    dbc.Row(dcc.Graph(id="CU2Map")),
                ]),
                dbc.Col([
                    dbc.Tabs([
                        dbc.Tab([
                            dbc.Row(dcc.Graph(id='RepG2AIO')),
                            dbc.Row(dcc.Graph(id='Sick2AIO')),
                            dbc.Row(dcc.Graph(id='Dead2AIO'))],
                            label='Tab1'),
                        dbc.Tab([
                            dbc.Row(dcc.Graph(id='LiveS2AIO')),
                            dbc.Row(dcc.Graph(id='Zoon2AIO'))],
                            label='Tab2')                        
                        ])
                    ])
            ])
    ])

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 1!", className="card-text"),
            dbc.Button("Click here", color="success"),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)


tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Tab 1"),
        dbc.Tab(tab2_content, label="Tab 2"),
        dbc.Tab(
            "This tab's content is never seen", label="Tab 3", disabled=True
        ),
    ]
)

# layout =  html.Div([
#             dbc.Row([
#                 dbc.Col([
#                     dbc.Row([
#                         dbc.Col(ddDivision), dbc.Col(ddDistrict), dbc.Col(ddUpazila)
#                         ]),
#                     dbc.Row(dcc.Graph(id="CU2Map")),
#                 ]),
#                 dbc.Col([
#                     dbc.Row(dcc.Graph(id='RepG2AIO')),
#                     dbc.Row(dcc.Graph(id='Sick2AIO')),
#                     dbc.Row(dcc.Graph(id='Dead2AIO')),
                    
#                     ])
#             ])
#     ])


# dbc.Container(
#     [dbc.Col([dcc.Graph(id='CU2Map')])
#      ]
#     [
#         html.Div(
#             [ dbc.Row(
#                     [   dbc.Col(
#                             [dbc.Card([ddDivision, ddDistrict, ddUpazila], body=True)
#                              ], width=2),
#         #                 dbc.Col([
#         #                     dbc.Row([dbc.Card(dcc.Graph(
#         #                                     id='CU2Map',
#         # #                                    figure=figMap
#         #                                     ), body=True)])
#         #                     ], width=5
#         #                    ),
#                     ]
#                 ),
#             ]
#         ),
#     ],
#     fluid=True,
#     className="dbc",
# )



#@app.callback(
@callback(
        Output ('cU2District', 'options'),
        Output ('cU2Upazila', 'options'),
        Input ('cU2Division', 'value'),
        Input ('cU2District', 'value')
        )
def set_DisnUpalist(cU2Division, cU2District):  
    ddDislist=None
    ddUpalist=None
 

    if cU2Division is None:
        a="", 
        b="",
        #raise PreventUpdate
    else:
        ddDislist=fetchDistrictlist(cU2Division)
        a = [{'label': i['District'], 'value': i['value']} for i in ddDislist]
        if cU2District is None:
            b="", 
            #raise PreventUpdate
        else:
            ddUpalist=fetchUpazilalist(cU2District)
            b=[{'label': i['Upazila'], 'value': i['value']} for i in ddUpalist] 
    return a, b 
    #return ddDislist
## shape overlay of selected geotile(s)


#@app.callback(
@callback(
    Output ('CU2Map', 'figure'),
    Output ('RepG2AIO', 'figure'),
    Output ('Sick2AIO', 'figure'),
    Output ('Dead2AIO', 'figure'),
    Output ('LiveS2AIO', 'figure'),
    Output ('Zoon2AIO', 'figure'),
    
    Input('CU2Map', 'clickData'),    
    Input("cU2Division",'value'),
    Input("cU2District",'value'),
    Input("cU2Upazila",'value'),
)
def update_whatever(geoTile, cU2Division, cU2District, cU2Upazila):  
   
    if geoTile is not None:
        print(geoTile['points'][0]['location'])
        #print(geoTile)
        ### only names and surrounding shape, find method to identify upazila


    
    path=path3
    loc=3
    title='basic_info_upazila'
    pname='upazilaname'
    splace=' Upazila'
    variab='upazila'
    labl='Incidences per upazila'
    
    Rfig = plot_map(path, loc, bahis_sourcedata, title, pname, splace, variab, labl)

###tab1
    sub_bahis_sourcedata=date_subset(start_date, end_date)
    tmp=sub_bahis_sourcedata['basic_info_date'].dt.date.value_counts()
    tmp=tmp.reset_index()
    tmp=tmp.rename(columns={'index':'date'})
    tmp['date'] = pd.to_datetime(tmp['date']) 
    # tmp=tmp.reset_index()
    # tmp.resample('W-SUN')
    #print(tmp.dtypes)        
    figgR= px.bar(tmp, x='date', y='basic_info_date')  
    figgR.update_layout(height=250, margin={"r":0,"t":0,"l":0,"b":0}) 
    
    tmp=sub_bahis_sourcedata['patient_info_sick_number'].groupby(sub_bahis_sourcedata['basic_info_date'].dt.to_period('W-SUN')).sum().astype(int)
    tmp=tmp.reset_index()
#    tmp['basic_info_date'].resample('W-SUN')
    tmp=tmp.rename(columns={'basic_info_date':'date'})
    tmp['date'] = tmp['date'].astype('datetime64[D]')
    figgSick= px.bar(tmp, x='date', y='patient_info_sick_number')  
    figgSick.update_layout(height=250, margin={"r":0,"t":0,"l":0,"b":0})   

    tmp=sub_bahis_sourcedata['patient_info_dead_number'].groupby(sub_bahis_sourcedata['basic_info_date'].dt.to_period('W-SUN')).sum().astype(int)
    tmp=tmp.reset_index()
#    tmp['basic_info_date'].resample('W-SUN')
    tmp=tmp.rename(columns={'basic_info_date':'date'})
    tmp['date'] = tmp['date'].astype('datetime64[D]')
    figgDead= px.bar(tmp, x='date', y='patient_info_dead_number')  
    figgDead.update_layout(height=250, margin={"r":0,"t":0,"l":0,"b":0})   
    
    ####tab2
    poultry=['Chicken', 'Duck', 'Goose', 'Pegion', 'Quail', 'Turkey']
    sub_bahis_sourcedataP=sub_bahis_sourcedata[sub_bahis_sourcedata['species'].isin(poultry)]

    tmpdg= bahis_dgdata.drop_duplicates(subset='name', keep="first")
    to_replace=tmpdg['name'].tolist()
    replace_with=tmpdg['Disease type'].tolist()
    sub_bahis_sourcedataP['top_diagnosis']= sub_bahis_sourcedataP.top_diagnosis.replace(to_replace, replace_with, regex=True)                                        
    sub_bahis_sourcedataP=sub_bahis_sourcedataP.drop(sub_bahis_sourcedataP[sub_bahis_sourcedataP['top_diagnosis']=='Zoonotic diseases'].index)

    tmp= sub_bahis_sourcedataP.groupby(['top_diagnosis'])['species'].agg('count').reset_index()
    tmp=tmp.sort_values(by='species', ascending=False)
    tmp=tmp.rename({'species' : 'counts'}, axis=1)
    tmp=tmp.head(10)
    tmp=tmp.iloc[::-1]
    fpoul =px.bar(tmp, x='counts', y='top_diagnosis',title='Top10 Poultry Diseases')
    #figg.append_trace(px.bar(tmp, x='counts', y='top_diagnosis',title='Top10 Poultry Diseases'), row=1, col=1) #, labels={'counts': 'Values', 'top_diagnosis': 'Disease'})#, orientation='h')
    
    lanimal=['Buffalo', 'Cattle', 'Goat', 'Sheep']
    sub_bahis_sourcedataLA=sub_bahis_sourcedata[sub_bahis_sourcedata['species'].isin(lanimal)] 
   
    tmpdg= bahis_dgdata.drop_duplicates(subset='name', keep="first")
    to_replace=tmpdg['name'].tolist()
    replace_with=tmpdg['Disease type'].tolist()
    sub_bahis_sourcedataLA['top_diagnosis']= sub_bahis_sourcedataLA.top_diagnosis.replace(to_replace, replace_with, regex=True)  
    sub_bahis_sourcedataLA=sub_bahis_sourcedataLA.drop(sub_bahis_sourcedataLA[sub_bahis_sourcedataLA['top_diagnosis']=='Zoonotic diseases'].index)

    tmp= sub_bahis_sourcedataLA.groupby(['top_diagnosis'])['species'].agg('count').reset_index()
    tmp=tmp.sort_values(by='species', ascending=False)
    tmp=tmp.rename({'species' : 'counts'}, axis=1)
    tmp=tmp.head(10)
    tmp=tmp.iloc[::-1]
    flani = px.bar(tmp, x='counts', y='top_diagnosis',title='Top10 Large Animal Diseases')
    #subpl.add_traces(flani, row=1, col=1)#, row=2, col=1) #, labels={'counts': 'Values', 'top_diagnosis': 'Disease'})#, orientation='h')
    subpl=[fpoul, flani]
    figgLiveS= make_subplots(rows=2, cols=1)
    for i, figure in enumerate(subpl):
        for trace in range(len(figure['data'])):
            figgLiveS.append_trace(figure['data'][trace], row=i+1, col=1)
    figgLiveS.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0}) 
#    if cReport=='Zoonotic Disease Cases':   
    #subpl= make_subplots(rows=2, cols=1),
    poultry=['Chicken', 'Duck', 'Goose', 'Pegion', 'Quail', 'Turkey']
    sub_bahis_sourcedataP=sub_bahis_sourcedata[sub_bahis_sourcedata['species'].isin(poultry)]

    tmpdg= bahis_dgdata.drop_duplicates(subset='name', keep="first")
    tmpdg=tmpdg[tmpdg['Disease type']=='Zoonotic diseases']
    tmpdg=tmpdg['name'].tolist()
    sub_bahis_sourcedataP= sub_bahis_sourcedataP[sub_bahis_sourcedataP['top_diagnosis'].isin(tmpdg)]    
    
    # to_replace=tmpdg['name'].tolist()
    # replace_with=tmpdg['Disease type'].tolist()
    # sub_bahis_sourcedataP['top_diagnosis']= sub_bahis_sourcedataP.top_diagnosis.replace(to_replace, replace_with, regex=True)                                        
    # sub_bahis_sourcedataP=sub_bahis_sourcedataP[sub_bahis_sourcedataP['top_diagnosis']=='Zoonotic diseases']

    tmp= sub_bahis_sourcedataP.groupby(['top_diagnosis'])['species'].agg('count').reset_index()
    tmp=tmp.sort_values(by='species', ascending=False)
    tmp=tmp.rename({'species' : 'counts'}, axis=1)
    tmp=tmp.head(10)
    tmp=tmp.iloc[::-1]
    fpoul =px.bar(tmp, x='counts', y='top_diagnosis',title='Top10 Poultry Diseases')
    #figg.append_trace(px.bar(tmp, x='counts', y='top_diagnosis',title='Top10 Poultry Diseases'), row=1, col=1) #, labels={'counts': 'Values', 'top_diagnosis': 'Disease'})#, orientation='h')
    
    lanimal=['Buffalo', 'Cattle', 'Goat', 'Sheep']
    sub_bahis_sourcedataLA=sub_bahis_sourcedata[sub_bahis_sourcedata['species'].isin(lanimal)] 
  
#        tmpdg= bahis_dgdata.drop_duplicates(subset='name', keep="first")
    sub_bahis_sourcedataLA= sub_bahis_sourcedataLA[sub_bahis_sourcedataLA['top_diagnosis'].isin(tmpdg)]    
    
    # to_replace=tmpdg['name'].tolist()
    # replace_with=tmpdg['Disease type'].tolist()
    # sub_bahis_sourcedataLA['top_diagnosis']= sub_bahis_sourcedataLA.top_diagnosis.replace(to_replace, replace_with, regex=True)  
    # sub_bahis_sourcedataLA=sub_bahis_sourcedataLA[sub_bahis_sourcedataLA['top_diagnosis']=='Zoonotic diseases']

    tmp= sub_bahis_sourcedataLA.groupby(['top_diagnosis'])['species'].agg('count').reset_index()
    tmp=tmp.sort_values(by='species', ascending=False)
    tmp=tmp.rename({'species' : 'counts'}, axis=1)
    tmp=tmp.head(10)
    tmp=tmp.iloc[::-1]
    flani = px.bar(tmp, x='counts', y='top_diagnosis',title='Top10 Large Animal Diseases')
    #subpl.add_traces(flani, row=1, col=1)#, row=2, col=1) #, labels={'counts': 'Values', 'top_diagnosis': 'Disease'})#, orientation='h')
    subpl=[fpoul, flani]
    figgZoon= make_subplots(rows=2, cols=1)
    for i, figure in enumerate(subpl):
        for trace in range(len(figure['data'])):
            figgZoon.append_trace(figure['data'][trace], row=i+1, col=1)
    figgZoon.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0}) 

    return Rfig, figgR, figgSick, figgDead, figgLiveS, figgZoon














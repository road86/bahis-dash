# # -*- coding: utf-8 -*-
# """
# Created on Sun Jan 22 07:48:14 2023

# @author: yoshka
# """

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
path1= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/divdata.geojson" #8 Division
path2= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/distdata.geojson" #64 District
# path1= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM1_simplified.geojson" #8 Division
# path2= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM2_simplified.geojson" #64 District
#path3= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM3_simplified.geojson" #495 Upazila
path3= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/upadata.geojson" #495 Upazila
# path4= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM4_simplified.geojson" #4562 Union

# only one path is necessary, remove rest potentially

### consider time mask at a later stage, currently only upa selection is focus

bahis_sdtmp = pd.read_csv(sourcefilename) 
bahis_sdtmp['basic_info_date'] = pd.to_datetime(bahis_sdtmp['basic_info_date'])
    
# def fetchsourcedata():  # count reports / delete variable sdtmp
#     bahis_sd=[]
#     bahis_sdtmp = pd.read_csv(sourcefilename) 
#     bahis_sd = pd.to_numeric(bahis_sdtmp['basic_info_upazila']).dropna().astype(int)
# #    del bahis_sdtmp
#     return bahis_sd
# bahis_sourcedata= fetchsourcedata() # later numbers are accumulated for number of reports, maybe accumulate here already.


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
            id="Division",
            clearable=True,
        ),
    ],
    className="mb-4",
)

ddDistrict = html.Div(
    [
        dbc.Label("Select District"),
        dcc.Dropdown(
            id="District",
            clearable=True,
        ),
    ],
    className="mb-4",
)

ddUpazila = html.Div(
    [
        dbc.Label("Select Upazila"),
        dcc.Dropdown(
            id="Upazila",
            clearable=True,
        ),
    ],
    className="mb-4",
)


def open_data(path):
    with open(path) as f:
        data = json.load(f)
                
    return data

def plot_map(path, loc, sub_bahis_sourcedata, title, pnumber, pname, splace, variab, labl):
    subDist=bahis_geodata[(bahis_geodata["loc_type"]==loc)]  # select (here) upazila level (results in 545 values -> comes from Dhaka and Chittagon and islands in the SW)
    reports = sub_bahis_sourcedata.value_counts().to_frame() #(results in 492 values, what about the rest, plot the rest where there is nothing)
    reports[pnumber] = reports.index
    reports.index = reports.index.astype(int)   # upazila name
    reports[pnumber] = reports[pnumber].astype(int)
    reports= reports.loc[reports[pnumber] != 'nan']    # unknown reason for now. does this have to be beore reports in sub_bahis_sourcedata?
    data = open_data(path)

    reports[pname] = reports.index
    for i in range(reports.shape[0]): # go through all upazila report values
        reports[pname].iloc[i] = subDist[subDist['value']==reports.index[i]]['name'].values[0] ###still to work with the copy , this goes with numbers and nnot names
    reports[pname]=reports[pname].str.title()  
    
    reports.set_index(pnumber)                 
        
    fig = px.choropleth_mapbox(reports, geojson=data, locations=pnumber, color=title,
                            featureidkey='properties.'+pnumber,
#                            featureidkey="Cmap",
                            color_continuous_scale="YlOrBr",
                            range_color=(0, reports[title].max()),
                            mapbox_style="carto-positron",
                            zoom=6.0, center = {"lat": 23.7, "lon": 90.3},
                            opacity=0.5,
                            labels={variab:labl}, 
                            hover_name=pname
                          )
    fig.update_layout(autosize=True, coloraxis_showscale=False, margin={"r":0,"t":0,"l":0,"b":0}, height=600) #, width=760 , height=800, ) #, coloraxis_showscale= False) #width= 1000, height=600, 
    return fig


layout =  html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col(ddDivision), dbc.Col(ddDistrict), dbc.Col(ddUpazila)
                        ]),
                    dbc.Row(dcc.Graph(id="Map")),
                    dbc.Row(dcc.Slider(min=1, max=3, step=1,
                                       marks={1:'Division', 
                                              2:'District', 
                                              3:'Upazila',}, 
                            value=3,
                            id="geoSlider")
                            )
                ], width= 4),
                dbc.Col([
                    dbc.Tabs([
                        dbc.Tab([
                            dbc.Row(dcc.Graph(id='Reports')),
                            dbc.Row(dcc.Graph(id='Sick')),
                            dbc.Row(dcc.Graph(id='Dead'))],
                            label='Reports'),
                        dbc.Tab([
                            dbc.Row(dcc.Graph(id='Livestock')),
                            dbc.Row(dcc.Graph(id='Zoonotic'))],
                            label='Diseases')                        
                        ])
                    ], width=8)
            ])
    ])


## shape overlay of selected geotile(s)

@callback(
    Output ('District', 'options'),
    Output ('Upazila', 'options'),

    Output ('Map', 'figure'),
    Output ('Reports', 'figure'),
    Output ('Sick', 'figure'),
    Output ('Dead', 'figure'),
    Output ('Livestock', 'figure'),
    Output ('Zoonotic', 'figure'),
#    Output ('geoSlider', 'children'),

    Input ('geoSlider', 'value'),
    Input ('Map', 'clickData'),    
    Input ('Division', 'value'),
    Input ('District', 'value'),
    Input("Upazila",'value'),
)
def update_whatever(geoSlider, geoTile, cU2Division, cU2District, cU2Upazila):  
   
    sub_bahis_sourcedata=date_subset(start_date, end_date)

    ddDislist=None
    ddUpalist=None
    

    if cU2Division is None:
        vDistrict="", 
        vUpa="",
        #raise PreventUpdate
    else:
        ddDislist=fetchDistrictlist(cU2Division)
        vDistrict = [{'label': i['District'], 'value': i['value']} for i in ddDislist]
        if cU2District is None:
            vUpa="", 
            #raise PreventUpdate
        else:
            ddUpalist=fetchUpazilalist(cU2District)
            vUpa=[{'label': i['Upazila'], 'value': i['value']} for i in ddUpalist] 
    
    # if geoTile is not None:
    #     print(geoTile['points'][0]['location'])
        
    if not cU2Upazila:
        if not cU2District:
            if not cU2Division:
                sub_bahis_sourcedata=sub_bahis_sourcedata

            else:
                sub_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata['basic_info_division']==cU2Division] #DivNo]   
 
        else:
            sub_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata['basic_info_district']==cU2District]

    else:
        sub_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata['basic_info_upazila']==cU2Upazila]
    #### change 1 and 2 with bad database check plot map and change value reference
    if geoSlider== 1:
        path=path1
        loc=1
        title='basic_info_division'
        pnumber='divnumber'
        pname='divisionname'
        splace=' Division'
        variab='division'
        labl='Incidences per division'
        bahis_sourcedata = pd.to_numeric(bahis_sdtmp['basic_info_division']).dropna().astype(int)
        # if geoTile is not None:
        #     print(geoTile['points'][0]['location'])
        #     cU2Division=geoTile['points'][0]['location']
        #     ddDislist=fetchDistrictlist(geoTile['points'][0]['location'])
        #     vDistrict = [{'label': i['District'], 'value': i['value']} for i in ddDislist]
    if geoSlider== 2:
        path=path2
        loc=2
        title='basic_info_district'
        pnumber='districtnumber'
        pname='districtname'
        splace=' District'
        variab='district'
        labl='Incidences per district'
        bahis_sourcedata = pd.to_numeric(bahis_sdtmp['basic_info_district']).dropna().astype(int)
    if geoSlider== 3:
        path=path3
        loc=3
        title='basic_info_upazila'
        pnumber='upazilanumber'
        pname='upazilaname'
        splace=' Upazila'
        variab='upazila'
        labl='Incidences per upazila'
        bahis_sourcedata = pd.to_numeric(bahis_sdtmp['basic_info_upazila']).dropna().astype(int)
    
    Rfig = plot_map(path, loc, bahis_sourcedata, title, pnumber, pname, splace, variab, labl)

###tab1

    tmp=sub_bahis_sourcedata['basic_info_date'].dt.date.value_counts()
    tmp=tmp.to_frame()
    tmp['counts']=tmp['basic_info_date']

    tmp['basic_info_date']=pd.to_datetime(tmp.index)
    tmp=tmp['counts'].groupby(tmp['basic_info_date'].dt.to_period('W-SUN')).sum().astype(int)
    tmp=tmp.to_frame()
    tmp['basic_info_date']=tmp.index
    tmp['basic_info_date']=tmp['basic_info_date'].astype('datetime64[D]')
            
    figgR= px.bar(tmp, x='basic_info_date', y='counts') 
    figgR.update_layout(height=225, margin={"r":0,"t":0,"l":0,"b":0}) 
    
    tmp=sub_bahis_sourcedata['patient_info_sick_number'].groupby(sub_bahis_sourcedata['basic_info_date'].dt.to_period('W-SUN')).sum().astype(int)
    tmp=tmp.reset_index()
    tmp=tmp.rename(columns={'basic_info_date':'date'})
    tmp['date'] = tmp['date'].astype('datetime64[D]')
    figgSick= px.bar(tmp, x='date', y='patient_info_sick_number')  
    figgSick.update_layout(height=225, margin={"r":0,"t":0,"l":0,"b":0})   

    tmp=sub_bahis_sourcedata['patient_info_dead_number'].groupby(sub_bahis_sourcedata['basic_info_date'].dt.to_period('W-SUN')).sum().astype(int)
    tmp=tmp.reset_index()
    tmp=tmp.rename(columns={'basic_info_date':'date'})
    tmp['date'] = tmp['date'].astype('datetime64[D]')
    figgDead= px.bar(tmp, x='date', y='patient_info_dead_number')  
    figgDead.update_layout(height=225, margin={"r":0,"t":0,"l":0,"b":0})   
    
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
    fpoul.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0}) 
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
    flani.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})
    #subpl.add_traces(flani, row=1, col=1)#, row=2, col=1) #, labels={'counts': 'Values', 'top_diagnosis': 'Disease'})#, orientation='h')
    subpl=[fpoul, flani]
    figgLiveS= make_subplots(rows=2, cols=1)
    for i, figure in enumerate(subpl):
        for trace in range(len(figure['data'])):
            figgLiveS.append_trace(figure['data'][trace], row=i+1, col=1)
    figgLiveS.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0}) 
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
    fpoul.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) 
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
    flani = px.bar(tmp, x='counts', y='top_diagnosis',title='Top10 Ruminant Diseases')
    flani.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) 
    #subpl.add_traces(flani, row=1, col=1)#, row=2, col=1) #, labels={'counts': 'Values', 'top_diagnosis': 'Disease'})#, orientation='h')
    subpl=[fpoul, flani]
    figgZoon= make_subplots(rows=2, cols=1)
    for i, figure in enumerate(subpl):
        for trace in range(len(figure['data'])):
            figgZoon.append_trace(figure['data'][trace], row=i+1, col=1)
    figgZoon.update_layout(height=180, margin={"r":0,"t":0,"l":0,"b":0}) 

    return vDistrict, vUpa, Rfig, figgR, figgSick, figgDead, figgLiveS, figgZoon
















# from datetime import timedelta
# import plotly.graph_objs as go
# import numpy as np
# from dash import dcc, html
# import dash
# import pandas as pd


# dash.register_page(__name__)

# def holidays():
#     #year = dt.now().year
    
#     d1 = pd.to_datetime('01.01.2022') #dt.date(2022, 8, 1)
#     d2 = pd.to_datetime('01.01.2023') #dt.date(2023, 7, 15)

#     delta = d2 - d1

#     dates_in_year = [d1 + timedelta(i) for i in range(delta.days+1)] #gives me a list with datetimes for each day a year
#     weekdays_in_year = [i.weekday() for i in dates_in_year] #gives [0,1,2,3,4,5,6,0,1,2,3,4,5,6,…] (ticktext in xaxis dict translates this to weekdays
#     weeknumber_of_dates = [i.strftime("%Gww%V")[2:] for i in dates_in_year] #gives [1,1,1,1,1,1,1,2,2,2,2,2,2,2,…] name is self-explanatory
#     z = np.random.randint(2, size=(len(dates_in_year)))
#     text = [str(i) for i in dates_in_year] #gives something like list of strings like ‘2018-01-25’ for each date. Used in data trace to make good hovertext.
#     #4cc417 green #347c17 dark green
#     colorscale=[[False, '#eeeeee'], [True, '#76cf63']]

#     data = [
#     go.Heatmap(
#     x = weeknumber_of_dates,
#     y = weekdays_in_year,
#     z = z,
#     text=text,
#     hoverinfo='text',
#     xgap=3, # this
#     ygap=3, # and this is used to make the grid-like apperance
#     showscale=False,
#     colorscale=colorscale
#     )
#     ]
    
#     layout = go.Layout(
#     title='activity chart',
#     height=280,
#     yaxis=dict(
#     showline = False, showgrid = False, zeroline = False,
#     tickmode='array',
#     ticktext=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
#     tickvals=[0,1,2,3,4,5,6],
#     ),
#     xaxis=dict(
#     showline = False, showgrid = False, zeroline = False,
#     ),
#     font={'size':10, 'color':'#9e9e9e'},
#     plot_bgcolor=('#fff'),
#     margin = dict(t=40),
#     )

#     fig = go.Figure(data=data, layout=layout)
#     return fig

# #app = dash.Dash()
# layout = html.Div([
# dcc.Graph(id='heatmap-test', figure=holidays(), config={'displayModeBar': False})
# ])


# # Import necessary libraries 
# import dash
# from dash import dash_table, dcc, html, callback
# from dash.dependencies import Input, Output
# import pandas as pd
# from datetime import datetime, timedelta
# import numpy as np
# import plotly.express as px

# sourcepath = 'C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/'
# #geofilename = sourcepath + 'newbahis_geo_cluster.csv'   # the available geodata from the bahis project
# sourcefilename =sourcepath + 'preped_data2.csv'   
# bahis_sd = pd.read_csv(sourcefilename)
# img_logo= 'assets/Logo.png'

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
    
#     # restrict to data from 2019
#     tmask= (bahis_sd['basic_info_date']>= pd.to_datetime('01.01.2019')) & (bahis_sd['basic_info_date'] <= pd.to_datetime(bahis_sd['basic_info_date'].max()))
#     sub_data=bahis_sd.loc[tmask]
 
    
#     rep = sub_data.filter(['basic_info_district', 'basic_info_date'], axis=1)
#     rep = rep.groupby('basic_info_district').resample('W-Fri', on='basic_info_date').sum()
#     rep = rep.rename(columns={'basic_info_district': 'reports'})
#     rep = rep.reset_index()
    
#     del bahis_sd
#     #print(rep)
#     return rep
# bahis_sourcedata= fetchsourcedata()

# tmp=bahis_sourcedata['basic_info_district'].unique()
# #tmpp=pd.DataFrame([tmp]).transpose()
# #tmpp.columns=['district']
# wklst=np.arange(bahis_sourcedata['basic_info_date'].max(), bahis_sourcedata['basic_info_date'].min(), timedelta(weeks=-1)).astype(datetime)
# tmpp=pd.DataFrame(data=[], index=tmp, columns=wklst)
# for i in bahis_sourcedata.itertuples():
#     # print(int(i[1]))
#     # print(pd.to_datetime(i[2]))
#     # print(int(i[3]))
#     tmpp.loc[i[1],pd.to_datetime(i[2])]=int(i[3])
    

#                 # sub_bahis_sourcedata= sub_bahis_sourcedata

#                 # path=path2
#                 # loc=2
#                 # title='basic_info_district'
#                 # pname='districtname'
#                 # splace=' District'
#                 # variab='district'
#                 # labl='Incidences per district'
#     # subDist=bahis_geodata[(bahis_geodata["loc_type"]==loc)]
#     # reports = sub_bahis_sourcedata[title].value_counts().to_frame()
#     # reports[pname] = reports.index
#     # reports= reports.loc[reports[pname] != 'nan']

#     # data = open_data(path)
#     # for i in data['features']:
#     #     i['id']= i['properties']['shapeName'].replace(" Division","")
#     # for i in range(reports.shape[0]):
#     #     reports[pname].iloc[i] = subDist.loc[subDist['value']==int(reports[pname].iloc[i]),'name'].iloc[0]
#     # reports=reports.sort_values(pname)
#     # reports[pname]=reports[pname].str.capitalize()
        
#     # Rfigg=px.bar(reports, x=pname, y=title, labels= {variab:labl})# ,color='basic_info_division')
#     # Rfigg.update_layout(autosize=True, height=500, margin={"r":0,"t":0,"l":0,"b":0}) # width= 100, height=500, margin={"r":0,"t":0,"l":0,"b":0})

# bahis_sourcedata['id'] = bahis_sourcedata['basic_info_district']
# bahis_sourcedata.set_index('id', inplace=True, drop=False)


# ##df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
# # add an id column and set it as the index
# # in this case the unique ID is just the country name, so we could have just
# # renamed 'country' to 'id' (but given it the display name 'country'), but
# # here it's duplicated just to show the more general pattern.

# fig=px.imshow(tmpp)


# ##df['id'] = df['country']
# ##df.set_index('id', inplace=True, drop=False)

# #app = Dash(__name__)
# dash.register_page(__name__)

# layout = html.Div([
#     dcc.Graph(figure=fig)
# #1    dash_table.DataTable(
# #1        tmpp.to_dict('records'), [{"name": i, "id": i} for i in tmpp.columns])
# #     dash_table.DataTable(
# #         id='datatable-row-ids',
# #         columns=[
# #             {'name': i, 'id': i, 'deletable': True} for i in tmpp.columns
# # #            {'name': i, 'id': i, 'deletable': True} for i in bahis_sourcedata.columns
# # #            {'name': i, 'id': i, 'deletable': True} for i in df.columns
# #             # omit the id column
# #             if i != 'id'
# #         ],
# #         data=tmpp.to_dict('records'),
# # #        data=bahis_sourcedata.to_dict('records'),
# # #        data=df.to_dict('records'),
# #         editable=True,
# #         filter_action="native",
# #         sort_action="native",
# #         sort_mode='multi',
# #         row_selectable='multi',
# #         row_deletable=True,
# #         selected_rows=[],
# #         page_action='native',
# #         page_current= 0,
# #         page_size= 10,
# #     ),
# #     html.Div(id='datatable-row-ids-container')
# ])


# # @callback(
# #     Output('datatable-row-ids-container', 'children'),
# #     Input('datatable-row-ids', 'derived_virtual_row_ids'),
# #     Input('datatable-row-ids', 'selected_row_ids'),
# #     Input('datatable-row-ids', 'active_cell'))
# # def update_graphs(row_ids, selected_row_ids, active_cell):
# #     # When the table is first rendered, `derived_virtual_data` and
# #     # `derived_virtual_selected_rows` will be `None`. This is due to an
# #     # idiosyncrasy in Dash (unsupplied properties are always None and Dash
# #     # calls the dependent callbacks when the component is first rendered).
# #     # So, if `rows` is `None`, then the component was just rendered
# #     # and its value will be the same as the component's dataframe.
# #     # Instead of setting `None` in here, you could also set
# #     # `derived_virtual_data=df.to_rows('dict')` when you initialize
# #     # the component.
# #     selected_id_set = set(selected_row_ids or [])

# #     if row_ids is None:
# #         dff = tmpp
# # #        dff = bahis_sourcedata
# # #        dff = df
# #         # pandas Series works enough like a list for this to be OK
# #         row_ids = tmpp['id']
# # #        row_ids = bahis_sourcedata['id']
# # #        row_ids = df['id']
# #     else:
# #         dff = tmpp.loc[row_ids]
# # #        dff = bahis_sourcedata.loc[row_ids]
# # #        dff = df.loc[row_ids]

# #     active_row_id = active_cell['row_id'] if active_cell else None

# #     colors = ['#FF69B4' if id == active_row_id
# #               else '#7FDBFF' if id in selected_id_set
# #               else '#0074D9'
# #               for id in row_ids]

# #     return [
# #         dcc.Graph(
# #             id=column + '--row-ids',
# #             figure={
# #                 'data': [
# #                     {
# #                         'x': dff['basic_info_district'],
# # #                        'x': dff['basic_info_district'],
# # #                        'x': dff['country'],
# #                         'y': dff[column],
# #                         'type': 'bar',
# #                         'marker': {'color': colors},
# #                     }
# #                 ],
# #                 'layout': {
# #                     'xaxis': {'automargin': True},
# #                     'yaxis': {
# #                         'automargin': True,
# #                         'title': {'text': column}
# #                     },
# #                     'height': 250,
# #                     'margin': {'t': 10, 'l': 10, 'r': 10},
# #                 },
# #             },
# #         )
# #         # check if column exists - user may have deleted it
# #         # If `column.deletable=False`, then you don't
# #         # need to do this check.
# #         for column in ['basic_info_date', 'reports'] if column in dff
# # #        for column in ['pop', 'lifeExp', 'gdpPercap'] if column in dff
# #     ]


# # if __name__ == '__main__':
# #     app.run_server(debug=True)

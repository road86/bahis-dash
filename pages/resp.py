# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 18:07:34 2023

@author: yoshka
"""


# Import necessary libraries 
import dash
from dash import dcc, html, callback #, ctx #Dash, #dash_table, dbc 
import plotly.express as px
import dash_bootstrap_components as dbc #dbc deprecationwarning
import pandas as pd
from dash.dependencies import Input, Output
import json  
from datetime import date


pd.options.mode.chained_assignment = None

#dash.register_page(__name__) #, path='/') for entry point probably

sourcepath = 'exported_data/'
geofilename = sourcepath + 'newbahis_geo_cluster.csv'   # the available geodata from the bahis project
sourcefilename =sourcepath + 'resp_data.csv'   
path1= "geodata/divdata.geojson" #8 Division
path2= "geodata/distdata.geojson" #64 District
path3= "geodata/upadata.geojson" #495 Upazila

resp_data = pd.read_csv(sourcefilename) 
resp_data['date'] = pd.to_datetime(resp_data['date'])
    
def fetchgeodata():  
    geodata = pd.read_csv(geofilename)
    geodata = geodata.drop(geodata[(geodata['loc_type']==4) | (geodata['loc_type']==5)].index)
    return geodata
geodata= fetchgeodata()


def fetchDivisionlist():   #### fetched names; make detour via numbers for all div, dis and upa,
    ddDivlist=geodata[(geodata["loc_type"]==1)][['value', 'name']] #.str.capitalize()
    ddDivlist['name']=ddDivlist['name'].str.capitalize()
    ddDivlist=ddDivlist.rename(columns={'name':'Division'})
    ddDivlist=ddDivlist.sort_values(by=['Division'])
    diccc=ddDivlist.to_dict('records')
    return diccc
ddDivlist=fetchDivisionlist()

def fetchDistrictlist(SelDiv):   
    DivNo=SelDiv
    ddDislist=geodata[geodata['parent']==DivNo][['value','name']] #.str.capitalize()
    ddDislist['name']=ddDislist['name'].str.capitalize()
    ddDislist=ddDislist.rename(columns={'name':'District'})   
    ddDislist=ddDislist.sort_values(by=['District'])
    diccc=ddDislist.to_dict('records')
    return diccc

def fetchUpazilalist(SelDis):   
    DisNo=SelDis
    ddUpalist=geodata[geodata['parent']==DisNo][['value','name']] #.str.capitalize()
    ddUpalist['name']=ddUpalist['name'].str.capitalize()
    ddUpalist=ddUpalist.rename(columns={'name':'Upazila'})     
    ddUpalist=ddUpalist.sort_values(by=['Upazila'])
    diccc=ddUpalist.to_dict('records')
    return diccc 

start_date=min(resp_data['date']).date()
end_date=max(resp_data['date']).date()


def date_subset(sdate, edate):
    dates=[sdate, edate]
    tmask= (resp_data['date']>= pd.to_datetime(dates[0])) & (resp_data['date'] <= pd.to_datetime(dates[1]))
    return resp_data.loc[tmask]

def disease_subset(cDisease, dis_sub_data):
    if 'All Diseases' in cDisease:
        dis_sub_data=dis_sub_data 
    else:
        dis_sub_data=dis_sub_data[dis_sub_data['disease'].isin(cDisease)] 
    return dis_sub_data

ddDivision = html.Div(
    [
        dbc.Label("Select Division"),
        dcc.Dropdown(
            options=[{'label': i['Division'], 'value': i['value']} for i in ddDivlist],
            id="rDivision",
            clearable=True,
        ),
    ],
    className="mb-4",
)

ddDistrict = html.Div(
    [
        dbc.Label("Select District"),
        dcc.Dropdown(
            id="rDistrict",
            clearable=True,
        ),
    ],
    className="mb-4",
)

ddUpazila = html.Div(
    [
        dbc.Label("Select Upazila"),
        dcc.Dropdown(
            id="rUpazila",
            clearable=True,
        ),
    ],
    className="mb-4",
)

def fetchdiseaselist():
    dislis= resp_data['disease'].unique()
    dislis= pd.DataFrame(dislis, columns=['disease'])
    ddDList= dislis['disease'].sort_values()
    return ddDList.tolist()
ddDList= fetchdiseaselist()
ddDList.insert(0, 'All Diseases')


def open_data(path):
    with open(path) as f:
        data = json.load(f)             
    return data

def plot_map(path, loc, sub_data, title, pnumber, pname, splace, variab, labl):
    subDist=geodata[(geodata["loc_type"]==loc)]  # select (here) upazila level (results in 545 values -> comes from Dhaka and Chittagon and islands in the SW)
    reports = sub_data.value_counts().to_frame() #(results in 492 values, what about the rest, plot the rest where there is nothing)
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
                            color_continuous_scale="YlOrBr",
                            range_color=(0, reports[title].max()),
                            mapbox_style="carto-positron",
                            zoom=5.8, center = {"lat": 23.7, "lon": 90.3},
                            opacity=0.5,
                            labels={variab:labl}, 
                            hover_name=pname
                          )
    fig.update_layout(autosize=True, coloraxis_showscale=False, margin={"r":0,"t":0,"l":0,"b":0}, height=550) #, width=760 , height=800, ) #, coloraxis_showscale= False) #width= 1000, height=600, 
    return fig


layout =  html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col(ddDivision), dbc.Col(ddDistrict), dbc.Col(ddUpazila)
                        ]),
#                    dbc.Row(dcc.RangeSlider(min=1, max=104, marks={1:'1', 104:'104'}, step=1, value=[1,104], id="test")),
                    dbc.Row(dcc.Graph(id="rMap")),
                    dbc.Row(dcc.Slider(min=1, max=3, step=1,
                                       marks={1:'Division', 
                                              2:'District', 
                                              3:'Upazila',}, 
                            value=3,
                            id="rgeoSlider")
                            )
                ], width= 4),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dcc.DatePickerRange(
                                    id='rdaterange',
                                    min_date_allowed=start_date,
                                    start_date=date(end_date.year-1, end_date.month, end_date.day),
                                    max_date_allowed=end_date,
                                    initial_visible_month=end_date,
                                    end_date=end_date
                                ),
                            ]),
                        dbc.Col([
                            dcc.Dropdown(
                                ddDList,
                                "All Diseases",
                                id="rDiseaselist",
                                multi=True,
                                clearable=False,
                                ),
                            ])                        
                        ]),
                    dbc.Row([
                        dbc.Row(dcc.Graph(id='rReports')),
                        dbc.Row(dcc.Graph(id='rSick')),
                        dbc.Row(dcc.Graph(id='rDead'))
                        ])
                        #label='rReports'),
                    ], width=8)
            ])
    ])


## shape overlay of selected geotile(s)

@callback(
    Output ('rDistrict', 'options'),
    Output ('rUpazila', 'options'),

    Output ('rMap', 'figure'),
    Output ('rReports', 'figure'),
    Output ('rSick', 'figure'),
    Output ('rDead', 'figure'),

    Input ('rgeoSlider', 'value'),
    Input ('rMap', 'clickData'),  
    Input ('rReports', 'clickData'),  
    Input ('rSick', 'clickData'),  
    Input ('rDead', 'clickData'),  
    
    Input ('rDivision', 'value'),
    Input ('rDistrict', 'value'),
    Input ("rUpazila",'value'),
    Input ("rdaterange",'start_date'),
    Input ("rdaterange",'end_date'),
    Input ("rDiseaselist",'value'),
)
def update_whatever(rgeoSlider, geoTile, clkRep, clkSick, clkDead, rDivision, rDistrict, rUpazila, start_date, end_date, diseaselist):      
    date_sub=date_subset(start_date, end_date)
    sub_data=disease_subset(diseaselist, date_sub)

    ddDislist=None
    ddUpalist=None
    

    if rDivision is None:
        vDistrict="", 
        vUpa="",
    else:
        ddDislist=fetchDistrictlist(rDivision)
        vDistrict = [{'label': i['District'], 'value': i['value']} for i in ddDislist]
        if rDistrict is None:
            vUpa="", 
            #raise PreventUpdate
        else:
            ddUpalist=fetchUpazilalist(rDistrict)
            vUpa=[{'label': i['Upazila'], 'value': i['value']} for i in ddUpalist]        
    if not rUpazila:
        if not rDistrict:
            if not rDivision:
                sub_data=sub_data
            else:
                sub_data= sub_data.loc[sub_data['division']==rDivision] #DivNo]   
 
        else:
            sub_data= sub_data.loc[sub_data['district']==rDistrict]

    else:
        sub_data= sub_data.loc[sub_data['upazila']==rUpazila]
    #### change 1 and 2 with bad database check plot map and change value reference
    if rgeoSlider== 1:
        path=path1
        loc=1
        title='division'
        pnumber='divnumber'
        pname='divisionname'
        splace=' Division'
        variab='division'
        labl='Incidences per division'
        incsub_data = pd.to_numeric(sub_data['division']).dropna().astype(int)
    if rgeoSlider== 2:
        path=path2
        loc=2
        title='district'
        pnumber='districtnumber'
        pname='districtname'
        splace=' District'
        variab='district'
        labl='Incidences per district'
        incsub_data = pd.to_numeric(sub_data['district']).dropna().astype(int)
    if rgeoSlider== 3:
        path=path3
        loc=3
        title='upazila'
        pnumber='upazilanumber'
        pname='upazilaname'
        splace=' Upazila'
        variab='upazila'
        labl='Incidences per upazila'
        incsub_data = pd.to_numeric(sub_data['upazila']).dropna().astype(int)
    
    Rfig = plot_map(path, loc, incsub_data, title, pnumber, pname, splace, variab, labl)

###tab1

    tmp=sub_data['date'].dt.date.value_counts()
    tmp=tmp.to_frame()
    tmp['counts']=tmp['date']

    tmp['date']=pd.to_datetime(tmp.index)
    tmp=tmp['counts'].groupby(tmp['date'].dt.to_period('W-SAT')).sum().astype(int)
    tmp=tmp.to_frame()
    tmp['date']=tmp.index
    tmp['date']=tmp['date'].astype('datetime64[D]')
            
    figgR= px.bar(tmp, x='date', y='counts') 
    figgR.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0}) 
    
    tmp=sub_data['cases'].groupby(sub_data['date'].dt.to_period('W-SAT')).sum().astype(int)
    tmp=tmp.reset_index()
    tmp=tmp.rename(columns={'date':'date'})
    tmp['date'] = tmp['date'].astype('datetime64[D]')
    figgSick= px.bar(tmp, x='date', y='cases')  
    figgSick.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})   

    tmp=sub_data['deaths'].groupby(sub_data['date'].dt.to_period('W-SAT')).sum().astype(int)
    tmp=tmp.reset_index()
    tmp=tmp.rename(columns={'date':'date'})
    tmp['date'] = tmp['date'].astype('datetime64[D]')
    figgDead= px.bar(tmp, x='date', y='deaths')  
    figgDead.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})   
    


    return vDistrict, vUpa, Rfig, figgR, figgSick, figgDead










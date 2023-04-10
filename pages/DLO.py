# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 08:14:39 2023

@author: yoshka
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 10:13:47 2023

@author: yoshka
"""


# Import necessary libraries
import dash
from dash import dcc, html, callback, ctx#Dash, #dash_table, dbc
import plotly.express as px
import dash_bootstrap_components as dbc #dbc deprecationwarning
import pandas as pd
from dash.dependencies import Input, Output
import os, glob
from datetime import date, datetime
import numpy as np 


pd.options.mode.chained_assignment = None

dash.register_page(__name__)    #register page to main dash app

#sourcepath='C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/'    #for local debugging purposes
sourcepath = 'exported_data/'
sourcefilename =os.path.join(sourcepath, 'preped_data2.csv')  
geofilename = glob.glob(sourcepath + 'newbahis_geo_cluster*.csv')[-1]

firstrun=True
vDis=[]
vUpa=[]

def fetchgeodata():     #fetch geodata from bahis, delete mouzas and unions
    geodata = pd.read_csv(geofilename)
    geodata = geodata.drop(geodata[(geodata['loc_type']==4) | (geodata['loc_type']==5)].index)  #drop mouzas and unions
    geodata=geodata.drop(['id', 'longitude', 'latitude', 'updated_at'], axis=1)
    geodata['parent']=geodata[['parent']].astype(np.uint16)   # assuming no mouza and union is taken into 
    geodata[['value']]=geodata[['value']].astype(np.uint32)   
    geodata[['loc_type']]=geodata[['loc_type']].astype(np.uint8)
    return geodata
bahis_geodata= fetchgeodata()


def fetchDivisionlist(bahis_geodata):   # division lsit is always the same, caching possible
    Divlist=bahis_geodata[(bahis_geodata["loc_type"]==1)][['value', 'name']] 
    Divlist['name']=Divlist['name'].str.capitalize()
    Divlist=Divlist.rename(columns={'name':'Division'})
    Divlist=Divlist.sort_values(by=['Division'])
    return Divlist.to_dict('records')
Divlist=fetchDivisionlist(bahis_geodata)


def fetchDistrictlist(SelDiv, bahis_geodata): # district list is dependent on selected division
    Dislist=bahis_geodata[bahis_geodata['parent']==SelDiv][['value','name']] 
    Dislist['name']=Dislist['name'].str.capitalize()
    Dislist=Dislist.rename(columns={'name':'District'})
    Dislist=Dislist.sort_values(by=['District'])
    return Dislist.to_dict('records')

def fetchUpazilalist(SelDis, bahis_geodata):   # upazila list is dependent on selected district
    Upalist=bahis_geodata[bahis_geodata['parent']==SelDis][['value','name']] #.str.capitalize()
    Upalist['name']=Upalist['name'].str.capitalize()
    Upalist=Upalist.rename(columns={'name':'Upazila'})
    Upalist=Upalist.sort_values(by=['Upazila'])
    return Upalist.to_dict('records')


layout =  html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.Label("Select Division"),
                        dcc.Dropdown(
                            options=[{'label': i['Division'], 'value': i['value']} for i in Divlist],
                            id="DLO_Division",
                            clearable=True,
                        ), 
                    ])
                ]),
                dbc.Col([
                    dbc.Card([
                        dbc.Label("Select District"),
                        dcc.Dropdown(
                            id="DLO_District",
                            clearable=True,
                        ),
                    ])
                ]),
                dbc.Col([
                    dbc.Card([
                        dbc.Label("Select Upazila"),
                        dcc.Dropdown(
                            id="DLO_Upazila",
                            clearable=True,
                        )
                    ])
                ])
            ]),
        dbc.Row([
            (dcc.Graph(id='DLO_Reports')),
            ]),
        dbc.Row([
            (dcc.Graph(id='DLO_Sick')),
            ]),
        dbc.Row([
            (dcc.Graph(id='DLO_Dead')),
            ])
            
])
                        


## shape overlay of selected geotile(s)

@callback(                             #splitting callbacks to prevent updates?
                              #dash cleintsied callback with js
    Output ('DLO_District', 'options'),
    Output ('DLO_Upazila', 'options'),
    Output ('DLO_Reports', 'figure'),
    Output ('DLO_Sick', 'figure'),
    Output ('DLO_Dead', 'figure'),


    Input ('DLO_Division', 'value'),
    Input ('DLO_District', 'value'),
    Input ("DLO_Upazila",'value'),

)

def selectDLO(SelDiv, SelDis, SelUpa):
    global bahis_geodata, vDis, vUpa, firstrun, bahis_data

    starttime_tab1=datetime.now()
    
    end_date=date(2023,3,1)
    # bahis_data=pd.DataFrame(columns=['date'])
    figDLORep={}    
    figDLOSick={}    
    figDLODead={}    
    # tmp = pd.DataFrame(columns=['date','counts'])
    
    if firstrun==True:
        vDis=[]
        vUpa=[]
        firstrun=False
    
    if ctx.triggered_id=='DLO_Division':
        if not SelDiv:      
            vDis="",
        else:
            Dislist=fetchDistrictlist(SelDiv, bahis_geodata)
            vDis = [{'label': i['District'], 'value': i['value']} for i in Dislist]
            vUpa="",
            
    if ctx.triggered_id=='DLO_District':
        if not SelDis:
            Dislist=fetchDistrictlist(SelDiv, bahis_geodata)
            vDis = [{'label': i['District'], 'value': i['value']} for i in Dislist]
            vUpa="",            
        else: 
            Upalist=fetchUpazilalist(SelDis, bahis_geodata)
            vUpa=[{'label': i['Upazila'], 'value': i['value']} for i in Upalist]
            
            bahis_data = pd.read_csv(sourcefilename)
            bahis_data= bahis_data.loc[bahis_data['basic_info_district']==SelDis]
            bahis_data['from_static_bahis']=bahis_data['basic_info_date'].str.contains('/') # new data contains -, old data contains /
            bahis_data['basic_info_date'] = pd.to_datetime(bahis_data['basic_info_date'])      
            del bahis_data['Unnamed: 0']
            bahis_data=bahis_data.rename(columns={'basic_info_date':'date', 
                                                'basic_info_division':'division', 
                                                'basic_info_district':'district', 
                                                'basic_info_upazila':'upazila',
                                                'patient_info_species':'species_no',
                                                'diagnosis_treatment_tentative_diagnosis':'tentative_diagnosis',
                                                'patient_info_sick_number':'sick',
                                                'patient_info_dead_number':'dead',
                                                })
            bahis_data[['division', 'district', 'species_no']]=bahis_data[['division', 'district', 'species_no']].astype(np.uint16)   
            bahis_data[['upazila', 'sick', 'dead']]=bahis_data[['upazila',  'sick', 'dead']].astype(np.uint32)
            bahis_data['dead'] = bahis_data['dead'].clip(lower=0)
            bahis_data=bahis_data[bahis_data['date']>=datetime(2019, 7, 1)]
            bahis_geodata=bahis_geodata.loc[bahis_geodata['value'].astype('string').str.startswith(str(SelDis))]
            print(bahis_data.shape)
            print(bahis_geodata.shape)
            
            tmp=bahis_data['date'].dt.date.value_counts()
            tmp=tmp.to_frame()
            tmp['counts']=tmp['date']
            tmp['date']=pd.to_datetime(tmp.index)
            tmp=tmp['counts'].groupby(tmp['date'].dt.to_period('W-SAT')).sum().astype(int)
            tmp=tmp.to_frame()
            tmp['date']=tmp.index
            tmp['date']=tmp['date'].astype('datetime64[D]')
            
            figDLORep= px.bar(tmp, x='date', y='counts', labels={'date':'Date', 'counts':'No. of Reports'})
            figDLORep.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})
            figDLORep.add_annotation(
                x=end_date,
                y=max(tmp),
                text="total reports " + str('{:,}'.format(bahis_data['date'].dt.date.value_counts().sum())),
                showarrow=False,
                font=dict(
                    family="Courier New, monospace",
                    size=12,
                    color="#ffffff"
                    ),
                align="center",
        
                bordercolor="#c7c7c7",
                borderwidth=2,
                borderpad=4,
                bgcolor="#ff7f0e",
                opacity=0.8
                )
            tmp=bahis_data[['sick','dead']].groupby(bahis_data['date'].dt.to_period('W-SAT')).sum().astype(int)
            tmp=tmp.reset_index()
            tmp=tmp.rename(columns={'date':'date'})
            tmp['date'] = tmp['date'].astype('datetime64[D]')
            figDLOSick= px.bar(tmp, x='date', y='sick', labels={'date':'Date', 'sick':'No. of Sick Animals'})
            figDLOSick.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})
            figDLOSick.add_annotation(
                x=end_date,
                y=max(tmp),
                text="total sick " + str('{:,}'.format(int(bahis_data['sick'].sum()))), ###realy outlyer
                showarrow=False,
                font=dict(
                    family="Courier New, monospace",
                    size=12,
                    color="#ffffff"
                    ),
                align="center",
                bordercolor="#c7c7c7",
                borderwidth=2,
                borderpad=4,
                bgcolor="#ff7f0e",
                opacity=0.8
                )
        
            figDLODead= px.bar(tmp, x='date', y='dead', labels={'date':'Date', 'dead':'No. of Dead Animals'})
            figDLODead.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})
            figDLODead.add_annotation(
                x=end_date,
                y=max(tmp),
                text="total dead " + str('{:,}'.format(int(bahis_data['dead'].sum()))), ###really
                showarrow=False,
                font=dict(
                    family="Courier New, monospace",
                    size=12,
                    color="#ffffff"
                    ),
                align="center",
                bordercolor="#c7c7c7",
                borderwidth=2,
                borderpad=4,
                bgcolor="#ff7f0e",
                opacity=0.8
                )
            
    if ctx.triggered_id=='DLO_Upazila':            
        if not SelUpa:      ##### currently fast but eventually keep tmp values to not caluclate a second time
            tmp=bahis_data['date'].dt.date.value_counts()
            tmp=tmp.to_frame()
            tmp['counts']=tmp['date']
            tmp['date']=pd.to_datetime(tmp.index)
            tmp=tmp['counts'].groupby(tmp['date'].dt.to_period('W-SAT')).sum().astype(int)
            tmp=tmp.to_frame()
            tmp['date']=tmp.index
            tmp['date']=tmp['date'].astype('datetime64[D]')
            
            figDLORep= px.bar(tmp, x='date', y='counts', labels={'date':'Date', 'counts':'No. of Reports'})
            figDLORep.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})
            figDLORep.add_annotation(
                x=end_date,
                y=max(tmp),
                text="total reports " + str('{:,}'.format(bahis_data['date'].dt.date.value_counts().sum())),
                showarrow=False,
                font=dict(
                    family="Courier New, monospace",
                    size=12,
                    color="#ffffff"
                    ),
                align="center",
        
                bordercolor="#c7c7c7",
                borderwidth=2,
                borderpad=4,
                bgcolor="#ff7f0e",
                opacity=0.8
                )
            tmp=bahis_data[['sick','dead']].groupby(bahis_data['date'].dt.to_period('W-SAT')).sum().astype(int)
            tmp=tmp.reset_index()
            tmp=tmp.rename(columns={'date':'date'})
            tmp['date'] = tmp['date'].astype('datetime64[D]')
            figDLOSick= px.bar(tmp, x='date', y='sick', labels={'date':'Date', 'sick':'No. of Sick Animals'})
            figDLOSick.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})
            figDLOSick.add_annotation(
                x=end_date,
                y=max(tmp),
                text="total sick " + str('{:,}'.format(int(bahis_data['sick'].sum()))), ###realy outlyer
                showarrow=False,
                font=dict(
                    family="Courier New, monospace",
                    size=12,
                    color="#ffffff"
                    ),
                align="center",
                bordercolor="#c7c7c7",
                borderwidth=2,
                borderpad=4,
                bgcolor="#ff7f0e",
                opacity=0.8
                )
        
            figDLODead= px.bar(tmp, x='date', y='dead', labels={'date':'Date', 'dead':'No. of Dead Animals'})
            figDLODead.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})
            figDLODead.add_annotation(
                x=end_date,
                y=max(tmp),
                text="total dead " + str('{:,}'.format(int(bahis_data['dead'].sum()))), ###really
                showarrow=False,
                font=dict(
                    family="Courier New, monospace",
                    size=12,
                    color="#ffffff"
                    ),
                align="center",
                bordercolor="#c7c7c7",
                borderwidth=2,
                borderpad=4,
                bgcolor="#ff7f0e",
                opacity=0.8
                )

        else:
            bahis_upadata = bahis_data
            bahis_upadata= bahis_data.loc[bahis_upadata['upazila']==SelUpa]
            bahis_upageodata=bahis_geodata.loc[bahis_geodata['value'].astype('string').str.startswith(str(SelUpa))]
            print(bahis_upadata.shape)
            print(bahis_upageodata.shape)
            
            tmp=bahis_upadata['date'].dt.date.value_counts()
            tmp=tmp.to_frame()
            tmp['counts']=tmp['date']
            tmp['date']=pd.to_datetime(tmp.index)
            tmp=tmp['counts'].groupby(tmp['date'].dt.to_period('W-SAT')).sum().astype(int)
            tmp=tmp.to_frame()
            tmp['date']=tmp.index
            tmp['date']=tmp['date'].astype('datetime64[D]')
            
            figDLORep= px.bar(tmp, x='date', y='counts', labels={'date':'Date', 'counts':'No. of Reports'})
            figDLORep.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})
            figDLORep.add_annotation(
                x=end_date,
                y=max(tmp),
                text="total reports " + str('{:,}'.format(bahis_data['date'].dt.date.value_counts().sum())),
                showarrow=False,
                font=dict(
                    family="Courier New, monospace",
                    size=12,
                    color="#ffffff"
                    ),
                align="center",
        
                bordercolor="#c7c7c7",
                borderwidth=2,
                borderpad=4,
                bgcolor="#ff7f0e",
                opacity=0.8
                )
            tmp=bahis_upadata[['sick','dead']].groupby(bahis_upadata['date'].dt.to_period('W-SAT')).sum().astype(int)
            tmp=tmp.reset_index()
            tmp=tmp.rename(columns={'date':'date'})
            tmp['date'] = tmp['date'].astype('datetime64[D]')
            figDLOSick= px.bar(tmp, x='date', y='sick', labels={'date':'Date', 'sick':'No. of Sick Animals'})
            figDLOSick.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})
            figDLOSick.add_annotation(
                x=end_date,
                y=max(tmp),
                text="total sick " + str('{:,}'.format(int(bahis_data['sick'].sum()))), ###realy outlyer
                showarrow=False,
                font=dict(
                    family="Courier New, monospace",
                    size=12,
                    color="#ffffff"
                    ),
                align="center",
                bordercolor="#c7c7c7",
                borderwidth=2,
                borderpad=4,
                bgcolor="#ff7f0e",
                opacity=0.8
                )
        
            figDLODead= px.bar(tmp, x='date', y='dead', labels={'date':'Date', 'dead':'No. of Dead Animals'})
            figDLODead.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})
            figDLODead.add_annotation(
                x=end_date,
                y=max(tmp),
                text="total dead " + str('{:,}'.format(int(bahis_data['dead'].sum()))), ###really
                showarrow=False,
                font=dict(
                    family="Courier New, monospace",
                    size=12,
                    color="#ffffff"
                    ),
                align="center",
                bordercolor="#c7c7c7",
                borderwidth=2,
                borderpad=4,
                bgcolor="#ff7f0e",
                opacity=0.8
                )
 
    endtime_tab1 = datetime.now()
    print('DLO timing : ' + str(endtime_tab1-starttime_tab1))   

    return vDis, vUpa, figDLORep, figDLOSick, figDLODead

# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 10:13:47 2023

@author: yoshka
"""


# Import necessary libraries
import dash
from dash import dcc, html, callback, ctx, dash_table #Dash, #dash_table, dbc
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc #dbc deprecationwarning
import pandas as pd
from dash.dependencies import Input, Output, State
import json, os, glob
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from plotly.subplots import make_subplots
import numpy as np 
from dash.exceptions import PreventUpdate
from dash.dash import no_update

pd.options.mode.chained_assignment = None

dash.register_page(__name__)    #register page to main dash app

#sourcepath='C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/'    #for local debugging purposes
sourcepath = 'exported_data/'
sourcefilename =os.path.join(sourcepath, 'preped_data2.csv')  
geofilename = glob.glob(sourcepath + 'newbahis_geo_cluster*.csv')[-1]

firstrun=True
vDis=[]
vUpa=[]
dislis=[]
maxdates=[]
startDate=None
endDate=None
Diseases=None


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

def resetvalues():
    # firstrun=True
    # UpaSelected=False
    figULORep={}    
    figULOSick={}    
    figULODead={}  
    # UpaSelected=True
    minSelDate=""
    maxSelDate=""
    startDate=None
    endDate=None
    disabSelDate=True
    Diseases=None
    dislis=[]
    return figULORep, figULOSick, figULODead, minSelDate, maxSelDate, startDate, endDate, disabSelDate, Diseases, dislis


def updateFig(bahis_data):
    tmpR=bahis_data['date'].value_counts()
    tmpR=tmpR.to_frame()
    tmpR['counts']=tmpR['date']
    tmpR['date']=pd.to_datetime(tmpR.index)
    timediff=maxdates[1]- maxdates[0] 

    if timediff <= timedelta(days=30):
        tmpR=tmpR['counts'].groupby(tmpR['date']).sum().astype(int)
        tmpR=tmpR.resample('D').sum().fillna(0)
        tmpSD=bahis_data[['sick','dead']].groupby(bahis_data['date']).sum().astype(int)  
        tmpSD=tmpSD.resample('D').sum().fillna(0)
    elif timediff > timedelta(days=30):
        tmpR=tmpR['counts'].groupby(tmpR['date'].dt.to_period('W-SAT')).sum().astype(int)
        tmpSD=bahis_data[['sick','dead']].groupby(bahis_data['date'].dt.to_period('W-SAT')).sum().astype(int)  
        
    tmpR=tmpR.to_frame()
    tmpR['date']=tmpR.index
    tmpR['date']=tmpR['date'].astype('datetime64[D]')
   
    tmpSD=tmpSD.reset_index()
    tmpSD=tmpSD.rename(columns={'date':'date'})
    tmpSD['date'] = tmpSD['date'].astype('datetime64[D]')
        
    figULORep={}
    if timediff <= timedelta(days=30):
        figULORep= px.line(tmpR, x='date', y='counts', labels={'date':'Date', 'counts':'No. of Reports'}, markers=True)
    elif timediff > timedelta(days=30): 
        figULORep= px.bar(tmpR, x='date', y='counts', labels={'date':'Date', 'counts':'No. of Reports'})
    figULORep.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})
    figULORep.add_annotation(
        x=maxdates[1],
        y=max(tmpR),
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
    
    figULOSick={}
    if timediff <= timedelta(days=30):
        figULOSick= px.line(tmpSD, x='date', y='sick', labels={'date':'Date', 'sick':'No. of Sick Animals'}, markers=True)
    elif timediff > timedelta(days=30): 
        figULOSick= px.bar(tmpSD, x='date', y='sick', labels={'date':'Date', 'sick':'No. of Sick Animals'})
    figULOSick.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})
    figULOSick.add_annotation(
        x=maxdates[1],
        y=max(tmpSD),
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
    figULOSick.update_yaxes(rangemode="tozero")
    
    figULODead={}
    if timediff <= timedelta(days=30):
        figULODead= px.line(tmpSD, x='date', y='dead', labels={'date':'Date', 'dead':'No. of Dead Animals'}, markers=True)
    elif timediff > timedelta(days=30): 
        figULODead= px.bar(tmpSD, x='date', y='dead', labels={'date':'Date', 'dead':'No. of Dead Animals'})
    figULODead.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})
    figULODead.add_annotation(
        x=maxdates[1],
        y=max(tmpSD),
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
    return figULORep, figULOSick, figULODead


layout =  html.Div([

            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Alert")),
                    dbc.ModalBody("No data available for this selection"),
                ],
                id="modal",
                is_open=False,
            ),
            
    
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dcc.Dropdown(
                            options=[{'label': i['Division'], 'value': i['value']} for i in Divlist],
                            id="ULO_Division",
                            placeholder="Select Division",
                            clearable=True,
                        ), 
                    ])
                ]),
                dbc.Col([
                    dbc.Card([
                        dcc.Dropdown(
                            id="ULO_District",
                            placeholder="Select District",
                            clearable=True,
                        ),
                    ])
                ]),
                dbc.Col([
                    dbc.Card([
                        dcc.Dropdown(
                            id="ULO_Upazila",
                            placeholder="Select Upazila",                            
                            clearable=True,
                        )
                    ])
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id="ULO_dislis",
                        placeholder="Select Disease",
                        multi=True,
                        clearable=True,
                        )
                    ]),
                dbc.Col([
                    dcc.DatePickerRange(
                        id='ULO_SelDate',
                        display_format='D MMM, YYYY',
                        updatemode="bothdates",
                        clearable=True
                    ),
                    ])
                ]),
            dbc.Row([
                (dcc.Graph(id='ULO_Reports')),
                ]),
            dbc.Row([
                (dcc.Graph(id='ULO_Sick')),
                ]),
            dbc.Row([
                (dcc.Graph(id='ULO_Dead')),
                ]),
                        
])
                        


## shape overlay of selected geotile(s)

@callback(                             #splitting callbacks to prevent updates?
                              #dash cleintsied callback with js
    Output ('ULO_Division', 'value'),
    Output ('ULO_District', 'value'),
    Output ('ULO_Upazila', 'value'),
    Output ('ULO_District', 'options'),
    Output ('ULO_Upazila', 'options'),
    Output ('ULO_dislis', 'options'),
    Output ('ULO_dislis', 'value'),
    Output ('ULO_SelDate', 'min_date_allowed'),
    Output ('ULO_SelDate', 'max_date_allowed'),
    Output ('ULO_SelDate', 'start_date'),
    Output ('ULO_SelDate', 'end_date'),
    Output ('ULO_SelDate', 'disabled'),    
    Output ('ULO_Reports', 'figure'),
    Output ('ULO_Sick', 'figure'),
    Output ('ULO_Dead', 'figure'),
    Output ("modal", "is_open"),

    Input ('ULO_Division', 'value'),
    Input ('ULO_District', 'value'),
    Input ('ULO_Upazila','value'),
    Input ('ULO_dislis','value'),
    Input ('ULO_SelDate', 'start_date'),
    Input ('ULO_SelDate', 'end_date'),
    
    State("modal", "is_open"),

)

def selectULO(SelDiv, SelDis, SelUpa, SelDiseases, sdate, edate, is_open): #, alert):
    global bahis_data, bahis_subdata, bahis_geodata, vDis, vUpa, dislis, Diseases, firstrun, maxdates,  startDate, endDate, disabSelDate, UpaSelected #, end_date

    starttime_tab1=datetime.now()
        
    minSelDate=""
    maxSelDate=""
    figULORep={}    
    figULOSick={}    
    figULODead={}    
    
    if firstrun==True:
        disabSelDate=True
        SelDiv=""
        SelDiseases=""
        vDis=[]
        vUpa=[]
        dislis=[]
        firstrun=False
        UpaSelected=False
        
    
    if ctx.triggered_id=='ULO_dislis' or ctx.triggered_id=='ULO_SelDate':
        if edate is not None:
            startDate=sdate
            endDate=edate
            bahis_subdata=bahis_data[(bahis_data['date']>= sdate) & (bahis_data['date']<= edate)]
            maxdates=[min(bahis_data['date']),max(bahis_data['date'])] 
            minSelDate=maxdates[0]
            maxSelDate=maxdates[1]
            maxdates=[pd.Timestamp(sdate),pd.Timestamp(edate)] 

#            if len(SelDiseases) != 0:
            if SelDiseases:
                if 'All Diseases' in SelDiseases:
                    bahis_subdata=bahis_subdata
                else:
                    bahis_subdata=bahis_subdata[bahis_subdata['top_diagnosis'].isin(SelDiseases)]
            
            figULORep, figULOSick, figULODead = updateFig(bahis_subdata)
        else:
            startDate=None
            endDate=None
            bahis_subdata=bahis_data
            maxdates=[min(bahis_data['date']),max(bahis_data['date'])] 
            minSelDate=maxdates[0]
            maxSelDate=maxdates[1]

#            if len(SelDiseases) != 0:
            if SelDiseases:
                if 'All Diseases' in SelDiseases:
                    bahis_subdata=bahis_subdata
                else:
                    bahis_subdata=bahis_subdata[bahis_subdata['top_diagnosis'].isin(SelDiseases)]
            figULORep, figULOSick, figULODead = updateFig(bahis_subdata)
        Diseases=SelDiseases
            
    if ctx.triggered_id=='ULO_Division':
        if not SelDiv:      
            vDis=[]
            SelDis=""
            vUpa=[]
            dislis=[]
            figULORep, figULOSick, figULODead, minSelDate, maxSelDate, startDate, endDate, disabSelDate, Diseases, dislis = resetvalues()
        else:
            Dislist=fetchDistrictlist(SelDiv, bahis_geodata)
            vDis = [{'label': i['District'], 'value': i['value']} for i in Dislist]
            vUpa="",
            figULORep, figULOSick, figULODead, minSelDate, maxSelDate, startDate, endDate, disabSelDate, Diseases, dislis = resetvalues()
            
    if ctx.triggered_id=='ULO_District':
        if not SelDis:
            figULORep, figULOSick, figULODead, minSelDate, maxSelDate, startDate, endDate, disabSelDate, Diseases, dislis = resetvalues()
            Dislist=fetchDistrictlist(SelDiv, bahis_geodata)
            vDis = [{'label': i['District'], 'value': i['value']} for i in Dislist]
            vUpa="", 
            SelUpa=""
        else: 
            Upalist=fetchUpazilalist(SelDis, bahis_geodata)
            vUpa=[{'label': i['Upazila'], 'value': i['value']} for i in Upalist]
            
    if ctx.triggered_id=='ULO_Upazila':            
        if SelUpa:
            UpaSelected=True
            minSelDate=""
            maxSelDate=""
            disabSelDate=True
            SelDiseases=""
            dislis=[]
            bahis_data = pd.read_csv(sourcefilename)
            bahis_data= bahis_data.loc[bahis_data['basic_info_upazila']==SelUpa]
            bahis_data['from_static_bahis']=bahis_data['basic_info_date'].str.contains('/') # new data contains -, old data contains /
            bahis_data['basic_info_date'] = pd.to_datetime(bahis_data['basic_info_date'])
            del bahis_data['Unnamed: 0']
            bahis_data=bahis_data.rename(columns={'basic_info_date':'date', 
                                                'basic_info_division':'division', 
                                                'basic_info_district':'district', 
                                                'basic_info_upazila':'upazila',
                                                'patient_info_species':'species_no',
                                                'diagnosis_treatment_top_diagnosis':'top_diagnosis',
                                                'patient_info_sick_number':'sick',
                                                'patient_info_dead_number':'dead',
                                                })
            bahis_data[['division', 'district', 'species_no']]=bahis_data[['division', 'district', 'species_no']].astype(np.uint16)   
            bahis_data[['upazila', 'sick', 'dead']]=bahis_data[['upazila',  'sick', 'dead']].astype(np.int32)
            bahis_data['dead'] = bahis_data['dead'].clip(lower=0)
#            maxdates=[min(bahis_data['date']),max(bahis_data['date'])] 
#            bahis_data=bahis_data[bahis_data['date'].dt.date>= maxdates[1]-relativedelta(months=12)] #datetime(2019, 7, 1)]
            if not bahis_data.shape[0] == 0:
                bahis_data=bahis_data[bahis_data['date'].dt.year== max(bahis_data['date']).year]
                maxdates=[min(bahis_data['date']),max(bahis_data['date'])] 
                disabSelDate=False
                minSelDate=maxdates[0]
                maxSelDate=maxdates[1]
    
                dislis= bahis_data['top_diagnosis'].unique()
                dislis= pd.DataFrame(dislis, columns=['Disease'])
                dislis= dislis['Disease'].sort_values().tolist()
                dislis.insert(0, 'All Diseases')
                          
                figULORep, figULOSick, figULODead = updateFig(bahis_data)
            else:

                return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, not is_open

        else:
            figULORep, figULOSick, figULODead, minSelDate, maxSelDate, startDate, endDate, disabSelDate, Diseases, dislis = resetvalues()

             
    endtime_tab1 = datetime.now()
    print('ULO timing : ' + str(endtime_tab1-starttime_tab1))   

    return SelDiv, SelDis, SelUpa, vDis, vUpa, dislis, Diseases, minSelDate, maxSelDate, startDate, endDate, disabSelDate, figULORep, figULOSick, figULODead, no_update


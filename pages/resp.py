# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 18:07:34 2023

@author: yoshka
"""


# Import necessary libraries 
import dash
from dash import dcc, html, callback #, ctx #Dash, #dash_table, dbc 
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc #dbc deprecationwarning
import pandas as pd
from dash.dependencies import Input, Output
import json  
from datetime import date
from dateutil.relativedelta import relativedelta


pd.options.mode.chained_assignment = None

dash.register_page(__name__) #, path='/') for entry point probably

lpath='C:/Users/yoshka/Documents/GitHub/bahis-dash/'
npath=''
sourcepath = lpath+'exported_data/'
geofilename = sourcepath + 'newbahis_geo_cluster.csv'   # the available geodata from the bahis project
sourcefilename =sourcepath + 'resp_data.csv'   
reportsfilename =sourcepath + 'resp_rep_data.csv'  
path1= "geodata/divdata.geojson" #8 Division
path2= "geodata/distdata.geojson" #64 District
path3= "geodata/upadata.geojson" #495 Upazila

resp_data = pd.read_csv(sourcefilename) 
resp_data['date'] = pd.to_datetime(resp_data['date'])

resp_rep_data = pd.read_csv(sourcefilename) 
resp_rep_data['date'] = pd.to_datetime(resp_rep_data['date'])
    
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
start_date=date(2023, 1, 1)


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
                                    start_date=start_date,
#                                    start_date=date(end_date.year-1, end_date.month, end_date.day),
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
                        dbc.Tabs([
                            dbc.Tab([
                                dbc.Row(dcc.Graph(id='Livestock')),
                                dbc.Row(dcc.Graph(id='Zoonotic'))],
                                label='Reports'),                     
                            dbc.Tab([
 #                               dbc.Row(dcc.Graph(id='rReports')),
                                dbc.Row(dcc.Graph(id='rSick')),
                                dbc.Row(dcc.Graph(id='rDead'))],
                            label='Disease Cases')
                            ])                                
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
#    Output ('rReports', 'figure'),
    Output ('rSick', 'figure'),
    Output ('rDead', 'figure'),

    Input ('rgeoSlider', 'value'),
    Input ('rMap', 'clickData'),  
#    Input ('rReports', 'clickData'),  
    Input ('rSick', 'clickData'),  
    Input ('rDead', 'clickData'),  
    
    Input ('rDivision', 'value'),
    Input ('rDistrict', 'value'),
    Input ("rUpazila",'value'),
    Input ("rdaterange",'start_date'),
    Input ("rdaterange",'end_date'),
    Input ("rDiseaselist",'value'),
)
def update_whatever(rgeoSlider, geoTile, clkSick, clkDead, rDivision, rDistrict, rUpazila, start_date, end_date, diseaselist):       #clkRep, 
    date_sub=date_subset(start_date, end_date)
    sub_data=disease_subset(diseaselist, date_sub)

    tmp1as= pd.to_datetime(start_date)-relativedelta(years=1)   
    tmp1ae= pd.to_datetime(start_date)-relativedelta(days=1)
    sub1a_data=date_subset(tmp1as, tmp1ae)
    sub1a_data=disease_subset(diseaselist, sub1a_data)

    tmp2as= pd.to_datetime(start_date)-relativedelta(years=2)   
    tmp2ae= pd.to_datetime(start_date)-relativedelta(years=1)-relativedelta(days=1)
    sub2a_data=date_subset(tmp2as, tmp2ae)
    sub2a_data=disease_subset(diseaselist, sub2a_data)


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
                sub1a_data=sub1a_data
            else:
                sub_data= sub_data.loc[sub_data['division']==rDivision] #DivNo]   
                sub1a_data= sub1a_data.loc[sub1a_data['division']==rDivision] #DivNo]   
        else:
            sub_data= sub_data.loc[sub_data['district']==rDistrict]
            sub1a_data= sub1a_data.loc[sub1a_data['district']==rDistrict]
    else:
        sub_data= sub_data.loc[sub_data['upazila']==rUpazila]
        sub1a_data= sub1a_data.loc[sub_data['upazila']==rUpazila]
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

    # tmp=sub_data['date'].dt.date.value_counts()
    # tmp=tmp.to_frame()
    # tmp['counts']=tmp['date']

    # tmp['date']=pd.to_datetime(tmp.index)
    # tmp=tmp['counts'].groupby(tmp['date'].dt.to_period('W-SAT')).sum().astype(int)
    # tmp=tmp.to_frame()
    # tmp['date']=tmp.index
    # tmp['date']=tmp['date'].astype('datetime64[D]')

    # tmp2=sub1a_data['date'].dt.date.value_counts()
    # tmp2=tmp2.to_frame()
    # tmp2['counts']=tmp2['date']

    # tmp2['date']=pd.to_datetime(tmp2.index)
    # tmp2=tmp2['counts'].groupby(tmp2['date'].dt.to_period('W-SAT')).sum().astype(int)
    # tmp2=tmp2.to_frame()
    # tmp2['date']=tmp2.index
    # tmp2['date']=tmp2['date'].astype('datetime64[D]')
    # tmp2['date']=tmp2['date']+pd.offsets.Day(365)
            
    # figgR= px.bar(tmp, x='date', y='counts') 
    # figgR.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0}) 
 
    # figgRR = px.line(tmp2, x='date', y='counts')
    # figgRR['data'][0]['line']['color']='rgb(204, 0, 0)'
    # figgRR['data'][0]['line']['width']=1
    # figgR= go.Figure(data=figgR.data + figgRR.data)
    # figgR.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0}) 
    # figgR.add_annotation(
    #     x=end_date,
    #     y=max(tmp),
    #     #xref="x",
    #     #yref="y",
    #     text="total reports " + str('{:,}'.format(sub_data['date'].dt.date.value_counts().sum())),
    #     showarrow=False,
    #     font=dict(
    #         family="Courier New, monospace",
    #         size=12,
    #         color="#ffffff"
    #         ),
    #     align="center",
    #     #arrowhead=2,
    #     #arrowsize=1,
    #     #arrowwidth=2,
    #     #arrowcolor="#636363",
    #     #ax=20,
    #     #ay=-30,
    #     bordercolor="#c7c7c7",
    #     borderwidth=2,
    #     borderpad=4,
    #     bgcolor="#ff7f0e",
    #     opacity=0.8
    #     )
    
    
    tmp=sub_data['cases'].groupby(sub_data['date'].dt.to_period('W-SAT')).sum().astype(int)
    tmp=tmp.reset_index()
    tmp=tmp.rename(columns={'date':'date'})
    tmp['date'] = tmp['date'].astype('datetime64[D]')

    tmp1a=sub1a_data['cases'].groupby(sub1a_data['date'].dt.to_period('W-SAT')).sum().astype(int)
    tmp1a=tmp1a.reset_index()
    tmp1a=tmp1a.rename(columns={'date':'date'})
    tmp1a['date'] = tmp1a['date'].astype('datetime64[D]')
    tmp1a['date']=tmp1a['date']+pd.offsets.Day(365)
    
    figgSick= px.bar(tmp, x='date', y='cases')  
    figgSick.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})   

    figgSickk= px.line(tmp1a, x='date', y='cases')  
    figgSickk['data'][0]['line']['color']='rgb(204, 0, 0)'
    figgSickk['data'][0]['line']['width']=1
    figgSick= go.Figure(data=figgSick.data + figgSickk.data)
    figgSick.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0}) 
    figgSick.add_annotation(
        x=end_date,
        y=max(tmp1a),
        #xref="x",
        #yref="y",
        text="total reports " + str('{:,}'.format(sub_data['date'].dt.date.value_counts().sum())),
        showarrow=False,
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="#ffffff"
            ),
        align="center",
        #arrowhead=2,
        #arrowsize=1,
        #arrowwidth=2,
        #arrowcolor="#636363",
        #ax=20,
        #ay=-30,
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="#ff7f0e",
        opacity=0.8
    )

    tmp=sub_data['deaths'].groupby(sub_data['date'].dt.to_period('W-SAT')).sum().astype(int)
    tmp=tmp.reset_index()
    tmp=tmp.rename(columns={'date':'date'})
    tmp['date'] = tmp['date'].astype('datetime64[D]')
    
    tmp1a=sub1a_data['deaths'].groupby(sub1a_data['date'].dt.to_period('W-SAT')).sum().astype(int)
    tmp1a=tmp1a.reset_index()
    tmp1a=tmp1a.rename(columns={'date':'date'})
    tmp1a['date'] = tmp1a['date'].astype('datetime64[D]')
    tmp1a['date']=tmp1a['date']+pd.offsets.Day(365)
    
    figgDead= px.bar(tmp, x='date', y='deaths')  
    figgDead.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})   
    
    figgDeadd= px.line(tmp1a, x='date', y='deaths')  
    figgDeadd['data'][0]['line']['color']='rgb(204, 0, 0)'
    figgDeadd['data'][0]['line']['width']=1
    figgDead= go.Figure(data=figgDead.data + figgDeadd.data)
    figgDead.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0}) 
    figgDead.add_annotation(
        x=end_date,
        y=max(tmp1a),
        #xref="x",
        #yref="y",
        text="total reports " + str('{:,}'.format(sub_data['date'].dt.date.value_counts().sum())),
        showarrow=False,
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="#ffffff"
            ),
        align="center",
        #arrowhead=2,
        #arrowsize=1,
        #arrowwidth=2,
        #arrowcolor="#636363",
        #ax=20,
        #ay=-30,
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="#ff7f0e",
        opacity=0.8
    )


    return vDistrict, vUpa, Rfig, figgSick, figgDead #figgR, 










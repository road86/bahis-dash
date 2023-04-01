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
from dash import dcc, html, callback, ctx #Dash, #dash_table, dbc
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc #dbc deprecationwarning
import pandas as pd
from dash.dependencies import Input, Output
import json, os, glob
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from plotly.subplots import make_subplots
import numpy as np 

pd.options.mode.chained_assignment = None

dash.register_page(__name__)    #register page to main dash app

#sourcepath='C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/'    #for local debugging purposes
#path0= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM0_simplified.geojson" #1 Nation # reminder: found shapefiles from the data.humdata.org
sourcepath = 'exported_data/'
geofilename = glob.glob(sourcepath + 'newbahis_geo_cluster*.csv')[-1]   # the available geodata from the bahis project (Masterdata)
dgfilename = os.path.join(sourcepath, 'Diseaselist.csv')   # disease grouping info (Masterdata)
sourcefilename =os.path.join(sourcepath, 'preped_data2.csv')    # main data resource of prepared data from old and new bahis
path1= "geodata/divdata.geojson" #8 Division
path2= "geodata/distdata.geojson" #64 District
path3= "geodata/upadata.geojson" #495 Upazila

firstrun=True

def fetchsourcedata(): #fetch and prepare source data
    bahis_data = pd.read_csv(sourcefilename)
    bahis_data['from_static_bahis']=bahis_data['basic_info_date'].str.contains('/') # new data contains -, old data contains /
    bahis_data['basic_info_date'] = pd.to_datetime(bahis_data['basic_info_date'])      
#    bahis_data = pd.to_numeric(bahis_data['basic_info_upazila']).dropna().astype(int) # empty upazila data can be eliminated, if therre is
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
    #assuming non negative values from division, district, upazila, speciesno, sick and dead
    bahis_data[['division', 'district', 'species_no']]=bahis_data[['division', 'district', 'species_no']].astype(np.uint16)   
    bahis_data[['upazila', 'sick', 'dead']]=bahis_data[['upazila',  'sick', 'dead']].astype(np.uint32)
#    bahis_data[['species', 'tentative_diagnosis', 'top_diagnosis']]=bahis_data[['species', 'tentative_diagnosis', 'top_diagnosis']].astype(str) # can you change object to string and does it make a memory difference`?
    bahis_data['dead'] = bahis_data['dead'].clip(lower=0)
    bahis_data=bahis_data[bahis_data['date']>=datetime(2019, 7, 1)]
    return bahis_data
bahis_data=fetchsourcedata() 

def sne_date(bahis_data):
    start_date=min(bahis_data['date']).date()
    end_date=max(bahis_data['date']).date()
    dates=[start_date, end_date]
    return dates

start_date=date(2019, 1, 1)
end_date=date(2023,3,1)
dates=[start_date, end_date]

ddDList=[]
Divlist=[]
def fetchdisgroupdata(): #fetch and prepare disease groups
    bahis_dgdata= pd.read_csv(dgfilename)
#    bahis_dgdata= bahis_dgdata[['species', 'name', 'id', 'Disease type']] remark what might be helpful: reminder: memory size
    bahis_dgdata= bahis_dgdata[['name', 'Disease type']] 
    bahis_dgdata= bahis_dgdata.dropna()
#    bahis_dgdata[['name', 'Disease type']] = str(bahis_dgdata[['name', 'Disease type']])    #can you change object to string and does it make a memory difference?
    return bahis_dgdata
bahis_dgdata= fetchdisgroupdata()

def fetchgeodata():     #fetch geodata from bahis, delete mouzas and unions
    geodata = pd.read_csv(geofilename)
    geodata = geodata.drop(geodata[(geodata['loc_type']==4) | (geodata['loc_type']==5)].index)  #drop mouzas and unions
    geodata=geodata.drop(['id', 'longitude', 'latitude', 'updated_at'], axis=1)
    geodata['parent']=geodata[['parent']].astype(np.uint16)   # assuming no mouza and union is taken into 
    geodata[['value']]=geodata[['value']].astype(np.uint32)   
    geodata[['loc_type']]=geodata[['loc_type']].astype(np.uint8)
    return geodata
bahis_geodata= fetchgeodata()

#cache these values

def fetchDivisionlist(bahis_geodata):   # division lsit is always the same, caching possible
    Divlist=bahis_geodata[(bahis_geodata["loc_type"]==1)][['value', 'name']] 
    Divlist['name']=Divlist['name'].str.capitalize()
    Divlist=Divlist.rename(columns={'name':'Division'})
    Divlist=Divlist.sort_values(by=['Division'])
    return Divlist.to_dict('records')
#Divlist=fetchDivisionlist()


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


def date_subset(dates, bahis_data):
    
    tmask= (bahis_data['date']>= pd.to_datetime(dates[0])) & (bahis_data['date'] <= pd.to_datetime(dates[1]))
    return bahis_data.loc[tmask]

def disease_subset(cDisease, sub_bahis_sourcedata):
    if 'All Diseases' in cDisease:
        sub_bahis_sourcedata=sub_bahis_sourcedata
    else:
        sub_bahis_sourcedata=sub_bahis_sourcedata[sub_bahis_sourcedata['top_diagnosis'].isin(cDisease)]
    return sub_bahis_sourcedata

ddDivision = html.Div(
    [
        dbc.Label("Select Division"),
        dcc.Dropdown(
            options=[{'label': i['Division'], 'value': i['value']} for i in Divlist],
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

def fetchdiseaselist(bahis_data):
    dislis= bahis_data['top_diagnosis'].unique()
    dislis= pd.DataFrame(dislis, columns=['Disease'])
    dislis= dislis['Disease'].sort_values().tolist()
    dislis.insert(0, 'All Diseases')
    return dislis

def natNo(sub_bahis_sourcedata):
    mask=(sub_bahis_sourcedata['date']>= datetime.now()-timedelta(days=7)) & (sub_bahis_sourcedata['date'] <= datetime.now())
    ################print(mask.value_counts(True])
    tmp_sub_data=sub_bahis_sourcedata['date'].loc[mask]
    diff=tmp_sub_data.shape[0]

    tmp_sub_data=sub_bahis_sourcedata['sick'].loc[mask]
    diffsick=int(tmp_sub_data.sum().item())

    tmp_sub_data=sub_bahis_sourcedata['dead'].loc[mask]
    diffdead=int(tmp_sub_data.sum().item())
    return([diff, diffsick, diffdead])

def fIndicator(sub_bahis_sourcedata):

    [diff, diffsick, diffdead]=natNo(sub_bahis_sourcedata)

    RfigIndic = go.Figure()

    RfigIndic.add_trace(go.Indicator(
        mode = "number+delta",
        title = 'Total Reports',
        value = sub_bahis_sourcedata.shape[0], #f"{bahis_sourcedata.shape[0]:,}"),
        delta = {'reference': sub_bahis_sourcedata.shape[0]-diff}, #'f"{diff:,}"},
        domain = {'row': 0, 'column': 0}))

    RfigIndic.add_trace(go.Indicator(
        mode = "number+delta",
        title = 'Sick Animals',
        value = sub_bahis_sourcedata['sick'].sum(), #f"{int(bahis_sourcedata['sick'].sum()):,}",
        delta= {'reference': sub_bahis_sourcedata['sick'].sum()-diffsick}, #f"{diffsick:,}",
        domain = {'row': 0, 'column': 1}))

    RfigIndic.add_trace(go.Indicator(
        mode = "number+delta",
        title = 'Dead Animals',
        value = sub_bahis_sourcedata['dead'].sum(), #f"{int(bahis_sourcedata['dead'].sum()):,}",
        delta = {'reference': sub_bahis_sourcedata['dead'].sum()-diffdead}, #f"{diffdead:,}",
        domain = {'row': 0, 'column': 2},
        ))

    RfigIndic.update_layout(height=235,
        grid = {'rows': 1, 'columns': 3},# 'pattern': "independent"},
        #?template=template_from_url(theme),

        )
    return RfigIndic


def open_data(path):
    with open(path) as f:
        data = json.load(f)
    return data


        # path=path3
        # loc=3
        # title='upazila'
        # pnumber='upazilanumber'
        # pname='upazilaname'
        # splace=' Upazila'
        # variab='upazila'
        # labl='Incidences per upazila'
        # incsub_bahis_sourcedata = pd.to_numeric(sub_bahis_sourcedata['upazila']).dropna().astype(int)
        

def plot_map(path, loc, subDist, reports, title, pnumber, pname, splace, variab, labl):
#    reports = sub_bahis_sourcedata
    reports[pnumber] = reports.index #1
#    print (reports)
    reports.index = reports.index.astype(int)   # upazila name
    reports[pnumber] = reports[pnumber].astype(int)
    reports= reports.loc[reports[pnumber] != 'nan']    # unknown reason for now. does this have to be beore reports in sub_bahis_sourcedata? reports, where there are no geonumbers?
    data = open_data(path) #1

    reports[pname] = reports.index
    tmp=subDist[['value', 'name']]
    tmp=tmp.rename(columns={'value':pnumber, 'name':pname})
    tmp[pname]=tmp[pname].str.title()
    tmp['Index']=tmp[pnumber]
    tmp=tmp.set_index('Index')
    tmp[title]=-(reports[title].max())

    # works somewhat, but now preselection of district is also -1 set -1 only for selected ones.

#    for i in range(tmp.shape[0]):
#    aaa=pd.merge(tmp, reports, how="left", on=[pnumber])
    aaa=reports.combine_first(tmp)
    aaa[pname]=tmp[pname]
    del tmp
    del reports
    # aaa=aaa.drop([pname+'_y'], axis=1)
    # aaa=aaa.rename(columns={'upazilaname'+'_x': 'upazilaname'})
    reports=aaa
    for i in range(reports.shape[0]): # go through all upazila report values
        reports[pname].iloc[i] = subDist[subDist['value']==reports.index[i]]['name'].values[0] ###still to work with the copy , this goes with numbers and nnot names
    reports[pname]=reports[pname].str.title()

    reports.set_index(pnumber) #1

    fig = px.choropleth_mapbox(reports, geojson=data, locations=pnumber, color=title,
                            featureidkey='properties.'+pnumber,
#                            featureidkey="Cmap",
                            color_continuous_scale="RdBu_r", #"YlOrBr",
                            color_continuous_midpoint=0,
                            range_color=(-reports[title].max(), reports[title].max()),
                            mapbox_style="carto-positron",
                            zoom=5.8, center = {"lat": 23.7, "lon": 90.3},
                            opacity=0.5,
                            labels={variab:labl},
#                            hover_name=pname
                          )
    fig.update_layout(autosize=True, coloraxis_showscale=False, margin={"r":0,"t":0,"l":0,"b":0}, height=550) #, width=760 , height=800, ) #, coloraxis_showscale= False) #width= 1000, height=600,
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
                    dbc.Row([
                        dbc.Col([
                            dcc.DatePickerRange(
                                    id='daterange',
                                    min_date_allowed=start_date,
                                    start_date=date(2022, 1, 1) ,
                                    max_date_allowed=end_date,
                                    # start_date=date(end_date.year-1, end_date.month, end_date.day),
                                    initial_visible_month=end_date,
                                    end_date=date(2022, 12, 31)
                                    #end_date=end_date
                                ),
                            ]),
                        dbc.Col([
                            dcc.Dropdown(
                                ddDList,
                                "All Diseases",
                                id="Diseaselist",
                                multi=True,
                                clearable=False,
                                ),
                            ])
                        ]),
                    dbc.Row([
                        dbc.Tabs([
                            dbc.Tab([
                                dbc.Row(dcc.Graph(id='Reports')),
                                dbc.Row(dcc.Graph(id='Sick')),
                                dbc.Row(dcc.Graph(id='Dead'))],
                                label='Reports', tab_id='ReportsTab'),
                            dbc.Tab([
                                dbc.Row(dcc.Graph(id='Livestock')),
                                dbc.Row(dcc.Graph(id='Zoonotic'))],
                                label='Diseases', tab_id='DiseaseTab'),
                            dbc.Tab([
                                dbc.Card(dbc.Col([dcc.Graph(id='DRindicators'),
                                                  dcc.Graph(id='DRRepG1')])
                                         )],
                                label='Reports per Geolocation', tab_id='GeoRepTab'),
                            dbc.Tab([
                                dbc.Card(dbc.Col([dcc.Graph(id='figMonthly')])
                                          )],
                                label='Monthly Comparison', tab_id='MonthCompTab')
                            ], id='tabs')
                        ])
                    ], width=8)
            ])
    ])


## shape overlay of selected geotile(s)

@callback(
    Output ('Division', 'options'),
    Output ('District', 'options'),
    Output ('Upazila', 'options'),
    Output ('Diseaselist', 'options'),

    Output ('Map', 'figure'),
    Output ('Reports', 'figure'),
    Output ('Sick', 'figure'),
    Output ('Dead', 'figure'),
    Output ('Livestock', 'figure'),
    Output ('Zoonotic', 'figure'),
    Output ('DRRepG1', 'figure'),
    Output ('DRindicators', 'figure'),
    Output ('figMonthly', 'figure'),

    # Input ('cache_bahis_data', 'data'),
    # Input ('cache_bahis_dgdata', 'data'),
    # Input ('cache_bahis_geodata', 'data'),
    Input ('geoSlider', 'value'),
    Input ('Map', 'clickData'),
    Input ('Reports', 'clickData'),
    Input ('Sick', 'clickData'),
    Input ('Dead', 'clickData'),

    Input ('Division', 'value'),
    Input ('District', 'value'),
    Input ("Upazila",'value'),
    Input ("daterange",'start_date'),
    Input ("daterange",'end_date'),
    Input ("Diseaselist",'value'),
    Input ('tabs', 'active_tab'),
    Input ('Map', 'clickData'),
)
#def update_whatever(cbahis_data, cbahis_dgdata, cbahis_geodata, geoSlider, geoTile, clkRep, clkSick, clkDead, cU2Division, cU2District, cU2Upazila, start_date, end_date, diseaselist):
def update_whatever(geoSlider, geoTile, clkRep, clkSick, clkDead, SelDiv, SelDis, SelUpa, start_date, end_date, diseaselist, tabs, geoclick):
    global firstrun, vDiv, vDis, vUpa, ddDList, path, pnumber, loc, title, incsub_bahis_sourcedata
    print(geoclick)
    # print(clkRep)
    # print(clkSick)
    # print(pd.DataFrame(cbahis_data).shape)
    # print(pd.DataFrame(cbahis_dgdata).shape)
    # print(pd.DataFrame(cbahis_geodata).shape)
    # bahis_data=pd.DataFrame(cbahis_data)
    # bahis_data['date']= pd.to_datetime(bahis_data['date'])
    # bahis_dgdata=pd.DataFrame(cbahis_dgdata)
    # bahis_geodata=pd.DataFrame(cbahis_geodata)

    dates = sne_date(bahis_data)
    subDist=bahis_geodata
    sub_bahis_sourcedata=bahis_data
    monthlydatabasis=sub_bahis_sourcedata
        
    if firstrun==True:  #inital settings
        sub_bahis_sourcedata=date_subset(dates, bahis_data)
        ddDList= fetchdiseaselist(sub_bahis_sourcedata)
        ddDList.insert(0, 'All Diseases')
        Divlist=fetchDivisionlist(bahis_geodata)
        vDiv = [{'label': i['Division'], 'value': i['value']} for i in Divlist]
        vDis=[]
        vUpa=[]
        # figgLiveS=lambda:None
        # figgZoon=[] 
        # Rfigg=[] 
        # Rfindic=[]
        # figMonthly=[]
        
        path=path3
        loc=3
        title='upazila'
        pnumber='upazilanumber'
        pname='upazilaname'
        splace=' Upazila'
        variab='upazila'
        labl='Incidences per upazila'
        incsub_bahis_sourcedata = pd.to_numeric(sub_bahis_sourcedata['upazila']).dropna().astype(int).value_counts().to_frame()
        
        firstrun=False
        print(firstrun)
        
    if ctx.triggered_id=='daterange':
        sub_bahis_sourcedata=date_subset(dates, bahis_data)
        
    if ctx.triggered_id=='Diseaselist':
        sub_bahis_sourcedata=disease_subset(diseaselist, sub_bahis_sourcedata)
        monthlydatabasis=disease_subset(diseaselist, bahis_data)
    
    if ctx.triggered_id=='Division':
        if not SelDiv:
            sub_bahis_sourcedata=sub_bahis_sourcedata
#                sub1a_bahis_sourcedata=sub1a_bahis_sourcedata
            subDist=bahis_geodata        
            vDis="",
        else:
            sub_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata['division']==SelDiv] #DivNo]
#                sub1a_bahis_sourcedata= sub1a_bahis_sourcedata.loc[sub1a_bahis_sourcedata['division']==cU2Division] #DivNo]
            subDist=bahis_geodata.loc[bahis_geodata['parent'].astype('string').str.startswith(str(SelDiv))]
            monthlydatabasis=monthlydatabasis.loc[monthlydatabasis['division']==SelDiv]           
            Dislist=fetchDistrictlist(SelDiv, bahis_geodata)
            vDis = [{'label': i['District'], 'value': i['value']} for i in Dislist]
            vUpa="",

    if ctx.triggered_id=='District':
        if not SelDis:
            sub_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata['division']==SelDiv] #DivNo]
#                sub1a_bahis_sourcedata= sub1a_bahis_sourcedata.loc[sub1a_bahis_sourcedata['division']==cU2Division] #DivNo]
            subDist=bahis_geodata.loc[bahis_geodata['parent'].astype('string').str.startswith(str(SelDiv))]
            monthlydatabasis=monthlydatabasis.loc[monthlydatabasis['division']==SelDiv]           
            Dislist=fetchDistrictlist(SelDiv, bahis_geodata)
            vDis = [{'label': i['District'], 'value': i['value']} for i in Dislist]
            vUpa="",            
        else: 
            sub_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata['district']==SelDis] #DivNo]
#                sub1a_bahis_sourcedata= sub1a_bahis_sourcedata.loc[sub1a_bahis_sourcedata['division']==cU2Division] #DivNo]
            subDist=bahis_geodata.loc[bahis_geodata['parent'].astype('string').str.startswith(str(SelDis))]
            monthlydatabasis=monthlydatabasis.loc[monthlydatabasis['district']==SelDis]                       
            Upalist=fetchUpazilalist(SelDis, bahis_geodata)
            vUpa=[{'label': i['Upazila'], 'value': i['value']} for i in Upalist]
            
    if ctx.triggered_id=='Upazila':            
        if not SelUpa:
            sub_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata['district']==SelDis] #DivNo]
#                sub1a_bahis_sourcedata= sub1a_bahis_sourcedata.loc[sub1a_bahis_sourcedata['division']==cU2Division] #DivNo]
            subDist=bahis_geodata.loc[bahis_geodata['parent'].astype('string').str.startswith(str(SelDis))]
            monthlydatabasis=monthlydatabasis.loc[monthlydatabasis['district']==SelDis]                       
        else:
            sub_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata['upazila']==SelUpa]
    #        sub1a_bahis_sourcedata= sub1a_bahis_sourcedata.loc[sub1a_bahis_sourcedata['upazila']==cU2Upazila]
            subDist=bahis_geodata.loc[bahis_geodata['value'].astype('string').str.startswith(str(SelUpa))]
            monthlydatabasis=monthlydatabasis.loc[monthlydatabasis['upazila']==SelUpa]

    # tmps= pd.to_datetime(start_date)-relativedelta(years=1)
    # tmpe= pd.to_datetime(end_date)-relativedelta(years=1)
    # tdates=[tmps, tmpe]
    # sub1a_bahis_sourcedata=date_subset(tdates, bahis_data)
    # sub1a_bahis_sourcedata=disease_subset(diseaselist, sub1a_bahis_sourcedata)

    if ctx.triggered_id=='geoSlider':
        if geoSlider== 1:
            path=path1
            loc=1
            title='division'
            pnumber='divnumber'
            pname='divisionname'
            splace=' Division'
            variab='division'
            labl='Incidences per division'
            incsub_bahis_sourcedata = pd.to_numeric(sub_bahis_sourcedata['division']).dropna().astype(int).value_counts().to_frame()

    #        bahis_sourcedata = pd.to_numeric(bahis_data['division']).dropna().astype(int)
            # if geoTile is not None:
            #     print(geoTile['points'][0]['location'])
            #     cU2Division=geoTile['points'][0]['location']
            #     Dislist=fetchDistrictlist(geoTile['points'][0]['location'])
            #     vDistrict = [{'label': i['District'], 'value': i['value']} for i in Dislist]
        if geoSlider== 2:
            path=path2
            loc=2
            title='district'
            pnumber='districtnumber'
            pname='districtname'
            splace=' District'
            variab='district'
            labl='Incidences per district'
            incsub_bahis_sourcedata = pd.to_numeric(sub_bahis_sourcedata['district']).dropna().astype(int).value_counts().to_frame()
        if geoSlider== 3:
            path=path3
            loc=3
            title='upazila'
            pnumber='upazilanumber'
            pname='upazilaname'
            splace=' Upazila'
            variab='upazila'
            labl='Incidences per upazila'
            incsub_bahis_sourcedata = pd.to_numeric(sub_bahis_sourcedata['upazila']).dropna().astype(int).value_counts().to_frame()

    Rfig = plot_map(path, loc, subDist, incsub_bahis_sourcedata, title, pnumber, pname, splace, variab, labl)

###tab1
    
    tmp=sub_bahis_sourcedata['date'].dt.date.value_counts()
    tmp=tmp.to_frame()
    tmp['counts']=tmp['date']

    tmp['date']=pd.to_datetime(tmp.index)
    tmp=tmp['counts'].groupby(tmp['date'].dt.to_period('W-SAT')).sum().astype(int)
    tmp=tmp.to_frame()
    tmp['date']=tmp.index
    tmp['date']=tmp['date'].astype('datetime64[D]')

    # tmp2=sub1a_bahis_sourcedata['date'].dt.date.value_counts()
    # tmp2=tmp2.to_frame()
    # tmp2['counts']=tmp2['date']

    # tmp2['date']=pd.to_datetime(tmp2.index)
    # tmp2=tmp2['counts'].groupby(tmp2['date'].dt.to_period('W-SAT')).sum().astype(int)
    # tmp2=tmp2.to_frame()
    # tmp2['date']=tmp2.index
    # tmp2['date']=tmp2['date'].astype('datetime64[D]')
    # tmp2['date']=tmp2['date']+pd.offsets.Day(365)

    figgR= px.bar(tmp, x='date', y='counts', labels={'date':'Date', 'counts':'No. of Reports'})
    #figgR= figgR.add_trace(px.bar(tmp2, x='date', y='counts', labels={'date':'Date', 'counts':'No. of Reports'}))
    # figgRR = px.line(tmp2, x='date', y='counts')

    # figgRR['data'][0]['line']['color']='rgb(204, 0, 0)'
    # figgRR['data'][0]['line']['width']=1
    # figgR= go.Figure(data=figgR.data + figgRR.data)
    figgR.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})
    figgR.add_annotation(
        x=end_date,
        y=max(tmp),
        #xref="x",
        #yref="y",
        text="total reports " + str('{:,}'.format(sub_bahis_sourcedata['date'].dt.date.value_counts().sum())),
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

    tmp=sub_bahis_sourcedata[['sick','dead']].groupby(sub_bahis_sourcedata['date'].dt.to_period('W-SAT')).sum().astype(int)
    tmp=tmp.reset_index()
    tmp=tmp.rename(columns={'date':'date'})
    tmp['date'] = tmp['date'].astype('datetime64[D]')
    figgSick= px.bar(tmp, x='date', y='sick', labels={'date':'Date', 'sick':'No. of Sick Animals'})
    figgSick.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})
    figgSick.add_annotation(
        x=end_date,
        y=max(tmp),
        #xref="x",
        #yref="y",
        text="total sick " + str('{:,}'.format(int(sub_bahis_sourcedata['sick'].sum()))),
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

    figgDead= px.bar(tmp, x='date', y='dead', labels={'date':'Date', 'dead':'No. of Dead Animals'})
    figgDead.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})
    figgDead.add_annotation(
        x=end_date,
        y=max(tmp),
        #xref="x",
        #yref="y",
        text="total dead " + str('{:,}'.format(int(sub_bahis_sourcedata['dead'].sum()))),
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
    fpoul.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
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
    flani.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    #subpl.add_traces(flani, row=1, col=1)#, row=2, col=1) #, labels={'counts': 'Values', 'top_diagnosis': 'Disease'})#, orientation='h')
    subpl=[fpoul, flani]
    figgLiveS= make_subplots(rows=2, cols=1)
    for i, figure in enumerate(subpl):
        for trace in range(len(figure['data'])):
            figgLiveS.append_trace(figure['data'][trace], row=i+1, col=1)
    figgLiveS.update_layout(height=400, margin={"r":0,"t":0,"l":0,"b":0})

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
    figgZoon.update_layout(height=100, margin={"r":0,"t":0,"l":0,"b":0})


### tab3 geolocation

    reports=incsub_bahis_sourcedata

    reports['cases']=reports[title]
    reports[title] = reports.index
    reports= reports.loc[reports[title] != 'nan']

    for i in range(reports.shape[0]):
        reports[title].iloc[i] = subDist.loc[subDist['value']==int(reports[title].iloc[i]),'name'].iloc[0]

    reports=reports.sort_values(title)
    reports[title]=reports[title].str.capitalize()

    Rfigg=px.bar(reports, x=title, y='cases', labels= {variab:labl})# ,color='division')
    Rfigg.update_layout(autosize=True, height=400, margin={"r":0,"t":0,"l":0,"b":0})

    Rfindic=fIndicator(sub_bahis_sourcedata)


### tab 4 monthly currently not geo resolved and disease, because of bahis_data, either ata is time restricted or


    monthly=monthlydatabasis['sick'].groupby(monthlydatabasis['date'].dt.to_period('M')).sum().astype(int)
    monthly=monthly.reset_index()
    monthly=monthly.rename(columns={'date':'date'})
    monthly['date']=monthly['date'].astype(str)
    monthly['date'] = pd.to_datetime(monthly['date'])
    monthlydata={'sick':monthly['sick'],
               'date':monthly['date']}
    monthlydata=pd.DataFrame(monthlydata)

    figMonthly= px.bar(monthlydata, x=pd.DatetimeIndex(monthlydata['date']).month, y=monthlydata['sick'], color=pd.DatetimeIndex(monthlydata['date']).year.astype(str), barmode ='group')


    return vDiv, vDis, vUpa, ddDList, Rfig, figgR, figgSick,figgDead, figgLiveS, figgZoon, Rfigg, Rfindic, figMonthly






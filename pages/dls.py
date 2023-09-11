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
from dash import dcc, html, callback, ctx, dash_table #Dash, #dash_table, dbc
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc #dbc deprecationwarning
import pandas as pd
from dash.dependencies import Input, Output, State
import json, os, glob
from datetime import date, datetime, timedelta
#from dateutil.relativedelta import relativedelta
from plotly.subplots import make_subplots
import numpy as np
from dash.dash import no_update


starttime_start=datetime.now()

pd.options.mode.chained_assignment = None

dash.register_page(__name__)    #register page to main dash app

#sourcepath='C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/'    #for local debugging purposes
#path0= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM0_simplified.geojson" #1 Nation # reminder: found shapefiles from the data.humdata.org
sourcepath = 'exported_data/'
geofilename = glob.glob(sourcepath + 'newbahis_geo_cluster*.csv')[-1]   # the available geodata from the bahis project (Masterdata)
dgfilename = os.path.join(sourcepath, 'Diseaselist.csv')   # disease grouping info (Masterdata)
sourcefilename =os.path.join(sourcepath, 'preped_data2.csv')    # main data resource of prepared data from old and new bahis
path1= os.path.join(sourcepath,"processed_geodata","divdata.geojson") #8 Division
path2= os.path.join(sourcepath,"processed_geodata","distdata.geojson") #64 District
path3= os.path.join(sourcepath,"processed_geodata","upadata.geojson") #495 Upazila

firstrun=True

def fetchsourcedata(): #fetch and prepare source data
    bahis_data = pd.read_csv(sourcefilename)
    bahis_data['from_static_bahis']=bahis_data['basic_info_date'].str.contains('/') # new data contains -, old data contains /
    bahis_data['basic_info_date'] = pd.to_datetime(bahis_data['basic_info_date'],errors = 'coerce')
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
    bahis_data[['upazila', 'sick', 'dead']]=bahis_data[['upazila',  'sick', 'dead']].astype(np.int32) #converting into uint makes odd values)
#    bahis_data[['species', 'tentative_diagnosis', 'top_diagnosis']]=bahis_data[['species', 'tentative_diagnosis', 'top_diagnosis']].astype(str) # can you change object to string and does it make a memory difference`?
    bahis_data['dead'] = bahis_data['dead'].clip(lower=0)
#    bahis_data=bahis_data[bahis_data['date']>=datetime(2019, 7, 1)]
# limit to this year    bahis_data=bahis_data[bahis_data['date'].dt.year== max(bahis_data['date']).year]
    return bahis_data
bahis_data=fetchsourcedata()
sub_bahis_sourcedata=bahis_data
monthlydatabasis=sub_bahis_sourcedata


def sne_date(bahis_data):
    start_date=min(bahis_data['date']).date()
    end_date=max(bahis_data['date']).date()
    dates=[start_date, end_date]
    return dates

start_date=date(2019, 1, 1)
end_date=date(2023,12,31)
dates=[start_date, end_date]

ddDList=[]
Divlist=[]

def fetchdisgroupdata(): #fetch and prepare disease groups
    bahis_dgdata= pd.read_csv(dgfilename)
#    bahis_dgdata= bahis_dgdata[['species', 'name', 'id', 'Disease type']] remark what might be helpful: reminder: memory size
    bahis_dgdata= bahis_dgdata[['name', 'Disease type']]
    bahis_dgdata= bahis_dgdata.dropna()
#    bahis_dgdata[['name', 'Disease type']] = str(bahis_dgdata[['name', 'Disease type']])    #can you change object to string and does it make a memory difference?
    bahis_dgdata = bahis_dgdata.drop_duplicates(subset='name', keep="first")
    return bahis_dgdata
bahis_dgdata= fetchdisgroupdata()
to_replace=bahis_dgdata['name'].tolist()
replace_with=bahis_dgdata['Disease type'].tolist()


def fetchgeodata():     #fetch geodata from bahis, delete mouzas and unions
    geodata = pd.read_csv(geofilename)
    geodata = geodata.drop(geodata[(geodata['loc_type']==4) | (geodata['loc_type']==5)].index)  #drop mouzas and unions
    geodata=geodata.drop(['id', 'longitude', 'latitude', 'updated_at'], axis=1)
    geodata['parent']=geodata[['parent']].astype(np.uint16)   # assuming no mouza and union is taken into
    geodata[['value']]=geodata[['value']].astype(np.uint32)
    geodata[['loc_type']]=geodata[['loc_type']].astype(np.uint8)
    return geodata
bahis_geodata= fetchgeodata()
subDist=bahis_geodata


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
        sub_bahis_sourcedata=sub_bahis_sourcedata[sub_bahis_sourcedata['top_diagnosis']==cDisease]
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

    RfigIndic.update_layout(height=100,
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


def plot_map(path, loc, subDistM, sub_bahis_sourcedata, title, pnumber, pname, splace, variab, labl):
    reports = sub_bahis_sourcedata[title].value_counts().to_frame()
    reports[pnumber] = reports.index #1
    reports.index = reports.index.astype(int)   # upazila name
    reports[pnumber] = reports[pnumber].astype(int)
    reports= reports.loc[reports[pnumber] != 'nan']    # unknown reason for now. does this have to be beore reports in sub_bahis_sourcedata? reports, where there are no geonumbers?
    data = open_data(path) #1

    reports[pname] = reports.index
    tmp=subDistM[['value', 'name']]
    tmp=tmp.rename(columns={'value':pnumber, 'name':pname})
    tmp[pname]=tmp[pname].str.title()
    tmp['Index']=tmp[pnumber]
    tmp=tmp.set_index('Index')
    tmp[title]=-(reports[pname].max())

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
        reports[pname].iloc[i] = subDistM[subDistM['value']==reports.index[i]]['name'].values[0] ###still to work with the copy , this goes with numbers and nnot names
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
                                    start_date=date(2023, 1, 1) ,
                                    max_date_allowed=end_date,
                                    # start_date=date(end_date.year-1, end_date.month, end_date.day),
                                    # initial_visible_month=end_date,
                                    end_date=date(2023, 12, 31)
                                    #end_date=end_date
                                ),
                            ]),
                        dbc.Col([
                            dcc.Dropdown(
                                ddDList,
                                "All Diseases",
                                id="Diseaselist",
                                multi=False,
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
                                dbc.Row(dbc.Col([
                                        html.Label("Top 10 Diseases"),
                                        dcc.Graph(id='Livestock')
                                    ])),
                                dbc.Row(dbc.Col([
                                        html.Label("Top 10 Zoonotic Diseases"),
                                        dcc.Graph(id='Zoonotic')
                                        ])
                                    )],
                                label='Diseases', tab_id='DiseaseTab'),
                            dbc.Tab([
                                dbc.Card(dbc.Col([dbc.Row(dcc.Graph(id='DRindicators')),
                                                  dbc.Row(dcc.Graph(id='DRRepG1')),
                                                  dbc.Row([html.Label("Non-Reporting Regions (Please handle with care as geoshape files and geolocations have issues)", id='NRlabel'),
                                                      html.Div(id='AlertTable')])])
                                         )],
                                label='Reports per Geolocation', tab_id='GeoRepTab'),
                            dbc.Tab([
                                dbc.Card(dbc.Col([dcc.Graph(id='figMonthly')])
                                          )],
                                label='Monthly Comparison', tab_id='MonthCompTab'),
                            dbc.Tab([
                                dbc.Card(
                                    dbc.Row([html.Label("Export Data", id='ExportLabel'),
                                             html.Div(id='ExportTab')])
                                    )],
                                label='Export Data', tab_id='ExportTab')
                            ], id='tabs')
                        ])
                    ], width=8)
            ])
    ])


endtime_start = datetime.now()
print('initialize : ' + str(endtime_start-starttime_start))


## shape overlay of selected geotile(s)

@callback(
                              #dash cleintsied callback with js
    Output ('Division', 'value'),
    Output ('District', 'value'),
    Output ('Upazila', 'value'),
    Output ('Division', 'options'),
    Output ('District', 'options'),
    Output ('Upazila', 'options'),
    Output ('Diseaselist', 'options'),

#    Output ('Map', 'figure'),
    Output ('Reports', 'figure'),
    Output ('Sick', 'figure'),
    Output ('Dead', 'figure'),

    Output ('Livestock', 'figure'),
    Output ('Zoonotic', 'figure'),
    Output ('DRindicators', 'figure'),
    Output ('DRRepG1', 'figure'),
    Output ('NRlabel', 'children'),
    Output ('AlertTable', 'children'),

#    Output ('GeoDynTable', 'children'),
    Output ('figMonthly', 'figure'),
    Output ('ExportLabel', 'children'),
    Output ('ExportTab', 'children'),

    Output ('geoSlider' , 'value'),

    # Input ('cache_bahis_data', 'data'),
    # Input ('cache_bahis_dgdata', 'data'),
    # Input ('cache_bahis_geodata', 'data'),
#    Input ('geoSlider', 'value'),
    Input ('Map', 'clickData'),
    Input ('Reports', 'clickData'),
    Input ('Sick', 'clickData'),
    Input ('Dead', 'clickData'),

    Input ('Division', 'value'),
    Input ('District', 'value'),
    Input ("Upazila",'value'),
    Input ("daterange",'start_date'),  #make state to prevent upate before submitting
    Input ("daterange",'end_date'), #make state to prevent upate before submitting

    Input ("Diseaselist",'value'),
    Input ('tabs', 'active_tab'),

    State ('geoSlider', 'value'),
    #Input ('Map', 'clickData'),
)

#def update_whatever(geoSlider, geoTile, clkRep, clkSick, clkDead, SelDiv, SelDis, SelUpa, start_date, end_date, diseaselist, tabs, geoclick):
def update_whatever(geoTile, clkRep, clkSick, clkDead, SelDiv, SelDis, SelUpa, start_date, end_date, diseaselist, tabs, geoSlider):

    starttime_general=datetime.now()

    global firstrun, vDiv, vDis, vUpa, ddDList, path, variab, labl, splace, pname, pnumber, loc, title, incsub_bahis_sourcedata, sub_bahis_sourcedata, monthlydatabasis, subDist
#    print(geoclick)


    # starttime=datetime.now()
    # endtime = datetime.now()
    # print(endtime-starttime)
    # print(clkRep)
    # print(clkSick)
    # print(pd.DataFrame(cbahis_data).shape)
    # print(pd.DataFrame(cbahis_dgdata).shape)
    # print(pd.DataFrame(cbahis_geodata).shape)
    # bahis_data=pd.DataFrame(cbahis_data)
    # bahis_data['date']= pd.to_datetime(bahis_data['date'])
    # bahis_dgdata=pd.DataFrame(cbahis_dgdata)
    # bahis_geodata=pd.DataFrame(cbahis_geodata)

    dates = [start_date, end_date]
    print(start_date)
    #sub_bahis_sourcedata=bahis_data
    sub_bahis_sourcedata=date_subset(dates, bahis_data)

    NRlabel= 'Non-Reporting Regions (Please handle with care as geoshape files and geolocations have issues)'
    if firstrun==True:  #inital settings
#        dates = sne_date(bahis_data)
        ddDList= fetchdiseaselist(sub_bahis_sourcedata)
#        ddDList.insert(0, 'All Diseases')
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
        labl='Reports per upazila'
        firstrun=False
        #subDist=subDist[subDist['loc_type']==loc]


#    if ctx.triggered_id=='daterange':
#        sub_bahis_sourcedata=date_subset(dates, bahis_data)

    if ctx.triggered_id=='Diseaselist':
        sub_bahis_sourcedata=disease_subset(diseaselist, sub_bahis_sourcedata)

    if ctx.triggered_id=='Division':
        if not SelDiv:
            sub_bahis_sourcedata=bahis_data
            subDist=bahis_geodata
            vDis=[]
            Dislist=""
            vUpa=[]
            Upalist=[]
            SelDis=""
            SelUpa=""
        else:
            sub_bahis_sourcedata= bahis_data.loc[bahis_data['division']==SelDiv] #DivNo]
            subDist=bahis_geodata.loc[bahis_geodata['parent'].astype('string').str.startswith(str(SelDiv))]
            Dislist=fetchDistrictlist(SelDiv, bahis_geodata)
            vDis = [{'label': i['District'], 'value': i['value']} for i in Dislist]
            vUpa=[]
            SelUpa=""

    if ctx.triggered_id=='District':
        if not SelDis:
            sub_bahis_sourcedata= bahis_data.loc[bahis_data['division']==SelDiv] #DivNo]
            subDist=bahis_geodata.loc[bahis_geodata['parent'].astype('string').str.startswith(str(SelDiv))]
            Dislist=fetchDistrictlist(SelDiv, bahis_geodata)
            vDis = [{'label': i['District'], 'value': i['value']} for i in Dislist]
            Upalist=""
            vUpa=[]
            SelUpa=""
        else:
            sub_bahis_sourcedata= bahis_data.loc[bahis_data['district']==SelDis] #DivNo]    from basic data in case on switches districts in current way, switching leads to zero data but speed
            subDist=bahis_geodata.loc[bahis_geodata['parent'].astype('string').str.startswith(str(SelDis))]
            Upalist=fetchUpazilalist(SelDis, bahis_geodata)
            vUpa=[{'label': i['Upazila'], 'value': i['value']} for i in Upalist]

    if ctx.triggered_id=='Upazila':
        if not SelUpa:
            sub_bahis_sourcedata= bahis_data.loc[bahis_data['district']==SelDis] #DivNo] from basic data in case on switches districts in current way, switching leads to zero data but speed
            subDist=bahis_geodata.loc[bahis_geodata['parent'].astype('string').str.startswith(str(SelDis))]
        else:
            sub_bahis_sourcedata= bahis_data.loc[bahis_data['upazila']==SelUpa]
            subDist=bahis_geodata.loc[bahis_geodata['value'].astype('string').str.startswith(str(SelUpa))]


#    if ctx.triggered_id=='geoSlider':
    if geoSlider== 1:
        path=path1
        loc=geoSlider
        title='division'
        pnumber='divnumber'
        pname='divisionname'
        splace=' Division'
        variab='division'
        labl='Reports per division'
        subDistM=subDist[subDist['loc_type']==geoSlider]
        #subDist=bahis_geodata[bahis_geodata['loc_type']==geoSlider]

#        bahis_sourcedata = pd.to_numeric(bahis_data['division']).dropna().astype(int)
        # if geoTile is not None:
        #     print(geoTile['points'][0]['location'])
        #     cU2Division=geoTile['points'][0]['location']
        #     Dislist=fetchDistrictlist(geoTile['points'][0]['location'])
        #     vDistrict = [{'label': i['District'], 'value': i['value']} for i in Dislist]
    if geoSlider== 2:
        path=path2
        loc=geoSlider
        title='district'
        pnumber='districtnumber'
        pname='districtname'
        splace=' District'
        variab='district'
        labl='Reports per district'
        subDistM=subDist[subDist['loc_type']==geoSlider]
        #subDist=bahis_geodata[bahis_geodata['loc_type']==geoSlider]

    if geoSlider== 3:
        path=path3
        loc=geoSlider
        loc=3
        title='upazila'
        pnumber='upazilanumber'
        pname='upazilaname'
        splace=' Upazila'
        variab='upazila'
        labl='Reports per upazila'
        subDistM=subDist[subDist['loc_type']==3]
        #subDist=bahis_geodata[bahis_geodata['loc_type']==geoSlider]

#    Rfig = plot_map(path, loc, subDistM, sub_bahis_sourcedata, title, pnumber, pname, splace, variab, labl)
    endtime_general = datetime.now()
    print('general callback : ' + str(endtime_general-starttime_general))

###tab1

    if tabs == 'ReportsTab':
        starttime_tab1=datetime.now()

        tmp=sub_bahis_sourcedata['date'].dt.date.value_counts()
        tmp=tmp.to_frame()
        tmp['counts']=tmp['date'] 
        tmp['date']=pd.to_datetime(tmp.index)
        tmp=tmp['counts'].groupby(tmp['date'].dt.to_period('W-SAT')).sum().astype(int)
        tmp=tmp.to_frame()
        tmp['date']=tmp.index
        tmp['date']=tmp['date'].astype('datetime64[D]')

        figgR= px.bar(tmp, x='date', y='counts', labels={'date':'', 'counts':'No. of Reports'})
        figgR.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})
        figgR.update_xaxes(range=[datetime.strptime(dates[0],"%Y-%m-%d")-timedelta(days=6), datetime.strptime(dates[1],"%Y-%m-%d")+timedelta(days=6)])
        figgR.add_annotation(
            x= datetime.strptime(dates[1],"%Y-%m-%d")-timedelta(days=int(((datetime.strptime(dates[1],"%Y-%m-%d")-datetime.strptime(dates[0],"%Y-%m-%d")).days)*0.08)),
            y=max(tmp),
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
        figgSick= px.bar(tmp, x='date', y='sick', labels={'date':'', 'sick':'No. of Sick Animals'})
        figgSick.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})
        figgSick.update_xaxes(range=[datetime.strptime(dates[0],"%Y-%m-%d")-timedelta(days=6), datetime.strptime(dates[1],"%Y-%m-%d")+timedelta(days=6)])   #manual setting should be done better with [start_date,end_date] annotiation is invisible and bar is cut
        figgSick.add_annotation(
            x=datetime.strptime(dates[1],"%Y-%m-%d")-timedelta(days=int(((datetime.strptime(dates[1],"%Y-%m-%d")-datetime.strptime(dates[0],"%Y-%m-%d")).days)*0.08)),
            y=max(tmp),
            text="total sick " + str('{:,}'.format(int(sub_bahis_sourcedata['sick'].sum()))), ###realy outlyer
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

        figgDead= px.bar(tmp, x='date', y='dead', labels={'date':'', 'dead':'No. of Dead Animals'})
        figgDead.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0})
        figgDead.update_xaxes(range=[datetime.strptime(dates[0],"%Y-%m-%d")-timedelta(days=6), datetime.strptime(dates[1],"%Y-%m-%d")+timedelta(days=6)])
        figgDead.add_annotation(
            x=datetime.strptime(dates[1],"%Y-%m-%d")-timedelta(days=int(((datetime.strptime(dates[1],"%Y-%m-%d")-datetime.strptime(dates[0],"%Y-%m-%d")).days)*0.08)),
            y=max(tmp),
            text="total dead " + str('{:,}'.format(int(sub_bahis_sourcedata['dead'].sum()))), ###really
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
        print('tab1 : ' + str(endtime_tab1-starttime_tab1))
        return SelDiv, SelDis, SelUpa, vDiv, vDis, vUpa, ddDList, figgR, figgSick, figgDead, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, geoSlider



####tab2

    if tabs == 'DiseaseTab':

        starttime_tab2=datetime.now()

        #preprocess groupdata ?

        poultry=['Chicken', 'Duck', 'Goose', 'Pegion', 'Quail', 'Turkey']
        sub_bahis_sourcedataP=sub_bahis_sourcedata[sub_bahis_sourcedata['species'].isin(poultry)]

        # tmpdg= bahis_dgdata.drop_duplicates(subset='name', keep="first")
        # to_replace=tmpdg['name'].tolist()
        # replace_with=tmpdg['Disease type'].tolist()
        sub_bahis_sourcedataP['top_diagnosis']= sub_bahis_sourcedataP.top_diagnosis.replace(to_replace, replace_with, regex=True)

        poultryTT=sub_bahis_sourcedataP.drop(sub_bahis_sourcedataP[sub_bahis_sourcedataP['top_diagnosis']=='Zoonotic diseases'].index)
        
        tmp= poultryTT.groupby(['top_diagnosis'])['species'].agg('count').reset_index()
        
        tmp=tmp.sort_values(by='species', ascending=False)
        tmp=tmp.rename({'species' : 'counts'}, axis=1)
        tmp=tmp.head(10)
        tmp=tmp.iloc[::-1]
        fpoul =px.bar(tmp, x='counts', y='top_diagnosis',title='Top10 Poultry Diseases')
        fpoul.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        #figg.append_trace(px.bar(tmp, x='counts', y='top_diagnosis',title='Top10 Poultry Diseases'), row=1, col=1) #, labels={'counts': 'Values', 'top_diagnosis': 'Disease'})#, orientation='h')

        lanimal=['Buffalo', 'Cattle', 'Goat', 'Sheep']
        sub_bahis_sourcedataLA=sub_bahis_sourcedata[sub_bahis_sourcedata['species'].isin(lanimal)]

        # tmpdg= bahis_dgdata.drop_duplicates(subset='name', keep="first")
        # to_replace=tmpdg['name'].tolist()
        # replace_with=tmpdg['Disease type'].tolist()
        sub_bahis_sourcedataLA['top_diagnosis']= sub_bahis_sourcedataLA.top_diagnosis.replace(to_replace, replace_with, regex=True)
        LATT=sub_bahis_sourcedataLA.drop(sub_bahis_sourcedataLA[sub_bahis_sourcedataLA['top_diagnosis']=='Zoonotic diseases'].index)

        tmp= LATT.groupby(['top_diagnosis'])['species'].agg('count').reset_index() 

        tmp=tmp.sort_values(by='species', ascending=False)
        tmp=tmp.rename({'species' : 'counts'}, axis=1)
        tmp=tmp.head(10)
        tmp=tmp.iloc[::-1]
        flani = px.bar(tmp, x='counts', y='top_diagnosis',title='Top10 Large Animal Diseases')
        flani.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        subpl=[fpoul, flani]
        figgLiveS= make_subplots(rows=2, cols=1)
        for i, figure in enumerate(subpl):
            for trace in range(len(figure['data'])):
                figgLiveS.append_trace(figure['data'][trace], row=i+1, col=1)
        figgLiveS.update_layout(height=350, margin={"r":0,"t":0,"l":0,"b":0})

        poultry=['Chicken', 'Duck', 'Goose', 'Pegion', 'Quail', 'Turkey']
        sub_bahis_sourcedataP=sub_bahis_sourcedata[sub_bahis_sourcedata['species'].isin(poultry)]

        # tmpdg= bahis_dgdata.drop_duplicates(subset='name', keep="first")
        tmpdg=bahis_dgdata[bahis_dgdata['Disease type']=='Zoonotic diseases']
        tmpdg=tmpdg['name'].tolist()
        sub_bahis_sourcedataP= sub_bahis_sourcedataP[sub_bahis_sourcedataP['top_diagnosis'].isin(tmpdg)]

        tmp= sub_bahis_sourcedataP.groupby(['top_diagnosis'])['species'].agg('count').reset_index() 

        tmp=tmp.sort_values(by='species', ascending=False)
        tmp=tmp.rename({'species' : 'counts'}, axis=1)
        tmp=tmp.head(10)
        tmp=tmp.iloc[::-1]
        fpoul =px.bar(tmp, x='counts', y='top_diagnosis',title='Top10 Poultry Diseases')
        fpoul.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        lanimal=['Buffalo', 'Cattle', 'Goat', 'Sheep']
        sub_bahis_sourcedataLA=sub_bahis_sourcedata[sub_bahis_sourcedata['species'].isin(lanimal)]

        sub_bahis_sourcedataLA= sub_bahis_sourcedataLA[sub_bahis_sourcedataLA['top_diagnosis'].isin(tmpdg)]

        tmp= sub_bahis_sourcedataLA.groupby(['top_diagnosis'])['species'].agg('count').reset_index() 

        tmp=tmp.sort_values(by='species', ascending=False)
        tmp=tmp.rename({'species' : 'counts'}, axis=1)
        tmp=tmp.head(10)
        tmp=tmp.iloc[::-1]
        flani = px.bar(tmp, x='counts', y='top_diagnosis',title='Top10 Ruminant Diseases')
        flani.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        subpl=[fpoul, flani]
        figgZoon= make_subplots(rows=2, cols=1)
        for i, figure in enumerate(subpl):
            for trace in range(len(figure['data'])):
                figgZoon.append_trace(figure['data'][trace], row=i+1, col=1)
        figgZoon.update_layout(height=150, margin={"r":0,"t":0,"l":0,"b":0})

        endtime_tab2 = datetime.now()
        print('tab2 : ' + str(endtime_tab2-starttime_tab2))
        return SelDiv, SelDis, SelUpa, vDiv, vDis, vUpa, ddDList, no_update,  no_update, no_update, figgLiveS, figgZoon, no_update, no_update, no_update, no_update, no_update, no_update, no_update, geoSlider


### tab3 geolocation

    if tabs == 'GeoRepTab':

        starttime_tab3=datetime.now()

        # geoSlider "if" can be included to accumulate over different resolution
        
        reports=sub_bahis_sourcedata[title].value_counts().to_frame()

        reports['cases']=reports[title]
        reports[title] = reports.index
        reports= reports.loc[reports[title] != 'nan']

        for i in range(reports.shape[0]):
            reports[title].iloc[i] = subDistM.loc[subDistM['value']==int(reports[title].iloc[i]),'name'].iloc[0]

        reports=reports.sort_values(title)
        reports[title]=reports[title].str.capitalize()

        tmp=subDistM[['value', 'name']]
        tmp=tmp.rename(columns={'value':pnumber, 'name':pname})
        tmp[pname]=tmp[pname].str.title()
        tmp['Index']=tmp[pnumber]
        tmp=tmp.set_index('Index')
        aaa=reports.combine_first(tmp)
        aaa[pname]=tmp[pname]
        alerts=aaa[aaa.isna().any(axis=1)]
        alerts= alerts[[pname, pnumber]]
        del tmp
        del aaa


        Rfindic=fIndicator(sub_bahis_sourcedata)
        Rfindic.update_layout(height=100, margin={"r":0,"t":30,"l":0,"b":0})

        Rfigg=px.bar(reports, x=title, y='cases', labels= {variab:labl, 'cases':'Reports'})# ,color='division')
        Rfigg.update_layout(autosize=True, height=200, margin={"r":0,"t":0,"l":0,"b":0})

        NRlabel= 'Regions with no data in the current database: ' + str(len(alerts)) + ' (Please handle with care as geoshape files and geolocations have issues)'
        AlertTable= dash_table.DataTable(
                                    #columns=[{'upazilaname': i, 'upazilanumber': i} for i in alerts.loc[:,:]], #['Upazila','total']]],
                                    style_header={
                                            'overflow': 'hidden',
                                            'maxWidth': 0,
                                            'fontWeight': 'bold',
                                            },
                                    style_cell={'textAlign': 'left'},
                                    export_format='csv',
                                    style_table={'height': '220px', 'overflowY': 'auto'},
                                    style_as_list_view=True,
                                    fixed_rows={'headers': True},
                                    data=alerts.to_dict('records'),
                                    ),

        endtime_tab3 = datetime.now()
        print('tab3 : ' + str(endtime_tab3-starttime_tab3))
        return SelDiv, SelDis, SelUpa, vDiv, vDis, vUpa, ddDList, no_update, no_update, no_update, no_update, no_update, Rfindic, Rfigg, NRlabel, AlertTable, no_update, no_update, no_update, geoSlider


#### tab 4 geodyn tab per current year

 # removed since Completeness is replacing this tab

### tab 5 monthly currently not geo resolved and disease, because of bahis_data, either ata is time restricted or

    if tabs == 'MonthCompTab':

        starttime_tab5=datetime.now()

        monthly=bahis_data.groupby([bahis_data['date'].dt.year.rename('year'), bahis_data['date'].dt.month.rename('month')])['date'].agg({'count'})
        monthly=monthly.rename({'count':'reports'}, axis=1)
        monthly=monthly.reset_index()
        monthly['year']=monthly['year'].astype(str)
        figMonthly = px.bar(data_frame=monthly,
                            x='month',
                            y='reports',
                            labels={'month':'Month','reports':'Reports'},
                            color='year',
                            barmode='group')
        figMonthly.update_xaxes(dtick="M1", tickformat="%B")

        endtime_tab5 = datetime.now()
        print('tab5 : ' + str(endtime_tab5-starttime_tab5))
        return SelDiv, SelDis, SelUpa, vDiv, vDis, vUpa, ddDList, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, figMonthly, no_update, no_update, geoSlider

### tab 6 export tab

    if tabs == 'ExportTab':

        starttime_tab6=datetime.now()

        ExportTable=sub_bahis_sourcedata.copy()
        ExportTable['date']=ExportTable['date'].dt.strftime('%Y-%m-%d')
        del ExportTable['Unnamed: 0.1']
        ExportTable.drop('species_no', inplace=True, axis=1)
        ExportTable.drop('tentative_diagnosis', inplace=True, axis=1)
        ExportTable.rename(columns={'top_diagnosis': 'Diagnosis'}, inplace=True)
        ExportTable=ExportTable.merge(bahis_geodata[['value','name']], left_on='division', right_on='value')
        ExportTable['division']=ExportTable['name'].str.capitalize()
        ExportTable.drop(['name','value'], inplace=True, axis=1)

        ExportTable=ExportTable.merge(bahis_geodata[['value','name']], left_on='district', right_on='value')
        ExportTable['district']=ExportTable['name'].str.capitalize()
        ExportTable.drop(['name','value'], inplace=True, axis=1)

        ExportTable=ExportTable.merge(bahis_geodata[['value','name']], left_on='upazila', right_on='value')
        ExportTable['upazila']=ExportTable['name'].str.capitalize()
        ExportTable.drop(['name','value'], inplace=True, axis=1)

        ExportLabel= 'Export Data Size: ' + str(ExportTable.shape)
        
        ExportTab= dash_table.DataTable(
                                    style_header={
    #                                        'overflow': 'hidden',
    #                                        'maxWidth': 0,
                                            'fontWeight': 'bold',
                                            },
                                    style_cell={'textAlign': 'left'},
                                    export_format='csv',
                                    style_table={'height': '500px', 'overflowY': 'auto'},
    #                                style_as_list_view=True,
    #                                fixed_rows={'headers': True},
                                    data=ExportTable.to_dict('records'),
                                    columns=[{"name": i, "id": i} for i in ExportTable.columns],
                                    ),

        endtime_tab6 = datetime.now()
        print('tab6 : ' + str(endtime_tab6-starttime_tab6))
        return SelDiv, SelDis, SelUpa, vDiv, vDis, vUpa, ddDList, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, ExportLabel, ExportTab, geoSlider




@callback(
    Output ('Map', 'figure'),
#    Output ('geoSlider', 'value'),

    Input ('geoSlider', 'value'),
    State ('Division','value'),
    State ('District','value'),
    State ('Upazila','value'),
    prevent_initial_call=True,
)

def export(geoSlider, Division, District, Upazila):


#    if ctx.triggered_id=='geoSlider':
    if geoSlider== 1:
        if not Division:
            path=path1
            loc=geoSlider
            title='division'
            pnumber='divnumber'
            pname='divisionname'
            splace=' Division'
            variab='division'
            labl='Reports per division'
            subDistM=subDist[subDist['loc_type']==geoSlider]
        else:
            path=path1
            loc=geoSlider
            title='division'
            pnumber='divnumber'
            pname='divisionname'
            splace=' Division'
            variab='division'
            labl='Reports per division'
            subDistM=subDist[subDist['loc_type']==geoSlider]
    if geoSlider== 2:
        if not District:
            path=path2
            loc=geoSlider
            title='district'
            pnumber='districtnumber'
            pname='districtname'
            splace=' District'
            variab='district'
            labl='Reports per district'
            subDistM=subDist[subDist['loc_type']==geoSlider]
        else:
            geoSlider=3

    if geoSlider== 3:
        path=path3
        loc=geoSlider
        title='upazila'
        pnumber='upazilanumber'
        pname='upazilaname'
        splace=' Upazila'
        variab='upazila'
        labl='Reports per upazila'
        subDistM=subDist[subDist['loc_type']==geoSlider]

    Rfig = plot_map(path, loc, subDistM, sub_bahis_sourcedata, title, pnumber, pname, splace, variab, labl)
    return Rfig #, geoSlider

# make callback for tabs

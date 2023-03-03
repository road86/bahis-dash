# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 15:12:34 2022

@author: yoshka
"""

import dash
from dash import dcc, html, callback #Dash, #dash_table, dbc 
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
from dash.dependencies import Input, Output
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
import json  
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots


#### handle with care suppresses: 
# SettingWithCopyWarning:
# A value is trying to be set on a copy of a slice from a DataFrame
# See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
pd.options.mode.chained_assignment = None


dash.register_page(__name__)

# ##these for other solution
# dash.register_page(
#     __name__,
#     path='/urlpath',
#     title='name of tab',
#     name='presentationname'
# )

#dbc_css = "/dbc.min.css"
#app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])

########################
img_logo= 'assets/Logo.png'

gifpath = 'C:/Users/yoshka/Documents/GitHub/bahis-dash/logos/'
sourcepath = 'C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/'
geofilename = sourcepath + 'newbahis_geo_cluster.csv'   # the available geodata from the bahis project
dgfilename = sourcepath + 'Diseaselist.csv'   # disease grouping info
sourcefilename =sourcepath + 'preped_data2.csv'   
bahis_sd = pd.read_csv(sourcefilename)
img_logo= 'assets/Logo.png'

path0= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM0_simplified.geojson" #1 Nation # found shapefiles from the data.humdata.org
path1= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM1_simplified.geojson" #8 Division
path2= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM2_simplified.geojson" #64 District
path3= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM3_simplified.geojson" #495 Upazila
path4= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM4_simplified.geojson" #4562 Union

def fetchsourcedata():
    bahis_sd = pd.read_csv(sourcefilename) 
    bahis_sd['basic_info_division'] = pd.to_numeric(bahis_sd['basic_info_division'])
    bahis_sd['basic_info_district'] = pd.to_numeric(bahis_sd['basic_info_district'])
    bahis_sd['basic_info_upazila'] = pd.to_numeric(bahis_sd['basic_info_upazila'])
    bahis_sd['basic_info_date'] = pd.to_datetime(bahis_sd['basic_info_date'])
    return bahis_sd
bahis_sourcedata= fetchsourcedata()

def fetchgeodata():
    return pd.read_csv(geofilename)
bahis_geodata= fetchgeodata()

def fetchdisgroupdata():
    bahis_dgdata= pd.read_csv(dgfilename)
    bahis_dgdata= bahis_dgdata[['species', 'name', 'id', 'Disease type']]  
    bahis_dgdata= bahis_dgdata[['name', 'Disease type']]
    bahis_dgdata= bahis_dgdata.dropna() 
    return bahis_dgdata
bahis_dgdata= fetchdisgroupdata()

# app = Dash(__name__)

# colors = {
#     'background': '#ffffff',
#     'text': '#000000'
# }

def fetchdiseaselist():
    dislis= bahis_sourcedata['top_diagnosis'].unique()
    dislis= pd.DataFrame(dislis, columns=['Disease'])
#    dislis.sort_values(by=['Disease'])
    ddDList= dislis['Disease'].sort_values()
    return ddDList.tolist()
ddDList= fetchdiseaselist()
ddDList.insert(0, 'All Diseases')

def fetchDivisionlist():   
    ddDivlist=bahis_geodata[(bahis_geodata["loc_type"]==1)]['name'].str.capitalize()
    ddDivlist.name='Division'
    ddDivlist=ddDivlist.sort_values()
    return ddDivlist.tolist()
ddDivlist=fetchDivisionlist()
#ddDivlist.insert(0,'Select All')

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

# if SelDiv:
#     ddDislist=fetchDistrictlist(SelDiv)
#     ddDislist.insert(0,'Select All')
# else:
    
    
# ddDislist=[]

# ddDislist.insert(0,'Select All Diseases')

start_date=min(bahis_sourcedata['basic_info_date']).date()
end_date=max(bahis_sourcedata['basic_info_date']).date()
start_date=date(2021, 1, 1)

def natNo(sub_bahis_sourcedata):
    mask=(sub_bahis_sourcedata['basic_info_date']>= datetime.now()-timedelta(days=30)) & (sub_bahis_sourcedata['basic_info_date'] <= datetime.now())
    ################print(mask.value_counts(True])
    tmp_sub_data=sub_bahis_sourcedata['basic_info_date'].loc[mask]
    diff=tmp_sub_data.shape[0]
        
    tmp_sub_data=sub_bahis_sourcedata['patient_info_sick_number'].loc[mask]
    diffsick=int(tmp_sub_data.sum().item())
    
    tmp_sub_data=sub_bahis_sourcedata['patient_info_dead_number'].loc[mask]
    diffdead=int(tmp_sub_data.sum().item())
    return([diff, diffsick, diffdead])

#[diff, diffsick, diffdead]=natNo()

def fIndicator(sub_bahis_sourcedata):
    
    [diff, diffsick, diffdead]=natNo(sub_bahis_sourcedata)
 
    figIndic = go.Figure()
    
    figIndic.add_trace(go.Indicator(
        mode = "number+delta",
        title = 'Total Reports',
        value = sub_bahis_sourcedata.shape[0], #f"{bahis_sourcedata.shape[0]:,}"),
        delta = {'reference': sub_bahis_sourcedata.shape[0]-diff}, #'f"{diff:,}"},
        domain = {'row': 0, 'column': 0}))
    
    figIndic.add_trace(go.Indicator(
        mode = "number+delta",
        title = 'Sick Animals',
        value = sub_bahis_sourcedata['patient_info_sick_number'].sum(), #f"{int(bahis_sourcedata['patient_info_sick_number'].sum()):,}",
        delta= {'reference': sub_bahis_sourcedata['patient_info_sick_number'].sum()-diffsick}, #f"{diffsick:,}",
        domain = {'row': 0, 'column': 1}))
    
    figIndic.add_trace(go.Indicator(
        mode = "number+delta",
        title = 'Dead Animals',
        value = sub_bahis_sourcedata['patient_info_dead_number'].sum(), #f"{int(bahis_sourcedata['patient_info_dead_number'].sum()):,}",
        delta = {'reference': sub_bahis_sourcedata['patient_info_dead_number'].sum()-diffdead}, #f"{diffdead:,}",
        domain = {'row': 0, 'column': 2},
        ))
    
    figIndic.update_layout(height=235,
        grid = {'rows': 1, 'columns': 3},# 'pattern': "independent"},
        #?template=template_from_url(theme),
    
        )
    return figIndic

# ddReplist=['Reports', 'Sick Animals', 'Dead Animals', 'Month-wise comparison', 'Livestock Disease Cases', 'Zoonotic Disease Cases']

# ddReport = html.Div(
#     [
# #        dbc.Label("Select Report"),
#         dcc.Dropdown(
#             ddReplist,
#             'Reports',
#             id="cReportAIO",
#             clearable=False,
#         ),
#     ],
#     className="mb-4",
# )

dpDate = html.Div(
    [
         dcc.DatePickerRange(
            id='cDateAIO',
            min_date_allowed=start_date,
            max_date_allowed=end_date,
            initial_visible_month=date(2022, 1, 1),
            start_date=date(2021, 1, 1),
            end_date=end_date
            ),
     ],
    className='mb-4',
)

def date_subset(sdate, edate):
    dates=[sdate, edate]
    tmask= (bahis_sourcedata['basic_info_date']>= pd.to_datetime(dates[0])) & (bahis_sourcedata['basic_info_date'] <= pd.to_datetime(dates[1]))
    return bahis_sourcedata.loc[tmask]

def disease_subset(cDisease, sub_bahis_sourcedata):
    if 'All Diseases' in cDisease:
        sub_bahis_sourcedata=sub_bahis_sourcedata 
    else:
        sub_bahis_sourcedata=sub_bahis_sourcedata[sub_bahis_sourcedata['top_diagnosis'].isin(cDisease)] 
    return sub_bahis_sourcedata

#def geo_subset()

ddDivision = html.Div(
    [
        #dbc.Label("Select Division"),
        dcc.Dropdown(
            ddDivlist,
            id="cDivisionAIO",
            clearable=True,
            placeholder="Division",
        ),
    ],
    className="mb-4",
)

ddDistrict = html.Div(
    [
        #dbc.Label("Select District"),
        dcc.Dropdown(
            id="cDistrictAIO",
            clearable=True,
            placeholder="District",
        ),
    ],
    className="mb-4",
)

ddUpazila = html.Div(
    [
        #dbc.Label("Select Upazila"),
        dcc.Dropdown(
            id="cUpazilaAIO",
            clearable=True,
            placeholder="Upazila",
        ),
    ],
    className="mb-4",
)

ddDisease = html.Div(
    [
#        dbc.Label("Select disease"),
        dcc.Dropdown(
            ddDList,
            "All Diseases",
            id="cDiseaseAIO",
            multi=True,
            clearable=False,
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
    reports = sub_bahis_sourcedata[title].value_counts().to_frame()
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
                            zoom=5, center = {"lat": 23.7, "lon": 90.3},
                            opacity=0.5,
                            template=template_from_url(theme),
                            labels={variab:labl}
                          )
    ## make scaling off
    fig.update_layout(autosize=True, margin={"r":0,"t":0,"l":0,"b":0}, height=300, coloraxis_showscale=False) #, width=760 , height=800) #, coloraxis_showscale= False) #width= 1000, height=600, 
    return fig
                      
   
tabs=dbc.Card([
        dbc.Row([
            dbc.Card(
                dcc.Graph(id='indicatorsAIO'), body=True
                )
            ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dcc.Graph(id='RepG1AIO'), body=True
                    )
                ]),
            dbc.Col([
                dbc.Card(
                    dcc.Graph(id='MonthAIO'), body=True
                    )
                ]),
            ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dcc.Graph(id='SickAIO'), body=True
                    )
                ]),
            dbc.Col([
                dbc.Card(
                    dcc.Graph(id='DeadAIO'), body=True
                    )
                ]),
            ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dcc.Graph(id='LiveSAIO'), body=True
                    )
                ]),
            dbc.Col([
                dbc.Card(
                    dcc.Graph(id='ZoonAIO'), body=True
                    )
                ]),
            ])
        ]
 #       ]) 
    )
        
        # dbc.Col([dcc.Graph(id='indicators',
        #                          #figure=fIndicator()
        #                         ),
        #                 #width=8),  
        #       #justify="center", align="center", className="mb-42"), #"h-50"),
        #               dcc.Graph(id='RepG1')]
        #               )
        #      ) #, dcc.Graph(id='RepG2')]) #figure=figReport))


# stylesheet with the .dbc class
#dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
#app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])

header = html.H4(
    "BAHIS dashboard", className="bg-primary text-white p-2 mb-2 text-center"
)

row = html.Div(
    dbc.Row(
        [
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
        #            dbc.Col([            
                        dbc.Row([
                            dbc.Card([dpDate, ddDisease, ddDivision, ddDistrict, ddUpazila], body=True) #ddReport, dpDate, ddDisease, ddDivision, ddDistrict, ddUpazila], body=True)
                            ]), #, width=3),
        #                ], align='center'), 
                        html.Br(),
                        dbc.Row([
                            dbc.Card(dcc.Graph(
                                    id='CMapAIO',
                                    ), body=True)
        #                    ]), #, width=3),
                        ]), #, width=2),#, align='center'),
        #                style={"width": "18rem"},
                ])
            ),
            width=3),
       dbc.Col(     
            dbc.Card(    
                dbc.CardBody([             
                    dbc.Col([tabs
                        #dbc.Col([tabs])
                        ])# , width="auto")#, align='center')     
                    ])
                ),
            width=9),
       ]#color = 'dark'
    )
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
    Output ('cUpazilaAIO', 'options'),
    Input ('cDistrictAIO', 'value')
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
        Output ('cDistrictAIO', 'options'),
        Input ('cDivisionAIO', 'value')
        )
def set_Dislist(cDivision):  
    ddDislist=None
    if cDivision is None:
        ddDislist="",
        #raise PreventUpdate
    else:
        ddDislist=fetchDistrictlist(cDivision)
    return ddDislist

@callback(
        Output ('cMapAIO', 'figure'),
        [Input ('CMapAIO', 'clickData')]
        )
def update_region(geoTile):  
    print('Herasdasde')
    if geoTile is not None:
        print(geoTile['points'][0])['location'],
        print('There')
    else:
        print('Here')



#@app.callback(
@callback(
    Output ('CMapAIO', 'figure'),
    Output ('RepG1AIO', 'figure'),
    Output ('MonthAIO', 'figure'),
    Output ('SickAIO', 'figure'),
    Output ('DeadAIO', 'figure'),
    Output ('LiveSAIO', 'figure'),
    Output ('ZoonAIO', 'figure'),
    Output ('indicatorsAIO', 'figure'),
    
    #Output ('RepG2', 'figure'),
    
    Input('CMapAIO', 'clickData'),
#    Input("cReportAIO", 'value'),
    Input("cDateAIO",'start_date'),
    Input("cDateAIO",'end_date'),
    Input("cDiseaseAIO",'value'),
    Input("cDivisionAIO",'value'),
    Input("cDistrictAIO",'value'),
    Input("cUpazilaAIO",'value'),
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
)
def update_whatever(geoTile, start_date, end_date, cDisease, cDivision, cDistrict, cUpazila, theme):   #cReport, start_date, end_date, cDisease, cDivision, cDistrict, cUpazila, theme):   

    if geoTile is not None:
        print(geoTile['points'][0]['location'])
    
#    ddReplist=['Reports', 'Diseased Animals', 'Dead Animals', 'Monthly Comparison', 'Top 10 Numbers', 'Heat Map', 'Alerts']
 
    sub_bahis_sourcedata=date_subset(start_date, end_date)
    sub_bahis_sourcedata=disease_subset(cDisease, sub_bahis_sourcedata)

    if not cUpazila:
        if not cDistrict:
            if not cDivision:
                sub_bahis_sourcedata=sub_bahis_sourcedata
                path=path1
                loc=1
                title='basic_info_division'
                pname='divisionname'
                splace=' Division'
                variab='division'
                labl='Incidences per division'
            else:
                DivNo= bahis_geodata.loc[(bahis_geodata['name'].str.capitalize()==cDivision) & (bahis_geodata['loc_type']==1),'value'].values[0]
                sub_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata['basic_info_division']==int(DivNo)]   
                # path=path1
                # loc=1
                # title='basic_info_division'
                # pname='divisionname'
                # splace=' Division'
                # variab='division'
                # labl='Incidences per division'
                path=path2
                loc=2
                title='basic_info_district'
                pname='districtname'
                splace=' District'
                variab='district'
                labl='Incidences per district'
        else:
            DisNo= bahis_geodata.loc[(bahis_geodata['name'].str.capitalize()==cDistrict) & (bahis_geodata['loc_type']==2),'value'].values[0]
            sub_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata['basic_info_district']==int(DisNo)]
            path=path3
            loc=3
            title='basic_info_upazila'
            pname='upazilaname'
            splace=' Upazila'
            variab='Upazila'
            labl='Incidences per Upazila'
    else:
        #####check this
        UpaNo= bahis_geodata.loc[(bahis_geodata['name'].str.capitalize()==cUpazila) & (bahis_geodata['loc_type']==3),'value'].values[0]
        sub_bahis_sourcedata= sub_bahis_sourcedata.loc[sub_bahis_sourcedata['basic_info_upazila']==int(UpaNo)]
        #sub_bahis_sourcedata= sub_bahis_sourcedata
        path=path3
        loc=3
        title='basic_info_upazila'
        pname='upazilaname'
        splace=' Upazila'
        variab='upazila'
        labl='Incidences per upazila'
                
    # loc=1
    # title='basic_info_division'
    # pname='divisionname'
    # splace=' Division'
    # variab='division'
    # labl='Incidences per division'
    
    fig = plot_map(path, loc, sub_bahis_sourcedata, title, pname, splace, variab, labl, theme)

#def update_RepG1(cDate, cDisease, cDivision, cDistrict, cUpazila, theme):
#    figReport= go.Figure()

# 'Monthly Comparison', 'Top 10 Numbers', 'Heat Map', 'Alerts']
    
    #print(sub_bahis_sourcedata.dtypes)
#    if cReport=="Reports":
    tmp=sub_bahis_sourcedata['basic_info_date'].dt.date.value_counts()
    tmp=tmp.reset_index()
    tmp=tmp.rename(columns={'index':'date'})
    tmp['date'] = pd.to_datetime(tmp['date'])    
    #print(tmp.dtypes)        
    figgR= px.bar(tmp, x='date', y='basic_info_date')  
    figgR.update_layout(height=400)   
#    if cReport=='Month-wise comparison':
    tmp=sub_bahis_sourcedata['patient_info_sick_number'].groupby(sub_bahis_sourcedata['basic_info_date'].dt.to_period('M')).sum().astype(int)
    tmp=tmp.reset_index()
    tmp=tmp.rename(columns={'basic_info_date':'date'})
    tmp['date']=tmp['date'].astype(str)
    tmp['date'] = pd.to_datetime(tmp['date'])
    #tots= str(int(subs_bahis_sourcedata['patient_info_sick_number'].sum()))
    tmpdata={'sick':tmp['patient_info_sick_number'],
              'date':tmp['date']}
    tmpdata=pd.DataFrame(tmpdata)
#        figg= px.bar(tmpdata, x='month(date)', y='sick:Q', color='year(date)', barmode ='group')
    figgMonth= px.bar(tmpdata, x=pd.DatetimeIndex(tmpdata['date']).month, y='sick', color=pd.DatetimeIndex(tmpdata['date']).year.astype(str), barmode ='group')
#        figg.update_layout(height=400,xaxis=dict(tickformat="%d-%m"))   
#    if cReport=='Sick Animals':
    tmp=sub_bahis_sourcedata['patient_info_sick_number'].groupby(sub_bahis_sourcedata['basic_info_date'].dt.to_period('D')).sum().astype(int)
    tmp=tmp.reset_index()
    tmp=tmp.rename(columns={'basic_info_date':'date'})
    tmp['date'] = tmp['date'].astype('datetime64[D]')
    #print(tmp.dtypes)
    figgSick= px.bar(tmp, x='date', y='patient_info_sick_number')  
    figgSick.update_layout(height=400)   
#    if cReport=='Dead Animals':
    tmp=sub_bahis_sourcedata['patient_info_dead_number'].groupby(sub_bahis_sourcedata['basic_info_date'].dt.to_period('D')).sum().astype(int)
    tmp=tmp.reset_index()
    tmp=tmp.rename(columns={'basic_info_date':'date'})
    tmp['date'] = tmp['date'].astype('datetime64[D]')
    #print(tmp.dtypes)
    #print(tmp)
    figgDead= px.bar(tmp, x='date', y='patient_info_dead_number')  
    figgDead.update_layout(height=400)   
#    if cReport=='Livestock Disease Cases':          #######very slow! maybe a little less brute force...
    #subpl= make_subplots(rows=2, cols=1),
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
    figgLiveS.update_layout(height=700) 
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
    figgZoon.update_layout(height=700) 

    
    findic=fIndicator(sub_bahis_sourcedata)

    return fig, figgR, figgMonth, figgSick, figgDead, figgLiveS, figgZoon, findic #, figgg, 

# if __name__ == "__main__":
#     app.run_server(debug=True)





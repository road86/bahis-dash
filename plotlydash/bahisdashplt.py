# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 15:12:34 2022

@author: yoshka
"""


from dash import Dash, dash_table, dcc, html #, dbc 
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
from dash.dependencies import Input, Output
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
import json  


# dbc_css = "/dbc.min.css"
# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])

########################
img_logo= 'assets/Logo.png'

gifpath = 'C:/Users/yoshka/Documents/GitHub/bahis-dash/logos/'
sourcepath = 'C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/'
geofilename = sourcepath + 'newbahis_geo_cluster.csv'   # the available geodata from the bahis project
sourcefilename =sourcepath + 'preped_data2.csv'   
bahis_sd = pd.read_csv(sourcefilename)
img_logo= 'assets/Logo.png'

path0= "geodata/geoBoundaries-BGD-ADM0_simplified.geojson" #1 Nation # found shapefiles from the data.humdata.org
path1= "C:/Users/yoshka/Documents/GitHub/bahis-dash/geodata/geoBoundaries-BGD-ADM1_simplified.geojson" #8 Division
path2= "geodata/geoBoundaries-BGD-ADM2_simplified.geojson" #64 District
path3= "geodata/geoBoundaries-BGD-ADM3_simplified.geojson" #495 Upazila
path4= "geodata/geoBoundaries-BGD-ADM4_simplified.geojson" #4562 Union



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

# app = Dash(__name__)

# colors = {
#     'background': '#ffffff',
#     'text': '#000000'
# }

def fetchdiseaselist():
    dislis= bahis_sourcedata['top_diagnosis'].unique()
    dislis= pd.DataFrame(dislis, columns=['Disease'])
    dislis.sort_values(by=['Disease'])
    ddDList= dislis['Disease']
    return ddDList.tolist()
ddDList= fetchdiseaselist()
ddDList.insert(0, 'Select All')

def fetchDivisionlist():   
    ddDivlist=bahis_geodata[(bahis_geodata["loc_type"]==1)]['name'].str.capitalize()
    ddDivlist.name='Division'
    ddDivlist=ddDivlist.sort_values()
    return ddDivlist.tolist()
ddDivlist=fetchDivisionlist()
ddDivlist.insert(0,'Select All')

start_date=min(bahis_sourcedata['basic_info_date']).date()
end_date=max(bahis_sourcedata['basic_info_date']).date()
start_date=date(2021, 1, 1)

def natNo():
    mask=(bahis_sourcedata['basic_info_date']> datetime.now()-timedelta(days=30)) & (bahis_sourcedata['basic_info_date'] < datetime.now())
    tmp_sub_data=bahis_sourcedata['basic_info_date'].loc[mask]
    diff=tmp_sub_data.shape[0]
    
    tmp_sub_data=bahis_sourcedata['patient_info_sick_number'].loc[mask]
    diffsick=int(tmp_sub_data.sum().item())
    
    tmp_sub_data=bahis_sourcedata['patient_info_dead_number'].loc[mask]
    diffdead=int(tmp_sub_data.sum().item())
    return([diff, diffsick, diffdead])

[diff, diffsick, diffdead]=natNo()

def fIndicator():
    figIndic = go.Figure()
    
    figIndic.add_trace(go.Indicator(
        mode = "number+delta",
        title = 'Total Reports',
        value = bahis_sourcedata.shape[0], #f"{bahis_sourcedata.shape[0]:,}"),
        delta = {'reference': diff}, #'f"{diff:,}"},
        domain = {'row': 0, 'column': 0}))
    
    figIndic.add_trace(go.Indicator(
        mode = "number+delta",
        title = 'Sick Animals',
        value = bahis_sourcedata['patient_info_sick_number'].sum(), #f"{int(bahis_sourcedata['patient_info_sick_number'].sum()):,}",
        delta= {'reference': diffsick}, #f"{diffsick:,}",
        domain = {'row': 0, 'column': 1}))
    
    figIndic.add_trace(go.Indicator(
        mode = "number+delta",
        title = 'Dead Animals',
        value = bahis_sourcedata['patient_info_dead_number'].sum(), #f"{int(bahis_sourcedata['patient_info_dead_number'].sum()):,}",
        delta = {'reference': diffdead}, #f"{diffdead:,}",
        domain = {'row': 0, 'column': 2}))
    
    figIndic.update_layout(height=250,
        grid = {'rows': 1, 'columns': 3},# 'pattern': "independent"},
        #?template=template_from_url(theme),
    
        )
    return figIndic

dpDate = html.Div(
    [
         dcc.DatePickerRange(
            id='cDate',
            min_date_allowed=start_date,
            max_date_allowed=end_date,
            initial_visible_month=date(2022, 1, 1),
            start_date=date(2021, 1, 1),
            end_date=end_date
            ),
     ],
    className='mb-4',
)


# def set_dates():
#     st.header('Please select the date range for the following reports')
#     colsdate, coledate, colplaceholder = st.columns([1,1,3])
#     with colsdate:
#         sdate= st.date_input('Select beginning date of report', value= start_date, min_value= start_date, max_value= end_date, key='sdate')
#     with coledate:
#         edate= st.date_input('Select ending date of report', value= end_date, min_value= start_date, max_value= end_date, key='edate')
#     dates=[sdate, edate]
#     st.subheader("Currently selected Date range: From " + str(dates[0]) + " until " + str(dates[1]))
#     return (bahis_sourcedata['basic_info_date']>= pd.to_datetime(dates[0])) & (bahis_sourcedata['basic_info_date'] <= pd.to_datetime(dates[1]))
# tmask=set_dates()

# @st.cache
# def date_subset():
#     return bahis_sourcedata.loc[tmask]
# sub_bahis_sourcedata=date_subset()


ddDivision = html.Div(
    [
        dbc.Label("Select Division"),
        dcc.Dropdown(
            ddDivlist,
            "pop",
            id="cDivision",
            clearable=False,
        ),
    ],
    className="mb-4",
)

ddDistrict = html.Div(
    [
        dbc.Label("Select District"),
        dcc.Dropdown(
            ["District", "Funny Disease", "Don't care Disease"],
            "pop",
            id="cDistrict",
            clearable=False,
        ),
    ],
    className="mb-4",
)

ddUpazila = html.Div(
    [
        dbc.Label("Select Upazila"),
        dcc.Dropdown(
            ["Upazila", "Funny Disease", "Don't care Disease"],
            "pop",
            id="cUpazila",
            clearable=False,
        ),
    ],
    className="mb-4",
)

ddDisease = html.Div(
    [
        dbc.Label("Select disease"),
        dcc.Dropdown(
            ddDList,
            "pop",
            id="cDisease",
            clearable=False,
        ),
    ],
    className="mb-4",
)


    # if 'Select All' in disease_chosen_D:
    #     subd_bahis_sourcedata=sub_bahis_sourcedata 
    # else:     
    #     subd_bahis_sourcedata=sub_bahis_sourcedata[sub_bahis_sourcedata['top_diagnosis'].isin(disease_chosen_D)] 
        
        

def open_data(path):
    with open(path) as f:
        data = json.load(f)
        return data

def plot_map(path, loc, subd_bahis_sourcedata, title, pname, splace, variab, labl):
    subDist=bahis_geodata[(bahis_geodata["loc_type"]==loc)]  
    reports = bahis_sourcedata[title].value_counts().to_frame()
    reports.index = reports.index.astype(int)
    reports[pname] = reports.index
    reports= reports.loc[reports[pname] != 'nan']    
    data = open_data(path1)

    for i in data['features']:
        i['id']= i['properties']['shapeName'].replace(splace,"")
    for i in range(reports.shape[0]):
        #reports[pname].iloc[i] = subDist.loc[subDist['value']==int(reports[pname].iloc[i]),'name'].iloc[0]
        reports[pname].iloc[i] = subDist[subDist['value']==reports.index[i]]['name'].values[0]
#    reports[pname]=reports[pname].str.title()                   

    fig = px.choropleth_mapbox(reports, geojson=data, locations=pname, color=title,
                            featureidkey="Cmap",
                            color_continuous_scale="YlOrBr",
                            range_color=(0, reports[title].max()),
                            mapbox_style="carto-positron",
                            zoom=6.4, center = {"lat": 23.7, "lon": 90},
                            opacity=0.5,
                            labels={variab:labl}
                          )
    fig.update_layout(autosize=True, margin={"r":0,"t":0,"l":0,"b":0}, width=850 , height=800) #, coloraxis_showscale= False) #width= 1000, height=600, 
    return fig
                      

# figReport= go.Figure()
# tmp=bahis_sourcedata['basic_info_date'].dt.date.value_counts()
# tmp=tmp.reset_index()
# tmp=tmp.rename(columns={'index':'date'})
# tmp['date'] = pd.to_datetime(tmp['date'])    
# tots= str(bahis_sourcedata.shape[0])

# figReport= px.bar(tmp, x='date', y='basic_info_date')
    
tabs=dbc.Card([dcc.Graph(id='RepG1'), dcc.Graph(id='RepG2')]) #figure=figReport))


# stylesheet with the .dbc class
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])

header = html.H4(
    "BAHIS dashboard", className="bg-primary text-white p-2 mb-2 text-center"
)

row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Img(src=img_logo, style={'width':'100%', 'margin-left': '20px'} ), width=3),
                dbc.Col(html.Div(header), width=8),
                dbc.Col(html.Div("Placeholder"), width=1),
            ]),
        dbc.Row(),
        dbc.Row(
            [
                dbc.Col(html.B(html.H1("National numbers")), width=2),
                dbc.Col(dcc.Graph(
                                id='indicators',
                                figure=fIndicator()
                            ),width=8),  
            ], justify="center", align="center", className="mb-42"), #"h-50"),
        dbc.Row(
            [
                dbc.Col(
                    [dbc.Card([dpDate, ddDisease, ddDivision, ddDistrict, ddUpazila], body=True)
                     ], width=2),
                dbc.Col([
                    dbc.Row([dbc.Card([html.H4("Description")], body=True)]),
                    dbc.Row([dbc.Card(dcc.Graph(
                                    id='CMap',
#                                    figure=figMap
                                    ), body=True)])
                     ], width=5
                    ),
                dbc.Col([tabs], width=5),
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

app.layout = dbc.Container(
    [
        html.Div("Preselect local/server"),
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

@app.callback(
    
    Output ('CMap', 'figure'),
    Output ('RepG1', 'figure'),
    Output ('RepG2', 'figure'),
    
    Input("cDate",'start_date'),
    Input("cDisease",'value'),
    Input("cDivision",'value'),
    Input("cDistrict",'value'),
    Input("cUpazila",'value'),
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
)

def update_whatever(start_date, cDisease, cDivision, cDistrict, cUpazila, theme):
 
    loc=1
    title='basic_info_division'
    pname='divisionname'
    splace=' Division' 
    variab='division'
    labl='Incidences per division'
    
    fig = plot_map(path1, loc, bahis_sourcedata, title, pname, splace, variab, labl)

#def update_RepG1(cDate, cDisease, cDivision, cDistrict, cUpazila, theme):
#    figReport= go.Figure()
    tmp=bahis_sourcedata['basic_info_date'].dt.date.value_counts()
    tmp=tmp.reset_index()
    tmp=tmp.rename(columns={'index':'date'})
    tmp['date'] = pd.to_datetime(tmp['date'])    
#    tots= str(bahis_sourcedata.shape[0])
    
    figg= px.bar(tmp, x='date', y='basic_info_date')        
    return fig, figg, figg

if __name__ == "__main__":
    app.run_server(debug=True)



















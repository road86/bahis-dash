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
import altair as alt    


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
    bahis_sd = pd.read_csv(sourcefilename) ################CC
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
            id='my-date-picker-range',
            min_date_allowed=start_date,
            max_date_allowed=end_date,
            initial_visible_month=date(2022, 1, 1),
            start_date=date(2021, 1, 1),
            end_date=end_date
            ),
     ],
    className='mb-4',
)

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

def open_data(path):
    with open(path) as f:
        data = json.load(f)
        return data

def plot_map(path, loc, subd_bahis_sourcedata, title, pname, splace, variab, labl):
    #path= path1
    subDist=bahis_geodata[(bahis_geodata["loc_type"]==loc)]
    reports = subd_bahis_sourcedata[title].value_counts().to_frame()
    reports[pname] = reports.index
    reports= reports.loc[reports[pname] != 'nan']    
    data = open_data(path)
    for i in range(reports.shape[0]):
        reports[pname].iloc[i] = subDist.loc[subDist['value']==int(reports[pname].iloc[i]),'name'].iloc[0]
    reports[pname]=reports[pname].str.title()                   
    for i in data['features']:
        i['id']= i['properties']['shapeName'].replace(splace,"")

    fig = px.choropleth_mapbox(reports, geojson=data, locations=pname, color=title,
                            color_continuous_scale="Viridis",
                            range_color=(0, reports[title].max()),
                            mapbox_style="carto-positron",
                            zoom=5.5, center = {"lat": 23.7, "lon": 90},
                            opacity=0.5,
                            labels={variab:labl}
                          )
    fig.update_layout(autosize=True, margin={"r":0,"t":0,"l":0,"b":0}, coloraxis_showscale= False) #width= 1000, height=600, 
    return fig

loc=1
title='basic_info_division'
pname='divisionname'
splace=' Division' 
variab='division'
labl='Incidences per division'
figMap = plot_map(path1, loc, bahis_sourcedata, title, pname, splace, variab, labl)
                        

figReport= go.Figure()
#region_placeholder.header('Report Dynamics for: Bangladesh')
tmp=bahis_sourcedata['basic_info_date'].dt.date.value_counts()
tmp=tmp.reset_index()
tmp=tmp.rename(columns={'index':'date'})
tmp['date'] = pd.to_datetime(tmp['date'])    
tots= str(bahis_sourcedata.shape[0])

figReport= px.bar(tmp, x='date', y='basic_info_date')
    
#     tmp2w, height=600).mark_line(point=alt.OverlayMarkDef(color="red")).encode( #interpolate='basis').encode(
#     alt.X('date:T', title='report date', axis= alt.Axis(format='%Y %B %d')), # scale= alt.Scale(nice={'interval': 'week', 'step': 4})), 
#     alt.Y('basic_info_date:Q', title='reports'),
#     color=alt.Color('Category:N', legend=None)
#     ).properties(title='Registered reports :  ' + tots)
# altair_chart(line_chart, use_container_width=True)



df = px.data.gapminder()
years = df.year.unique()
continents = df.continent.unique()

table = html.Div(
    dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i, "deletable": True} for i in df.columns],
        data=df.to_dict("records"),
        page_size=10,
        editable=True,
        cell_selectable=True,
        filter_action="native",
        sort_action="native",
        style_table={"overflowX": "auto"},
        row_selectable="multi",
    ),
    className="dbc-row-selectable",
)

tab1 = dbc.Tab([dcc.Graph(id="line-chart")], label="Line Chart")
tab2 = dbc.Tab([dcc.Graph(id="scatter-chart")], label="Scatter Chart")
tab3 = dbc.Tab([table], label="Table", className="p-4")
#tabs = dbc.Card(dbc.Tabs([tab1, tab2, tab3]))


tabs=dbc.Card(dcc.Graph(figure=figReport))


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
                                    id='Map',
                                    figure=figMap
                                    ), body=True)])
                     ], width=5
                    ),
                dbc.Col([tabs], width=5),
#                dbc.Col(html.Div("One of three columns"), width=3),
            ]
        ),
    ]
)

# checklist = html.Div(
#     [
#         dbc.Label("Select Continents"),
#         dbc.Checklist(
#             id="continents",
#             options=[{"label": i, "value": i} for i in continents],
#             value=continents,
#             inline=True,
#         ),
#     ],
#     className="mb-4",
# )

slider = html.Div(
    [
        dbc.Label("Select Years"),
        dcc.RangeSlider(
            years[0],
            years[-1],
            5,
            id="years",
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
            value=[years[2], years[-2]],
            className="p-0",
        ),
    ],
    className="mb-4",
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
colors = html.Div(
    [dbc.Button(f"{color}", color=f"{color}", size="sm") for color in theme_colors]
)
colors = html.Div(["Theme Colors:", colors], className="mt-2")


# controls = dbc.Card(
#     [dropdown, checklist, slider],
#     body=True,
# )

# tab1 = dbc.Tab([dcc.Graph(id="line-chart")], label="Line Chart")
# tab2 = dbc.Tab([dcc.Graph(id="scatter-chart")], label="Scatter Chart")
# tab3 = dbc.Tab([table], label="Table", className="p-4")
# tabs = dbc.Card(dbc.Tabs([tab1, tab2, tab3]))

app.layout = dbc.Container(
    [
        html.Div("Preselect local/server"),
        row,
        dbc.Row(
            [
                dbc.Col(
                    [
                       # controls,
                        ThemeChangerAIO(aio_id="theme")
                    ],
                    width=4,
                ),
#                dbc.Col([tabs, colors], width=8),
            ]
        ),
    ],
    fluid=True,
    className="dbc",
)


@app.callback(


    Output("line-chart", "figure"),
    Output("scatter-chart", "figure"),
    Output("table", "data"),
#    Input("indicator", "value"),
    Input("continents", "value"),
    Input("years", "value"),
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
)
def update_line_chart(continent, yrs, theme): #indicator, 
    if continent == []: # or indicator is None:
        return {}, {}, []

    dff = df[df.year.between(yrs[0], yrs[1])]
    dff = dff[dff.continent.isin(continent)]
    data = dff.to_dict("records")

    # fig = px.line(
    #     dff,
    #     x="year",
    #     y=indicator,
    #     color="continent",
    #     line_group="country",
    #     template=template_from_url(theme),
    # )

    fig_scatter = px.scatter(
        df.query(f"year=={yrs[1]} & continent=={continent}"),
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        log_x=True,
        size_max=60,
        template=template_from_url(theme),
        title="Gapminder %s: %s theme" % (yrs[1], template_from_url(theme)),
    )

    return fig, fig_scatter, data


if __name__ == "__main__":
    app.run_server(debug=True)
















###############################


# #gifpath = 'logos/'
# #sourcepath = 'exported_data/'
# gifpath = 'C:/Users/yoshka/Documents/GitHub/bahis-dash/logos/'
# sourcepath = 'C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/'
# geofilename = sourcepath + 'newbahis_geo_cluster.csv'   # the available geodata from the bahis project
# sourcefilename =sourcepath + 'preped_data2.csv'   
# bahis_sd = pd.read_csv(sourcefilename)
# img_logo= 'assets/Logo.png'

# def fetchsourcedata():
# #    bahis_sd = pd.read_csv(sourcefilename) ################CC
#     bahis_sd['basic_info_division'] = pd.to_numeric(bahis_sd['basic_info_division'])
#     bahis_sd['basic_info_district'] = pd.to_numeric(bahis_sd['basic_info_district'])
#     bahis_sd['basic_info_upazila'] = pd.to_numeric(bahis_sd['basic_info_upazila'])
#     bahis_sd['basic_info_date'] = pd.to_datetime(bahis_sd['basic_info_date'])
#     return bahis_sd
# bahis_sourcedata= fetchsourcedata()

# app = Dash(__name__)

# colors = {
#     'background': '#ffffff',
#     'text': '#000000'
# }

# mask=(bahis_sourcedata['basic_info_date']> datetime.now()-timedelta(days=30)) & (bahis_sourcedata['basic_info_date'] < datetime.now())
# tmp_sub_data=bahis_sourcedata['basic_info_date'].loc[mask]
# diff=tmp_sub_data.shape[0]

# tmp_sub_data=bahis_sourcedata['patient_info_sick_number'].loc[mask]
# diffsick=int(tmp_sub_data.sum().item())

# tmp_sub_data=bahis_sourcedata['patient_info_dead_number'].loc[mask]
# diffdead=int(tmp_sub_data.sum().item())


# fig = go.Figure()

# fig.add_trace(go.Indicator(
#     mode = "number+delta",
#     value = bahis_sourcedata.shape[0], #f"{bahis_sourcedata.shape[0]:,}"),
#     delta = {'reference': diff}, #'f"{diff:,}"},
#     domain = {'row': 0, 'column': 0}))

# fig.add_trace(go.Indicator(
#     mode = "number+delta",
#     value = bahis_sourcedata['patient_info_sick_number'].sum(), #f"{int(bahis_sourcedata['patient_info_sick_number'].sum()):,}",
#     delta= {'reference': diffsick}, #f"{diffsick:,}",
#     domain = {'row': 0, 'column': 1}))

# fig.add_trace(go.Indicator(
#     mode = "number+delta",
#     value = bahis_sourcedata['patient_info_dead_number'].sum(), #f"{int(bahis_sourcedata['patient_info_dead_number'].sum()):,}",
#     delta = {'reference': diffdead}, #f"{diffdead:,}",
#     domain = {'row': 0, 'column': 2}))

# fig.update_layout(
#     grid = {'rows': 1, 'columns': 3, 'pattern': "independent"},

#     )

# bahis_sourcedata=bahis_sourcedata.loc[bahis_sourcedata['basic_info_date']>=pd.to_datetime("20190101")]
# start_date=min(bahis_sourcedata['basic_info_date']).date()
# end_date=max(bahis_sourcedata['basic_info_date']).date()
# dates=[start_date, end_date]



# ######################## Layout

# app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    
#     html.Img(src=img_logo, style={'width':'25%', 'margin-left': '20px'} ),
    
   
#     html.H1(
#         children='BAHIS dashboard',
#         style={
#             'textAlign': 'left',
#             'color': colors['text'],
#             'font-family': 'Helvetica',
#             'font_size': '72px',
#         }
#     ),
    
#     html.Div(children=[
#         html.Div(children=[
#             html.H1(
#                 children='National numbers:',
#                 style={
#                     'textAlign': 'left',
#                     'color': colors['text'],
#                     'font-family': 'Helvetica'
#                 }
#                 )],#style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'}
#         ),
#         html.Div(children=[            
#             dcc.Graph(
#                 id='example-graph-2',
#                 figure=fig
#             ),
#             ],style={'display': 'inline-block'}#, 'vertical-align': 'top'} #, 'margin-left': '3vw', 'margin-top': '3vw'}
#         ),
#         ], style={'display': 'inline-block'} #'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'}
#     ),     
    

#     html.Div(children=[
    
#         dcc.DatePickerRange(
#             id='my-date-picker-range',
#             min_date_allowed=start_date,
#             max_date_allowed=end_date,
#             #initial_visible_month=start_date,
#             start_date=start_date,
#             end_date=end_date
#         ),
#         html.Div(id='output-container-date-picker-range')
#     ]),
    
#     dcc.Graph(
#         id='example-graph-3',
#         figure=fig
#     ),        
# ])


# ######################### Callback

# @app.callback(
#     Output('output-container-date-picker-range', 'children'),
#     Input('my-date-picker-range', 'start_date'),
#     Input('my-date-picker-range', 'end_date'))
# def update_output(start_date, end_date):
#     string_prefix = 'You have selected: '
#     if start_date is not None:
#         start_date_object = date.fromisoformat(start_date)
#         start_date_string = start_date_object.strftime('%B %d, %Y')
#         string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
#     if end_date is not None:
#         end_date_object = date.fromisoformat(end_date)
#         end_date_string = end_date_object.strftime('%B %d, %Y')
#         string_prefix = string_prefix + 'End Date: ' + end_date_string
#     if len(string_prefix) == len('You have selected: '):
#         return 'Select a date to see it displayed here'
#     else:
#         return string_prefix
    
# if __name__ == '__main__':
#     app.run_server(debug=True)


# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 15:12:34 2022

@author: yoshka
"""


from dash import Dash, dcc, html #, dbc 
#import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
from dash.dependencies import Input, Output

#gifpath = 'logos/'
#sourcepath = 'exported_data/'
gifpath = 'C:/Users/yoshka/Documents/GitHub/bahis-dash/logos/'
sourcepath = 'C:/Users/yoshka/Documents/GitHub/bahis-dash/exported_data/'
geofilename = sourcepath + 'newbahis_geo_cluster.csv'   # the available geodata from the bahis project
sourcefilename =sourcepath + 'preped_data2.csv'   
bahis_sd = pd.read_csv(sourcefilename)
img_logo= 'assets/Logo.png'

def fetchsourcedata():
#    bahis_sd = pd.read_csv(sourcefilename) ################CC
    bahis_sd['basic_info_division'] = pd.to_numeric(bahis_sd['basic_info_division'])
    bahis_sd['basic_info_district'] = pd.to_numeric(bahis_sd['basic_info_district'])
    bahis_sd['basic_info_upazila'] = pd.to_numeric(bahis_sd['basic_info_upazila'])
    bahis_sd['basic_info_date'] = pd.to_datetime(bahis_sd['basic_info_date'])
    return bahis_sd
bahis_sourcedata= fetchsourcedata()

app = Dash(__name__)

colors = {
    'background': '#ffffff',
    'text': '#000000'
}

mask=(bahis_sourcedata['basic_info_date']> datetime.now()-timedelta(days=30)) & (bahis_sourcedata['basic_info_date'] < datetime.now())
tmp_sub_data=bahis_sourcedata['basic_info_date'].loc[mask]
diff=tmp_sub_data.shape[0]

tmp_sub_data=bahis_sourcedata['patient_info_sick_number'].loc[mask]
diffsick=int(tmp_sub_data.sum().item())

tmp_sub_data=bahis_sourcedata['patient_info_dead_number'].loc[mask]
diffdead=int(tmp_sub_data.sum().item())


fig = go.Figure()

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = bahis_sourcedata.shape[0], #f"{bahis_sourcedata.shape[0]:,}"),
    delta = {'reference': diff}, #'f"{diff:,}"},
    domain = {'row': 0, 'column': 0}))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = bahis_sourcedata['patient_info_sick_number'].sum(), #f"{int(bahis_sourcedata['patient_info_sick_number'].sum()):,}",
    delta= {'reference': diffsick}, #f"{diffsick:,}",
    domain = {'row': 0, 'column': 1}))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = bahis_sourcedata['patient_info_dead_number'].sum(), #f"{int(bahis_sourcedata['patient_info_dead_number'].sum()):,}",
    delta = {'reference': diffdead}, #f"{diffdead:,}",
    domain = {'row': 0, 'column': 2}))

fig.update_layout(
    grid = {'rows': 1, 'columns': 3, 'pattern': "independent"},

    )

bahis_sourcedata=bahis_sourcedata.loc[bahis_sourcedata['basic_info_date']>=pd.to_datetime("20190101")]
start_date=min(bahis_sourcedata['basic_info_date']).date()
end_date=max(bahis_sourcedata['basic_info_date']).date()
dates=[start_date, end_date]



######################## Layout

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    
    html.Img(src=img_logo, style={'width':'25%', 'margin-left': '20px'} ),
    
   
    html.H1(
        children='BAHIS dashboard',
        style={
            'textAlign': 'left',
            'color': colors['text'],
            'font-family': 'Helvetica',
            'font_size': '72px',
        }
    ),
    
    html.Div(children=[
        html.Div(children=[
            html.H1(
                children='National numbers:',
                style={
                    'textAlign': 'left',
                    'color': colors['text'],
                    'font-family': 'Helvetica'
                }
                )],#style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'}
        ),
        html.Div(children=[            
            dcc.Graph(
                id='example-graph-2',
                figure=fig
            ),
            ],style={'display': 'inline-block'}#, 'vertical-align': 'top'} #, 'margin-left': '3vw', 'margin-top': '3vw'}
        ),
        ], style={'display': 'inline-block'} #'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'}
    ),     
    

    html.Div(children=[
    
        dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=start_date,
            max_date_allowed=end_date,
            #initial_visible_month=start_date,
            start_date=start_date,
            end_date=end_date
        ),
        html.Div(id='output-container-date-picker-range')
    ]),
    
    dcc.Graph(
        id='example-graph-3',
        figure=fig
    ),        
])


######################### Callback

@app.callback(
    Output('output-container-date-picker-range', 'children'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix
    
if __name__ == '__main__':
    app.run_server(debug=True)


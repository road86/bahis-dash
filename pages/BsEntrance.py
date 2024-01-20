import dash
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
# import json


dash.register_page(__name__,)  # register page to main dash app

layout = [
    html.Label("Biosecurity Practice Entrance"),
    dbc.Row(
                dcc.Graph(id="BSEntrance"),
            ),
    html.Div(id="dummy"),
]


@callback(
    Output("BSEntrance", "figure"),
    Input("dummy", "id"),
    State("cache_page_farmdata", "data"),
    State("cache_page_settings", "data"),
    prevent_initial_call=True
)
def BSEntrance(dummy, data, settings):
    farmdata = pd.read_json(data, orient="split")
    print(farmdata.shape[0])
    print(len(farmdata[(farmdata['outsider_vehicles_entry']==0)])),
    print(len(farmdata[(farmdata['outsider_vehicles_entry']==1)])),
    # print(farmdata['workers_approve_visitor_entry']),
    # print(farmdata['manure_collector_entry']),
    # print(farmdata['fenced_and_duck_chicken_proof']),
    # print(farmdata['dead_birds_disposed_safely']),
    # print(farmdata['sign_posted_1st']),
    
    fig = []
    return fig

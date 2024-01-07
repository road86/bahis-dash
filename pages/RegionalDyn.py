import dash
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import json
import plotly.express as px

dash.register_page(__name__,)  # register page to main dash app

layout = [
    html.Label("Regional Dynamics Report"),
    dbc.Row([
            dbc.Col(
                dcc.Graph(id="RegionalDynamics")
            ),
            html.Div(id="dummy"),
            ])
]


@callback(
    Output("RegionalDynamics", "figure"),
    Input("dummy", "id"),
    State("cache_page_data", "data"),
    State("cache_page_geodata", "data"),
    State("cache_page_settings", "data"),
    prevent_initial_call=True
)
def RegionalStats(dummy, data, geodata, settings):

    reportsdata = pd.read_json(data, orient="split")
    geolocdata = pd.read_json(geodata, orient="split")
    geoResolutionNo = json.loads(settings)["georesolution"]

    geolocdata = geolocdata[geolocdata["loc_type"] == geoResolutionNo]
    
    if geoResolutionNo == 1:
        geoResolution = "division"
    if geoResolutionNo == 2:
        geoResolution = "district"
    if geoResolutionNo == 3:
        geoResolution = "upazila"
    reportsdata["date"] = pd.to_datetime(reportsdata["date"])
    reportsdata = reportsdata.sort_values(by=["date"])
    reportsdata["entries"] = 1
    reportsdata["acc"] = reportsdata.groupby(geoResolution)["entries"].cumsum() 
    reportsdata[geoResolution] = reportsdata[geoResolution].map(geolocdata.set_index("value")["name"])
    reportsdata[geoResolution]=reportsdata[geoResolution].str.capitalize()
    RegionalDynamics = px.line(reportsdata, x="date", y="acc", color=geoResolution, markers=True,
                               title="Sum of Reports over Dates by " + geoResolution)

    return RegionalDynamics

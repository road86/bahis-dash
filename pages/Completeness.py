import dash
from components import CompletenessReport
from dash import html, dcc, callback, ctx
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd


dash.register_page(__name__,)  # register page to main dash app

layout = [ 
        html.Label("Weekly Completeness"),
        dbc.Col(
            [
                dcc.Graph(id="Completeness")
            ]
        )
]


@callback(
    Output("Completeness", "figure"),
    State("Completeness", "figure"),
    State("cache_bahis_data", "data"),
    State("cache_bahis_geodata", "data"),
    State("cache_page_settings", "data"),
    prevent_initial_call=True
)

def Completeness(CompletenessFig, sourcedata, geodata, settings): 

    reportsdata = pd.read_json(sourcedata, orient="split")
    geoNameNNumber = pd.read_json(geodata, orient="split")
    if SelectedUpazila==None:
        CompletenessFig = CompletenessReport.generate_reports_heatmap(reportsdata,
            geoNameNNumber, DateRange[0], DateRange[1], SelectedDivision, SelectedDistrict)
    else:
        CompletenessFig = CompletenessFig
    
    return CompletenessFig 
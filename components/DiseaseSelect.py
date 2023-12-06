from components import fetchdata
import dash_bootstrap_components as dbc
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import pandas as pd

ddDList=[]

Form = html.Div([
    dcc.Store(id="cache_bahis_data"),
#    dbc.Label("Select Disease"),
    dcc.Dropdown(
        ddDList,
        "All Diseases",
        id="Disease",
        multi=False,
        clearable=False,
    ),
])

@callback(
    Output("Disease", "options", allow_duplicate=True),
    Input("cache_bahis_data", "data"),
    prevent_initial_call=True
)

def DiseaseList(bahis_data):
    List = fetchdata.fetchDiseaselist(pd.read_json(bahis_data, orient="split"))
    return List

#         ddDList = fetchdata.fetchdiseaselist(sub_bahis_sourcedata)
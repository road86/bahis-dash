import pandas as pd
from dash import callback, dcc, html
from dash.dependencies import Input, Output

from components import fetchdata

ddDList = []

Form = html.Div(
    [
        #    dcc.Store(id="cache_bahis_data"),
        #    dbc.Label("Select Disease"),
        dcc.Dropdown(
            ddDList,
            "All Diseases",
            id="Disease",
            multi=False,
            clearable=False,
        ),
    ]
)


@callback(
    Output("Disease", "options", allow_duplicate=True), Input("cache_bahis_data", "data"), prevent_initial_call=True
)
def DiseaseList(bahis_data):
    List = fetchdata.fetchDiseaselist(pd.read_json(bahis_data, orient="split"))
    return List

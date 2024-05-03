import pandas as pd
from dash import callback, dcc, html
from dash.dependencies import Input, Output

from components import fetchdata

ddSList = []

Form = html.Div(
    [
        dcc.Dropdown(
            ddSList,
            "All Species",
            id="Species",
            multi=False,
            clearable=False,
        ),
    ]
)


@callback(
    Output("Species", "options", allow_duplicate=True), Input("cache_bahis_data", "data"), prevent_initial_call=True
)
def DiseaseList(bahis_data):
    List = fetchdata.fetchDiseaselist(pd.read_json(bahis_data, orient="split"))
    return List

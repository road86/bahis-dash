import pandas as pd
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State

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


@callback(Output("Species", "options"), Input("cache_page_data", "data"))  # , prevent_initial_call=True
def Specieslist(bahis_data):
    List = fetchdata.fetchSpecieslist(pd.read_json(bahis_data, orient="split"))
    return List

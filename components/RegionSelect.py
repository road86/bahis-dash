import dash_bootstrap_components as dbc
import pandas as pd
from dash import callback, dcc, html
from dash.dependencies import Input, Output

from components import fetchdata

Form = html.Div(
    [
        # dcc.Store(id="cache_bahis_geodata"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(id="Division", clearable=True, placeholder="Select Division"),
                    ]
                ),
                dbc.Col(
                    [
                        dcc.Dropdown(id="District", clearable=True, placeholder="Select District"),
                    ]
                ),
                dbc.Col(
                    [
                        dcc.Dropdown(id="Upazila", clearable=True, placeholder="Select Upazila"),
                    ]
                ),
            ]
        )
    ]
)


@callback(Output("Division", "options"), Input("cache_bahis_geodata", "data"), prevent_initial_call=True)
def DivisionList(geodata):
    List = fetchdata.fetchDivisionlist(pd.read_json(geodata, orient="split"))
    DivisionList = [{"label": i["Division"], "value": i["value"]} for i in List]
    return DivisionList

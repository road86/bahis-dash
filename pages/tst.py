import dash
from components import fetchdata
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd



dash.register_page(__name__)  # register page to main dash app

Divlist = []

ddDivision = html.Div(
    [
        dbc.Label("Division"),
        dcc.Dropdown(
            options=[{"label": i["Division"], "value": i["value"]} for i in Divlist],
            id="Division",
            clearable=True,
            placeholder="Select Division"
        ),
    ],
    className="mb-4",
)

ddDistrict = html.Div(
    [
        dbc.Label("District"),
        dcc.Dropdown(
            id="District",
            clearable=True,
            placeholder="Select District"
        ),
    ],
    className="mb-4",
)

ddUpazila = html.Div(
    [
        dbc.Label("Upazila"),
        dcc.Dropdown(
            id="Upazila",
            clearable=True,
            placeholder="Select Upazila"
        ),
    ],
    className="mb-4",
)

layout = html.Div([
    # dcc.Store(id="cache_bahis_data", storage_type="memory"),
    # dcc.Store(id="cache_bahis_dgdata", storage_type="memory"),
    # dcc.Store(id="cache_bahis_distypes", storage_type="memory"),
    dcc.Store(id="cache_bahis_geodata"),
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            dbc.Row([dbc.Col(ddDivision), dbc.Col(ddDistrict), dbc.Col(ddUpazila)])
                        ),
                    ),
                    dbc.Card(
                        dbc.CardBody(
                            [dcc.Graph(id="Map"),
                                dcc.Slider(
                                    min=1,
                                    max=3,
                                    step=1,
                                    marks={
                                        1: "Division",
                                        2: "District",
                                        3: "Upazila",
                                    },
                                    value=3,
                                    id="geoSlider",
                            )
                            ]
                        )
                    )
                ],
                width=4,
            ),
        ]
    )
]),

@callback(
    Output("Division", "options"),
    Input("cache_bahis_geodata", "data")
)
def divlist(data):
    Divlist = fetchdata.fetchDivisionlist(pd.read_json(data, orient="split"))
    vDiv = [{"label": i["Division"], "value": i["value"]} for i in Divlist]
    return vDiv
import dash
from components import ReportsSickDead
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import json


dash.register_page(
    __name__,
)  # register page to main dash app


def layout_gen(aid=None, **other_unknown_query_strings):
    if aid is not None:
        dcc.Store(id="cache_aid", storage_type="memory", data=aid),
    return html.Div(
        [
            # html.Label("Remaining Animals Report"),
            html.H2("Remaining Animals Report", style={"textAlign": "center", "font-weight": "bold"}),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Row(dcc.Graph(id="ReportsR")),
                            dbc.Row(dcc.Graph(id="SickR")),
                            dbc.Row(dcc.Graph(id="DeadR")),
                        ]
                    ),
                    dbc.Col(
                        [
                            dcc.Slider(
                                min=1,
                                max=3,
                                step=1,
                                marks={
                                    1: "Reports monthly",
                                    2: "Reports weekly",
                                    3: "Reports daily",
                                },
                                value=2,
                                vertical=True,
                                id="RperiodSlider",
                            )
                        ],
                        width=1,
                    ),
                    html.Div(id="dummy"),
                ]
            ),
        ]
    )


layout = layout_gen


@callback(
    Output("ReportsR", "figure"),
    Output("SickR", "figure"),
    Output("DeadR", "figure"),
    Input("RperiodSlider", "value"),
    Input("dummy", "id"),
    State("cache_page_data", "data"),
    State("cache_page_settings", "data"),
    prevent_initial_call=True,
)
def Poultry(RperiodClick, dummy, data, settings):
    reportsdata = pd.read_json(data, orient="split")
    DateRange = json.loads(settings)["daterange"]
    LargeAnimal = ["Buffalo", "Cattle", "Goat", "Sheep"]
    reportsdata = reportsdata[~reportsdata["species"].isin(LargeAnimal)]
    Poultry = ["Chicken", "Duck", "Goose", "Pegion", "Quail", "Turkey"]
    reportsdata = reportsdata[~reportsdata["species"].isin(Poultry)]
    figheight = 190

    figgRR, figgRSick, figgRDead = ReportsSickDead.ReportsSickDead(
        reportsdata, DateRange, RperiodClick, figheight, "NPoultry"
    )
    return figgRR, figgRSick, figgRDead

import json

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State

from components import ReportsSickDead, SpeciesSelect, fetchdata

dash.register_page(
    __name__,
)  # register page to main dash app


def layout_gen(aid=None, **other_unknown_query_strings):
    if aid is not None:
        dcc.Store(id="cache_aid", storage_type="memory", data=aid),
    return html.Div(
        [
            # html.Label("Specieswise Report"),
            html.H2("Specieswise Report", style={"textAlign": "center", "font-weight": "bold"}),
            dbc.Row(SpeciesSelect.Form),
            html.Br(),
            html.Div(id="dummy"),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Row(dcc.Graph(id="ReportsSW")),
                            dbc.Row(dcc.Graph(id="SickSW")),
                            dbc.Row(dcc.Graph(id="DeadSW")),
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
                                id="SWperiodSlider",
                            )
                        ],
                        width=1,
                    ),
                ]
            ),
        ]
    )


layout = layout_gen


@callback(
    Output("ReportsSW", "figure"),
    Output("SickSW", "figure"),
    Output("DeadSW", "figure"),
    Input("Species", "value"),
    Input("SWperiodSlider", "value"),
    Input("dummy", "id"),
    State("cache_page_data", "data"),
    State("cache_page_settings", "data"),
    prevent_initial_call=True,
)
def SpeciesWise(Species, SWperiodClick, dummy, data, settings):
    reportsdata = pd.read_json(data, orient="split")
    DateRange = json.loads(settings)["daterange"]
    reportsdata = fetchdata.species_subset(Species, reportsdata)
    figheight = 190

    figgSWR, figgSWSick, figgSWDead = ReportsSickDead.ReportsSickDead(
        reportsdata, DateRange, SWperiodClick, figheight, Species
    )
    return figgSWR, figgSWSick, figgSWDead

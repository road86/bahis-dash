from dash import html, callback, dcc
from dash.dependencies import Output, Input, State
import dash
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")


def fIndicator(sub_bahis_sourcedata):
    RfigIndic = go.Figure()

    RfigIndic.add_trace(
        go.Indicator(
            mode="number",
            title="Number of Reports",
            value=sub_bahis_sourcedata.shape[0],  # f"{bahis_sourcedata.shape[0]:,}"),
            domain={"row": 0, "column": 0},
        )
    )

    RfigIndic.add_trace(
        go.Indicator(
            mode="number",
            title="Sick Animals",
            value=sub_bahis_sourcedata["sick"].sum(),  # f"{int(bahis_sourcedata['sick'].sum()):,}",
            domain={"row": 0, "column": 1},
        )
    )

    RfigIndic.add_trace(
        go.Indicator(
            mode="number",
            title="Dead Animals",
            value=sub_bahis_sourcedata["dead"].sum(),  # f"{int(bahis_sourcedata['dead'].sum()):,}",
            domain={"row": 0, "column": 2},
        )
    )

    RfigIndic.update_layout(
        height=100,
        grid={"rows": 1, "columns": 3},  # 'pattern': "independent"},
    )
    return RfigIndic


def GeoRep(sub_bahis_sourcedata):
    Rfindic = fIndicator(sub_bahis_sourcedata)
    Rfindic.update_layout(height=100, margin={"r": 0, "t": 30, "l": 0, "b": 0})

    return Rfindic


def layout_gen(aid=None, **other_unknown_query_strings):
    html.Div(id="dummy"),
    return html.Div(
        [
            html.Div(
                [
                    html.H2("Welcome to the bahis dashboard.", style={"textAlign": "center"}),
                    html.H2(
                        "Please select a report from the menu on the top left.",
                        style={"textAlign": "center", "marginBottom": "1.5em"},
                    ),
                ]
            ),
            dbc.Card(dcc.Graph(id="no")),
        ]
    )


layout = layout_gen


@callback(
    Output("dummy", "id"),
    Output("cache_aid", "data"),
    Input("dummy", "id"),
    Input("url", "search"),
    State("cache_aid", "data"),
)
def set_store(id, url, prev):
    if url != "":
        aid = url.split("=")[1]
    else:
        aid = None
    if aid is None:
        return id, None
    else:
        return id, aid


@callback(
    Output("no", "figure"),
    Input("cache_page_data", "data"),
)
def RegionalStats(data):
    reportsdata = pd.read_json(data, orient="split")

    Rfindic = GeoRep(reportsdata)
    return Rfindic

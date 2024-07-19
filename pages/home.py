import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State

dash.register_page(__name__, path="/")


def GeoRep(sub_bahis_sourcedata, farmdata, ai_investdata, dis_investdata, lifestock_assessdata):
    figPat = go.Figure()
    figPat.add_trace(
        go.Indicator(
            mode="number",
            title={"text": "Patient Registry", "font": {"size": 20}},
            value=sub_bahis_sourcedata.shape[0],  # f"{bahis_sourcedata.shape[0]:,}"),
            number={"valueformat": ".0f", "font": {"size": 50}},
            domain={"row": 0, "column": 0},
        )
    )

    figFarm = go.Figure()
    figFarm.add_trace(
        go.Indicator(
            mode="number",
            title={"text": "Poultry Farm Assessment", "font": {"size": 20}},
            value=farmdata.shape[0],
            number={"valueformat": ".0f", "font": {"size": 50}},
            domain={"row": 0, "column": 1},  # visible=False
        )
    )

    figAvI = go.Figure()
    figAvI.add_trace(
        go.Indicator(
            mode="number",
            title={"text": "Avian Influenza Investigation", "font": {"size": 20}},
            value=ai_investdata.shape[0],
            number={"valueformat": ".0f", "font": {"size": 50}},
            domain={"row": 0, "column": 2},
            # visible=False,
        )
    )

    figDisI = go.Figure()
    figDisI.add_trace(
        go.Indicator(
            mode="number",
            title={"text": "Disease Investigation", "font": {"size": 20}},
            value=dis_investdata.shape[0],
            number={"valueformat": ".0f", "font": {"size": 50}},
            domain={"row": 0, "column": 3},
            # visible=False,
        )
    )

    figLSI = go.Figure()
    figLSI.add_trace(
        go.Indicator(
            mode="number",
            title={"text": "Participatory Lifestock Assessment", "font": {"size": 20}},
            value=lifestock_assessdata.shape[0],
            number={"valueformat": ".0f", "font": {"size": 50}},
            domain={"row": 0, "column": 4},
            # visible=False,
        )
    )
    figPat.update_layout(height=200)
    figFarm.update_layout(height=200)
    figAvI.update_layout(height=200)
    figDisI.update_layout(height=200)
    figLSI.update_layout(height=200)

    # RfigIndic.update_layout(
    #     height=100,
    #     grid={"rows": 1, "columns": 5},
    # )
    # # Rfindic = fIndicator(sub_bahis_sourcedata, farmdata, ai_investdata, dis_investdata, lifestock_assessdata)
    # RfigIndic.update_layout(height=100, margin={"r": 0, "t": 30, "l": 0, "b": 0})

    return figPat, figFarm, figAvI, figDisI, figLSI


def layout_gen(aid=None, **other_unknown_query_strings):
    if aid is not None:
        dcc.Store(id="cache_aid", storage_type="memory", data=aid),
    return html.Div(
        [
            html.Div(
                [
                    html.H1("Welcome to the bahis dashboard.", style={"textAlign": "center", "font-weight": "bold"}),
                    html.H3(
                        "-> Please select a report from the menu on the top left.",
                        style={"textAlign": "center", "marginBottom": "1.5em", "color": "green"},
                    ),
                ]
            ),
            html.Div(id="dummy"),
            html.Br(),
            html.H2("Number of Reports from:", style={"textAlign": "left"}),  # , "font-weight": "bold"}),
            dbc.Row(
                [
                    dbc.Col(dbc.Card(dcc.Graph(id="pat"))),
                    # dbc.Col(dbc.Card(dcc.Graph(id="farm")), lg=6, sm=4),
                    # dbc.Col(dbc.Card(dcc.Graph(id="AvI")), lg=6, sm=4),
                    # dbc.Col(dbc.Card(dcc.Graph(id="DisI")), lg=6, sm=4),
                    # dbc.Col(dbc.Card(dcc.Graph(id="LSA")), lg=6, sm=4),
                ]
            ),
        ]
    )


layout = layout_gen


@callback(
    # Output("dummy", "id"),
    Output("cache_aid", "data"),
    # Input("dummy", "id"),
    Input("url", "search"),
    State("cache_aid", "data"),
)
def set_store(url, prev):  # id, url, prev):
    if url != "":
        aid = url.split("=")[1]
    else:
        aid = None
    if aid is None:
        return None  # id, None
    else:
        return aid  # id, aid


# @callback(
#     Output("pat", "figure"),
#     Output("farm", "figure"),
#     Output("AvI", "figure"),
#     Output("DisI", "figure"),
#     Output("LSA", "figure"),
#     Input("dummy", "id"),
#     Input("cache_page_data", "data"),
#     Input("cache_page_farmdata", "data"),
#     Input("cache_page_ai_invest", "data"),
#     Input("cache_page_dis_invest", "data"),
#     Input("cache_page_lifestock_assess", "data"),
# )
# def RegionalStats(dummy, data, farmdata, ai_investdata, dis_investdata, lifestock_assessdata):
#     reportsdata = pd.read_json(data, orient="split")
#     farmdata = pd.read_json(farmdata, orient="split")
#     ai_investdata = pd.read_json(ai_investdata, orient="split")
#     dis_investdata = pd.read_json(dis_investdata, orient="split")
#     lifestock_assessdata = pd.read_json(lifestock_assessdata, orient="split")
#     figPat, figFarm, figAvI, figDisI, figLSI = GeoRep(
#         reportsdata, farmdata, ai_investdata, dis_investdata, lifestock_assessdata
#     )
#     return figPat, figFarm, figAvI, figDisI, figLSI

@callback(
    Output("pat", "figure"),
    Input("dummy", "id"),
    Input("cache_page_data", "data"),
)
def RegionalStats(dummy, data, ):
    reportsdata = pd.read_json(data, orient="split")

    figPat = go.Figure()
    return figPat.add_trace(
        go.Indicator(
            mode="number",
            title={"text": "Patient Registry", "font": {"size": 20}},
            value=reportsdata.shape[0],  # f"{bahis_sourcedata.shape[0]:,}"),
            number={"valueformat": ".0f", "font": {"size": 50}},
            domain={"row": 0, "column": 0},
        )
    )

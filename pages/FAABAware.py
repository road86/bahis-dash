# import plotly.express as px
import json

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as px
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State

from components import fetchdata

dash.register_page(
    __name__,
)  # register page to main dash app

layout = [
    html.Label("Antibiotics Usage Report AWaRe"),
    dbc.Row(
        dcc.Graph(id="ABAware"),
    ),
    html.Div(id="dummy"),
]


@callback(
    Output("ABAware", "figure"),
    Input("cache_filenames", "data"),
    Input("dummy", "id"),
    State("cache_page_farmdata", "data"),
    State("cache_page_settings", "data"),
    prevent_initial_call=True,
)
def BSEntrance(filenames, dummy, data, settings):
    farmdata = pd.read_json(data, orient="split")
    farmdatafilename = json.loads(filenames)["farmdata"]
    fulldata = fetchdata.fetchfarmdata(farmdatafilename)
    medsfilename = json.loads(filenames)["meds"]
    medsdata = fetchdata.fetchmedsdata(medsfilename)

    text1 = "WATCH"
    text2 = "ACCESS"
    text3 = "non-labelled"
    text4 = "empty"
    categories = [text1, text2, text3, text4]

    if type(json.loads(settings)["upazila"]) == int:
        fulldata = fulldata.loc[fulldata["upazila"] == json.loads(settings)["upazila"]]
    else:
        if type(json.loads(settings)["district"]) == int:
            fulldata = fulldata.loc[fulldata["district"] == json.loads(settings)["district"]]
        else:
            if type(json.loads(settings)["division"]) == int:
                fulldata = fulldata.loc[fulldata["division"] == json.loads(settings)["division"]]
            else:
                fulldata = fulldata

    a = (farmdata["g1"].dropna().astype("int").isin(medsdata[medsdata["aware"] == "WATCH"]["id"])).sum()
    b = (farmdata["g1"].dropna().astype("int").isin(medsdata[medsdata["aware"] == "ACCESS"]["id"])).sum()
    c = (
        (farmdata["g1"].dropna()).astype("int").sum()
        - (farmdata["g1"].dropna().astype("int").isin(medsdata[medsdata["aware"] == "WATCH"]["id"])).sum()
        - (farmdata["g1"].dropna().astype("int").isin(medsdata[medsdata["aware"] == "ACCESS"]["id"])).sum()
    )
    d = farmdata["g1"].isna().sum()
    selectedtime = [a, b, c, d]
    a = (fulldata["g1"].dropna().astype("int").isin(medsdata[medsdata["aware"] == "WATCH"]["id"])).sum()
    b = (fulldata["g1"].dropna().astype("int").isin(medsdata[medsdata["aware"] == "ACCESS"]["id"])).sum()
    c = (
        (fulldata["g1"].dropna()).astype("int").sum()
        - (fulldata["g1"].dropna().astype("int").isin(medsdata[medsdata["aware"] == "WATCH"]["id"])).sum()
        - (fulldata["g1"].dropna().astype("int").isin(medsdata[medsdata["aware"] == "ACCESS"]["id"])).sum()
    )
    d = fulldata["g1"].isna().sum()
    fulltime = [a, b, c, d]

    fig = px.Figure(
        data=[
            px.Bar(name="selected timeframe", x=categories, y=selectedtime),
            px.Bar(name="fulltime", x=categories, y=fulltime),
        ]
    )
    fig.update_layout(height=550)
    # fig.update_layout(yaxis_tickformat="2%", yaxis_range=[0, 1], height=550)
    #    fig = {}
    return fig

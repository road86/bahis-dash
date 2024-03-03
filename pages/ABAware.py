import dash
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from components import fetchdata
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as px

# import plotly.express as px
import json


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
    # print(farmdata.iloc[:, 5]) until 10
    farmdatafilename = json.loads(filenames)["farmdata"]
    fulldata = fetchdata.fetchfarmdata(farmdatafilename)
    medsfilename = json.loads(filenames)["meds"]
    medsdata = fetchdata.fetchmedsdata(medsfilename)
    print(medsdata)
    # if type(json.loads(settings)["upazila"]) == int:
    #     fulldata = fulldata.loc[fulldata["upazila"] == json.loads(settings)["upazila"]]
    # else:
    #     if type(json.loads(settings)["district"]) == int:
    #         fulldata = fulldata.loc[fulldata["district"] == json.loads(settings)["district"]]
    #     else:
    #         if type(json.loads(settings)["division"]) == int:
    #             fulldata = fulldata.loc[fulldata["division"] == json.loads(settings)["division"]]
    #         else:
    #             fulldata = fulldata

    # selectedtime = [
    #     len(farmdata[(farmdata["outsider_vehicles_entry"] == 1)]) / farmdata.shape[0],
    #     len(farmdata[(farmdata["workers_approve_visitor_entry"] == 1)]) / farmdata.shape[0],
    #     len(farmdata[(farmdata["manure_collector_entry"] == 1)]) / farmdata.shape[0],
    #     len(farmdata[(farmdata["fenced_and_duck_chicken_proof"] == 1)]) / farmdata.shape[0],
    #     len(farmdata[(farmdata["dead_birds_disposed_safely"] == 1)]) / farmdata.shape[0],
    #     len(farmdata[(farmdata["sign_posted_1st"] == 1)]) / farmdata.shape[0],
    # ]
    # fulltime = [
    #     len(fulldata[(fulldata["outsider_vehicles_entry"] == 1)]) / fulldata.shape[0],
    #     len(fulldata[(fulldata["workers_approve_visitor_entry"] == 1)]) / fulldata.shape[0],
    #     len(fulldata[(fulldata["manure_collector_entry"] == 1)]) / fulldata.shape[0],
    #     len(fulldata[(fulldata["fenced_and_duck_chicken_proof"] == 1)]) / fulldata.shape[0],
    #     len(fulldata[(fulldata["dead_birds_disposed_safely"] == 1)]) / fulldata.shape[0],
    #     len(fulldata[(fulldata["sign_posted_1st"] == 1)]) / fulldata.shape[0],
    # ]

    # fig = px.Figure(
    #     data=[
    #         px.Bar(name="selected timeframe", x=categories, y=selectedtime),
    #         px.Bar(name="fulltime", x=categories, y=fulltime),
    #     ]
    # )
    # fig.update_layout(yaxis_tickformat="2%", yaxis_range=[0, 1], height=550)
    fig = {}
    return fig

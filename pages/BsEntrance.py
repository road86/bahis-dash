import dash
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from components import pathnames, fetchdata
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as px

# import plotly.express as px
import json


dash.register_page(
    __name__,
)  # register page to main dash app

layout = [
    # html.Label("Biosecurity Practice Entrance"),
    html.H2("Biosecurity Practice Entrance", style={"textAlign": "center", "font-weight": "bold"}),
    dbc.Row(
        dcc.Graph(id="BSEntrance"),
    ),
    html.Div(id="dummy"),
]


@callback(
    Output("BSEntrance", "figure"),
    Input("dummy", "id"),
    State("cache_page_farmdata", "data"),
    State("cache_page_settings", "data"),
    prevent_initial_call=True,
)
def BSEntrance(dummy, data, settings):
    farmdata = pd.read_json(data, orient="split")
    text1 = "a1. Outside vehicles do not enter farm, only essential vehicles"
    text2 = "a2. Only workers and approved visitors enter farm"
    text3 = "a3. No manure collectors enter farm"
    text4 = "a4. Farm area is fully fenced and duck/chicken proof"
    text5 = "a5. Dead birds disposed safely"
    text6 = "a6. Signs posted"
    # print(farmdata.iloc[:, 5]) until 10
    categories = [text1, text2, text3, text4, text5, text6]
    sourcepath = "exported_data/"  # called also in Top10, make global or settings parameter
    geofilename, dgfilename, sourcefilename, farmdatafilename, path1, path2, path3 = pathnames.get_pathnames(sourcepath)
    fulldata = fetchdata.fetchfarmdata(farmdatafilename)
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

    selectedtime = [
        len(farmdata[(farmdata["outsider_vehicles_entry"] == 1)]) / farmdata.shape[0],
        len(farmdata[(farmdata["workers_approve_visitor_entry"] == 1)]) / farmdata.shape[0],
        len(farmdata[(farmdata["manure_collector_entry"] == 1)]) / farmdata.shape[0],
        len(farmdata[(farmdata["fenced_and_duck_chicken_proof"] == 1)]) / farmdata.shape[0],
        len(farmdata[(farmdata["dead_birds_disposed_safely"] == 1)]) / farmdata.shape[0],
        len(farmdata[(farmdata["sign_posted_1st"] == 1)]) / farmdata.shape[0],
    ]
    fulltime = [
        len(fulldata[(fulldata["outsider_vehicles_entry"] == 1)]) / fulldata.shape[0],
        len(fulldata[(fulldata["workers_approve_visitor_entry"] == 1)]) / fulldata.shape[0],
        len(fulldata[(fulldata["manure_collector_entry"] == 1)]) / fulldata.shape[0],
        len(fulldata[(fulldata["fenced_and_duck_chicken_proof"] == 1)]) / fulldata.shape[0],
        len(fulldata[(fulldata["dead_birds_disposed_safely"] == 1)]) / fulldata.shape[0],
        len(fulldata[(fulldata["sign_posted_1st"] == 1)]) / fulldata.shape[0],
    ]

    fig = px.Figure(
        data=[
            px.Bar(name="selected timeframe", x=categories, y=selectedtime),
            px.Bar(name="fulltime", x=categories, y=fulltime),
        ]
    )
    fig.update_layout(yaxis_tickformat="2%", yaxis_range=[0, 1], yaxis_title="total farm", height=550)
    return fig

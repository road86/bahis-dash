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
    html.Label("Biosecurity Practice Equipment"),
    html.H2("Biosecurity Practice Equipment", style={"textAlign": "center", "font-weight": "bold"}),
    dbc.Row(
        dcc.Graph(id="BSProduction"),
    ),
    html.Div(id="dummy"),
]


@callback(
    Output("BSEqupment", "figure"),
    Input("dummy", "id"),
    State("cache_page_farmdata", "data"),
    State("cache_page_settings", "data"),
    prevent_initial_call=True,
)
def BSEntrance(dummy, data, settings):
    farmdata = pd.read_json(data, orient="split")
    text1 = "d1. No movement of vehicles in and out of the production area"
    text2 = "d2. Only workers enter production area"
    categories = [text1, text2]
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
        len(farmdata[(farmdata["materials_cleaned"] == 1)]) / farmdata.shape[0],
        len(farmdata[(farmdata["materials_disinfect"] == 1)]) / farmdata.shape[0],
    ]
    fulltime = [
        len(fulldata[(fulldata["materials_cleaned"] == 1)]) / fulldata.shape[0],
        len(fulldata[(fulldata["materials_disinfect"] == 1)]) / fulldata.shape[0],
    ]

    fig = px.Figure(
        data=[
            px.Bar(name="selected timeframe", x=categories, y=selectedtime),
            px.Bar(name="fulltime", x=categories, y=fulltime),
        ]
    )
    fig.update_layout(yaxis_tickformat="2%", yaxis_range=[0, 1], yaxis_title="total farm", height=550)
    return fig

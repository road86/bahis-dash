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
    html.Label("Biosecurity Practice Personell"),
    dbc.Row(
        dcc.Graph(id="BSPersonell"),
    ),
    html.Div(id="dummy"),
]


@callback(
    Output("BSPersonell", "figure"),
    Input("dummy", "id"),
    State("cache_page_farmdata", "data"),
    State("cache_page_settings", "data"),
    prevent_initial_call=True,
)
def BSEntrance(dummy, data, settings):
    farmdata = pd.read_json(data, orient="split")
    text1 = "c1. Outside footwear legt outside farm"
    text2 = "c2. Workers and visitors change clothes upon entering farm"
    text3 = "c3. Workers and visitors use only dedicated footwear in production area"
    text4 = "c4. Workers and visitors shower upon entering farm"
    categories = [text1, text2, text3, text4]
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
        len(farmdata[(farmdata["footwear_left_outside"] == 1)]) / farmdata.shape[0],
        len(farmdata[(farmdata["change_clothes_upon_entering_farm"] == 1)]) / farmdata.shape[0],
        len(farmdata[(farmdata["use_dedicated_footwear"] == 1)]) / farmdata.shape[0],
        len(farmdata[(farmdata["shower_before_enter_farm"] == 1)]) / farmdata.shape[0],
    ]
    fulltime = [
        len(fulldata[(fulldata["footwear_left_outside"] == 1)]) / fulldata.shape[0],
        len(fulldata[(fulldata["change_clothes_upon_entering_farm"] == 1)]) / fulldata.shape[0],
        len(fulldata[(fulldata["use_dedicated_footwear"] == 1)]) / fulldata.shape[0],
        len(fulldata[(fulldata["shower_before_enter_farm"] == 1)]) / fulldata.shape[0],
    ]

    fig = px.Figure(
        data=[
            px.Bar(name="selected timeframe", x=categories, y=selectedtime),
            px.Bar(name="fulltime", x=categories, y=fulltime),
        ]
    )
    fig.update_layout(yaxis_tickformat="2%", yaxis_range=[0, 1], height=550)
    return fig

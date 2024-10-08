import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State

dash.register_page(
    __name__,
)

layout = [
    html.H2("Antibiotic Usage", style={"textAlign": "center", "font-weight": "bold"}),
    dbc.Row(
        dcc.Graph(id="ABUsage"),
    ),
    html.Div(id="dummy"),
]


@callback(
    Output("ABUsage", "figure"),
    Input("cache_filenames", "data"),
    Input("dummy", "id"),
    State("cache_page_farmdata", "data"),
    State("cache_page_settings", "data"),
    prevent_initial_call=True,
)
def BSEntrance(filenames, dummy, data, settings):
    farmdata = pd.read_json(data, orient="split")
    selected_columns = [
        "g1g1",
        "g1g2",
        "g1g3",
        "g1g4",
        "g2g1",
        "g2g2",
        "g2g3",
        "g2g4",
        "g3g1",
        "g3g2",
        "g3g3",
        "g3g4",
        "g4g1",
        "g4g2",
        "g4g3",
        "g4g4",
        "g5g1",
        "g5g2",
        "g5g3",
        "g5g4",
    ]
    farmdata["uniqueV"] = farmdata[selected_columns].apply(lambda x: len(x.unique()), axis=1)
    usage = farmdata["uniqueV"].value_counts()
    usage = usage.reset_index()
    usage.columns = ["Usage", "Counts"]
    usage["Usage"] = usage["Usage"] - 1
    total_counts = usage["Counts"].sum()
    usage["Relative Counts"] = usage["Counts"] / total_counts * 100
    fig = px.bar(usage, x="Usage", y="Counts")
    fig.data[0].y = usage["Relative Counts"]
    fig.update_xaxes(tickmode="linear", dtick=1)
    fig.update_layout(xaxis_title="Number of Antibiotics", yaxis_title="Total Farm Percentage", height=550)
    # fig = {}
    return fig

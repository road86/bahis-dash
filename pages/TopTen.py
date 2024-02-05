import dash
from components import pathnames, fetchdata
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

dash.register_page(
    __name__,
)  # register page to main dash app


def TopTen(sub_bahis_sourcedata, bahis_dgdata, distype, to_replace, replace_with):
    poultry = ["Chicken", "Duck", "Goose", "Pegion", "Quail", "Turkey"]
    sub_bahis_sourcedataP = sub_bahis_sourcedata[sub_bahis_sourcedata["species"].isin(poultry)]
    sub_bahis_sourcedataP["top_diagnosis"] = sub_bahis_sourcedataP.top_diagnosis.replace(
        to_replace, replace_with, regex=True
    )
    tmp = sub_bahis_sourcedataP.groupby(["top_diagnosis"])["species"].agg("count").reset_index()
    tmp = tmp.sort_values(by="species", ascending=False)
    tmp = tmp.rename({"species": "counts"}, axis=1)
    tmp = tmp.head(10)
    tmp = tmp.iloc[::-1]
    fpoul = px.bar(tmp, x="counts", y="top_diagnosis", labels={"counts": "Counts", "top_diagnosis": ""}, title="")
    fpoul.update_layout(height=250, margin={"r": 0, "t": 0, "l": 0, "b": 0})

    lanimal = ["Buffalo", "Cattle", "Goat", "Sheep"]
    sub_bahis_sourcedataLA = sub_bahis_sourcedata[sub_bahis_sourcedata["species"].isin(lanimal)]
    sub_bahis_sourcedataLA["top_diagnosis"] = sub_bahis_sourcedataLA.top_diagnosis.replace(
        to_replace, replace_with, regex=True
    )
    tmp = sub_bahis_sourcedataLA.groupby(["top_diagnosis"])["species"].agg("count").reset_index()
    tmp = tmp.sort_values(by="species", ascending=False)
    tmp = tmp.rename({"species": "counts"}, axis=1)
    tmp["counts"] = tmp["counts"] / 1000
    tmp = tmp.head(10)
    tmp = tmp.iloc[::-1]
    flani = px.bar(
        tmp, x="counts", y="top_diagnosis", labels={"counts": "Counts in Thousands", "top_diagnosis": ""}, title=""
    )
    flani.update_layout(height=250, margin={"r": 0, "t": 0, "l": 0, "b": 0})

    tmpdg = bahis_dgdata[bahis_dgdata["Disease type"] == distype]
    selected_diseases = tmpdg["name"].tolist()
    sub_bahis_sourcedata = sub_bahis_sourcedata[sub_bahis_sourcedata["top_diagnosis"].isin(selected_diseases)]
    tmp = sub_bahis_sourcedata.groupby(["top_diagnosis"])["species"].agg("count").reset_index()
    tmp = tmp.sort_values(by="species", ascending=False)
    tmp = tmp.rename({"species": "counts"}, axis=1)
    tmp = tmp.head(10)
    tmp = tmp.iloc[::-1]
    figDisTyp = px.bar(tmp, x="counts", y="top_diagnosis", labels={"counts": "Counts", "top_diagnosis": ""}, title="")
    figDisTyp.update_layout(height=200, margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return flani, fpoul, figDisTyp


def layout_gen(aid=None, **other_unknown_query_strings):
    if aid is not None:
        dcc.Store(id="cache_aid", storage_type="memory", data=aid),
    return html.Div(
        [
            html.Label("Top10 Report"),
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [html.Label("Top 10 Large Animal Diseases"), dcc.Graph(id="LATop10")],
                                    width=6,
                                ),
                                dbc.Col(
                                    [html.Label("Top 10 Poultry Diseases"), dcc.Graph(id="PTop10")],
                                    width=6,
                                ),
                            ]
                        )
                    ]
                )
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Select Disease Type"),
                                        dcc.Dropdown(
                                            id="Distypes",
                                            clearable=False,
                                        ),
                                    ],
                                    width=2,
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Top 10 Disease Types"),
                                        dcc.Graph(id="figDistypes"),
                                    ]
                                ),
                            ]
                        )
                    ]
                )
            ),
            html.Div(id="dummy"),
        ]
    )


layout = layout_gen


@callback(
    Output("LATop10", "figure"),
    Output("PTop10", "figure"),
    Output("figDistypes", "figure"),
    Output("Distypes", "options"),
    Input("Distypes", "value"),
    Input("dummy", "id"),
    State("cache_page_data", "data"),
    prevent_initial_call=True,
)
def TopTenView(SelDistypes, dummy, data):
    sourcepath = "exported_data/"  # make global variable or in settings
    geofilename, dgfilename, sourcefilename, farmdatafilename, path1, path2, path3 = pathnames.get_pathnames(sourcepath)
    [bahis_dgdata, bahis_distypes] = fetchdata.fetchdisgroupdata(dgfilename)
    vDistypes = bahis_distypes["Disease type"]
    reportsdata = pd.read_json(data, orient="split")
    to_replace = bahis_dgdata["name"].tolist()
    replace_with = bahis_dgdata["Disease type"].tolist()

    flani, fpoul, figDistypes = TopTen(reportsdata, bahis_dgdata, SelDistypes, to_replace, replace_with)
    return flani, fpoul, figDistypes, vDistypes

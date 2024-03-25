import json

import dash
import pandas as pd
import plotly.express as px
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State

from components import fetchdata

dash.register_page(
    __name__,
)  # register page to main dash app


def yearlyComp(alldata, bahis_data, diseaselist):
    monthly = bahis_data.groupby(
        [bahis_data["date"].dt.year.rename("Year"), bahis_data["date"].dt.month.rename("Month")]
    )["date"].agg({"count"})
    monthly = monthly.rename({"count": "reports"}, axis=1)
    monthly = monthly.reset_index()
    monthly["reports"] = monthly["reports"]
    monthly["Year"] = monthly["Year"].astype(str)

    monthlyA = alldata.groupby([alldata["date"].dt.year.rename("Year"), alldata["date"].dt.month.rename("Month")])[
        "date"
    ].agg({"count"})
    monthlyA = monthlyA.rename({"count": "reports"}, axis=1)
    monthlyA = monthlyA.reset_index()
    monthlyA["reports"] = monthlyA["reports"]
    monthlyA["Year"] = monthlyA["Year"].astype(str)
    result = monthlyA.copy()
    result.iloc[:, -1] = monthly.iloc[:, -1] / monthlyA.iloc[:, -1]

    figYearlyComp = px.bar(
        data_frame=result,
        x="Month",
        y="reports",
        labels={"reports": "Reports in % of all reported diseases"},
        color="Year",
        barmode="group",
    )
    figYearlyComp.update_xaxes(dtick="M1")  # , tickformat="%B \n%Y")
    figYearlyComp.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            ticktext=[
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ],
            title="",
        ),
        title={
            "text": 'Disease dynamics for "' + str(diseaselist) + '"',
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
    )
    return figYearlyComp


def layout_gen(aid=None, **other_unknown_query_strings):
    if aid is not None:
        dcc.Store(id="cache_aid", storage_type="memory", data=aid),
    return html.Div(
        [
            # html.Label("Yearly Comparison (Click on traces to select/de-select them)"),
            html.H2("Yearly Comparison", style={"textAlign": "center", "font-weight": "bold"}),
            dcc.Graph(id="figMonthlyP"),
            html.Div(id="dummy"),
        ]
    )


layout = layout_gen


@callback(
    Output("figMonthlyP", "figure"),
    Input("cache_filenames", "data"),
    Input("dummy", "id"),
    State("cache_page_settings", "data"),
    State("cache_page_geodata", "data"),
    prevent_initial_call=True,
)
def YearlyComparison(filenames, dummy, settings, page_geodata):
    sourcefilename = json.loads(filenames)["source"]
    fulldata = fetchdata.fetchsourcedata(sourcefilename)
    alldata = fetchdata.fetchsourcedata(sourcefilename)
    #    fulldata = pd.read_json(data, orient="split")
    geodata = pd.read_json(page_geodata, orient="split")

    #    fulldata = fetchdata.date_subset(json.loads(settings)["daterange"], fulldata)
    fulldata = fetchdata.disease_subset(json.loads(settings)["disease"], fulldata)

    if type(json.loads(settings)["upazila"]) == int:
        fulldata = fulldata.loc[fulldata["upazila"] == json.loads(settings)["upazila"]]
        geodata = geodata.loc[geodata["value"] == json.loads(settings)["upazila"]]
    else:
        if type(json.loads(settings)["district"]) == int:
            fulldata = fulldata.loc[fulldata["district"] == json.loads(settings)["district"]]
            geodata = geodata.loc[geodata["parent"] == json.loads(settings)["district"]]
        else:
            if type(json.loads(settings)["division"]) == int:
                fulldata = fulldata.loc[fulldata["division"] == json.loads(settings)["division"]]
                geodata = geodata.loc[geodata["parent"] == json.loads(settings)["division"]]
            else:
                fulldata = fulldata
                geodata = geodata

    figMonthly = yearlyComp(alldata, fulldata, json.loads(settings)["disease"])
    return figMonthly

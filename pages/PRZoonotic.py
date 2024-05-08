import json
from datetime import datetime, timedelta

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State

from components import fetchdata

dash.register_page(
    __name__,
)  # register page to main dash app


def TrendReports(sub_bahis_sourcedata, dates, periodClick, figheight):
    tmp = sub_bahis_sourcedata["date"].dt.date.value_counts()
    tmp = tmp.to_frame()
    tmp["counts"] = tmp["date"]
    tmp["date"] = pd.to_datetime(tmp.index)

    if periodClick == 3:
        tmp = tmp["counts"].groupby(tmp["date"]).sum().astype(int)
    if periodClick == 2:
        tmp = tmp["counts"].groupby(tmp["date"].dt.to_period("W-SAT")).sum().astype(int)
    if periodClick == 1:
        tmp = tmp["counts"].groupby(tmp["date"].dt.to_period("M")).sum().astype(int)
    tmp = tmp.to_frame()
    tmp["date"] = tmp.index
    tmp["date"] = tmp["date"].astype("datetime64[D]")

    fig = px.bar(tmp, x="date", y="counts", labels={"date": "", "counts": "No. of Reports"})
    fig.update_layout(height=figheight, margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_xaxes(
        range=[
            datetime.strptime(dates[0], "%Y-%m-%d") - timedelta(days=6),
            datetime.strptime(dates[1], "%Y-%m-%d") + timedelta(days=6),
        ]
    )
    fig.add_annotation(
        x=datetime.strptime(dates[1], "%Y-%m-%d")
        - timedelta(
            days=int(((datetime.strptime(dates[1], "%Y-%m-%d") - datetime.strptime(dates[0], "%Y-%m-%d")).days) * 0.08)
        ),
        y=max(tmp),
        text="total reports " + str("{:,}".format(sub_bahis_sourcedata["date"].size)),
        showarrow=False,
        font=dict(family="Courier New, monospace", size=12, color="#ffffff"),
        align="center",
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="#ff7f0e",
        opacity=0.8,
    )
    return fig


def layout_gen(aid=None, **other_unknown_query_strings):
    if aid is not None:
        dcc.Store(id="cache_aid", storage_type="memory", data=aid),
    return html.Div(
        [
            # html.Label("Zoonotic Disease Report (Click on traces to select/de-select them)"),
            html.H2("Zoonotic Disease Report", style={"textAlign": "center", "font-weight": "bold"}),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Row(dcc.Graph(id="TrendReports")),
                        ]
                    ),
                    html.Div(id="dummy"),
                ]
            ),
        ]
    )


layout = layout_gen


@callback(
    Output("TrendReports", "figure"),
    Input("cache_filenames", "data"),
    Input("dummy", "id"),
    State("cache_page_data", "data"),
    State("cache_page_settings", "data"),
    prevent_initial_call=True,
)
def ZooTrend(filenames, dummy, data, settings):
    dgfilename = json.loads(filenames)["dg"]
    [bahis_dgdata, bahis_distypes] = fetchdata.fetchdisgroupdata(dgfilename)
    tmpdg = bahis_dgdata[bahis_dgdata["Disease type"] == "Zoonotic diseases"]
    selected_diseases = tmpdg["name"].tolist()

    reportsdata = pd.read_json(data, orient="split")
    DateRange = json.loads(settings)["daterange"]
    reportsdata = reportsdata[reportsdata["top_diagnosis"].isin(selected_diseases)]

    Diseases = reportsdata.groupby(["top_diagnosis"])["species"].agg("count").reset_index()
    Diseases = Diseases.sort_values(by="species", ascending=False)
    Diseases = Diseases.rename({"species": "counts"}, axis=1)
    Diseases = Diseases.head(10)
    reportsdata = reportsdata[reportsdata["top_diagnosis"].isin(Diseases["top_diagnosis"])]
    reportsdata["date"] = pd.to_datetime(reportsdata["date"])
    tmp = reportsdata.groupby(["date", "top_diagnosis"]).size().reset_index(name="incidences")

    dates = tmp["date"].unique()
    diagnoses = tmp["top_diagnosis"].unique()
    date_diagnosis_combinations = pd.MultiIndex.from_product([dates, diagnoses], names=["date", "top_diagnosis"])
    result_df = pd.DataFrame(index=date_diagnosis_combinations).reset_index()

    # Merge with the grouped DataFrame to fill missing values with 0
    final_df = pd.merge(result_df, tmp, on=["date", "top_diagnosis"], how="left").fillna(0)

    # Sort the final DataFrame by 'date' and 'top_diagnosis'
    final_df.sort_values(by=["date", "top_diagnosis"], inplace=True)

    figheight = 570
    figTrend = px.line(
        final_df,
        x="date",
        y="incidences",
        color="top_diagnosis",
        markers=True,
        category_orders={"top_diagnosis": Diseases["top_diagnosis"]},
    )
    figTrend.update_layout(height=figheight, margin={"r": 0, "t": 0, "l": 0, "b": 0}, legend_title_text="")
    # figTrend.update_xaxes(
    #     range=[
    #         datetime.strptime(DateRange[0], "%Y-%m-%d") - timedelta(days=6),
    #         datetime.strptime(DateRange[1], "%Y-%m-%d") + timedelta(days=6),
    #     ]
    # )
    figTrend.update_yaxes(title_text="No. of Reports"),  # tickvals=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    figTrend.add_annotation(
        x=datetime.strptime(DateRange[1], "%Y-%m-%d")
        - timedelta(
            days=int(
                ((datetime.strptime(DateRange[1], "%Y-%m-%d") - datetime.strptime(DateRange[0], "%Y-%m-%d")).days)
                * 0.08
            )
        ),
        # y=105,  # max(tmp),
        text="total reports " + str("{:,}".format(reportsdata["date"].size)),
        showarrow=False,
        font=dict(family="Courier New, monospace", size=12, color="#ffffff"),
        align="center",
        bordercolor="#c7c7c7",
        borderwidth=0,
        borderpad=0,
        bgcolor="#ff7f0e",
        opacity=0.8,
    )

    return figTrend

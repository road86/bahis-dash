import dash
from components import pathnames, fetchdata
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import json
from datetime import datetime, timedelta
import plotly.express as px


dash.register_page(__name__,)  # register page to main dash app


def TrendReports(sub_bahis_sourcedata, dates, periodClick, figheight):
    tmp = sub_bahis_sourcedata["date"].dt.date.value_counts()
    tmp = tmp.to_frame()
    tmp["counts"] = tmp["date"]
    tmp["date"] = pd.to_datetime(tmp.index)

    if periodClick == 3:
        tmp = (
            tmp['counts']
            .groupby(tmp['date'])
            .sum()
            .astype(int)
        )
    if periodClick == 2:
        tmp = (
            tmp['counts']
            .groupby(tmp['date'].dt.to_period('W-SAT'))
            .sum()
            .astype(int)
        )
    if periodClick == 1:
        tmp = (
            tmp['counts']
            .groupby(tmp['date'].dt.to_period('M'))
            .sum()
            .astype(int)
        )
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
            days=int(
                ((datetime.strptime(dates[1], "%Y-%m-%d") - datetime.strptime(dates[0], "%Y-%m-%d")).days) * 0.08
            )
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
    return html.Div([
        html.Label("Zoonotic Disease Report (Click on traces to select/de-select them)"),
        dbc.Row([
            dbc.Col(
                [
                    dbc.Row(dcc.Graph(id="TrendReports")),
                ]
            ),
            html.Div(id="dummy"),
        ])
    ])


layout = layout_gen

@callback(
    Output("TrendReports", "figure"),
    Input("dummy", "id"),
    State("cache_page_data", "data"),
    State("cache_page_settings", "data"),
    prevent_initial_call=True
)
def ZooTrend(dummy, data, settings):

    sourcepath = "exported_data/"       # make global variable or in settings
    geofilename, dgfilename, sourcefilename, farmdatafilename, path1, path2, path3 = pathnames.get_pathnames(sourcepath)
    [bahis_dgdata, bahis_distypes] = fetchdata.fetchdisgroupdata(dgfilename)
    tmpdg = bahis_dgdata[bahis_dgdata["Disease type"] == "Zoonotic diseases"]
    selected_diseases = tmpdg['name'].tolist()

    reportsdata = pd.read_json(data, orient="split")
    DateRange = json.loads(settings)["daterange"]
    reportsdata = reportsdata[reportsdata["top_diagnosis"].isin(selected_diseases)]

    Diseases = reportsdata.groupby(["top_diagnosis"])['species'].agg("count").reset_index()
    Diseases = Diseases.sort_values(by="species", ascending=False)
    Diseases = Diseases.rename({"species": "counts"}, axis=1)
    Diseases = Diseases.head(10)
    reportsdata = reportsdata[reportsdata["top_diagnosis"].isin(Diseases["top_diagnosis"])]
    reportsdata['date'] = pd.to_datetime(reportsdata['date'])
    tmp = reportsdata.groupby(['date', 'top_diagnosis']).size().reset_index(name='incidences')

    figheight = 570
    figTrend = px.line(tmp, x='date', y='incidences', color='top_diagnosis', markers=True,
                       category_orders={"top_diagnosis": Diseases['top_diagnosis']})
    figTrend.update_layout(height=figheight, margin={"r": 0, "t": 0, "l": 0, "b": 0})
    # figTrend.update_xaxes(
    #     range=[
    #         datetime.strptime(DateRange[0], "%Y-%m-%d") - timedelta(days=6),
    #         datetime.strptime(DateRange[1], "%Y-%m-%d") + timedelta(days=6),
    #     ]
    # )
    figTrend.add_annotation(
        x=datetime.strptime(DateRange[1], "%Y-%m-%d")
        - timedelta(
            days=int(
                ((datetime.strptime(DateRange[1], "%Y-%m-%d") - datetime.strptime(DateRange[0],
                                                                                  "%Y-%m-%d")).days) * 0.08
            )
        ),
        y=max(tmp),
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

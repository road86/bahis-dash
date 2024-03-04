import dash
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import pandas as pd
from datetime import date, datetime, timedelta
from components import fetchdata
import json


dash.register_page(__name__)  # register page to main dash app


def find_weeks(start, end):
    list_of_weeks = []
    # days_to_thursday = (3 - start.weekday()) % 7
    for i in range((end - start).days + 1):
        d = (start + timedelta(days=i)).isocalendar()[:2]  # e.g. (2011, 52)
        yearweek = "y{}w{:02}".format(*d)  # e.g. "201152"
        list_of_weeks.append(yearweek)
    return sorted(set(list_of_weeks))


def annotatetxt(annotations, text, x_val, yvalue):
    annotation_dict = dict(
        showarrow=False,
        text="<b>" + str(text) + "<b>",
        xref="x",
        yref="y",
        x=x_val,
        y=yvalue,
        font=dict(family="sans-serif"),
    )
    annotations.append(annotation_dict)


def generate_reports_heatmap(reportsdata, geoNameNNumber, start, end, division, district):
    start = datetime.strptime(str(start), "%Y-%m-%d")
    end = datetime.strptime(str(end), "%Y-%m-%d")
    compcols = False
    x_axis = find_weeks(start, end)  # [1:] without first week
    x_axis = [str(x) for x in x_axis]
    annotations = []
    if type(division) is not int:  # for national numbers
        Divisions = fetchdata.fetchDivisionlist(geoNameNNumber)
        y_axis = [x["Division"] for x in Divisions]
        y_axis_no = [x["value"] for x in Divisions]
        y_axis.reverse()
        y_axis_no.reverse()
        y_axis.append("Σ " + "Bangladesh")
        y_axis_no.append("Bangladesh")
        z = pd.DataFrame(index=x_axis, columns=y_axis)
        for ind_y, division in enumerate(y_axis):
            if division != "Σ " + "Bangladesh":
                tmp = reportsdata[(reportsdata["division"] == y_axis_no[ind_y])].date.value_counts()
                tmp = tmp.to_frame()
                tmp["counts"] = tmp["date"]
                tmp["date"] = pd.to_datetime(tmp.index)
                tmp = tmp.sort_values("date")
                for ind_x, x_val in enumerate(x_axis):
                    sum_of_record = tmp.loc[
                        (
                            (tmp["date"].dt.year.astype(str) == x_val[1:5])
                            & (tmp["date"].dt.isocalendar().week.astype(str).str.zfill(2) == x_val[6:8])
                        ),
                        "counts",
                    ].sum()
                    z[division][x_val] = sum_of_record
                    annotatetxt(annotations, sum_of_record, x_val, division)
            if division == "Σ " + "Bangladesh":
                tmp = reportsdata.date.value_counts()
                tmp = tmp.to_frame()
                tmp["counts"] = tmp["date"]
                tmp["date"] = pd.to_datetime(tmp.index)
                for ind_x, x_val in enumerate(x_axis):
                    sum_of_record = tmp.loc[
                        (
                            (tmp["date"].dt.year.astype(str) == x_val[1:5])
                            & (tmp["date"].dt.isocalendar().week.astype(str).str.zfill(2) == x_val[6:8])
                        ),
                        "counts",
                    ].sum()
                    z.loc[x_val, division] = sum_of_record
                    annotatetxt(annotations, sum_of_record, x_val, division)
    else:  # for divisional numbers
        if type(district) is not int:  # is None:
            Districts = fetchdata.fetchDistrictlist(division, geoNameNNumber)
            y_axis = [x["District"] for x in Districts]
            y_axis_no = [x["value"] for x in Districts]
            y_axis.reverse()
            y_axis_no.reverse()
            y_axis.append("Σ " + "Division")
            y_axis_no.append(int(division))
            z = pd.DataFrame(index=x_axis, columns=y_axis)
            for ind_y, district in enumerate(y_axis):  # go through divisions
                if district[:1] != "Σ":  # for districts
                    tmp = reportsdata[(reportsdata["district"] == y_axis_no[ind_y])].date.value_counts()
                    tmp = tmp.to_frame()
                    tmp["counts"] = tmp["date"]
                    tmp["date"] = pd.to_datetime(tmp.index)
                    for ind_x, x_val in enumerate(x_axis):
                        sum_of_record = tmp.loc[
                            (
                                (tmp["date"].dt.year.astype(str) == x_val[1:5])
                                & (tmp["date"].dt.isocalendar().week.astype(str).str.zfill(2) == x_val[6:8])
                            ),
                            "counts",
                        ].sum()
                        z[district][x_val] = sum_of_record
                        annotatetxt(annotations, sum_of_record, x_val, district)
                if district[:1] == "Σ":  # for districts
                    tmp = reportsdata.date.value_counts()
                    tmp = tmp.to_frame()
                    tmp["counts"] = tmp["date"]
                    tmp["date"] = pd.to_datetime(tmp.index)
                    for ind_x, x_val in enumerate(x_axis):
                        sum_of_record = tmp.loc[
                            (
                                (tmp["date"].dt.year.astype(str) == x_val[1:5])
                                & (tmp["date"].dt.isocalendar().week.astype(str).str.zfill(2) == x_val[6:8])
                            ),
                            "counts",
                        ].sum()
                        z.loc[x_val, district] = sum_of_record
                        annotatetxt(annotations, sum_of_record, x_val, district)
        else:  # for district numbers
            Upazilas = fetchdata.fetchUpazilalist(district, geoNameNNumber)
            y_axis = [x["Upazila"] for x in Upazilas]
            y_axis_no = [x["value"] for x in Upazilas]
            y_axis.reverse()
            y_axis_no.reverse()
            y_axis.append("Σ " + "District")
            y_axis_no.append(int(district))
            z = pd.DataFrame(index=x_axis, columns=y_axis)
            for ind_y, upazila in enumerate(y_axis):
                if upazila[:1] != "Σ":
                    compcols = True
                    tmp = reportsdata[(reportsdata["upazila"] == y_axis_no[ind_y])].date.value_counts()
                    tmp = tmp.to_frame()
                    tmp["counts"] = tmp["date"]
                    tmp["date"] = pd.to_datetime(tmp.index)
                    for ind_x, x_val in enumerate(x_axis):
                        daysub = 0
                        # weekly defined via isocalendar (starts with Monday)
                        # so does not coincide with bengalian time counts.
                        for weekday in [1, 2, 3, 6, 7]:  # Monday to Sunday skipping Thursday and Friday
                            if pd.Timestamp(
                                date.fromisocalendar(int(x_val[1:5]), int(x_val[6:8]), weekday)
                            ) in pd.to_datetime(tmp["date"]):
                                daysub = daysub + 1
                        z[upazila][x_val] = (daysub / 5) * 100
                        annotatetxt(annotations, "<b>" + "{:.0f}".format((daysub / 5) * 100) + " %<b>", x_val, upazila)
                if upazila[:1] == "Σ":  # for upazila
                    tmp = reportsdata.date.value_counts()
                    for ind_x, x_val in enumerate(x_axis):
                        z.loc[x_val, upazila] = round(z.loc[x_val].sum(), 2) / (z.shape[1] - 1)  # sum_of_record
                        annotatetxt(
                            annotations,
                            "<b>"
                            + "{:.0f}".format(round(z.loc[x_val].iloc[:-1].sum(), 2) / (z.shape[1] - 1))
                            + " %<b>",
                            x_val,
                            upazila,
                        )

    z = z.fillna(0)
    z = z.T
    z = z.to_numpy()
    # Heatmap
    hovertemplate = "<b> %{y}  %{x} <br><br> %{z} Records"

    if compcols:
        compcol = [[0, "red"], [0.2, "#d7301f"], [0.4, "#fc8d59"], [0.6, "#fdcc8a"], [0.8, "#fef0d9"], [1, "white"]]
    else:
        compcol = [[0, "white"], [0.2, "white"], [0.4, "white"], [0.6, "white"], [0.8, "white"], [1, "white"]]

    data = [
        dict(
            x=x_axis,
            y=y_axis,
            z=z,
            type="heatmap",
            name="",
            hovertemplate=hovertemplate,
            showscale=False,
            colorscale=compcol,
        )
    ]

    layout = dict(
        margin=dict(l=100, b=10, t=25, r=30),
        height=500,
        modebar={"orientation": "v"},
        font=dict(family="Open Sans"),
        annotations=annotations,
        # shapes=shapes,
        xaxis=dict(
            type="category",
            side="top",
            ticks="",
            ticklen=2,
            tickfont=dict(family="sans-serif"),
            tickcolor="#ffffff",
        ),
        yaxis=dict(type="category", side="left", ticks="", tickfont=dict(family="sans-serif"), ticksuffix=" "),
        hovermode="closest",
        showlegend=False,
    )

    return {"data": data, "layout": layout}  # , vDis


# def layout_gen():  # aid=None, **other_unknown_query_strings):  # aid=None, **other_unknown_query_strings):
#     # if aid is None:
#     return html.Div([
#         html.Label("Weekly Completeness"),
#         html.Div(id="dummy"),
#         dbc.Col(
#             [
#                 dcc.Graph(id="Completeness")
#             ]
#         )
#     ])
# else:
#     return html.Div([
#         # dcc.Store(id="cache_aid", storage_type="memory", data=aid),
#         html.Label("Weekly Completeness"),
#         html.Div(id="dummy"),
#         dbc.Col(
#             [
#                 dcc.Graph(id="Completeness")
#             ]
#         )
#     ])


layout = html.Div(
    [
        # html.Label("Weekly Completeness"),
        html.H2("Weekly Completeness", style={"textAlign": "center", "font-weight": "bold"}),
        html.Div(id="dummy"),
        dbc.Col([dcc.Graph(id="Completeness")]),
    ]  # layout_gen
)


@callback(
    Output("Completeness", "figure"),
    Input("Completeness", "figure"),
    # Input("Refresh", "n_clicks"),
    Input("dummy", "id"),
    # State("cache_bahis_data", "data"),
    # State("cache_bahis_geodata", "data"),
    State("cache_page_data", "data"),
    State("cache_page_geodata", "data"),
    State("cache_page_settings", "data"),
    prevent_initial_call=True,
)
def Completeness(CompletenessFig, dummy, data, geodata, settings):
    reportsdata = pd.read_json(data, orient="split")
    geoNameNNumber = pd.read_json(geodata, orient="split")
    if type((json.loads(settings))["upazila"]) != int:
        CompletenessFig = generate_reports_heatmap(
            reportsdata,
            geoNameNNumber,
            (json.loads(settings))["daterange"][0],
            (json.loads(settings))["daterange"][1],
            (json.loads(settings))["division"],
            (json.loads(settings))["district"],
        )
    #    else:
    #        CompletenessFig = CompletenessFig

    return CompletenessFig

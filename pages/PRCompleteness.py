import json
from datetime import datetime, timedelta

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State
from fractions import Fraction

from components import fetchdata

dash.register_page(__name__)  # register page to main dash app


def next_sunday(date):
    days_until_sunday = (5 - date.weekday()) % 7
    return date + timedelta(days=days_until_sunday)


def find_weeks(start, end):
    list_of_weeks = []
    current_date = start
    while current_date <= end:
        formatted_date = current_date.strftime("wk(%d.%b.%Y)")
        list_of_weeks.append(formatted_date)
        next_sunday_date = next_sunday(current_date)
        if next_sunday_date > end:
            break
        current_date = next_sunday_date + timedelta(days=1)  # Move to next Monday
    return list_of_weeks


# def find_weeks(start, end):
# list_of_weeks = []
# days_to_thursday = (3 - start.weekday()) % 7
# for i in range((end - start).days + 1):
#     d = (start + timedelta(days=i)).isocalendar()[:2]  # e.g. (2011, 52)
#     yearweek = "y{}w{:02}".format(*d)  # e.g. "201152"
#     list_of_weeks.append(yearweek)
# return sorted(set(list_of_weeks))


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


def parse_start_date(start_date_str):
    month_dict = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }
    day, month, year = start_date_str[3:-1].split(".")
    return datetime(int(year), month_dict[month], int(day))


def sum_records_by_week(tmp, start_date_str):
    start_date = parse_start_date(start_date_str)
    end_date = start_date + timedelta(days=6)
    week_mask = (tmp["date"] >= start_date) & (tmp["date"] <= end_date)
    sum_of_record = tmp.loc[week_mask, "counts"].sum()
    return sum_of_record


def nationalnumber(reportsdata, geoNameNNumber, division, x_axis, annotations):
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
                # sum_of_record = tmp.loc[
                #     (
                #         (tmp["date"].dt.year.astype(str) == x_val[1:5])
                #         & (tmp["date"].dt.isocalendar().week.astype(str).str.zfill(2) == x_val[6:8])
                #     ),
                #     "counts",
                # ].sum()
                sum_of_record = sum_records_by_week(tmp, x_val)
                z[division][x_val] = sum_of_record
                annotatetxt(annotations, sum_of_record, x_val, division)
        if division == "Σ " + "Bangladesh":
            tmp = reportsdata.date.value_counts()
            tmp = tmp.to_frame()
            tmp["counts"] = tmp["date"]
            tmp["date"] = pd.to_datetime(tmp.index)
            for ind_x, x_val in enumerate(x_axis):
                # sum_of_record = tmp.loc[
                #     (
                #         (tmp["date"].dt.year.astype(str) == x_val[1:5])
                #         & (tmp["date"].dt.isocalendar().week.astype(str).str.zfill(2) == x_val[6:8])
                #     ),
                #     "counts",
                # ].sum()
                sum_of_record = sum_records_by_week(tmp, x_val)
                z.loc[x_val, division] = sum_of_record
                annotatetxt(annotations, sum_of_record, x_val, division)
    return z, y_axis, annotatetxt


def divorlowernumber(reportsdata, geoNameNNumber, division, district, x_axis, annotations, compcols, end):
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
                    # sum_of_record = tmp.loc[
                    #     (
                    #         (tmp["date"].dt.year.astype(str) == x_val[1:5])
                    #         & (tmp["date"].dt.isocalendar().week.astype(str).str.zfill(2) == x_val[6:8])
                    #     ),
                    #     "counts",
                    # ].sum()
                    sum_of_record = sum_records_by_week(tmp, x_val)
                    z[district][x_val] = sum_of_record
                    annotatetxt(annotations, sum_of_record, x_val, district)
            if district[:1] == "Σ":  # for districts
                tmp = reportsdata.date.value_counts()
                tmp = tmp.to_frame()
                tmp["counts"] = tmp["date"]
                tmp["date"] = pd.to_datetime(tmp.index)
                for ind_x, x_val in enumerate(x_axis):
                    # sum_of_record = tmp.loc[
                    #     (
                    #         (tmp["date"].dt.year.astype(str) == x_val[1:5])
                    #         & (tmp["date"].dt.isocalendar().week.astype(str).str.zfill(2) == x_val[6:8])
                    #     ),
                    #     "counts",
                    # ].sum()
                    sum_of_record = sum_records_by_week(tmp, x_val)
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
            month_dict = {
                "Jan": 1,
                "Feb": 2,
                "Mar": 3,
                "Apr": 4,
                "May": 5,
                "Jun": 6,
                "Jul": 7,
                "Aug": 8,
                "Sep": 9,
                "Oct": 10,
                "Nov": 11,
                "Dec": 12,
            }
            if upazila[:1] == "Σ":
                tmp = reportsdata.date.value_counts().to_frame()
                tmp["counts"] = tmp["date"]
                tmp["date"] = pd.to_datetime(tmp.index)
            else:
                compcols = True
                tmp = reportsdata[reportsdata["upazila"] == y_axis_no[ind_y]].date.value_counts().to_frame()
                tmp["counts"] = tmp["date"]
                tmp["date"] = pd.to_datetime(tmp.index)

            for ind_x, x_val in enumerate(x_axis):
                daysub = 0
                day = int(x_val.split("(")[1][:2])
                month = x_val.split("(")[1][-9:-6]
                year = int(x_val.split("(")[1][7:-1])
                date_obj = datetime(year, month_dict[month], day)
                weekday = date_obj.weekday()
                if weekday == 6:
                    if pd.Timestamp(date_obj) in pd.to_datetime(tmp["date"]):
                        daysub += 1
                    counter = 0
                    a = -1
                elif weekday == 3 or weekday == 4:
                    counter = 5
                    a = weekday
                else:
                    counter = weekday
                    a = counter

                while counter < 6 and (date_obj + timedelta(days=counter - a - 1) < end):
                    if pd.Timestamp(date_obj + timedelta(days=counter - a)) in pd.to_datetime(tmp["date"]):
                        daysub += 1
                    if counter == 2:
                        counter += 3
                    else:
                        counter += 1

                z[upazila][x_val] = (daysub / 5) * 100
                annotatetxt(annotations, "<b>" + "{:.0f}".format((daysub / 5) * 100) + " %<b>", x_val, upazila)

    return z, y_axis, annotatetxt, compcols


def generate_reports_heatmap(reportsdata, geoNameNNumber, start, end, division, district):
    start = datetime.strptime(str(start), "%Y-%m-%d")
    end = datetime.strptime(str(end), "%Y-%m-%d")
    compcols = False
    x_axis = find_weeks(start, end)  # [1:] without first week
    x_axis = [str(x) for x in x_axis]
    annotations = []
    if type(division) is not int:  # for national numbers
        z, y_axis, annotatetxt = nationalnumber(reportsdata, geoNameNNumber, division, x_axis, annotations)
    else:  # for divisional numbers
        z, y_axis, annotatetxt, compcols = divorlowernumber(
            reportsdata, geoNameNNumber, division, district, x_axis, annotations, compcols, end
        )

    z = z.fillna(0)
    z = z.T
    z = z.to_numpy()
    # Heatmap
    if type(district) is int:
        hovertemplate = "<b> %{y}  %{x} <br><br> %{z} % report completeness"
    else:
        hovertemplate = "<b> %{y}  %{x} <br><br> %{z} Reports"

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
            fixedrange=True,
            side="top",
            ticks="",
            ticklen=2,
            tickfont=dict(family="sans-serif"),
            tickcolor="#ffffff",
        ),
        yaxis=dict(
            fixedrange=True, type="category", side="left", ticks="", tickfont=dict(family="sans-serif"), ticksuffix=" "
        ),
        hovermode="closest",
        showlegend=False,
    )

    return {"data": data, "layout": layout}  # , vDis


def layout_gen(aid=None, **other_unknown_query_strings):
    if aid is not None:
        dcc.Store(id="cache_aid", storage_type="memory", data=aid),
    return html.Div(
        [
            html.H2("Weekly Completeness", style={"textAlign": "center", "font-weight": "bold"}),
            html.Div(id="dummy"),
            html.Div(
                dbc.Col([dcc.Graph(id="Completeness", style={"overflowX": "scroll", "minWidth": "1200px"})]),
                style={"width": "100%", "overflowX": "auto"},
            ),
        ]
    )


layout = layout_gen


@callback(
    Output("Completeness", "figure"),
    # Output("Completeness", "style"),
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

        # style = {"width": "150%"}
    else:
        CompletenessFig = CompletenessFig

    return CompletenessFig  # , style


@callback(
    Output("Completeness", "style"),
    # Output("Completeness", "figure", allow_duplicate=True),
    Input("Completeness", "figure"),
    prevent_initial_call=True,
)
def adjust_scroll(fig):
    datapoints = len(fig["data"][0]["x"])
    return {"minWidth": str(datapoints * 120) + "px"}  # "overflowX": "scroll" if datapoints > 7 else "auto",

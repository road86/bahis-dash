import json
from datetime import datetime, timedelta
import plotly.express as px

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State

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


def parse_start_date(start_date_str):
    day, month, year = start_date_str[3:-1].split(".")
    return datetime(int(year), month_dict[month], int(day))


def sum_records_by_week(tmp, start_date_str):
    start_date = parse_start_date(start_date_str)
    end_date = start_date + timedelta(days=(6 - (6 - start_date.weekday())))
    week_mask = (tmp["date"] >= start_date) & (tmp["date"] <= end_date)
    return tmp.loc[week_mask, "counts"].sum()


def calculate_sum_of_records(tmp, x_val, end):
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

    return (daysub / 5) * 100


def process_data(reportsdata, y_axis_no, x_axis, end, level, name_key, annotations):
    z = pd.DataFrame(index=x_axis, columns=[x[name_key] for x in y_axis_no])
    col = pd.DataFrame(index=x_axis, columns=[x[name_key] for x in y_axis_no])
    for ind_y, area in enumerate(y_axis_no):
        tmp = reportsdata[(reportsdata[level] == area["value"])].date.value_counts().to_frame()
        tmp["counts"] = tmp["date"]
        tmp["date"] = pd.to_datetime(tmp.index)
        for ind_x, x_val in enumerate(x_axis):
            # sum_of_record = calculate_sum_of_records(tmp, x_val, end)
            sum_of_record = sum_records_by_week(tmp, x_val)
            weekly_comp = calculate_sum_of_records(tmp, x_val, end)
            svalue = str(sum_of_record) + " (" + "{:.0%}".format(weekly_comp / 100) + ")"
            z[area[name_key]][x_val] = sum_of_record  # svalue
            col[area[name_key]][x_val] = "{:.2f}".format(weekly_comp / 100)
            annotatetxt(annotations, svalue, x_val, area[name_key])
    return z, col


def process_aggregated_data(reportsdata, x_axis, end, level, annotations):
    z_aggregated = pd.DataFrame(index=x_axis, columns=["Σ " + level])
    col2 = pd.DataFrame(index=x_axis, columns=["Σ " + level])
    tmp = reportsdata.date.value_counts().to_frame()
    tmp["counts"] = tmp["date"]
    tmp["date"] = pd.to_datetime(tmp.index)
    for ind_x, x_val in enumerate(x_axis):
        sum_of_record = sum_records_by_week(tmp, x_val)
        weekly_comp = calculate_sum_of_records(tmp, x_val, end)
        svalue = str(sum_of_record) + " (" + "{:.0%}".format(weekly_comp / 100) + ")"
        z_aggregated.loc[x_val, "Σ " + level] = sum_of_record
        col2.loc[x_val, "Σ " + level] = "{:.2f}".format(weekly_comp / 100)
        annotatetxt(annotations, svalue, x_val, "Σ " + level)
    return z_aggregated, col2


def divorlowernumber(reportsdata, geoNameNNumber, division, district, upazila, x_axis, annotations, end):
    if not isinstance(division, int):  # for national numbers
        y_axis_no = fetchdata.fetchDivisionlist(geoNameNNumber)
        z, col = process_data(reportsdata, y_axis_no, x_axis, end, "division", "Division", annotations)
        z_aggregated, col2 = process_aggregated_data(reportsdata, x_axis, end, "Bangladesh", annotations)
        z_combined = pd.concat([z_aggregated, z], axis=1)
        y = [x["Division"] for x in y_axis_no]
        y.reverse()
        y.append("Σ Bangladesh")
        return z_combined, y, pd.concat([col2, col], axis=1)

    if not isinstance(district, int):  # for divisional numbers
        y_axis_no = fetchdata.fetchDistrictlist(division, geoNameNNumber)
        z, col = process_data(reportsdata, y_axis_no, x_axis, end, "district", "District", annotations)
        z_aggregated, col2 = process_aggregated_data(reportsdata, x_axis, end, "Division", annotations)
        z_combined = pd.concat([z_aggregated, z], axis=1)
        y = [x["District"] for x in y_axis_no]
        y.reverse()
        y.append("Σ Division")
        return z_combined, y, pd.concat([col2, col], axis=1)

    if not isinstance(upazila, int):  # for district numbers
        y_axis_no = fetchdata.fetchUpazilalist(district, geoNameNNumber)
        z, col = process_data(reportsdata, y_axis_no, x_axis, end, "upazila", "Upazila", annotations)
        z_aggregated, col2 = process_aggregated_data(reportsdata, x_axis, end, "District", annotations)
        z_combined = pd.concat([z_aggregated, z], axis=1)
        y = [x["Upazila"] for x in y_axis_no]
        y.reverse()
        y.append("Σ District")
        return z_combined, y, pd.concat([col2, col], axis=1)

    if isinstance(upazila, int):  # for upazila numbers
        y_axis_no = [
            {
                "value": int(geoNameNNumber[["value"]].to_string(index=False, header=False)),
                "Upazila": geoNameNNumber[["name"]].to_string(index=False, header=False).capitalize(),
            }
        ]
        z, col = process_data(reportsdata, y_axis_no, x_axis, end, "upazila", "Upazila", annotations)
        y = [x["Upazila"] for x in y_axis_no]
        y.reverse()
        return z, y, col


def generate_reports_heatmap(tmpexport, reportsdata, geoNameNNumber, start, end, division, district, upazila):
    start = datetime.strptime(str(start), "%Y-%m-%d")
    end = datetime.strptime(str(end), "%Y-%m-%d")
    x_axis = find_weeks(start, end)  # [1:] without first week
    x_axis = [str(x) for x in x_axis]
    annotations = []
    if reportsdata.shape[0] != 0:
        z, y_axis, col = divorlowernumber(
            reportsdata, geoNameNNumber, division, district, upazila, x_axis, annotations, end
        )
        z = z.fillna(0)
        z = z.T
        tmpexport = pd.DataFrame(z)
        z = z.to_numpy()
        col = col.fillna(0)
        col = col.T
        col = col.iloc[::-1]
        col = col.to_numpy()
        # Heatmap
        # if type(district) is int:
        #     hovertemplate = "<b> %{y}  %{x} <br><br> %{z} % report completeness"
        # else:
        hovertemplate = "<b> %{y}  %{x} <br><br> %{text} Reports"  # %{z} Reports"

        compcol = [[0, "#FF7777"], [0.2, "#FFAAAA"], [0.4, "#F3D0D7"], [0.6, "#FFE0B5"], [0.8, "#FFF2D7"], [1, "white"]]
        data = [
            dict(
                x=x_axis,
                y=y_axis,
                z=col,
                type="heatmap",
                name="",
                hovertemplate=hovertemplate,
                text=z,
                showscale=False,
                colorscale=compcol,
            )
        ]

        layout = dict(
            margin=dict(l=110, b=10, t=25, r=30),
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
                fixedrange=True,
                type="category",
                side="left",
                ticks="",
                tickfont=dict(family="sans-serif"),
                ticksuffix=" ",
            ),
            hovermode="closest",
            showlegend=False,
        )
        return tmpexport, {"data": data, "layout": layout}  # , vDis
    else:
        fig = px.scatter()

        fig.add_annotation(
            text="No data available", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(size=20)
        )

        # Update layout to center the annotation
        fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False), plot_bgcolor="white")

        return tmpexport, fig


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
            dcc.Store(id="exportdata"),
            dbc.Row(
                [
                    dbc.Col(html.Button("Export", id="btn_csv")),
                    dbc.Col(
                        html.P(
                            "The percentage represents the number of days reported out of 5 workdays.",
                            style={"font-size": "80%", "text-align": "right"},
                        ),
                        width=7,
                    ),
                ]
            ),
            dcc.Download(id="download-dataframe-csv"),
        ]
    )


layout = layout_gen


@callback(
    Output("Completeness", "figure"),
    Output("exportdata", "data"),
    Input("Completeness", "figure"),
    Input("dummy", "id"),
    State("cache_page_data", "data"),
    State("cache_page_geodata", "data"),
    State("cache_page_settings", "data"),
    State("exportdata", "data"),
    prevent_initial_call=True,
)
def Completeness(CompletenessFig, dummy, data, geodata, settings, tmpexport):
    reportsdata = pd.read_json(data, orient="split")
    geoNameNNumber = pd.read_json(geodata, orient="split")
    if tmpexport is not None:
        tmpexport = json.loads(tmpexport)
    else:
        tmpexport = []
    #    if type((json.loads(settings))["upazila"]) != int:
    tmpexport, CompletenessFig = generate_reports_heatmap(
        tmpexport,
        reportsdata,
        geoNameNNumber,
        (json.loads(settings))["daterange"][0],
        (json.loads(settings))["daterange"][1],
        (json.loads(settings))["division"],
        (json.loads(settings))["district"],
        (json.loads(settings))["upazila"],
    )
    #     # style = {"width": "150%"}
    # else:
    # CompletenessFig = CompletenessFig
    if not isinstance(tmpexport, pd.DataFrame):
        return CompletenessFig, "{}"  # Return an empty JSON object
    else:
        return CompletenessFig, tmpexport.to_json(date_format="iso", orient="split")
    # return CompletenessFig, tmpexport.to_json(date_format="iso", orient="split")  # , style


@callback(
    Output("Completeness", "style"),
    # Output("Completeness", "figure", allow_duplicate=True),
    Input("Completeness", "figure"),
    prevent_initial_call=True,
)
def adjust_scroll(fig):
    if fig["data"][0]["type"] == "heatmap":
        datapoints = len(fig["data"][0]["x"])
        return {"minWidth": str(datapoints * 120) + "px"}  # "overflowX": "scroll" if datapoints > 7 else "auto",
    else:
        return {"minWidth": "10px"}


@callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    State("exportdata", "data"),
    prevent_initial_call=True,
)
def func(n_clicks, data):
    tmpdata = json.loads(data)
    exportdata = pd.DataFrame(tmpdata["data"], columns=tmpdata["columns"], index=tmpdata["index"])
    return dcc.send_data_frame(exportdata.to_csv, "my_data.csv")

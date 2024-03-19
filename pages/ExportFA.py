import dash
from dash import html, dcc, callback, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
from components import fetchdata
import json


dash.register_page(
    __name__,
)  # register page to main dash app


def layout_gen(aid=None, **other_unknown_query_strings):
    if aid is not None:
        dcc.Store(id="cache_aid", storage_type="memory", data=aid),
    return html.Div(
        [
            html.Label("Export Data", id="ExportLabelFA"),
            html.Div(id="ExportTabFA"),
            html.Div(id="dummy"),
            # html.Button("download raw data", id="raw_csv"),
            # dcc.Download(id="raw_download"),
        ]
    )


layout = layout_gen


@callback(
    Output("ExportLabelFA", "children"),
    Output("ExportTabFA", "children"),
    Input("cache_filenames", "data"),
    Input("dummy", "id"),
    State("cache_page_farmdata", "data"),
    prevent_initial_call=True,
)
def Export(filenames, dummy, data):  # , fullgeodata):
    reportsdata = pd.read_json(data, orient="split")
    geofilename = json.loads(filenames)["geo"]
    fullgeodata = fetchdata.fetchgeodata(geofilename)

    ExportTable = reportsdata
    ExportTable["date"] = ExportTable["date"].dt.strftime("%Y-%m-%d")

    ExportTable.rename(columns={"top_diagnosis": "Diagnosis"}, inplace=True)

    ExportTable = ExportTable.merge(fullgeodata[["value", "name"]], left_on="division", right_on="value")
    ExportTable["division"] = ExportTable["name"].str.capitalize()
    ExportTable.drop(["name", "value"], inplace=True, axis=1)

    ExportTable = ExportTable.merge(fullgeodata[["value", "name"]], left_on="district", right_on="value")
    ExportTable["district"] = ExportTable["name"].str.capitalize()
    ExportTable.drop(["name", "value"], inplace=True, axis=1)

    ExportTable = ExportTable.merge(fullgeodata[["value", "name"]], left_on="upazila", right_on="value")
    ExportTable["upazila"] = ExportTable["name"].str.capitalize()
    ExportTable.drop(["name", "value"], inplace=True, axis=1)

    ExportLabel = "Export Data Entries: " + str(ExportTable.shape[0])

    ExportTab = (
        dash_table.DataTable(
            style_header={
                # 'overflow': 'hidden',
                # 'maxWidth': 0,
                "fontWeight": "bold",
            },
            style_cell={"textAlign": "left"},
            export_format="csv",
            style_table={"height": "500px", "overflowY": "auto"},
            # style_as_list_view=True,
            # fixed_rows={'headers': True},
            data=ExportTable.to_dict("records"),
            columns=[{"name": i, "id": i} for i in ExportTable.columns],
        ),
    )
    return ExportLabel, ExportTab

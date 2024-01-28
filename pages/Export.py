import dash
from dash import html, dcc, callback, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
from components import fetchdata, pathnames


dash.register_page(__name__,)  # register page to main dash app


def layout_gen(aid=None, **other_unknown_query_strings): 
    if aid is not None:
        dcc.Store(id="cache_aid", storage_type="memory", data=aid),
    return html.Div([
        html.Label("Export Data", id="ExportLabel"),
        html.Div(id="ExportTab"),
        html.Div(id="dummy"),
    ])


layout = layout_gen

@callback(
    Output("ExportLabel", "children"),
    Output("ExportTab", "children"),
    Input("dummy", "id"),
    State("cache_page_data", "data"),
    #    State("cache_bahis_geodata", "data"),
    prevent_initial_call=True
)
def Poultry(dummy, data):  # , fullgeodata):

    reportsdata = pd.read_json(data, orient="split")

    sourcepath = "exported_data/"           # called also in Top10, make global or settings parameter
    geofilename, dgfilename, sourcefilename, path1, path2, path3 = pathnames.get_pathnames(sourcepath)
    fullgeodata = fetchdata.fetchgeodata(geofilename)

    ExportTable = reportsdata
    ExportTable["date"] = ExportTable["date"].dt.strftime("%Y-%m-%d")
    # del ExportTable["Unnamed: 0.1"]

    ExportTable.drop("species_no", inplace=True, axis=1)
    ExportTable.drop("tentative_diagnosis", inplace=True, axis=1)
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

    ExportLabel = "Export Data Size: " + str(ExportTable.shape)

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

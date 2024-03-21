import json

import dash
import pandas as pd
from dash import callback, dash_table, dcc, html
from dash.dependencies import Input, Output

from components import fetchdata, pathnames

dash.register_page(__name__)

sourcepath = "exported_data/"  # called also in Top10, make global or settings parameter
(
    geofilename,
    dgfilename,
    sourcefilename,
    farmdatafilename,
    AIinvestdatafilename,
    DiseaseInvestdatafilename,
    PartLSAssisdatafilename,
    medfilename,
    path1,
    path2,
    path3,
) = pathnames.get_pathnames(sourcepath)

bahis_data = fetchdata.fetchsourcedata(sourcefilename)
farm_data = fetchdata.fetchfarmdata(farmdatafilename)
AIinvest_data = fetchdata.fetchAIinvestdata(AIinvestdatafilename)
DiseaseInvest_data = fetchdata.fetchDiseaseInvestdata(DiseaseInvestdatafilename)
PartLSAssis_data = fetchdata.fetchPartLSAssdata(PartLSAssisdatafilename)
geodata = fetchdata.fetchgeodata(geofilename)

patientrep = bahis_data[["date", "division", "district", "upazila"]].copy()
farmrep = farm_data[["date", "division", "district", "upazila"]].copy()
AIinrep = AIinvest_data[["date", "division", "district", "upazila"]].copy()
DisInrep = DiseaseInvest_data[["date", "division", "district", "upazila"]].copy()
PaLSrep = PartLSAssis_data[["date", "division", "district", "upazila"]].copy()
del bahis_data, farm_data, AIinvest_data, DiseaseInvest_data, PartLSAssis_data


def replaceno2name(data, geodata):
    data = data.merge(geodata[["value", "name"]], left_on="division", right_on="value")
    data["division"] = data["name"].str.capitalize()
    data.drop(["name", "value"], inplace=True, axis=1)

    data = data.merge(geodata[["value", "name"]], left_on="district", right_on="value")
    data["district"] = data["name"].str.capitalize()
    data.drop(["name", "value"], inplace=True, axis=1)

    data = data.merge(geodata[["value", "name"]], left_on="upazila", right_on="value")
    data["upazila"] = data["name"].str.capitalize()
    data.drop(["name", "value"], inplace=True, axis=1)
    return data


def layout_gen(aid=None, **other_unknown_query_strings):
    if aid is not None:
        dcc.Store(id="cache_aid", storage_type="memory", data=aid),
    return html.Div(
        [
            html.H2("Form Summary", style={"textAlign": "center", "font-weight": "bold"}),
            html.Div(id="Formdata"),
            html.Div(id="dummy"),
        ]
    )


layout = layout_gen


@callback(
    Output("Formdata", "children"),
    Input("dummy", "id"),
    Input("cache_page_settings", "data"),
    prevent_initial_call=True,
)
def Export(dummy, settings):  # , fullgeodata):
    pr = patientrep
    fr = farmrep
    ar = AIinrep
    dr = DisInrep
    lr = PaLSrep

    pr = fetchdata.date_subset(json.loads(settings)["daterange"], pr)
    fr = fetchdata.date_subset(json.loads(settings)["daterange"], fr)
    ar = fetchdata.date_subset(json.loads(settings)["daterange"], ar)
    dr = fetchdata.date_subset(json.loads(settings)["daterange"], dr)
    lr = fetchdata.date_subset(json.loads(settings)["daterange"], lr)

    if type(json.loads(settings)["upazila"]) == int:
        pr = pr.loc[pr["upazila"] == json.loads(settings)["upazila"]]
        fr = fr.loc[fr["upazila"] == json.loads(settings)["upazila"]]
        ar = ar.loc[ar["upazila"] == json.loads(settings)["upazila"]]
        dr = dr.loc[dr["upazila"] == json.loads(settings)["upazila"]]
        lr = lr.loc[lr["upazila"] == json.loads(settings)["upazila"]]
    else:
        if type(json.loads(settings)["district"]) == int:
            pr = pr.loc[pr["district"] == json.loads(settings)["district"]]
            fr = fr.loc[fr["district"] == json.loads(settings)["district"]]
            ar = ar.loc[ar["district"] == json.loads(settings)["district"]]
            dr = dr.loc[dr["district"] == json.loads(settings)["district"]]
            lr = lr.loc[lr["district"] == json.loads(settings)["district"]]
        else:
            if type(json.loads(settings)["division"]) == int:
                pr = pr.loc[pr["division"] == json.loads(settings)["division"]]
                fr = fr.loc[fr["division"] == json.loads(settings)["division"]]
                ar = ar.loc[ar["division"] == json.loads(settings)["division"]]
                dr = dr.loc[dr["division"] == json.loads(settings)["division"]]
                lr = lr.loc[lr["division"] == json.loads(settings)["division"]]
            else:
                pr = pr
                fr = fr
                ar = ar
                dr = dr
                lr = lr

    pr = replaceno2name(pr, geodata)
    fr = replaceno2name(fr, geodata)
    ar = replaceno2name(ar, geodata)
    dr = replaceno2name(dr, geodata)
    lr = replaceno2name(lr, geodata)

    pr = pr.groupby(["date", "division", "district", "upazila"]).size().reset_index(name="patients")
    fr = fr.groupby(["date", "division", "district", "upazila"]).size().reset_index(name="farm")
    ar = ar.groupby(["date", "division", "district", "upazila"]).size().reset_index(name="AIin")
    dr = dr.groupby(["date", "division", "district", "upazila"]).size().reset_index(name="DisIn")
    lr = lr.groupby(["date", "division", "district", "upazila"]).size().reset_index(name="PaLs")
    overview = pd.merge(pr, fr, on=["date", "division", "district", "upazila"], how="outer")
    overview = pd.merge(overview, ar, on=["date", "division", "district", "upazila"], how="outer")
    overview = pd.merge(overview, dr, on=["date", "division", "district", "upazila"], how="outer")
    overview = pd.merge(overview, lr, on=["date", "division", "district", "upazila"], how="outer")

    # ExportTable = reportsdata
    # ExportTable["date"] = ExportTable["date"].dt.strftime("%Y-%m-%d")
    # # del ExportTable["Unnamed: 0.1"]

    # ExportLabel = "Export Data Entries: " + str(ExportTable.shape[0])

    OverviewTab = (
        dash_table.DataTable(
            style_header={
                # 'overflow': 'hidden',
                # 'maxWidth': 0,
                "fontWeight": "bold",
            },
            style_cell={"textAlign": "left", "minWidth": 25, "width": 150, "maxWidth": 225},
            export_format="csv",
            fixed_rows={"headers": True},
            virtualization=True,
            style_table={"height": "450px"},  # , "overflowY": "auto"},
            # style_as_list_view=True,
            data=overview.to_dict("records"),
            columns=[{"name": i, "id": i} for i in overview.columns],
        ),
    )
    return OverviewTab

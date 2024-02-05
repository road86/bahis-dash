# create overall page
# store data in cache
# general layout: navbar and "body"

import dash
import dash_bootstrap_components as dbc
from components import navbar, pathnames, fetchdata
from dash import Dash, Input, Output, dcc, html, State, ctx

from components import RegionSelect, MapNResolution, DateRangeSelect, DiseaseSelect
import pandas as pd
import json

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    suppress_callback_exceptions=True,
    prevent_initial_callbacks="initial_duplicate",
)

dash.register_page(
    __name__,
)  # register page to main dash app

sourcepath = "exported_data/"  # called also in Top10, make global or settings parameter
geofilename, dgfilename, sourcefilename, farmdatafilename, path1, path2, path3 = pathnames.get_pathnames(sourcepath)
bahis_data = fetchdata.fetchsourcedata(sourcefilename)
farm_data = fetchdata.fetchfarmdata(farmdatafilename)
[bahis_dgdata, bahis_distypes] = fetchdata.fetchdisgroupdata(dgfilename)
bahis_geodata = fetchdata.fetchgeodata(geofilename)

create_date = fetchdata.create_date(sourcefilename)  # implement here


def decode(pathname):
    if pathname is not None:
        geoNo = ""
        for x in range(0, 12):
            geoNo = geoNo + str(int(ord(pathname[x])) - 66)
        return int(int(geoNo) / 42)
    else:
        return pathname


def layout_gen():
    img_logo = "assets/Logo.png"
    return html.Div(
        [
            dcc.Location(id="url", refresh=True),
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Button(
                                        "Menu",
                                        id="open-sidemenu",
                                        n_clicks=0,
                                        style={"font-size": "150%"},
                                    ),
                                    dbc.Offcanvas(
                                        html.Div(id="sidemenu_content"),
                                        id="sidemenu",
                                        title="Menu",
                                        is_open=False,
                                    ),
                                ]
                            ),
                            dbc.Col(
                                html.H1("BAHIS Dashboard (beta)"),
                                width=5,
                            ),
                            dbc.Col(
                                width=3,
                            ),
                        ],
                        justify="end",
                        align="center",
                    )
                ]
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(  # left side
                        [
                            dbc.Card(
                                dbc.CardBody(RegionSelect.Form),
                            ),
                            dbc.Card(dbc.CardBody(MapNResolution.Form)),
                        ],
                        width=4,
                    ),
                    dbc.Col(
                        [  # right side
                            dbc.Card(
                                dbc.CardBody([dbc.Row([dbc.Col(DateRangeSelect.Form), dbc.Col(DiseaseSelect.Form)])])
                            ),
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    dash.page_container,
                                                ]
                                            )
                                        )
                                    ]
                                ),
                            ),
                        ]
                    ),
                ]
            ),
            html.Br(),
            html.Div(id="dummy"),
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(html.P("Data last updated " + str(create_date), style={"font-size": "80%"})),
                            dbc.Col(
                                html.P(
                                    "Developed by the Department of Livestock Services (Bangladesh Government) with support from FAO Bangladesh ECTAD 2024",
                                    style={"font-size": "80%"},
                                ),
                                width=5,
                            ),
                            dbc.Col(
                                html.Img(src=img_logo, height="45px"),
                                width=5,
                            ),
                        ],
                        justify="end",
                        align="center",
                    )
                ]
            ),
            dcc.Store(id="cache_page_settings", storage_type="memory"),
            dcc.Store(id="cache_page_data", storage_type="memory"),
            dcc.Store(id="cache_page_farmdata", storage_type="memory"),
            dcc.Store(id="cache_page_geodata", storage_type="memory"),
            dcc.Store(id="cache_aid", storage_type="memory"),
        ],
        style={"margin": "10px"},
    )


app.layout = layout_gen


@app.callback(
    Output("sidemenu_content", "children"),
    Input("sidemenu", "is_open"),
    State("cache_aid", "data"),
)
def build_sidemenu(sidemenu_open, aid):
    if aid is not None:
        return navbar.Navbar(aid)
    else:
        return html.Div(html.Label("Wrong URL, please ask for support"))


@app.callback(
    Output("sidemenu", "is_open"),
    Input("open-sidemenu", "n_clicks"),
    State("sidemenu", "is_open"),
)
def display_valueNtoggle_offcanvas(n1, is_open):
    if n1:
        return (not is_open,)
    return is_open  # , id


@app.callback(
    Output("Division", "options", allow_duplicate=True),
    Output("District", "options"),
    Output("Upazila", "options"),
    Output("Division", "value"),
    Output("District", "value"),
    Output("Upazila", "value"),
    Output("geoSlider", "value"),
    Output("Disease", "options", allow_duplicate=True),
    Output("cache_page_settings", "data"),
    Input("Division", "value"),
    Input("District", "value"),
    Input("Upazila", "value"),
    Input("Division", "options"),
    Input("District", "options"),
    Input("Upazila", "options"),
    Input("geoSlider", "value"),
    Input("DateRange", "value"),
    Input("Disease", "value"),
    Input("cache_aid", "data"),
)
def Framework(
    SelectedDivision,
    SelectedDistrict,
    SelectedUpazila,
    DivisionList,
    DistrictList,
    UpazilaList,
    geoSlider,
    DateRange,
    SelectedDisease,
    aid,
):  # , urlid):
    # 20*42= 000 000 000 840
    # BBB BBB BBB JFB
    # 2015*42= 000 000 084 630
    # BBB BBB BJF HEB
    if aid is not None:
        aid = str(decode(aid))
    # else:
    #     aid is None
    geoNameNNumber = bahis_geodata
    # against node is null error
    if DistrictList is None:
        DistrictList = []
    if UpazilaList is None:
        UpazilaList = []

    DiseaseList = fetchdata.fetchDiseaselist(bahis_data)

    if aid == "1620859":
        List = fetchdata.fetchDivisionlist(bahis_geodata)
        DivisionList = [{"label": i["Division"], "value": i["value"]} for i in List]
    elif (aid is not None) and (aid != "1620859"):
        # List = fetchdata.fetchDivisionlist(bahis_geodata)
        # DivisionList = [{"label": i["Division"], "value": i["value"]} for i in List]
        SelectedDivision = int(aid[0:2])
        List = fetchdata.fetchDivisionlist(bahis_geodata)
        DivisionList = [{"label": i["Division"], "value": i["value"], "disabled": True} for i in List]
        List = fetchdata.fetchDistrictlist(SelectedDivision, geoNameNNumber)
        DistrictList = [{"label": i["District"], "value": i["value"]} for i in List]
        if len(str(aid)) == 4:
            SelectedDistrict = int(aid[0:4])
            List = fetchdata.fetchDistrictlist(SelectedDivision, geoNameNNumber)
            DistrictList = [{"label": i["District"], "value": i["value"], "disabled": True} for i in List]
            List = fetchdata.fetchUpazilalist(SelectedDistrict, geoNameNNumber)
            UpazilaList = [{"label": i["Upazila"], "value": i["value"]} for i in List]
    else:
        DiseaseList = fetchdata.fetchDiseaselist(bahis_data)
        List = fetchdata.fetchDivisionlist(bahis_geodata)
        DivisionList = [{"label": i["Division"], "value": i["value"]} for i in List]
        DistrictList = []
        UpazilaList = []
        DiseaseList = []

    if ctx.triggered_id == "geoSlider":
        if geoSlider == 2:
            if SelectedUpazila is not None:
                geoSlider = 3
        if geoSlider == 1:
            if SelectedUpazila is not None:
                geoSlider = 3
            elif SelectedDistrict is not None:
                geoSlider = 2

    if ctx.triggered_id == "Division":
        if not SelectedDivision:
            DistrictList = []
            SelectedDistrict = None
        else:
            List = fetchdata.fetchDistrictlist(SelectedDivision, geoNameNNumber)
            DistrictList = [{"label": i["District"], "value": i["value"]} for i in List]
        SelectedDistrict = None
        UpazilaList = []
        SelectedUpazila = None

    if ctx.triggered_id == "District":
        if not SelectedDistrict:
            UpazilaList = []
        else:
            if geoSlider == 1:
                geoSlider = 2
            List = fetchdata.fetchUpazilalist(SelectedDistrict, geoNameNNumber)
            UpazilaList = [{"label": i["Upazila"], "value": i["value"]} for i in List]
        SelectedUpazila = None

    if ctx.triggered_id == "Upazila":
        if geoSlider < 3:
            geoSlider = 3

    page_settings = {
        "division": SelectedDivision,
        "district": SelectedDistrict,
        "upazila": SelectedUpazila,
        "georesolution": geoSlider,
        "disease": SelectedDisease,
        "daterange": DateRange,
    }

    return (
        DivisionList,
        DistrictList,
        UpazilaList,
        SelectedDivision,
        SelectedDistrict,
        SelectedUpazila,
        geoSlider,
        DiseaseList,
        json.dumps(page_settings),
    )


@app.callback(
    Output("cache_page_data", "data"),
    Output("cache_page_farmdata", "data"),
    Output("cache_page_geodata", "data"),
    Output("Disease", "options", allow_duplicate=True),
    Input("cache_page_settings", "data"),
    Input("cache_aid", "data"),
)
def UpdatePageData(settings, aid):
    if aid is None:
        return None, None, None, []
    else:
        reportsdata = bahis_data
        geodata = bahis_geodata
        reportsdata = fetchdata.date_subset(json.loads(settings)["daterange"], reportsdata)
        reportsdata = fetchdata.disease_subset(json.loads(settings)["disease"], reportsdata)

        if type(json.loads(settings)["upazila"]) == int:
            reportsdata = reportsdata.loc[reportsdata["upazila"] == json.loads(settings)["upazila"]]
            geodata = geodata.loc[geodata["value"].astype(str).str[:6].astype(int) == json.loads(settings)["upazila"]]
        else:
            if type(json.loads(settings)["district"]) == int:
                reportsdata = reportsdata.loc[reportsdata["district"] == json.loads(settings)["district"]]
                geodata = geodata.loc[
                    geodata["value"].astype(str).str[:4].astype(int) == json.loads(settings)["district"]
                ]
            else:
                if type(json.loads(settings)["division"]) == int:
                    reportsdata = reportsdata.loc[reportsdata["division"] == json.loads(settings)["division"]]
                    geodata = geodata.loc[
                        geodata["value"].astype(str).str[:2].astype(int) == json.loads(settings)["division"]
                    ]
                else:
                    reportsdata = reportsdata
                    geodata = geodata

        farmdata = farm_data
        farmdata = fetchdata.date_subset(json.loads(settings)["daterange"], farmdata)
        farmdata = fetchdata.disease_subset(json.loads(settings)["disease"], farmdata)

        if type(json.loads(settings)["upazila"]) == int:
            farmdata = farmdata.loc[farmdata["upazila"] == json.loads(settings)["upazila"]]
        else:
            if type(json.loads(settings)["district"]) == int:
                farmdata = farmdata.loc[farmdata["district"] == json.loads(settings)["district"]]
            else:
                if type(json.loads(settings)["division"]) == int:
                    farmdata = farmdata.loc[farmdata["division"] == json.loads(settings)["division"]]
                else:
                    farmdata = farmdata

        page_data = reportsdata
        page_farmdata = farmdata
        page_geodata = geodata
        return (
            page_data.to_json(date_format="iso", orient="split"),
            page_farmdata.to_json(date_format="iso", orient="split"),
            page_geodata.to_json(date_format="iso", orient="split"),
            fetchdata.fetchDiseaselist(reportsdata),
        )


@app.callback(
    Output("Map", "figure", allow_duplicate=True),
    Output("dummy", "id", allow_duplicate=True),
    Input("cache_page_data", "data"),
    Input("cache_page_geodata", "data"),
    Input("cache_page_settings", "data"),
    Input("dummy", "id"),
)
def UpdateFigs(data, geodata, settings, dummy):
    if data is not None:
        MapFig = MapNResolution.plotMap(
            json.loads(settings)["georesolution"],
            pd.read_json(data, orient="split"),
            pd.read_json(geodata, orient="split"),
        )
        # dummy="1"
        return MapFig, dummy
    else:
        return {}, dummy


# Run the app on localhost:80
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)  # maybe debug false to prevent second loading
else:
    server = app.server

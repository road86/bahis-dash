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

dash.register_page(__name__,)  # register page to main dash app

sourcepath = "exported_data/"           # called also in Top10, make global or settings parameter
geofilename, dgfilename, sourcefilename, path1, path2, path3 = pathnames.get_pathnames(sourcepath)
bahis_data = fetchdata.fetchsourcedata(sourcefilename)
[bahis_dgdata, bahis_distypes] = fetchdata.fetchdisgroupdata(dgfilename)
bahis_geodata = fetchdata.fetchgeodata(geofilename)

create_date = fetchdata.create_date(sourcefilename)  # implement here


app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar.Navbar(),
        html.Br(),

        dbc.Row(
            [
                dbc.Col(            # left side
                    [
                        dbc.Card(
                            dbc.CardBody(RegionSelect.Form),
                        ),
                        dbc.Card(
                            dbc.CardBody(MapNResolution.Form)
                        )
                    ],
                    width=4,
                ),
                dbc.Col([          # right side
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            DateRangeSelect.Form
                                        ),
                                        dbc.Col(
                                            DiseaseSelect.Form
                                        )
                                    ]
                                )
                            ]
                        )
                    ),
                    dbc.Card(
                        dbc.CardBody(
                            [dbc.Card(
                                dbc.CardBody([
                                    dash.page_container,
                                ])
                            )]
                        ),
                    ),
                ])
            ]
        ),

        html.Br(),
        html.Div(id="dummy"),
        html.Label('Data last updated ' + str(create_date), style={'text-align': 'right'}),
        # dcc.Store(id="cache_bahis_data", storage_type="memory"),
        # dcc.Store(data=bahis_dgdata.to_json(date_format='iso', orient='split')
        # id="cache_bahis_dgdata", storage_type="memory"),
        # dcc.Store(data=bahis_distypes.to_json(date_format='iso', orient='split')
        # id="cache_bahis_distypes", storage_type="memory"),
        # dcc.Store(id="cache_bahis_geodata", storage_type="memory"),
        dcc.Store(id="cache_page_settings", storage_type="memory"),
        dcc.Store(id="cache_page_data", storage_type="memory"),
        dcc.Store(id="cache_page_geodata", storage_type="memory"),
    ]
)


# @app.callback(
#     Output("cache_bahis_data", "data"),
#     Output("cache_bahis_distypes", "data"),
#     Output("cache_bahis_geodata", "data"),
#     Input("dummy", "id")
# )

# def store2cache(dummy):
#     return bahis_data.to_json(date_format='iso', orient='split'), bahis_distypes.to_json
# (date_format='iso', orient='split'), bahis_geodata.to_json(date_format='iso', orient='split')


@app.callback(
    Output("sidemenu", "is_open"),
    Input("open-sidemenu", "n_clicks"),
    [State("sidemenu", "is_open")],
)
def display_valueNtoggle_offcanvas(n1, is_open):

    if n1:
        return not is_open,
    return is_open


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
    #    Output("cache_bahis_data", "data"),
    #    Output("cache_bahis_geodata", "data"),
    #    Output('page-content', 'children'),

    Input("Division", "value"),
    Input("District", "value"),
    Input("Upazila", "value"),
    Input("Division", "options"),
    Input("District", "options"),
    Input("Upazila", "options"),
    Input("geoSlider", "value"),
    Input("DateRange", "value"),
    Input("Disease", "value"),
    # Input("cache_bahis_geodata", "data"),
    State("url", "pathname"),
    # prevent_initial_call=True,
)
def Framework(SelectedDivision, SelectedDistrict, SelectedUpazila, DivisionList, DistrictList, UpazilaList,
              geoSlider, DateRange, SelectedDisease, urlid):

    if urlid.rsplit("/", 1)[-1].isnumeric():
        urlid = "/" + urlid.rsplit("/", 1)[-1]
    else:
        urlid = "/" 
    # navbar.Navbar(urlid),
    
    # geoNameNNumber = pd.read_json(geodata, orient="split")
    # geoResolution = "upazila"
    # shapePath = "exported_data/processed_geodata/upadata.geojson"
    # change to relative path names later further 3 instances

    geoNameNNumber = bahis_geodata

    # against node is null error
    if DistrictList is None:
        DistrictList = []
    if UpazilaList is None:
        UpazilaList = []

    List = fetchdata.fetchDivisionlist(bahis_geodata)
    DivisionList = [{"label": i["Division"], "value": i["value"]} for i in List]

    if urlid !=  "/":
        SelectedDivision = int(urlid[1:3])
        List = fetchdata.fetchDistrictlist(SelectedDivision, geoNameNNumber)
        DistrictList = [{"label": i["District"], "value": i["value"]} for i in List]
        if len(str(urlid)) - 1 == 4:
            SelectedDistrict = int(urlid[1:5])
            List = fetchdata.fetchUpazilalist(SelectedDistrict, geoNameNNumber)
            UpazilaList = [{"label": i["Upazila"], "value": i["value"]} for i in List]

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
        if urlid != "/":
            SelectedDivision = int(urlid[1:3])
            List = fetchdata.fetchDistrictlist(SelectedDivision, geoNameNNumber)
            DistrictList = [{"label": i["District"], "value": i["value"]} for i in List]
            SelectedDistrict = None
            if len(str(urlid)) - 1 == 4:
                SelectedDistrict = int(urlid[1:5])
                List = fetchdata.fetchUpazilalist(SelectedDistrict, geoNameNNumber)
                UpazilaList = [{"label": i["Upazila"], "value": i["value"]} for i in List]
            else:
                UpazilaList = []
        else:
            if not SelectedDivision:
                DistrictList = []
                SelectedDistrict = None
            else:
                List = fetchdata.fetchDistrictlist(SelectedDivision, geoNameNNumber)
                DistrictList = [{"label": i["District"], "value": i["value"]} for i in List]
            UpazilaList = []
        SelectedUpazila = None

    if ctx.triggered_id == "District":
        if len(str(urlid)) - 1 == 4:
            SelectedDistrict = int(urlid[1:5])
            List = fetchdata.fetchUpazilalist(SelectedDistrict, geoNameNNumber)
            UpazilaList = [{"label": i["Upazila"], "value": i["value"]} for i in List]
        else:
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

    DiseaseList = fetchdata.fetchDiseaselist(bahis_data)

    page_settings = {
        "division": SelectedDivision,
        "district": SelectedDistrict,
        "upazila": SelectedUpazila,
        "georesolution": geoSlider,
        "disease": SelectedDisease,
        "daterange": DateRange,
    }

    return DivisionList, DistrictList, UpazilaList, SelectedDivision, SelectedDistrict, SelectedUpazila, geoSlider, \
        DiseaseList, json.dumps(page_settings)


@app.callback(
    Output("cache_page_data", "data"),
    Output("cache_page_geodata", "data"),
    Input("cache_page_settings", "data"),
)
def UpdatePageData(settings):

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
            geodata = geodata.loc[geodata["value"].astype(str).str[:4].astype(int) == json.loads(settings)["district"]]
        else:
            if type(json.loads(settings)["division"]) == int:
                reportsdata = reportsdata.loc[reportsdata["division"] == json.loads(settings)["division"]]
                geodata = geodata.loc[geodata["value"].astype(str).str[:2].astype(int) == json.loads(settings)
                                      ["division"]]
            else:
                reportsdata = reportsdata
                geodata = geodata

    page_data = reportsdata
    page_geodata = geodata
    return page_data.to_json(date_format='iso', orient='split'), page_geodata.to_json(date_format='iso', orient='split')


@app.callback(
    Output("Map", "figure", allow_duplicate=True),
    Output("dummy", "id", allow_duplicate=True),
    # Output("url", "pathname"),
    # Output('page-content', 'children'),
    Input("cache_page_data", "data"),
    Input("cache_page_geodata", "data"),
    Input("cache_page_settings", "data"),
    Input("dummy", "id"),
    # Input('page-content', 'children'),
    # State("url", "pathname"),
)
def UpdateFigs(data, geodata, settings, dummy):
    MapFig = MapNResolution.plotMap(json.loads(settings)["georesolution"],
                                    pd.read_json(data, orient="split"), pd.read_json(geodata, orient="split"))
    return MapFig, dummy


# Run the app on localhost:80
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)  # maybe debug false to prevent second loading
else:
    server = app.server

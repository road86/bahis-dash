import dash
from components import fetchdata, RegionSelect, MapNResolution
from dash import html, dcc, callback, ctx
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd


dash.register_page(__name__,)  # register page to main dash app

layout = html.Div([
    # dcc.Store(id="cache_bahis_data", storage_type="memory"),
    # dcc.Store(id="cache_bahis_dgdata", storage_type="memory"),
    # dcc.Store(id="cache_bahis_distypes", storage_type="memory"),
    dcc.Store(id="cache_bahis_geodata"),
    dbc.Row(
        [
            dbc.Col(
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
        ]
    )
]),

@callback(
    Output("District", "options"),
    Output("Upazila", "options"),
    Output("Map", "figure"),
    Input("Division", "value"),
    Input("District", "value"),
    Input("Upazila", "value"),
    Input("District", "options"),
    Input("Upazila", "options"),
    Input("geoSlider", "value"),
    Input("cache_bahis_data", "data"),
    Input("cache_bahis_geodata", "data"),
    prevent_initial_call=True
)

def RegionSelect(SelectedDivision, SelectedDistrict, SelectedUpazila, DistrictList, UpazilaList, geoSlider, sourcedata, geodata):
    bahis_geodata=pd.read_json(geodata, orient="split")
    if DistrictList == None: DistrictList = []
    if UpazilaList == None: UpazilaList = []

    if ctx.triggered_id == "Division":
        if not SelectedDivision:
#            subDist = bahis_geodata
            DistrictList = []
            UpazilaList = []
        else:
#            subDist = bahis_geodata.loc[bahis_geodata["parent"].astype("string").str.startswith(str(SelectedDivision))]
            List = fetchdata.fetchDistrictlist(SelectedDivision, bahis_geodata)
            DistrictList = [{"label": i["District"], "value": i["value"]} for i in List]
            UpazilaList = []
#            sub_bahis_sourcedata = bahis_data.loc[bahis_data["division"] == SelectedDivision]  # DivNo]

    if ctx.triggered_id == "District":
        if not SelectedDistrict:
#            subDist = bahis_geodata.loc[bahis_geodata["parent"].astype("string").str.startswith(str(SelectedDivision))]
            UpazilaList = []
#            sub_bahis_sourcedata = bahis_data.loc[bahis_data["division"] == SelectedDivision]  # DivNo]
        else:
#            subDist = bahis_geodata.loc[bahis_geodata["parent"].astype("string").str.startswith(str(SelectedDistrict))]
            List = fetchdata.fetchUpazilalist(SelectedDistrict, bahis_geodata)
            UpazilaList = [{"label": i["Upazila"], "value": i["value"]} for i in List]
#            sub_bahis_sourcedata = bahis_data.loc[bahis_data["district"] == SelectedDistrict]  # DivNo]

    if ctx.triggered_id == "Upazila":
        if not SelectedUpazila:
            print("a")
#            subDist = bahis_geodata.loc[bahis_geodata["parent"].astype("string").str.startswith(str(SelectedDistrict))]
#            sub_bahis_sourcedata = bahis_data.loc[bahis_data["district"] == SelectedDistrict]  # DivNo]
        else:
            print("b")
#            subDist = bahis_geodata.loc[bahis_geodata["value"].astype("string").str.startswith(str(SelectedUpazila ))]
#            sub_bahis_sourcedata = bahis_data.loc[bahis_data["upazila"] == SelectedUpazila ]

    if geoSlider == 1:
        geoResolution = "division"
        reportsdata = pd.read_json(sourcedata, orient="split")
        geoNameNNumber = pd.read_json(geodata, orient="split")
        shapePath = "exported_data/processed_geodata/divdata.geojson"
        Mapfig = MapNResolution.plotMap(geoResolution, geoSlider, reportsdata, geoNameNNumber, shapePath)

    if geoSlider == 2:
        geoResolution = "district"
        reportsdata = pd.read_json(sourcedata, orient="split")
        geoNameNNumber = pd.read_json(geodata, orient="split")
        shapePath = "exported_data/processed_geodata/distdata.geojson"
        Mapfig = MapNResolution.plotMap(geoResolution, geoSlider, reportsdata, geoNameNNumber, shapePath)

    if geoSlider == 3:
        geoResolution = "upazila"
        reportsdata = pd.read_json(sourcedata, orient="split")
        geoNameNNumber = pd.read_json(geodata, orient="split")
        shapePath = "exported_data/processed_geodata/upadata.geojson"
        Mapfig = MapNResolution.plotMap(geoResolution, geoSlider, reportsdata, geoNameNNumber, shapePath)

    # if ctx.triggered_id == 'geoSlider':
    #     Rfindic, Rfigg, NRlabel, AlertTable = GeoRep.GeoRep(sub_bahis_sourcedata, title,
    #                                                         subDistM, pnumber, pname, variab, labl)

    # Rfig = plot_map(path, subDistM, sub_bahis_sourcedata, title, pnumber, pname, variab, labl)

    return DistrictList, UpazilaList, Mapfig
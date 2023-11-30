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
    # dcc.Store(id="cache_bahis_geodata"),
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

    reportsdata = pd.read_json(sourcedata, orient="split")
    geoNameNNumber = pd.read_json(geodata, orient="split")
    if DistrictList is None: 
        DistrictList = []
    if UpazilaList is None: 
        UpazilaList = []

    if ctx.triggered_id == "Division":
        if not SelectedDivision:
            DistrictList = []
            UpazilaList = []
        else:
            reportsdata = reportsdata.loc[reportsdata["division"] == SelectedDivision]
            geoNameNNumber = geoNameNNumber.loc[geoNameNNumber["parent"].astype("string").str.startswith(str(SelectedDivision))]
            List = fetchdata.fetchDistrictlist(SelectedDivision, geoNameNNumber)
            DistrictList = [{"label": i["District"], "value": i["value"]} for i in List]
            UpazilaList = []

    if ctx.triggered_id == "District":
        if not SelectedDistrict:
            reportsdata = reportsdata.loc[reportsdata["division"] == SelectedDivision]
            geoNameNNumber = geoNameNNumber.loc[geoNameNNumber["parent"].astype("string").str.startswith(str(SelectedDivision))]
            UpazilaList = []
        else:
            reportsdata = reportsdata.loc[reportsdata["district"] == SelectedDistrict]
            geoNameNNumber = geoNameNNumber.loc[geoNameNNumber["parent"].astype("string").str.startswith(str(SelectedDistrict))]
            List = fetchdata.fetchUpazilalist(SelectedDistrict, geoNameNNumber)
            UpazilaList = [{"label": i["Upazila"], "value": i["value"]} for i in List]

    if ctx.triggered_id == "Upazila":
        if not SelectedUpazila:
            reportsdata = reportsdata.loc[reportsdata["district"] == SelectedDistrict]
            geoNameNNumber = geoNameNNumber.loc[geoNameNNumber["parent"].astype("string").str.startswith(str(SelectedDistrict))]
        else:
            reportsdata = reportsdata.loc[reportsdata["upazila"] == SelectedUpazila]  
            geoNameNNumber = geoNameNNumber.loc[geoNameNNumber["parent"].astype("string").str.startswith(str(SelectedUpazila))]

    if geoSlider == 1:
        geoResolution = "division"
        shapePath = "exported_data/processed_geodata/divdata.geojson"
    
    if geoSlider == 2:
        geoResolution = "district"
        shapePath = "exported_data/processed_geodata/distdata.geojson"
    
    if geoSlider == 3:
        geoResolution = "upazila"
        shapePath = "exported_data/processed_geodata/upadata.geojson"
    
    Mapfig = MapNResolution.plotMap(geoResolution, geoSlider, reportsdata, geoNameNNumber, shapePath)

    # if ctx.triggered_id == 'geoSlider':
    #     Rfindic, Rfigg, NRlabel, AlertTable = GeoRep.GeoRep(sub_bahis_sourcedata, title,
    #                                                         subDistM, pnumber, pname, variab, labl)

    # Rfig = plot_map(path, subDistM, sub_bahis_sourcedata, title, pnumber, pname, variab, labl)

    return DistrictList, UpazilaList, Mapfig
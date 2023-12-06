import dash
from components import fetchdata, RegionSelect, MapNResolution, DateRangeSelect, DiseaseSelect, CompletenessReport
from dash import html, dcc, callback, ctx
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd


dash.register_page(__name__,)  # register page to main dash app

layout = html.Div([
    # dcc.Store(id="cache_bahis_data", storage_type="memory"),
    # dcc.Store(id="cache_bahis_dgdata", storage_type="memory"),
    # dcc.Store(id="cache_bahis_distypes", storage_type="memory"),
    # dcc.Store(id="cache_bahis_geodata"),
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
                        [
                            dbc.Tab(
                                [
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.Label("Weekly Completeness"),
                                                dbc.Col(
                                                    [
                                                        dcc.Graph(id="Completeness")
                                                    ]
                                                )
                                            ]
                                        )
                                    )
                                ],
                                label="Completeness",
                                tab_id="CompletenessTab",
                            ),
                        ]
                    ),
                ),
            ])
        ]
    )
]),


@callback(
    Output("District", "options"),
    Output("Upazila", "options"),
    Output("Map", "figure"),
    Output("Completeness", "figure"),
    Input("Division", "value"),
    Input("District", "value"),
    Input("Upazila", "value"),
    Input("District", "options"),
    Input("Upazila", "options"),
    Input("geoSlider", "value"),
    Input("DateRange", "value"),
    Input("Disease", "value"),
    State("cache_bahis_data", "data"),
    State("cache_bahis_geodata", "data"),
    prevent_initial_call=True
)

def RegionSelect(SelectedDivision, SelectedDistrict, SelectedUpazila, DistrictList, UpazilaList, geoSlider, DateRange, SelectedDisease, sourcedata, geodata):

    reportsdata = pd.read_json(sourcedata, orient="split")
    geoNameNNumber = pd.read_json(geodata, orient="split")
    geoResolution = "upazila"
    shapePath = "exported_data/processed_geodata/upadata.geojson"       # change to relative path names later further 3 instances
    print(DateRange)
    print(SelectedDisease)

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
    
    MapFig = MapNResolution.plotMap(geoResolution, geoSlider, reportsdata, geoNameNNumber, shapePath)

    # if ctx.triggered_id == 'geoSlider':
    #     Rfindic, Rfigg, NRlabel, AlertTable = GeoRep.GeoRep(sub_bahis_sourcedata, title,
    #                                                         subDistM, pnumber, pname, variab, labl)

    # Rfig = plot_map(path, subDistM, sub_bahis_sourcedata, title, pnumber, pname, variab, labl)

    start = "2022-12-1 0:0:0"
    end = "2023-1-1 0:0:0" # date(2023, 1, 1)  #max(bahis_data['date']).date()
    diseaselist = "All Diseases"
    reset = False
    
    CompletenessFig = CompletenessReport.generate_reports_heatmap(reportsdata,
        geoNameNNumber, start, end, SelectedDivision, SelectedDistrict, diseaselist, reset)
    
    return DistrictList, UpazilaList, MapFig, CompletenessFig
import dash
from components import fetchdata, RegionSelect, MapNResolution, DateRangeSelect, DiseaseSelect, CompletenessReport
from dash import html, dcc, callback, ctx
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd


dash.register_page(__name__,)  # register page to main dash app

layout = [ # html.Div([
    dcc.Store(id="cache_bahis_data", storage_type="memory"),
    # dcc.Store(id="cache_bahis_dgdata", storage_type="memory"),
    # dcc.Store(id="cache_bahis_distypes", storage_type="memory"),
    dcc.Store(id="cache_bahis_geodata"),
    dcc.Store(id="cache_page_settings"),
#     dbc.Row(
#         [
#             dbc.Col(            # left side
#                 [
#                     dbc.Card(
#                         dbc.CardBody(RegionSelect.Form),
#                     ),
#                     dbc.Card(
#                         dbc.CardBody(MapNResolution.Form)
#                     )
#                 ],
#                 width=4,
#             ),
#             dbc.Col([          # right side
#                 dbc.Card(
#                     dbc.CardBody(
#                         [
#                             dbc.Row(
#                                 [
#                                     dbc.Col(
#                                         DateRangeSelect.Form
#                                     ),
#                                     dbc.Col(
#                                         DiseaseSelect.Form
#                                     )
#                                 ]
#                             )
#                         ]
#                     )
#                 ),
#                 dbc.Card(
#                     dbc.CardBody(
#                         [dbc.Card(
#                             dbc.CardBody(
#    [
        html.Label("Weekly Completeness"),
        dbc.Col(
            [
                dcc.Graph(id="Completeness")
            ]
        )
#    ]
#                             )
#                         )]
#                     ),
#                 ),
#             ])
#         ]
#     )
# ]),
]


@callback(
    # Output("District", "options", allow_duplicate=True),
    # Output("Upazila", "options", allow_duplicate=True),
    # Output("Map", "figure", allow_duplicate=True),
    Output("Completeness", "figure"),
    # Input("Division", "value"),
    # Input("District", "value"),
    # Input("Upazila", "value"),
    # Input("District", "options"),
    # Input("Upazila", "options"),
    # Input("geoSlider", "value"),
    # Input("DateRange", "value"),
    # Input("Disease", "value"),
    State("Completeness", "figure"),
    State("cache_bahis_data", "data"),
    State("cache_bahis_geodata", "data"),
    State("cache_page_settings", "data"),
    prevent_initial_call=True
)

def Completeness(CompletenessFig, sourcedata, geodata, settings): # SelectedDivision, SelectedDistrict, SelectedUpazila, DistrictList, UpazilaList, geoSlider, DateRange, SelectedDisease, CompletenessFig, sourcedata, geodata):

    reportsdata = pd.read_json(sourcedata, orient="split")
    geoNameNNumber = pd.read_json(geodata, orient="split")
    # geoResolution = "upazila"
    # shapePath = "exported_data/processed_geodata/upadata.geojson"       # change to relative path names later further 3 instances

    # reportsdata = fetchdata.date_subset(DateRange, reportsdata)
    # reportsdata = fetchdata.disease_subset(SelectedDisease, reportsdata)

    # if DistrictList is None: 
    #     DistrictList = []
    # if UpazilaList is None: 
    #     UpazilaList = []

    # if ctx.triggered_id == "Division":
    #     if not SelectedDivision:
    #         DistrictList = []
    #         UpazilaList = []
    #     else:
    #         reportsdata = reportsdata.loc[reportsdata["division"] == SelectedDivision]
    #         geoNameNNumber = geoNameNNumber.loc[geoNameNNumber["parent"].astype("string").str.startswith(str(SelectedDivision))]
    #         List = fetchdata.fetchDistrictlist(SelectedDivision, geoNameNNumber)
    #         DistrictList = [{"label": i["District"], "value": i["value"]} for i in List]
    #         UpazilaList = []
    
    # if ctx.triggered_id == "District":
    #     if not SelectedDistrict:
    #         reportsdata = reportsdata.loc[reportsdata["division"] == SelectedDivision]
    #         geoNameNNumber = geoNameNNumber.loc[geoNameNNumber["parent"].astype("string").str.startswith(str(SelectedDivision))]
    #         UpazilaList = []
    #     else:
    #         reportsdata = reportsdata.loc[reportsdata["district"] == SelectedDistrict]
    #         geoNameNNumber = geoNameNNumber.loc[geoNameNNumber["parent"].astype("string").str.startswith(str(SelectedDistrict))]
    #         List = fetchdata.fetchUpazilalist(SelectedDistrict, geoNameNNumber)
    #         UpazilaList = [{"label": i["Upazila"], "value": i["value"]} for i in List]

    # if ctx.triggered_id == "Upazila":
    #     if not SelectedUpazila:
    #         reportsdata = reportsdata.loc[reportsdata["district"] == SelectedDistrict]
    #         geoNameNNumber = geoNameNNumber.loc[geoNameNNumber["parent"].astype("string").str.startswith(str(SelectedDistrict))]
    #     else:
    #         reportsdata = reportsdata.loc[reportsdata["upazila"] == SelectedUpazila]  
    #         geoNameNNumber = geoNameNNumber.loc[geoNameNNumber["value"] == SelectedUpazila]     # check if valid for other "tabs"

    # if geoSlider == 1:
    #     geoResolution = "division"
    #     shapePath = "exported_data/processed_geodata/divdata.geojson"           # keep in mind to adjust
    
    # if geoSlider == 2:
    #     geoResolution = "district"
    #     shapePath = "exported_data/processed_geodata/distdata.geojson"
    
    # if geoSlider == 3:
    #     geoResolution = "upazila"
    #     shapePath = "exported_data/processed_geodata/upadata.geojson"
    
    # # if UpazilaList =  []
    # MapFig = MapNResolution.plotMap(geoResolution, geoSlider, reportsdata, geoNameNNumber, shapePath)

    # if ctx.triggered_id == 'geoSlider':
    #     Rfindic, Rfigg, NRlabel, AlertTable = GeoRep.GeoRep(sub_bahis_sourcedata, title,
    #                                                         subDistM, pnumber, pname, variab, labl)

    # Rfig = plot_map(path, subDistM, sub_bahis_sourcedata, title, pnumber, pname, variab, labl)
    print(settings)
    if SelectedUpazila==None:
        CompletenessFig = CompletenessReport.generate_reports_heatmap(reportsdata,
            geoNameNNumber, DateRange[0], DateRange[1], SelectedDivision, SelectedDistrict)
    else:
        CompletenessFig = CompletenessFig
    
    return CompletenessFig # DistrictList, UpazilaList, MapFig, CompletenessFig
# import dash
# from components import fetchdata, RegionSelect, MapNResolution, DateRangeSelect, DiseaseSelect, ReportsSickDead
# from dash import html, dcc, callback, ctx
# import dash_bootstrap_components as dbc
# from dash.dependencies import Input, Output
# import pandas as pd


# dash.register_page(__name__,)  # register page to main dash app

# layout = html.Div([
#     dbc.Row(
#         [
#             dbc.Col(
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
#                         [
#                             dbc.Row(
#                                 [
#                                     dbc.Col(
#                                         [
#                                             dbc.Row(dcc.Graph(id="ReportsLA")),
#                                             dbc.Row(dcc.Graph(id="SickLA")),
#                                             dbc.Row(dcc.Graph(id="DeadLA")),
#                                         ]
#                                     ),
#                                     dbc.Col(
#                                         [
#                                             dcc.Slider(
#                                                 min=1,
#                                                 max=3,
#                                                 step=1,
#                                                 marks={1: 'Reports monthly',
#                                                         2: 'Reports weekly',
#                                                         3: 'Reports daily',
#                                                         },
#                                                 value=2,
#                                                 vertical=True,
#                                                 id="LAperiodSlider"
#                                             )
#                                         ],
#                                         width=1,
#                                     ),
#                                 ]
#                             )
#                         ],
#                     )
#                 ),
#             ])
#         ]
#     )
# ]),


# @callback(
#     Output("District", "options", allow_duplicate=True),
#     Output("Upazila", "options", allow_duplicate=True),
#     Output("Map", "figure", allow_duplicate=True),
#     Output("ReportsLA", "figure"),
#     Output("SickLA", "figure"),
#     Output("DeadLA", "figure"),
#     Input("Division", "value"),
#     Input("District", "value"),
#     Input("Upazila", "value"),
#     Input("District", "options"),
#     Input("Upazila", "options"),
#     Input("geoSlider", "value"),
#     Input("DateRange", "value"),
#     Input("Disease", "value"),
#     Input("LAperiodSlider", "value"),    
#     Input("cache_bahis_data", "data"),
#     Input("cache_bahis_geodata", "data"),
#     prevent_initial_call=True
# )

# def LargeAnimal(SelectedDivision, SelectedDistrict, SelectedUpazila, DistrictList, UpazilaList, geoSlider, DateRange, SelectedDisease, LAperiodClick, sourcedata, geodata):

#     reportsdata = pd.read_json(sourcedata, orient="split")
#     geoNameNNumber = pd.read_json(geodata, orient="split")
#     geoResolution = "upazila"
#     shapePath = "exported_data/processed_geodata/upadata.geojson"   

#     reportsdata = fetchdata.date_subset(DateRange, reportsdata)
#     reportsdata = fetchdata.disease_subset(SelectedDisease, reportsdata)

#     if DistrictList is None: 
#         DistrictList = []
#     if UpazilaList is None: 
#         UpazilaList = []

#     if ctx.triggered_id == "Division":
#         if not SelectedDivision:
#             DistrictList = []
#             UpazilaList = []
#         else:
#             reportsdata = reportsdata.loc[reportsdata["division"] == SelectedDivision]
#             geoNameNNumber = geoNameNNumber.loc[geoNameNNumber["parent"].astype("string").str.startswith(str(SelectedDivision))]
#             List = fetchdata.fetchDistrictlist(SelectedDivision, geoNameNNumber)
#             DistrictList = [{"label": i["District"], "value": i["value"]} for i in List]
#             UpazilaList = []

#     if ctx.triggered_id == "District":
#         if not SelectedDistrict:
#             reportsdata = reportsdata.loc[reportsdata["division"] == SelectedDivision]
#             geoNameNNumber = geoNameNNumber.loc[geoNameNNumber["parent"].astype("string").str.startswith(str(SelectedDivision))]
#             UpazilaList = []
#         else:
#             reportsdata = reportsdata.loc[reportsdata["district"] == SelectedDistrict]
#             geoNameNNumber = geoNameNNumber.loc[geoNameNNumber["parent"].astype("string").str.startswith(str(SelectedDistrict))]
#             List = fetchdata.fetchUpazilalist(SelectedDistrict, geoNameNNumber)
#             UpazilaList = [{"label": i["Upazila"], "value": i["value"]} for i in List]
    
#     if ctx.triggered_id == "Upazila":
#         if not SelectedUpazila:
#             reportsdata = reportsdata.loc[reportsdata["district"] == SelectedDistrict]
#             geoNameNNumber = geoNameNNumber.loc[geoNameNNumber["parent"].astype("string").str.startswith(str(SelectedDistrict))]
#         else:
#             reportsdata = reportsdata.loc[reportsdata["upazila"] == SelectedUpazila]  
#             geoNameNNumber = geoNameNNumber.loc[geoNameNNumber["parent"].astype("string").str.startswith(str(SelectedUpazila))]

#     if geoSlider == 1:
#         geoResolution = "division"
#         shapePath = "exported_data/processed_geodata/divdata.geojson"
    
#     if geoSlider == 2:
#         geoResolution = "district"
#         shapePath = "exported_data/processed_geodata/distdata.geojson"
    
#     if geoSlider == 3:
#         geoResolution = "upazila"
#         shapePath = "exported_data/processed_geodata/upadata.geojson"
    
#     Mapfig = MapNResolution.plotMap(geoResolution, geoSlider, reportsdata, geoNameNNumber, shapePath)

#     LargeAnimal = ["Buffalo", "Cattle", "Goat", "Sheep"]
#     reportsdata = reportsdata[reportsdata["species"].isin(LargeAnimal)]
#     figheight = 175
#     figgLAR, figgLASick, figgLADead = ReportsSickDead.ReportsSickDead(reportsdata, DateRange, LAperiodClick, figheight)

#     return DistrictList, UpazilaList, Mapfig, figgLAR, figgLASick, figgLADead
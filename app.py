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

sourcepath = "exported_data/"
geofilename, dgfilename, sourcefilename, path1, path2, path3 = pathnames.get_pathnames(sourcepath)
bahis_data = fetchdata.fetchsourcedata(sourcefilename)
[bahis_dgdata, bahis_distypes] = fetchdata.fetchdisgroupdata(dgfilename)
bahis_geodata = fetchdata.fetchgeodata(geofilename)

create_date = fetchdata.create_date(sourcefilename)  # implement here

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar.Navbar(),
#        html.Div(id="page-1-display-value"),
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
                                dbc.CardBody(
                                    dash.page_container,
                                )
                            )]
                        ),
                    ),
                ])
            ]
        ),
        
        html.Br(),
        html.Div(id="dummy"),
        html.Label('Data from ' + str(create_date), style={'text-align': 'right'}),
#        dcc.Store(id="cache_bahis_data", storage_type="memory"),
#        dcc.Store(data=bahis_dgdata.to_json(date_format='iso', orient='split'), id="cache_bahis_dgdata", storage_type="memory"),
#        dcc.Store(data=bahis_distypes.to_json(date_format='iso', orient='split'), id="cache_bahis_distypes", storage_type="memory"),
#        dcc.Store(id="cache_bahis_geodata", storage_type="memory"),
        dcc.Store(id="cache_page_settings", storage_type="memory"),
        dcc.Store(id="cache_page_data", storage_type="memory"),
    ]
)


# @app.callback(
#     Output("cache_bahis_data", "data"),
#     Output("cache_bahis_distypes", "data"),
#     Output("cache_bahis_geodata", "data"),
#     Input("dummy", "id")
# )

# def store2cache(dummy):
#     return bahis_data.to_json(date_format='iso', orient='split'), bahis_distypes.to_json(date_format='iso', orient='split'), bahis_geodata.to_json(date_format='iso', orient='split')


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
    Output("Division", "options"), 
    Output("District", "options"),  
    Output("Upazila", "options"), 
#    Output("Map", "figure"),  
    Output("Disease", "options"),  
    Output("cache_page_settings", "data"),    
    Output("cache_page_data", "data"),    
   
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
    # Input("cache_bahis_data", "data"),
    # Input("cache_bahis_geodata", "data"),
)

def Framework(SelectedDivision, SelectedDistrict, SelectedUpazila, DivisionList, DistrictList, UpazilaList, geoSlider, DateRange, SelectedDisease):  # , sourcedata, geodata): 

    # reportsdata = pd.read_json(sourcedata, orient="split")
    # geoNameNNumber = pd.read_json(geodata, orient="split")
    reportsdata = bahis_data
    geoNameNNumber = bahis_geodata

    # geoResolution = "upazila"
    # shapePath = "exported_data/processed_geodata/upadata.geojson"       # change to relative path names later further 3 instances
    
    reportsdata = fetchdata.date_subset(DateRange, reportsdata)
    reportsdata = fetchdata.disease_subset(SelectedDisease, reportsdata)

    if SelectedDivision is None:
        List = fetchdata.fetchDivisionlist(bahis_geodata)
#        List = fetchdata.fetchDivisionlist(pd.read_json(geodata, orient="split"))
        DivisionList = [{"label": i["Division"], "value": i["value"]} for i in List]     
    DivisionList = DivisionList

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
            geoNameNNumber = geoNameNNumber.loc[geoNameNNumber["value"] == SelectedUpazila]     # check if valid for other "tabs"
   
    if SelectedUpazila != None:
        UpazilaEntry = SelectedUpazila
    else:
        UpazilaEntry= UpazilaList
        if SelectedDistrict != None:
            DistrictEntry = SelectedDistrict
        else:
            DistrictEntry = DistrictList
            if SelectedDivision != None:
                DivisionEntry = SelectedDivision
            else:
                DivisionEntry = DivisionList

    DiseaseList = fetchdata.fetchDiseaselist(bahis_data)

    page_settings = {  
        "division": DivisionEntry,
        "district": DistrictEntry,
        "upazila": UpazilaEntry,
        "georesolution": geoSlider,
        "disease": SelectedDisease,
        "daterange": DateRange,
    }
    
    page_data= reportsdata

    return DivisionList, DistrictList, UpazilaList, DiseaseList, json.dumps(page_settings), page_data.to_json(date_format='iso', orient='split')

@app.callback(
    Output("Map", "figure"),  
#    Output('page-content', 'children'),
    Input("geoSlider", "value"),
#    Input("cache_page_settings", "data"),    
    Input("cache_page_data", "data"),    
)

def UpdateFigs(geoSlider, data):  # settings, data): 
    #print(json.loads(settings)["georesolution"])

    if geoSlider == 1:
        geoResolution = "division"
        shapePath = "exported_data/processed_geodata/divdata.geojson"           # keep in mind to adjust
    
    if geoSlider == 2:
        geoResolution = "district"
        shapePath = "exported_data/processed_geodata/distdata.geojson"
    
    if geoSlider == 3:
        geoResolution = "upazila"
        shapePath = "exported_data/processed_geodata/upadata.geojson"

    MapFig = MapNResolution.plotMap(geoResolution, geoSlider, pd.read_json(data, orient="split"), bahis_geodata, shapePath)
    return MapFig

    

# Run the app on localhost:80
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)  # maybe debug false to prevent second loading
else:
    server = app.server

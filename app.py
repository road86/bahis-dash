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
    Output("District", "value"),  
    Output("Upazila", "value"),  
    Output("Disease", "options"),  
    Output("cache_page_settings", "data"),    
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

def Framework(SelectedDivision, SelectedDistrict, SelectedUpazila, DivisionList, DistrictList, UpazilaList, geoSlider, DateRange, SelectedDisease):  

    # geoNameNNumber = pd.read_json(geodata, orient="split")
    # geoResolution = "upazila"
    # shapePath = "exported_data/processed_geodata/upadata.geojson"       # change to relative path names later further 3 instances

    geoNameNNumber = bahis_geodata

    if SelectedDivision is None:
        List = fetchdata.fetchDivisionlist(bahis_geodata)
        DivisionList = [{"label": i["Division"], "value": i["value"]} for i in List]     
        DivisionEntry = DivisionList
    DivisionList = DivisionList

    if DistrictList is None: 
        DistrictList = []
    DistrictEntry = []

    if UpazilaList is None: 
        UpazilaList = []
    UpazilaEntry = []
    S = ""    
    U = ""

    if ctx.triggered_id == "Division":
        if not SelectedDivision:
            DivisionEntry = DivisionList
            DistrictList = []
            DistrictEntry = DistrictList
            UpazilaList = []
            UpazilaEntry = UpazilaList
        else:
            DivisionEntry = SelectedDivision
            List = fetchdata.fetchDistrictlist(SelectedDivision, geoNameNNumber)
            DistrictList = [{"label": i["District"], "value": i["value"]} for i in List]
            DistrictEntry = DistrictList
            UpazilaList = []
            UpazilaEntry = UpazilaList

    if ctx.triggered_id == "District":
        DivisionEntry = SelectedDivision
        if not SelectedDistrict:
            DistrictEntry = DistrictList
            UpazilaList = []
            UpazilaEntry = UpazilaList
        else:
            DistrictEntry = SelectedDistrict
            List = fetchdata.fetchUpazilalist(SelectedDistrict, geoNameNNumber)
            UpazilaList = [{"label": i["Upazila"], "value": i["value"]} for i in List]
            UpazilaEntry = UpazilaList
            S = SelectedDistrict

    if ctx.triggered_id == "Upazila":
        DivisionEntry = SelectedDivision
        DistrictEntry = SelectedDistrict
        S = SelectedDistrict
        if not SelectedUpazila:
            UpazilaEntry = UpazilaList
        else:
            UpazilaEntry = SelectedUpazila
            U = SelectedUpazila

    DiseaseList = fetchdata.fetchDiseaselist(bahis_data)

    page_settings = {  
        "division": DivisionEntry,
        "district": DistrictEntry,
        "upazila": UpazilaEntry,
        "georesolution": geoSlider,
        "disease": SelectedDisease,
        "daterange": DateRange,
    }

    return DivisionList, DistrictList, UpazilaList, S, U, DiseaseList, json.dumps(page_settings) #, page_data.to_json(date_format='iso', orient='split')

@app.callback(
    Output("cache_page_data", "data"),    
    Input("cache_page_settings", "data"),    
)

def UpdatePageData(settings):  

    reportsdata = bahis_data
    reportsdata = fetchdata.date_subset(json.loads(settings)["daterange"], reportsdata)
    reportsdata = fetchdata.disease_subset(json.loads(settings)["disease"], reportsdata)

    if type(json.loads(settings)["upazila"]) ==int:
        reportsdata = reportsdata.loc[reportsdata["upazila"] == json.loads(settings)["upazila"]]  
    else:        
        if type(json.loads(settings)["district"]) ==int:
            reportsdata = reportsdata.loc[reportsdata["district"] == json.loads(settings)["district"]]  
        else:
            if type(json.loads(settings)["division"]) ==int:
                reportsdata = reportsdata.loc[reportsdata["division"] == json.loads(settings)["division"]]  
            else:
                reportsdata = reportsdata

    page_data= reportsdata 
    return page_data.to_json(date_format='iso', orient='split')


@app.callback(
    Output("Map", "figure"),  
#    Output('page-content', 'children'),
    Input("geoSlider", "value"), 
    Input("cache_page_data", "data"),    
)

def UpdateFigs(geoSlider, data): 

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

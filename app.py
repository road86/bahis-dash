# create overall page
# store data in cache
# general layout: navbar and "body"

import dash
import dash_bootstrap_components as dbc
from components import navbar, pathnames, fetchdata
from dash import Dash, Input, Output, dcc, html, State

from components import fetchdata, RegionSelect, MapNResolution, DateRangeSelect, DiseaseSelect # , CompletenessReport
import pandas as pd


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
                                    # [
                                    dash.page_container,
                                    # [
                                    #     html.Label("Weekly Completeness"),
                                    #     dbc.Col(
                                    #         [
                                    #             dcc.Graph(id="Completeness")
                                    #         ]
                                    #     )
                                    # ]
                                )
                            )]
                        ),
                    ),
                ])
            ]
        ),
        
#        dash.page_container,
        html.Br(),
        html.Div(id="dummy"),
        html.Label('Data from ' + str(create_date), style={'text-align': 'right'}),
        dcc.Store(id="cache_bahis_data", storage_type="memory"),
        dcc.Store(data=bahis_dgdata.to_json(date_format='iso', orient='split'), id="cache_bahis_dgdata", storage_type="memory"),
        dcc.Store(data=bahis_distypes.to_json(date_format='iso', orient='split'), id="cache_bahis_distypes", storage_type="memory"),
        dcc.Store(id="cache_bahis_geodata", storage_type="memory"),
        dcc.Store(id="cache_page_settings", storage_type="memory"),
    ]
)


@app.callback(
    Output("cache_bahis_data", "data"),
    Output("cache_bahis_distypes", "data"),
    Output("cache_bahis_geodata", "data"),
    Input("dummy", "id")
)

def store2cache(dummy):
    return bahis_data.to_json(date_format='iso', orient='split'), bahis_distypes.to_json(date_format='iso', orient='split'), bahis_geodata.to_json(date_format='iso', orient='split')


@app.callback(
    Output("sidemenu", "is_open"),
    Input("open-sidemenu", "n_clicks"),
    [State("sidemenu", "is_open")],
)
def display_valueNtoggle_offcanvas(n1, is_open):

    if n1:
        return not is_open, 
    return is_open


# Run the app on localhost:80
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
else:
    server = app.server


@app.callback(
    Output("District", "options", allow_duplicate=True),
    Output("Upazila", "options", allow_duplicate=True),
    Output("Map", "figure", allow_duplicate=True),
    Output("cache_page_settings", "data"),    
#    Output("Completeness", "figure"),
    Input("Division", "value"),
    Input("District", "value"),
    Input("Upazila", "value"),
    Input("District", "options"),
    Input("Upazila", "options"),
    Input("geoSlider", "value"),
    Input("DateRange", "value"),
    Input("Disease", "value"),
#    State("Completeness", "figure"),
    State("cache_bahis_data", "data"),
    State("cache_bahis_geodata", "data"),
    State("cache_bahis_geodata", "data"),
    prevent_initial_call=True
)

def Framework(SelectedDivision, SelectedDistrict, SelectedUpazila, DistrictList, UpazilaList, geoSlider, DateRange, SelectedDisease, sourcedata, geodata): # CompletenessFig, sourcedata, geodata):

    reportsdata = pd.read_json(sourcedata, orient="split")
    geoNameNNumber = pd.read_json(geodata, orient="split")
    geoResolution = "upazila"
    shapePath = "exported_data/processed_geodata/upadata.geojson"       # change to relative path names later further 3 instances

    reportsdata = fetchdata.date_subset(DateRange, reportsdata)
    reportsdata = fetchdata.disease_subset(SelectedDisease, reportsdata)

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

    if geoSlider == 1:
        geoResolution = "division"
        shapePath = "exported_data/processed_geodata/divdata.geojson"           # keep in mind to adjust
    
    if geoSlider == 2:
        geoResolution = "district"
        shapePath = "exported_data/processed_geodata/distdata.geojson"
    
    if geoSlider == 3:
        geoResolution = "upazila"
        shapePath = "exported_data/processed_geodata/upadata.geojson"
    
    # if UpazilaList =  []
    MapFig = MapNResolution.plotMap(geoResolution, geoSlider, reportsdata, geoNameNNumber, shapePath)

    # if ctx.triggered_id == 'geoSlider':
    #     Rfindic, Rfigg, NRlabel, AlertTable = GeoRep.GeoRep(sub_bahis_sourcedata, title,
    #                                                         subDistM, pnumber, pname, variab, labl)

    # Rfig = plot_map(path, subDistM, sub_bahis_sourcedata, title, pnumber, pname, variab, labl)
    
    # if SelectedUpazila==None:
    #     CompletenessFig = CompletenessReport.generate_reports_heatmap(reportsdata,
    #         geoNameNNumber, DateRange[0], DateRange[1], SelectedDivision, SelectedDistrict)
    # else:
    #     CompletenessFig = CompletenessFig
    
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


    page_settings = {  
        "division": DivisionEntry,
        "district": DistrictEntry,
        "upazila": DistrictEntry,
        "disease": SelectedDisease,
        "daterange": DateRange
    }

    print(page_settings)

    return DistrictList, UpazilaList, MapFig, page_settings.to_json(date_format='iso', orient='split') # , CompletenessFig
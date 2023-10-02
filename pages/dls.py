import json
from datetime import date, datetime, timedelta

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import callback, ctx, dash_table, dcc, html
from dash.dash import no_update
from dash.dependencies import Input, Output
from components import yearly_comparison
from components import ReportsSickDead
from components import CompletenessReport
from components import pathnames
from components import fetchdata
from components import TopTen
from components import GeoRep


starttime_start = datetime.now()

pd.options.mode.chained_assignment = None

dash.register_page(__name__, path="/")
#dash.register_page(__name__)  # register page to main dash app

# #1 Nation # reminder: found shapefiles from the data.humdata.org
sourcepath = "exported_data/"
geofilename, dgfilename, sourcefilename, path1, path2, path3 = pathnames.get_pathnames(sourcepath)

firstrun = True

bahis_data = fetchdata.fetchsourcedata(sourcefilename)
sub_bahis_sourcedata = bahis_data

start_date = date(2019, 1, 1)
last_date = max(bahis_data['date']).date()
# last_date = date(2023, 12, 31)
dates = [start_date, last_date]

create_date = fetchdata.create_date(sourcefilename)

ddDList = []
Divlist = []
ddDistypes = []

bahis_dgdata, bahis_distypes = fetchdata.fetchdisgroupdata(dgfilename)
to_replace = bahis_dgdata["name"].tolist()
replace_with = bahis_dgdata["Disease type"].tolist()

bahis_geodata = fetchdata.fetchgeodata(geofilename)
subDist = bahis_geodata


ddDivision = html.Div(
    [
        dbc.Label("Division"),
        dcc.Dropdown(
            options=[{"label": i["Division"], "value": i["value"]} for i in Divlist],
            id="Division",
            clearable=True,
            placeholder="Select Division"
        ),
    ],
    className="mb-4",
)

ddDistrict = html.Div(
    [
        dbc.Label("District"),
        dcc.Dropdown(
            id="District",
            clearable=True,
            placeholder="Select District"
        ),
    ],
    className="mb-4",
)

ddUpazila = html.Div(
    [
        dbc.Label("Upazila"),
        dcc.Dropdown(
            id="Upazila",
            clearable=True,
            placeholder="Select Upazila"
        ),
    ],
    className="mb-4",
)

ddDiseaseType = html.Div(
    [
        dbc.Label("Select Disease Type"),
        dcc.Dropdown(
            id="Distypes",
            clearable=False,
        ),
    ],
    className="mb-4",
)


def open_data(path):
    with open(path) as f:
        data = json.load(f)
    return data


def plot_map(path, loc, subDistM, sub_bahis_sourcedata, title, pnumber, pname, splace, variab, labl):
    reports = sub_bahis_sourcedata[title].value_counts().to_frame()
    reports[pnumber] = reports.index  # 1
    reports.index = reports.index.astype(int)  # upazila name
    reports[pnumber] = reports[pnumber].astype(int)
    reports = reports.loc[
        reports[pnumber] != "nan"
    ]  # unknown reason for now. does this have to be beore reports in sub_bahis_sourcedata?
    # reports, where there are no geonumbers?
    data = open_data(path)  # 1
    reports[pname] = reports.index
    tmp = subDistM[["value", "name"]]
    tmp = tmp.rename(columns={"value": pnumber, "name": pname})
    tmp[pname] = tmp[pname].str.title()
    tmp["Index"] = tmp[pnumber]
    tmp = tmp.set_index("Index")
    tmp[title] = 0

    aaa = reports.combine_first(tmp)
    aaa[pname] = tmp[pname]
    del tmp
    del reports
    reports = aaa
    for i in range(reports.shape[0]):  # go through all upazila report values
        reports[pname].iloc[i] = subDistM[subDistM["value"] == reports.index[i]]["name"].values[
            0
        ]  # still to work with the copy , this goes with numbers and nnot names
    reports[pname] = reports[pname].str.title()
    reports.set_index(pnumber)  # 1

    custolor = [[0, "black"], [1 / reports[title].max(), "lightgray"], [1, "red"]]
    fig = px.choropleth_mapbox(
        reports,
        geojson=data,
        locations=pnumber,
        color=title,
        featureidkey="properties." + pnumber,
        color_continuous_scale=custolor,
        range_color=(1, reports[title].max()),
        mapbox_style="carto-positron",
        zoom=5.8,
        center={"lat": 23.7, "lon": 90.3},
        opacity=0.7,
        labels={variab: labl},
        hover_name=pname,
        hover_data={pname: False, pnumber: False}
    )
    fig.update_layout(
        autosize=True, coloraxis_showscale=True, margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=550
    )  # , width=760 , height=800, ) #, coloraxis_showscale= False) #width= 1000, height=600,
    return fig


layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                dbc.Row([dbc.Col(ddDivision), dbc.Col(ddDistrict), dbc.Col(ddUpazila)])
                            ),
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                [dcc.Graph(id="Map"),
                                    dcc.Slider(
                                        min=1,
                                        max=3,
                                        step=1,
                                        marks={
                                            1: "Division",
                                            2: "District",
                                            3: "Upazila",
                                        },
                                        value=3,
                                        id="geoSlider",
                                )
                                ]
                            )
                        )
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                dcc.DatePickerRange(
                                                    id="daterange",
                                                    min_date_allowed=start_date,
                                                    start_date=last_date - timedelta(weeks=6),  # date(2023, 1, 1),
                                                    max_date_allowed=create_date,
                                                    end_date=last_date,  # date(2023, 12, 31)
                                                ),
                                            ),
                                            dbc.Col(
                                                [
                                                    dcc.Dropdown(
                                                        ddDList,
                                                        "All Diseases",
                                                        id="Diseaselist",
                                                        multi=False,
                                                        clearable=False,
                                                    ),
                                                ],
                                            )
                                        ]
                                    )
                                ]
                            )
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    dbc.Tabs(
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
                                            dbc.Tab(
                                                [
                                                    dbc.Card(
                                                        dbc.CardBody(
                                                            [
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            [
                                                                                dbc.Row(dcc.Graph(id="ReportsLA")),
                                                                                dbc.Row(dcc.Graph(id="SickLA")),
                                                                                dbc.Row(dcc.Graph(id="DeadLA")),
                                                                            ]
                                                                        ),
                                                                        dbc.Col(
                                                                            [
                                                                                dcc.Slider(
                                                                                    min=1,
                                                                                    max=3,
                                                                                    step=1,
                                                                                    marks={1: 'Reports monthly',
                                                                                           2: 'Reports weekly',
                                                                                           3: 'Reports daily',
                                                                                           },
                                                                                    value=2,
                                                                                    vertical=True,
                                                                                    id="LAperiodSlider"
                                                                                )
                                                                            ],
                                                                            width=1,
                                                                        ),
                                                                    ]
                                                                )
                                                            ],
                                                        )
                                                    )
                                                ],
                                                label="Large Animal Reports",
                                                tab_id="ReportsLATab",
                                            ),
                                            dbc.Tab(
                                                [
                                                    dbc.Card(
                                                        dbc.CardBody(
                                                            [
                                                                dbc.Row([
                                                                    dbc.Col(
                                                                        [
                                                                            dbc.Row(dcc.Graph(id="ReportsP")),
                                                                            dbc.Row(dcc.Graph(id="SickP")),
                                                                            dbc.Row(dcc.Graph(id="DeadP")),
                                                                        ]
                                                                    ),
                                                                    dbc.Col(
                                                                        [
                                                                            dcc.Slider(
                                                                                min=1,
                                                                                max=3,
                                                                                step=1,
                                                                                marks={1: 'Reports monthly',
                                                                                       2: 'Reports weekly',
                                                                                       3: 'Reports daily',
                                                                                       },
                                                                                value=2,
                                                                                vertical=True,
                                                                                id="PperiodSlider"
                                                                            )
                                                                        ],
                                                                        width=1,
                                                                    ),
                                                                ])
                                                            ],
                                                        )
                                                    )

                                                ],
                                                label="Poultry Reports",
                                                tab_id="ReportsPTab",
                                            ),
                                            dbc.Tab(
                                                [
                                                    dbc.Card(
                                                        dbc.CardBody(
                                                            [
                                                                dbc.Row([
                                                                    dbc.Col(
                                                                        [
                                                                            html.Label("Top 10 Large Animal Diseases"),
                                                                            dcc.Graph(id="LATop10")
                                                                        ],
                                                                        width=6,
                                                                    ),
                                                                    dbc.Col(
                                                                        [
                                                                            html.Label("Top 10 Poultry Diseases"),
                                                                            dcc.Graph(id="PTop10")
                                                                        ],
                                                                        width=6,
                                                                    ),
                                                                ])
                                                            ]
                                                        )
                                                    ),
                                                    dbc.Card(
                                                        dbc.CardBody(
                                                            [
                                                                dbc.Row([
                                                                    dbc.Col(ddDiseaseType, width=2,),
                                                                    dbc.Col(
                                                                        [
                                                                            html.Label("Top 10 Disease Types"),
                                                                            dcc.Graph(id="figDistypes"),
                                                                        ]
                                                                    )
                                                                ])
                                                            ]
                                                        )
                                                    )
                                                ],
                                                label="Top10 Diseases",
                                                tab_id="DiseaseTab",
                                            ),
                                            dbc.Tab(
                                                [
                                                    dbc.Card(
                                                        dbc.Col(
                                                            [
                                                                dbc.Row(dcc.Graph(id="DRindicators")),
                                                                dbc.Row(dcc.Graph(id="DRRepG1")),
                                                                dbc.Row(
                                                                    [
                                                                        html.Label(
                                                                            "Non-Reporting Regions (Please handle with care as geoshape files and geolocations have issues)",
                                                                            id="NRlabel",
                                                                        ),
                                                                        html.Div(id="AlertTable"),
                                                                    ]
                                                                ),
                                                            ]
                                                        )
                                                    )
                                                ],
                                                label="Reports per Geolocation",
                                                tab_id="GeoRepTab",
                                            ),
                                            dbc.Tab(
                                                [dbc.Card(dbc.Col([dcc.Graph(id="figMonthly")]))],
                                                label="Yearly Comparison",
                                                tab_id="YearCompTab",
                                            ),
                                            dbc.Tab(
                                                [
                                                    dbc.Card(
                                                        dbc.Row(
                                                            [
                                                                html.Label("Export Data", id="ExportLabel"),
                                                                html.Div(id="ExportTab"),
                                                            ]
                                                        )
                                                    )
                                                ],
                                                label="Export Data",
                                                tab_id="ExportTab",
                                            ),
                                        ],
                                        id="tabs",
                                    )
                                ]
                            ),
                        ),
                        html.Label('Data from ' + str(create_date), style={'text-align': 'right'})
                    ],
                    width=8,
                ),
            ]
        )
    ]
)


endtime_start = datetime.now()
print("initialize : " + str(endtime_start - starttime_start))


# shape overlay of selected geotile(s)


@callback(
    # dash cleintsied callback with js
    Output("Division", "value"),
    Output("District", "value"),
    Output("Upazila", "value"),
    Output("Distypes", "value"),
    Output("Division", "options"),
    Output("District", "options"),
    Output("Upazila", "options"),
    Output("Diseaselist", "options"),
    Output("Distypes", "options"),
    Output('Map', 'figure'),
    Output("ReportsLA", "figure"),
    Output("SickLA", "figure"),
    Output("DeadLA", "figure"),
    Output("ReportsP", "figure"),
    Output("SickP", "figure"),
    Output("DeadP", "figure"),
    Output("LATop10", "figure"),
    Output("PTop10", "figure"),
    Output("figDistypes", "figure"),
    Output("DRindicators", "figure"),
    Output("DRRepG1", "figure"),
    Output("NRlabel", "children"),
    Output("AlertTable", "children"),
    Output("figMonthly", "figure"),
    Output("ExportLabel", "children"),
    Output("ExportTab", "children"),
    Output("Completeness", "figure"),
    Output("geoSlider", "value"),
    # Input ('cache_bahis_data', 'data'),
    # Input ('cache_bahis_dgdata', 'data'),
    # Input ('cache_bahis_geodata', 'data'),
    Input("Division", "value"),
    Input("District", "value"),
    Input("Upazila", "value"),
    Input("daterange", "start_date"),  # make state to prevent upate before submitting
    Input("daterange", "end_date"),  # make state to prevent upate before submitting
    Input("LAperiodSlider", "value"),
    Input("PperiodSlider", "value"),
    Input("Diseaselist", "value"),
    Input("Distypes", "value"),
    Input("tabs", "active_tab"),
    Input("geoSlider", "value"),
    # Input ('Map', 'clickData'),
)
def update_whatever(
    SelDiv,
    SelDis,
    SelUpa,
    start_date,
    end_date,
    LAperiodClick,
    PperiodClick,
    diseaselist,
    SelDistypes,
    tabs,
    geoSlider,
):
    starttime_general = datetime.now()

    global firstrun, \
        vDiv, \
        vDis, \
        vUpa, \
        ddDList, \
        vDistypes, \
        path, \
        variab, \
        subDistM, \
        labl, \
        splace, \
        pname, \
        pnumber, \
        loc, \
        title, \
        sub_bahis_sourcedata, \
        subDist
    #    print(geoclick)
    # print(clkRep)
    # print(clkSick)
    labl = "Reports"
    NRlabel = "Non-Reporting Regions (Please handle with care as geoshape files and geolocations have issues)"
    if firstrun is True:  # inital settings
        #        dates = sne_date(bahis_data)
        ddDList = fetchdata.fetchdiseaselist(sub_bahis_sourcedata)
        #        ddDList.insert(0, 'All Diseases')
        Divlist = fetchdata.fetchDivisionlist(bahis_geodata)
        vDistypes = bahis_distypes['Disease type']
        SelDistypes = vDistypes.iloc[0]
        vDiv = [{"label": i["Division"], "value": i["value"]} for i in Divlist]
        vDis = []
        vUpa = []
        path = path3
        loc = 3
        title = "upazila"
        pnumber = "upazilanumber"
        pname = "upazilaname"
        splace = " Upazila"
        variab = "upazila"
        subDistM = subDist[subDist["loc_type"] == 3]
        firstrun = False

    if ctx.triggered_id == "Division":
        if not SelDiv:
            subDist = bahis_geodata
            vDis = []
            Dislist = ""
            vUpa = []
            Upalist = []
            SelDis = None
            SelUpa = None
        else:
            subDist = bahis_geodata.loc[bahis_geodata["parent"].astype("string").str.startswith(str(SelDiv))]
            Dislist = fetchdata.fetchDistrictlist(SelDiv, bahis_geodata)
            vDis = [{"label": i["District"], "value": i["value"]} for i in Dislist]
            vUpa = []
            SelUpa = None

    if ctx.triggered_id == "District":
        if not SelDis:
            subDist = bahis_geodata.loc[bahis_geodata["parent"].astype("string").str.startswith(str(SelDiv))]
            Dislist = fetchdata.fetchDistrictlist(SelDiv, bahis_geodata)
            vDis = [{"label": i["District"], "value": i["value"]} for i in Dislist]
            Upalist = ""
            vUpa = []
            SelUpa = None
        else:
            # from basic data in case on switches districts in current way, switching leads to zero data but speed
            subDist = bahis_geodata.loc[bahis_geodata["parent"].astype("string").str.startswith(str(SelDis))]
            Upalist = fetchdata.fetchUpazilalist(SelDis, bahis_geodata)
            vUpa = [{"label": i["Upazila"], "value": i["value"]} for i in Upalist]

    if ctx.triggered_id == "Upazila":
        if not SelUpa:
            # from basic data in case on switches districts in current way, switching leads to zero data but speed
            subDist = bahis_geodata.loc[bahis_geodata["parent"].astype("string").str.startswith(str(SelDis))]
        else:
            subDist = bahis_geodata.loc[bahis_geodata["value"].astype("string").str.startswith(str(SelUpa))]

    if SelUpa:
        sub_bahis_sourcedata = bahis_data.loc[bahis_data["upazila"] == SelUpa]
    else:
        if SelDis:
            sub_bahis_sourcedata = bahis_data.loc[bahis_data["district"] == SelDis]  # DivNo]
        else:
            if SelDiv:
                sub_bahis_sourcedata = bahis_data.loc[bahis_data["division"] == SelDiv]  # DivNo]
            else:
                sub_bahis_sourcedata = bahis_data

    sub_bahis_sourcedata4yc = fetchdata.disease_subset(diseaselist, sub_bahis_sourcedata)

    dates = [start_date, end_date]
    sub_bahis_sourcedata = fetchdata.date_subset(dates, sub_bahis_sourcedata)
    sub_bahis_sourcedata = fetchdata.disease_subset(diseaselist, sub_bahis_sourcedata)

#    sub_bahis_sourcedata = date_subset(dates, sub_bahis_sourcedata4yc)

    if geoSlider == 1:
        path = path1
        loc = geoSlider
        title = "division"
        pnumber = "divnumber"
        pname = "divisionname"
        splace = " Division"
        variab = "division"
        subDistM = subDist[subDist["loc_type"] == geoSlider]
        # subDist=bahis_geodata[bahis_geodata['loc_type']==geoSlider]

    #        bahis_sourcedata = pd.to_numeric(bahis_data['division']).dropna().astype(int)
    # if geoTile is not None:
    #     print(geoTile['points'][0]['location'])
    #     cU2Division=geoTile['points'][0]['location']
    #     Dislist=fetchDistrictlist(geoTile['points'][0]['location'])
    #     vDistrict = [{'label': i['District'], 'value': i['value']} for i in Dislist]
    if geoSlider == 2:
        path = path2
        loc = geoSlider
        title = "district"
        pnumber = "districtnumber"
        pname = "districtname"
        splace = " District"
        variab = "district"
        subDistM = subDist[subDist["loc_type"] == geoSlider]
        # subDist=bahis_geodata[bahis_geodata['loc_type']==geoSlider]

    if geoSlider == 3:
        path = path3
        loc = geoSlider
        loc = 3
        title = "upazila"
        pnumber = "upazilanumber"
        pname = "upazilaname"
        splace = " Upazila"
        variab = "upazila"
        subDistM = subDist[subDist["loc_type"] == 3]
        # subDist=bahis_geodata[bahis_geodata['loc_type']==geoSlider]

    if ctx.triggered_id == 'geoSlider':
        Rfindic, Rfigg, NRlabel, AlertTable = GeoRep.GeoRep(sub_bahis_sourcedata, title,
                                                            subDistM, pnumber, pname, variab, labl)

    Rfig = plot_map(path, loc, subDistM, sub_bahis_sourcedata, title, pnumber, pname, splace, variab, labl)
    endtime_general = datetime.now()
    print("general callback : " + str(endtime_general - starttime_general))

# tab0

    if tabs == "CompletenessTab":
        starttime_tab0 = datetime.now()
        start = start_date + " 00:00:00"
        end = end_date + " 00:00:00"

        reset = False
        # # Find which one has been triggered
        # ctx = dash.callback_context

        # if ctx.triggered:
        #     prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        #     if prop_id == "reset-btn":
        #         reset = True
        #     if prop_id == "division-select":
        Completeness = CompletenessReport.generate_reports_heatmap(bahis_data,
                                                                   bahis_geodata, start, end, SelDiv,
                                                                   SelDis, diseaselist, reset)

        endtime_tab0 = datetime.now()
        print("tabCompleteness : " + str(endtime_tab0 - starttime_tab0))
        return (
            SelDiv,
            SelDis,
            SelUpa,
            SelDistypes,
            vDiv,
            vDis,
            vUpa,
            ddDList,
            vDistypes,
            Rfig,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            Completeness,
            geoSlider,
        )

    # tabLA

    if tabs == "ReportsLATab":
        starttime_tab1 = datetime.now()
        lanimal = ["Buffalo", "Cattle", "Goat", "Sheep"]
        sub_bahis_sourcedataLA = sub_bahis_sourcedata[sub_bahis_sourcedata["species"].isin(lanimal)]
        figheight = 175
        figgLAR, figgLASick, figgLADead = ReportsSickDead.ReportsSickDead(sub_bahis_sourcedataLA,
                                                                          dates, LAperiodClick, figheight)
        endtime_tab1 = datetime.now()
        print("tabLA : " + str(endtime_tab1 - starttime_tab1))
        return (
            SelDiv,
            SelDis,
            SelUpa,
            SelDistypes,
            vDiv,
            vDis,
            vUpa,
            ddDList,
            vDistypes,
            Rfig,
            figgLAR,
            figgLASick,
            figgLADead,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            geoSlider,
        )

# tabP

    if tabs == "ReportsPTab":
        starttime_tab1 = datetime.now()
        poultry = ["Chicken", "Duck", "Goose", "Pegion", "Quail", "Turkey"]
        sub_bahis_sourcedataP = sub_bahis_sourcedata[sub_bahis_sourcedata["species"].isin(poultry)]
        figheight = 175
        figgPR, figgPSick, figgPDead = ReportsSickDead.ReportsSickDead(sub_bahis_sourcedataP, dates,
                                                                       PperiodClick, figheight)
        endtime_tab1 = datetime.now()
        print("tabP : " + str(endtime_tab1 - starttime_tab1))
        return (
            SelDiv,
            SelDis,
            SelUpa,
            SelDistypes,
            vDiv,
            vDis,
            vUpa,
            ddDList,
            vDistypes,
            Rfig,
            no_update,
            no_update,
            no_update,
            figgPR,
            figgPSick,
            figgPDead,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            geoSlider,
        )

    # tab2

    if tabs == "DiseaseTab":
        starttime_tab2 = datetime.now()

        # preprocess groupdata ?
        flani, fpoul, figDistypes = TopTen.TopTen(sub_bahis_sourcedata, bahis_dgdata,
                                                  SelDistypes, to_replace, replace_with)
        endtime_tab2 = datetime.now()
        print("tabTop10 : " + str(endtime_tab2 - starttime_tab2))
        return (
            SelDiv,
            SelDis,
            SelUpa,
            SelDistypes,
            vDiv,
            vDis,
            vUpa,
            ddDList,
            vDistypes,
            Rfig,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            flani,
            fpoul,
            figDistypes,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            geoSlider,
        )

# tab3 geolocation
    if tabs == "GeoRepTab":
        starttime_tab3 = datetime.now()

        Rfindic, Rfigg, NRlabel, AlertTable = GeoRep.GeoRep(sub_bahis_sourcedata,
                                                            title, subDistM, pnumber, pname, variab, labl)

        endtime_tab3 = datetime.now()
        print("tabGeo : " + str(endtime_tab3 - starttime_tab3))
        return (
            SelDiv,
            SelDis,
            SelUpa,
            SelDistypes,
            vDiv,
            vDis,
            vUpa,
            ddDList,
            vDistypes,
            Rfig,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            Rfindic,
            Rfigg,
            NRlabel,
            AlertTable,
            no_update,
            no_update,
            no_update,
            no_update,
            geoSlider,
        )

    # tab 4 geodyn tab per current year

    # removed since Completeness is replacing this tab

    # tab 5 monthly currently not geo resolved and disease, because of bahis_data, either ata is time restricted or

    if tabs == "YearCompTab":
        starttime_tab5 = datetime.now()

        figMonthly = yearly_comparison.yearlyComp(sub_bahis_sourcedata4yc, diseaselist)

        endtime_tab5 = datetime.now()
        print("tabYearly : " + str(endtime_tab5 - starttime_tab5))
        return (
            SelDiv,
            SelDis,
            SelUpa,
            SelDistypes,
            vDiv,
            vDis,
            vUpa,
            ddDList,
            vDistypes,
            Rfig,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            figMonthly,
            no_update,
            no_update,
            no_update,
            geoSlider,
        )

    # tab 6 export tab

    if tabs == "ExportTab":
        starttime_tab6 = datetime.now()

        ExportTable = sub_bahis_sourcedata.copy()
        ExportTable["date"] = ExportTable["date"].dt.strftime("%Y-%m-%d")
        # del ExportTable["Unnamed: 0.1"]
        ExportTable.drop("species_no", inplace=True, axis=1)
        ExportTable.drop("tentative_diagnosis", inplace=True, axis=1)
        ExportTable.rename(columns={"top_diagnosis": "Diagnosis"}, inplace=True)
        ExportTable = ExportTable.merge(bahis_geodata[["value", "name"]], left_on="division", right_on="value")
        ExportTable["division"] = ExportTable["name"].str.capitalize()
        ExportTable.drop(["name", "value"], inplace=True, axis=1)

        ExportTable = ExportTable.merge(bahis_geodata[["value", "name"]], left_on="district", right_on="value")
        ExportTable["district"] = ExportTable["name"].str.capitalize()
        ExportTable.drop(["name", "value"], inplace=True, axis=1)

        ExportTable = ExportTable.merge(bahis_geodata[["value", "name"]], left_on="upazila", right_on="value")
        ExportTable["upazila"] = ExportTable["name"].str.capitalize()
        ExportTable.drop(["name", "value"], inplace=True, axis=1)

        ExportLabel = "Export Data Size: " + str(ExportTable.shape)

        ExportTab = (
            dash_table.DataTable(
                style_header={
                    #                                        'overflow': 'hidden',
                    #                                        'maxWidth': 0,
                    "fontWeight": "bold",
                },
                style_cell={"textAlign": "left"},
                export_format="csv",
                style_table={"height": "500px", "overflowY": "auto"},
                #                                style_as_list_view=True,
                #                                fixed_rows={'headers': True},
                data=ExportTable.to_dict("records"),
                columns=[{"name": i, "id": i} for i in ExportTable.columns],
            ),
        )

        endtime_tab6 = datetime.now()
        print("tab6 : " + str(endtime_tab6 - starttime_tab6))
        return (
            SelDiv,
            SelDis,
            SelUpa,
            SelDistypes,
            vDiv,
            vDis,
            vUpa,
            ddDList,
            vDistypes,
            Rfig,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            ExportLabel,
            ExportTab,
            no_update,
            geoSlider,
        )

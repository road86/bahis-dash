# create overall page
# store data in cache
# general layout: navbar and "body"

import dash
import dash_bootstrap_components as dbc
from components import pathnames, fetchdata
from dash import Dash, Input, Output, dcc, html, State, ctx, callback

from components import RegionSelect, MapNResolution, DateRangeSelect, DiseaseSelect
import pandas as pd
import json
from datetime import date, datetime
from dash.dash import no_update
from components import ReportsSickDead
from components import pathnames
from components import fetchdata
import plotly.express as px


# starttime_start = datetime.now()
# pd.options.mode.chained_assignment = None
# dash.register_page(__name__, path_template="ulo/<upazilano>")  # register page to main dash app

# sourcepath = "exported_data/"
# geofilename, dgfilename, sourcefilename, farmdatafilename, path1, path2, path3 = pathnames.get_pathnames(sourcepath)
# bahis_data = fetchdata.fetchsourcedata(sourcefilename)
# ULOsub_bahis_sourcedata = bahis_data
# ULOstart_date = date(2019, 1, 1)
# ULOlast_date = max(bahis_data['date']).date()
# ULOdates = [ULOstart_date, ULOlast_date]
# ULOcreate_date = fetchdata.create_date(sourcefilename)

# # ULOSelUpa = 201539

# ULOddDList = []

# bahis_geodata = fetchdata.fetchgeodata(geofilename)
# subDist = bahis_geodata



ulo = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    suppress_callback_exceptions=True,
    prevent_initial_callbacks="initial_duplicate",
)

dash.register_page(__name__,)  # register page to main dash app
starttime_start = datetime.now()
pd.options.mode.chained_assignment = None
# dash.register_page(__name__, path_template="ulo/<upazilano>")  # register page to main dash app

sourcepath = "exported_data/"           # called also in Top10, make global or settings parameter
geofilename, dgfilename, sourcefilename, farmdatafilename, path1, path2, path3 = pathnames.get_pathnames(sourcepath)
bahis_data = fetchdata.fetchsourcedata(sourcefilename)
[bahis_dgdata, bahis_distypes] = fetchdata.fetchdisgroupdata(dgfilename)
bahis_geodata = fetchdata.fetchgeodata(geofilename)
img_logo = "assets/Logo.png"
create_date = fetchdata.create_date(sourcefilename)  # implement here


ULOsub_bahis_sourcedata = bahis_data
ULOstart_date = date(2019, 1, 1)
ULOlast_date = max(bahis_data['date']).date()
ULOdates = [ULOstart_date, ULOlast_date]
ULOcreate_date = fetchdata.create_date(sourcefilename)

ULOSelUpa = 201539

ULOddDList = []

bahis_geodata = fetchdata.fetchgeodata(geofilename)
subDist = bahis_geodata

def yearlyComp(bahis_data, diseaselist):
    monthly = bahis_data.groupby(
        [bahis_data["date"].dt.year.rename("Year"), bahis_data["date"].dt.month.rename("Month")]
    )["date"].agg({"count"})
    monthly = monthly.rename({"count": "reports"}, axis=1)
    monthly = monthly.reset_index()
    monthly['reports'] = monthly['reports'] / 1000
    monthly["Year"] = monthly["Year"].astype(str)
    figYearlyComp = px.bar(
        data_frame=monthly,
        x="Month",
        y="reports",
        labels={"reports": "Reports in Thousands"},
        color="Year",
        barmode="group",
    )
    figYearlyComp.update_xaxes(dtick="M1")  # , tickformat="%B \n%Y")
    figYearlyComp.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            ticktext=['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December'],
            title=""
        ),
        title={
            'text': "Disease dynamics for \"" + str(diseaselist) + "\"",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    return figYearlyComp

def open_data(path):
    with open(path) as f:
        data = json.load(f)
    return data

# ULOSelUpa = int(upazilano)
Upazila = str(bahis_geodata[bahis_geodata["value"] == ULOSelUpa]['name'].iloc[0].capitalize())



ulo.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Label("BAHIS dashboard", style={"font-weight": "bold",
                                                                     "font-size": "200%"}),
                                width=5,
                            ),
                            dbc.Col(
                                html.Img(src=img_logo, height="30px"),
                                width=3,
                                # align='right'
                            )
                        ],
                        justify="end",
                        align="center"
                    )
                ]
            ),
        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Col([
                                                dbc.Row(html.Label(Upazila, style={"font-weight":
                                                                                    "bold", "font-size": "150%"})),
                                                dbc.Row(html.Label(ULOSelUpa, id="upazilano", hidden=True))]
                                            ),
                                            dbc.Col([
                                                    dcc.Dropdown(
                                                        ULOddDList,
                                                        "All Diseases",
                                                        id="ULODiseaselist",
                                                        multi=False,
                                                        clearable=False,
                                                    )]
                                                    ),
                                            dbc.Col(
                                                dcc.DatePickerRange(
                                                    id="ULOdaterange",
                                                    min_date_allowed=ULOstart_date,
                                                    start_date=date(2023, 1, 1),
                                                    max_date_allowed=ULOcreate_date,
                                                    end_date=ULOlast_date,  # date(2023, 12, 31)
                                                ),
                                            ),
                                        ]
                                    )
                                ]
                            )
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    dcc.Graph(id="ULOfigMonthly"),
                                ]
                            )
                        )
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
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
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            [
                                                                                dbc.Row(dcc.Graph
                                                                                        (id="ULOReportsLA")),
                                                                                dbc.Row(dcc.Graph
                                                                                        (id="ULOSickLA")),
                                                                                dbc.Row(dcc.Graph
                                                                                        (id="ULODeadLA")),
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
                                                                                    id="ULOLAperiodSlider"
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
                                                tab_id="ULOReportsLATab",
                                            ),
                                            dbc.Tab(
                                                [
                                                    dbc.Card(
                                                        dbc.CardBody(
                                                            [
                                                                dbc.Row([
                                                                    dbc.Col(
                                                                        [
                                                                            dbc.Row(dcc.Graph(id="ULOReportsP")),
                                                                            dbc.Row(dcc.Graph(id="ULOSickP")),
                                                                            dbc.Row(dcc.Graph(id="ULODeadP")),
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
                                                                                id="ULOPperiodSlider"
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
                                                tab_id="ULOReportsPTab",
                                            ),
                                        ],
                                        id="ULOtabs",
                                    )
                                ]
                            ),
                        ),
                    ],
                    width=6,
                ),
            ]
        ),



        # dbc.Row(
        #     [
        #         dbc.Col(            # left side
        #             [
        #                 dbc.Card(
        #                     dbc.CardBody(RegionSelect.Form),
        #                 ),
        #                 dbc.Card(
        #                     dbc.CardBody(MapNResolution.Form)
        #                 )
        #             ],
        #             width=4,
        #         ),
        #         dbc.Col([          # right side
        #             dbc.Card(
        #                 dbc.CardBody(
        #                     [
        #                         dbc.Row(
        #                             [
        #                                 dbc.Col(
        #                                     DateRangeSelect.Form
        #                                 ),
        #                                 dbc.Col(
        #                                     DiseaseSelect.Form
        #                                 )
        #                             ]
        #                         )
        #                     ]
        #                 )
        #             ),
        #             dbc.Card(
        #                 dbc.CardBody(
        #                     [dbc.Card(
        #                         dbc.CardBody([
        #                             dash.page_container,
        #                         ])
        #                     )]
        #                 ),
        #             ),
        #         ])
        #     ]
        # ),

        html.Br(),
        html.Div(id="dummy"),
        html.Label('Data from ' + str(create_date), style={'text-align': 'right'}),
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

##############

# def layout(upazilano=None):
#     #    layout = html.Div(
#     ULOSelUpa = int(upazilano)
#     Upazila = str(bahis_geodata[bahis_geodata["value"] == ULOSelUpa]['name'].iloc[0].capitalize())
#     return html.Div(
#         [
#             dbc.Row(
#                 [
#                     dbc.Col(
#                         [
#                             dbc.Card(
#                                 dbc.CardBody(
#                                     [
#                                         dbc.Row(
#                                             [
#                                                 dbc.Col([
#                                                     dbc.Row(html.Label(Upazila, style={"font-weight":
#                                                                                        "bold", "font-size": "150%"})),
#                                                     dbc.Row(html.Label(ULOSelUpa, id="upazilano", hidden=True))]
#                                                 ),
#                                                 dbc.Col([
#                                                         dcc.Dropdown(
#                                                             ULOddDList,
#                                                             "All Diseases",
#                                                             id="ULODiseaselist",
#                                                             multi=False,
#                                                             clearable=False,
#                                                         )]
#                                                         ),
#                                                 dbc.Col(
#                                                     dcc.DatePickerRange(
#                                                         id="ULOdaterange",
#                                                         min_date_allowed=ULOstart_date,
#                                                         start_date=date(2023, 1, 1),
#                                                         max_date_allowed=ULOcreate_date,
#                                                         end_date=ULOlast_date,  # date(2023, 12, 31)
#                                                     ),
#                                                 ),
#                                             ]
#                                         )
#                                     ]
#                                 )
#                             ),
#                             dbc.Card(
#                                 dbc.CardBody(
#                                     [
#                                         dcc.Graph(id="ULOfigMonthly"),
#                                     ]
#                                 )
#                             )
#                         ],
#                         width=6,
#                     ),
#                     dbc.Col(
#                         [
#                             dbc.Card(
#                                 dbc.CardBody(
#                                     [
#                                         dbc.Tabs(
#                                             [
#                                                 dbc.Tab(
#                                                     [
#                                                         dbc.Card(
#                                                             dbc.CardBody(
#                                                                 [
#                                                                     dbc.Row(
#                                                                         [
#                                                                             dbc.Col(
#                                                                                 [
#                                                                                     dbc.Row(dcc.Graph
#                                                                                             (id="ULOReportsLA")),
#                                                                                     dbc.Row(dcc.Graph
#                                                                                             (id="ULOSickLA")),
#                                                                                     dbc.Row(dcc.Graph
#                                                                                             (id="ULODeadLA")),
#                                                                                 ]
#                                                                             ),
#                                                                             dbc.Col(
#                                                                                 [
#                                                                                     dcc.Slider(
#                                                                                         min=1,
#                                                                                         max=3,
#                                                                                         step=1,
#                                                                                         marks={1: 'Reports monthly',
#                                                                                                2: 'Reports weekly',
#                                                                                                3: 'Reports daily',
#                                                                                                },
#                                                                                         value=2,
#                                                                                         vertical=True,
#                                                                                         id="ULOLAperiodSlider"
#                                                                                     )
#                                                                                 ],
#                                                                                 width=1,
#                                                                             ),
#                                                                         ]
#                                                                     )
#                                                                 ],
#                                                             )
#                                                         )
#                                                     ],
#                                                     label="Large Animal Reports",
#                                                     tab_id="ULOReportsLATab",
#                                                 ),
#                                                 dbc.Tab(
#                                                     [
#                                                         dbc.Card(
#                                                             dbc.CardBody(
#                                                                 [
#                                                                     dbc.Row([
#                                                                         dbc.Col(
#                                                                             [
#                                                                                 dbc.Row(dcc.Graph(id="ULOReportsP")),
#                                                                                 dbc.Row(dcc.Graph(id="ULOSickP")),
#                                                                                 dbc.Row(dcc.Graph(id="ULODeadP")),
#                                                                             ]
#                                                                         ),
#                                                                         dbc.Col(
#                                                                             [
#                                                                                 dcc.Slider(
#                                                                                     min=1,
#                                                                                     max=3,
#                                                                                     step=1,
#                                                                                     marks={1: 'Reports monthly',
#                                                                                            2: 'Reports weekly',
#                                                                                            3: 'Reports daily',
#                                                                                            },
#                                                                                     value=2,
#                                                                                     vertical=True,
#                                                                                     id="ULOPperiodSlider"
#                                                                                 )
#                                                                             ],
#                                                                             width=1,
#                                                                         ),
#                                                                     ])
#                                                                 ],
#                                                             )
#                                                         )

#                                                     ],
#                                                     label="Poultry Reports",
#                                                     tab_id="ULOReportsPTab",
#                                                 ),
#                                             ],
#                                             id="ULOtabs",
#                                         )
#                                     ]
#                                 ),
#                             ),
#                         ],
#                         width=6,
#                     ),
#                 ]
#             )
#         ]
#     )  # , ULOSelUpa


firstrun = True

# endtime_start = datetime.now()
# print("initialize : " + str(endtime_start - starttime_start))


@ulo.callback(
    # dash cleintsied callback with js
    Output("ULODiseaselist", "options"),
    Output("ULOReportsLA", "figure"),
    Output("ULOSickLA", "figure"),
    Output("ULODeadLA", "figure"),
    Output("ULOReportsP", "figure"),
    Output("ULOSickP", "figure"),
    Output("ULODeadP", "figure"),
    Output("ULOfigMonthly", "figure"),
    Input("ULOdaterange", "start_date"),  # make state to prevent upate before submitting
    Input("ULOdaterange", "end_date"),  # make state to prevent upate before submitting
    Input("ULOLAperiodSlider", "value"),
    Input("ULOPperiodSlider", "value"),
    Input("ULODiseaselist", "value"),
    Input("ULOtabs", "active_tab"),
    State("upazilano", "children")
)
def update_whatever(
    ULOstart_date,
    ULOend_date,
    ULOLAperiodClick,
    ULOPperiodClick,
    ULOdiseaselist,
    ULOtabs,
    ULOSelUpa,
):
    starttime_general = datetime.now()

    global firstrun, \
        ULOddDList, \
        ULOpath, \
        ULOvariab, \
        ULOsubDistM, \
        ULOtitle, \
        ULOsub_bahis_sourcedata, \
        ULOsubDist

    if firstrun is True:  # inital settings
        ULOddDList = fetchdata.fetchDiseaselist(ULOsub_bahis_sourcedata)
        firstrun = False

    ULOsubDist = bahis_geodata.loc[bahis_geodata["value"].astype("string").str.startswith(str(ULOSelUpa))]
    ULOsub_bahis_sourcedata = bahis_data.loc[bahis_data["upazila"] == ULOSelUpa]
    ULOsub_bahis_sourcedata4yc = fetchdata.disease_subset(ULOdiseaselist, ULOsub_bahis_sourcedata)

    ULOdates = [ULOstart_date, ULOend_date]
    ULOsub_bahis_sourcedata = fetchdata.date_subset(ULOdates, ULOsub_bahis_sourcedata)
    ULOsub_bahis_sourcedata = fetchdata.disease_subset(ULOdiseaselist, ULOsub_bahis_sourcedata)

#    ULOfigMonthly = yearly_comparison.yearlyComp(ULOsub_bahis_sourcedata4yc, ULOdiseaselist)
    ULOfigMonthly = yearlyComp(ULOsub_bahis_sourcedata4yc, ULOdiseaselist)

    endtime_general = datetime.now()
    print("general callback : " + str(endtime_general - starttime_general))

    if ULOtabs == "ULOReportsLATab":
        lanimal = ["Buffalo", "Cattle", "Goat", "Sheep"]
        ULOsub_bahis_sourcedataLA = ULOsub_bahis_sourcedata[ULOsub_bahis_sourcedata["species"].isin(lanimal)]
        ULOfigheight = 175
        ULOfiggLAR, ULOfiggLASick, ULOfiggLADead = ReportsSickDead.ReportsSickDead(ULOsub_bahis_sourcedataLA,
                                                                                   ULOdates, ULOLAperiodClick,
                                                                                   ULOfigheight)
        return (
            ULOddDList,
            ULOfiggLAR,
            ULOfiggLASick,
            ULOfiggLADead,
            no_update,
            no_update,
            no_update,
            ULOfigMonthly,
        )

    if ULOtabs == "ULOReportsPTab":
        starttime_tab1 = datetime.now()
        poultry = ["Chicken", "Duck", "Goose", "Pegion", "Quail", "Turkey"]
        ULOsub_bahis_sourcedataP = ULOsub_bahis_sourcedata[ULOsub_bahis_sourcedata["species"].isin(poultry)]
        ULOfigheight = 175
        ULOfiggPR, ULOfiggPSick, ULOfiggPDead = ReportsSickDead.ReportsSickDead(ULOsub_bahis_sourcedataP, ULOdates,
                                                                                ULOPperiodClick, ULOfigheight)
        endtime_tab1 = datetime.now()
        print("tabLA : " + str(endtime_tab1 - starttime_tab1))
        return (
            ULOddDList,
            no_update,
            no_update,
            no_update,
            ULOfiggPR,
            ULOfiggPSick,
            ULOfiggPDead,
            ULOfigMonthly,
        )



################





# @app.callback(
#     Output("cache_bahis_data", "data"),
#     Output("cache_bahis_distypes", "data"),
#     Output("cache_bahis_geodata", "data"),
#     Input("dummy", "id")
# )

# def store2cache(dummy):
#     return bahis_data.to_json(date_format='iso', orient='split'), bahis_distypes.to_json
# (date_format='iso', orient='split'), bahis_geodata.to_json(date_format='iso', orient='split')


# @ulo.callback(
#     Output("sidemenu", "is_open"),
#     Input("open-sidemenu", "n_clicks"),
#     [State("sidemenu", "is_open")],
# )
# def display_valueNtoggle_offcanvas(n1, is_open):

#     if n1:
#         return not is_open,
#     return is_open


# @ulo.callback(
#     Output("Division", "options", allow_duplicate=True),
#     Output("District", "options"),
#     Output("Upazila", "options"),
#     Output("District", "value"),
#     Output("Upazila", "value"),
#     Output("Disease", "options", allow_duplicate=True),
#     Output("cache_page_settings", "data"),
#     #    Output("cache_bahis_data", "data"),
#     #    Output("cache_bahis_geodata", "data"),
#     #    Output('page-content', 'children'),

#     Input("Division", "value"),
#     Input("District", "value"),
#     Input("Upazila", "value"),
#     Input("Division", "options"),
#     Input("District", "options"),
#     Input("Upazila", "options"),
#     Input("geoSlider", "value"),
#     Input("DateRange", "value"),
#     Input("Disease", "value"),
#     # Input("cache_bahis_geodata", "data"),
#     # prevent_initial_call=True,
# )
# def Framework(SelectedDivision, SelectedDistrict, SelectedUpazila, DivisionList, DistrictList, UpazilaList,
#               geoSlider, DateRange, SelectedDisease):

#     # geoNameNNumber = pd.read_json(geodata, orient="split")
#     # geoResolution = "upazila"
#     # shapePath = "exported_data/processed_geodata/upadata.geojson"
#     # change to relative path names later further 3 instances

#     geoNameNNumber = bahis_geodata

#     if SelectedDivision is None:
#         List = fetchdata.fetchDivisionlist(bahis_geodata)
#         DivisionList = [{"label": i["Division"], "value": i["value"]} for i in List]
#         DivisionEntry = DivisionList
#     else:
#         DivisionEntry = SelectedDivision
#     DivisionList = DivisionList

#     if DistrictList is None:
#         DistrictList = []
#     DistrictEntry = []

#     if UpazilaList is None:
#         UpazilaList = []
#     UpazilaEntry = []
#     S = ""
#     U = ""

#     if ctx.triggered_id == "Division":
#         if not SelectedDivision:
#             DivisionEntry = DivisionList
#             DistrictList = []
#             DistrictEntry = DistrictList
#             UpazilaList = []
#             UpazilaEntry = UpazilaList
#         else:
#             DivisionEntry = SelectedDivision
#             List = fetchdata.fetchDistrictlist(SelectedDivision, geoNameNNumber)
#             DistrictList = [{"label": i["District"], "value": i["value"]} for i in List]
#             DistrictEntry = DistrictList
#             UpazilaList = []
#             UpazilaEntry = UpazilaList

#     if ctx.triggered_id == "District":
#         DivisionEntry = SelectedDivision
#         if geoSlider == 1:
#             DistrictEntry = DistrictList
#             UpazilaList = []
#             UpazilaEntry = UpazilaList
#         else:
#             if not SelectedDistrict:
#                 DistrictEntry = DistrictList
#                 UpazilaList = []
#                 UpazilaEntry = UpazilaList
#             else:
#                 DistrictEntry = SelectedDistrict
#                 List = fetchdata.fetchUpazilalist(SelectedDistrict, geoNameNNumber)
#                 UpazilaList = [{"label": i["Upazila"], "value": i["value"]} for i in List]
#                 UpazilaEntry = UpazilaList
#                 S = SelectedDistrict

#     if ctx.triggered_id == "Upazila":
#         DivisionEntry = SelectedDivision
#         DistrictEntry = SelectedDistrict
#         S = SelectedDistrict
#         if geoSlider == 2:
#             UpazilaEntry = UpazilaList
#         else:
#             if not SelectedUpazila:
#                 UpazilaEntry = UpazilaList
#             else:
#                 UpazilaEntry = SelectedUpazila
#                 U = SelectedUpazila
#     #     shapePath = "exported_data/processed_geodata/divdata.geojson"
#                 # keep in mind to adjust in MapNResolution.py
#     DiseaseList = fetchdata.fetchDiseaselist(bahis_data)

#     page_settings = {
#         "division": DivisionEntry,
#         "district": DistrictEntry,
#         "upazila": UpazilaEntry,
#         "georesolution": geoSlider,
#         "disease": SelectedDisease,
#         "daterange": DateRange,
#     }

#     return DivisionList, DistrictList, UpazilaList, S, U, DiseaseList, json.dumps(page_settings)
#     # , bahis_geodata.to_json(date_format='iso', orient='split')


# @ulo.callback(
#     Output("cache_page_data", "data"),
#     Output("cache_page_geodata", "data"),
#     Input("cache_page_settings", "data"),
# )
# def UpdatePageData(settings):

#     reportsdata = bahis_data
#     geodata = bahis_geodata
#     reportsdata = fetchdata.date_subset(json.loads(settings)["daterange"], reportsdata)
#     reportsdata = fetchdata.disease_subset(json.loads(settings)["disease"], reportsdata)

#     if type(json.loads(settings)["upazila"]) == int:
#         reportsdata = reportsdata.loc[reportsdata["upazila"] == json.loads(settings)["upazila"]]
#         geodata = geodata.loc[geodata["value"] == json.loads(settings)["upazila"]]
#     else:
#         if type(json.loads(settings)["district"]) == int:
#             reportsdata = reportsdata.loc[reportsdata["district"] == json.loads(settings)["district"]]
#             geodata = geodata.loc[geodata["parent"] == json.loads(settings)["district"]]
#         else:
#             if type(json.loads(settings)["division"]) == int:
#                 reportsdata = reportsdata.loc[reportsdata["division"] == json.loads(settings)["division"]]
#                 geodata = geodata.loc[geodata["value"].astype(str).str[:2].astype(int) == json.loads(settings)
#                                       ["division"]]
#             else:
#                 reportsdata = reportsdata
#                 geodata = geodata

#     page_data = reportsdata
#     page_geodata = geodata
#     return page_data.to_json(date_format='iso', orient='split'), page_geodata.to_json(date_format='iso', orient='split')


# @ulo.callback(
#     Output("Map", "figure", allow_duplicate=True),
#     Output("dummy", "id", allow_duplicate=True),
#     # Output("url", "pathname"),
#     # Output('page-content', 'children'),
#     Input("cache_page_data", "data"),
#     Input("cache_page_geodata", "data"),
#     Input("cache_page_settings", "data"),
#     Input("dummy", "id"),
#     # Input('page-content', 'children'),
#     # State("url", "pathname"),
# )
# def UpdateFigs(data, geodata, settings, dummy):
#     MapFig = MapNResolution.plotMap(json.loads(settings)["georesolution"],
#                                     pd.read_json(data, orient="split"), pd.read_json(geodata, orient="split"))
#     return MapFig, dummy


# Run the app on localhost:80
if __name__ == "__main__":
    ulo.run(debug=True, host="0.0.0.0", port=80)  # maybe debug false to prevent second loading
else:
    server = ulo.server



##########################


# import json
# from datetime import date, datetime

# import dash
# import dash_bootstrap_components as dbc
# import pandas as pd
# from dash import callback, dcc, html
# from dash.dash import no_update
# from dash.dependencies import Input, Output, State
# # from components import yearly_comparison
# from components import ReportsSickDead
# from components import pathnames
# from components import fetchdata
# import plotly.express as px


# starttime_start = datetime.now()
# pd.options.mode.chained_assignment = None
# dash.register_page(__name__, path_template="ulo/<upazilano>")  # register page to main dash app

# sourcepath = "exported_data/"
# geofilename, dgfilename, sourcefilename, farmdatafilename, path1, path2, path3 = pathnames.get_pathnames(sourcepath)
# bahis_data = fetchdata.fetchsourcedata(sourcefilename)
# ULOsub_bahis_sourcedata = bahis_data
# ULOstart_date = date(2019, 1, 1)
# ULOlast_date = max(bahis_data['date']).date()
# ULOdates = [ULOstart_date, ULOlast_date]
# ULOcreate_date = fetchdata.create_date(sourcefilename)

# # ULOSelUpa = 201539

# ULOddDList = []

# bahis_geodata = fetchdata.fetchgeodata(geofilename)
# subDist = bahis_geodata


# def yearlyComp(bahis_data, diseaselist):
#     monthly = bahis_data.groupby(
#         [bahis_data["date"].dt.year.rename("Year"), bahis_data["date"].dt.month.rename("Month")]
#     )["date"].agg({"count"})
#     monthly = monthly.rename({"count": "reports"}, axis=1)
#     monthly = monthly.reset_index()
#     monthly['reports'] = monthly['reports'] / 1000
#     monthly["Year"] = monthly["Year"].astype(str)
#     figYearlyComp = px.bar(
#         data_frame=monthly,
#         x="Month",
#         y="reports",
#         labels={"reports": "Reports in Thousands"},
#         color="Year",
#         barmode="group",
#     )
#     figYearlyComp.update_xaxes(dtick="M1")  # , tickformat="%B \n%Y")
#     figYearlyComp.update_layout(
#         xaxis=dict(
#             tickmode='array',
#             tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
#             ticktext=['January', 'February', 'March', 'April', 'May', 'June',
#                       'July', 'August', 'September', 'October', 'November', 'December'],
#             title=""
#         ),
#         title={
#             'text': "Disease dynamics for \"" + str(diseaselist) + "\"",
#             'y': 0.95,
#             'x': 0.5,
#             'xanchor': 'center',
#             'yanchor': 'top'
#         }
#     )
#     return figYearlyComp


# def open_data(path):
#     with open(path) as f:
#         data = json.load(f)
#     return data


# def layout(upazilano=None):
#     #    layout = html.Div(
#     ULOSelUpa = int(upazilano)
#     Upazila = str(bahis_geodata[bahis_geodata["value"] == ULOSelUpa]['name'].iloc[0].capitalize())
#     return html.Div(
#         [
#             dbc.Row(
#                 [
#                     dbc.Col(
#                         [
#                             dbc.Card(
#                                 dbc.CardBody(
#                                     [
#                                         dbc.Row(
#                                             [
#                                                 dbc.Col([
#                                                     dbc.Row(html.Label(Upazila, style={"font-weight":
#                                                                                        "bold", "font-size": "150%"})),
#                                                     dbc.Row(html.Label(ULOSelUpa, id="upazilano", hidden=True))]
#                                                 ),
#                                                 dbc.Col([
#                                                         dcc.Dropdown(
#                                                             ULOddDList,
#                                                             "All Diseases",
#                                                             id="ULODiseaselist",
#                                                             multi=False,
#                                                             clearable=False,
#                                                         )]
#                                                         ),
#                                                 dbc.Col(
#                                                     dcc.DatePickerRange(
#                                                         id="ULOdaterange",
#                                                         min_date_allowed=ULOstart_date,
#                                                         start_date=date(2023, 1, 1),
#                                                         max_date_allowed=ULOcreate_date,
#                                                         end_date=ULOlast_date,  # date(2023, 12, 31)
#                                                     ),
#                                                 ),
#                                             ]
#                                         )
#                                     ]
#                                 )
#                             ),
#                             dbc.Card(
#                                 dbc.CardBody(
#                                     [
#                                         dcc.Graph(id="ULOfigMonthly"),
#                                     ]
#                                 )
#                             )
#                         ],
#                         width=6,
#                     ),
#                     dbc.Col(
#                         [
#                             dbc.Card(
#                                 dbc.CardBody(
#                                     [
#                                         dbc.Tabs(
#                                             [
#                                                 dbc.Tab(
#                                                     [
#                                                         dbc.Card(
#                                                             dbc.CardBody(
#                                                                 [
#                                                                     dbc.Row(
#                                                                         [
#                                                                             dbc.Col(
#                                                                                 [
#                                                                                     dbc.Row(dcc.Graph
#                                                                                             (id="ULOReportsLA")),
#                                                                                     dbc.Row(dcc.Graph
#                                                                                             (id="ULOSickLA")),
#                                                                                     dbc.Row(dcc.Graph
#                                                                                             (id="ULODeadLA")),
#                                                                                 ]
#                                                                             ),
#                                                                             dbc.Col(
#                                                                                 [
#                                                                                     dcc.Slider(
#                                                                                         min=1,
#                                                                                         max=3,
#                                                                                         step=1,
#                                                                                         marks={1: 'Reports monthly',
#                                                                                                2: 'Reports weekly',
#                                                                                                3: 'Reports daily',
#                                                                                                },
#                                                                                         value=2,
#                                                                                         vertical=True,
#                                                                                         id="ULOLAperiodSlider"
#                                                                                     )
#                                                                                 ],
#                                                                                 width=1,
#                                                                             ),
#                                                                         ]
#                                                                     )
#                                                                 ],
#                                                             )
#                                                         )
#                                                     ],
#                                                     label="Large Animal Reports",
#                                                     tab_id="ULOReportsLATab",
#                                                 ),
#                                                 dbc.Tab(
#                                                     [
#                                                         dbc.Card(
#                                                             dbc.CardBody(
#                                                                 [
#                                                                     dbc.Row([
#                                                                         dbc.Col(
#                                                                             [
#                                                                                 dbc.Row(dcc.Graph(id="ULOReportsP")),
#                                                                                 dbc.Row(dcc.Graph(id="ULOSickP")),
#                                                                                 dbc.Row(dcc.Graph(id="ULODeadP")),
#                                                                             ]
#                                                                         ),
#                                                                         dbc.Col(
#                                                                             [
#                                                                                 dcc.Slider(
#                                                                                     min=1,
#                                                                                     max=3,
#                                                                                     step=1,
#                                                                                     marks={1: 'Reports monthly',
#                                                                                            2: 'Reports weekly',
#                                                                                            3: 'Reports daily',
#                                                                                            },
#                                                                                     value=2,
#                                                                                     vertical=True,
#                                                                                     id="ULOPperiodSlider"
#                                                                                 )
#                                                                             ],
#                                                                             width=1,
#                                                                         ),
#                                                                     ])
#                                                                 ],
#                                                             )
#                                                         )

#                                                     ],
#                                                     label="Poultry Reports",
#                                                     tab_id="ULOReportsPTab",
#                                                 ),
#                                             ],
#                                             id="ULOtabs",
#                                         )
#                                     ]
#                                 ),
#                             ),
#                         ],
#                         width=6,
#                     ),
#                 ]
#             )
#         ]
#     )  # , ULOSelUpa


# firstrun = True

# endtime_start = datetime.now()
# print("initialize : " + str(endtime_start - starttime_start))


# @callback(
#     # dash cleintsied callback with js
#     Output("ULODiseaselist", "options"),
#     Output("ULOReportsLA", "figure"),
#     Output("ULOSickLA", "figure"),
#     Output("ULODeadLA", "figure"),
#     Output("ULOReportsP", "figure"),
#     Output("ULOSickP", "figure"),
#     Output("ULODeadP", "figure"),
#     Output("ULOfigMonthly", "figure"),
#     Input("ULOdaterange", "start_date"),  # make state to prevent upate before submitting
#     Input("ULOdaterange", "end_date"),  # make state to prevent upate before submitting
#     Input("ULOLAperiodSlider", "value"),
#     Input("ULOPperiodSlider", "value"),
#     Input("ULODiseaselist", "value"),
#     Input("ULOtabs", "active_tab"),
#     State("upazilano", "children")
# )
# def update_whatever(
#     ULOstart_date,
#     ULOend_date,
#     ULOLAperiodClick,
#     ULOPperiodClick,
#     ULOdiseaselist,
#     ULOtabs,
#     ULOSelUpa,
# ):
#     starttime_general = datetime.now()

#     global firstrun, \
#         ULOddDList, \
#         ULOpath, \
#         ULOvariab, \
#         ULOsubDistM, \
#         ULOtitle, \
#         ULOsub_bahis_sourcedata, \
#         ULOsubDist

#     if firstrun is True:  # inital settings
#         ULOddDList = fetchdata.fetchDiseaselist(ULOsub_bahis_sourcedata)
#         firstrun = False

#     ULOsubDist = bahis_geodata.loc[bahis_geodata["value"].astype("string").str.startswith(str(ULOSelUpa))]
#     ULOsub_bahis_sourcedata = bahis_data.loc[bahis_data["upazila"] == ULOSelUpa]
#     ULOsub_bahis_sourcedata4yc = fetchdata.disease_subset(ULOdiseaselist, ULOsub_bahis_sourcedata)

#     ULOdates = [ULOstart_date, ULOend_date]
#     ULOsub_bahis_sourcedata = fetchdata.date_subset(ULOdates, ULOsub_bahis_sourcedata)
#     ULOsub_bahis_sourcedata = fetchdata.disease_subset(ULOdiseaselist, ULOsub_bahis_sourcedata)

# #    ULOfigMonthly = yearly_comparison.yearlyComp(ULOsub_bahis_sourcedata4yc, ULOdiseaselist)
#     ULOfigMonthly = yearlyComp(ULOsub_bahis_sourcedata4yc, ULOdiseaselist)

#     endtime_general = datetime.now()
#     print("general callback : " + str(endtime_general - starttime_general))

#     if ULOtabs == "ULOReportsLATab":
#         lanimal = ["Buffalo", "Cattle", "Goat", "Sheep"]
#         ULOsub_bahis_sourcedataLA = ULOsub_bahis_sourcedata[ULOsub_bahis_sourcedata["species"].isin(lanimal)]
#         ULOfigheight = 175
#         ULOfiggLAR, ULOfiggLASick, ULOfiggLADead = ReportsSickDead.ReportsSickDead(ULOsub_bahis_sourcedataLA,
#                                                                                    ULOdates, ULOLAperiodClick,
#                                                                                    ULOfigheight)
#         return (
#             ULOddDList,
#             ULOfiggLAR,
#             ULOfiggLASick,
#             ULOfiggLADead,
#             no_update,
#             no_update,
#             no_update,
#             ULOfigMonthly,
#         )

#     if ULOtabs == "ULOReportsPTab":
#         starttime_tab1 = datetime.now()
#         poultry = ["Chicken", "Duck", "Goose", "Pegion", "Quail", "Turkey"]
#         ULOsub_bahis_sourcedataP = ULOsub_bahis_sourcedata[ULOsub_bahis_sourcedata["species"].isin(poultry)]
#         ULOfigheight = 175
#         ULOfiggPR, ULOfiggPSick, ULOfiggPDead = ReportsSickDead.ReportsSickDead(ULOsub_bahis_sourcedataP, ULOdates,
#                                                                                 ULOPperiodClick, ULOfigheight)
#         endtime_tab1 = datetime.now()
#         print("tabLA : " + str(endtime_tab1 - starttime_tab1))
#         return (
#             ULOddDList,
#             no_update,
#             no_update,
#             no_update,
#             ULOfiggPR,
#             ULOfiggPSick,
#             ULOfiggPDead,
#             ULOfigMonthly,
#         )

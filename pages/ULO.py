import json
from datetime import date, datetime

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import callback, dcc, html
from dash.dash import no_update
from dash.dependencies import Input, Output
from components import yearly_comparison
from components import ReportsSickDead
from components import pathnames
from components import fetchdata


starttime_start = datetime.now()
pd.options.mode.chained_assignment = None
dash.register_page(__name__)  # register page to main dash app

sourcepath = "exported_data/"
geofilename, dgfilename, sourcefilename, path1, path2, path3 = pathnames.get_pathnames(sourcepath)
bahis_data = fetchdata.fetchsourcedata(sourcefilename)
sub_bahis_sourcedata = bahis_data
start_date = date(2019, 1, 1)
last_date = max(bahis_data['date']).date()
dates = [start_date, last_date]
create_date = fetchdata.create_date(sourcefilename)
SelUpa = 201539

ddDList = []

bahis_geodata = fetchdata.fetchgeodata(geofilename)
subDist = bahis_geodata
Upazila = bahis_geodata[bahis_geodata["value"] == SelUpa]['name'].iloc[0].capitalize()

def open_data(path):
    with open(path) as f:
        data = json.load(f)
    return data


layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Label(Upazila, style={"font-weight": "bold", "font-size": "150%"})
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
                                            ),
                                            dbc.Col(
                                                dcc.DatePickerRange(
                                                    id="daterange",
                                                    min_date_allowed=start_date,
                                                    start_date=date(2023, 1, 1),
                                                    max_date_allowed=create_date,
                                                    end_date=last_date,  # date(2023, 12, 31)
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
                                    dcc.Graph(id="figMonthly"),
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
                                        ],
                                        id="tabs",
                                    )
                                ]
                            ),
                        ),
                        html.Label('Data from ' + str(create_date), style={'text-align': 'right'})
                    ],
                    width=6,
                ),
            ]
        )
    ]
)

firstrun = True

endtime_start = datetime.now()
print("initialize : " + str(endtime_start - starttime_start))


@callback(
    # dash cleintsied callback with js
    Output("Diseaselist", "options"),
    Output("ReportsLA", "figure"),
    Output("SickLA", "figure"),
    Output("DeadLA", "figure"),
    Output("ReportsP", "figure"),
    Output("SickP", "figure"),
    Output("DeadP", "figure"),
    Output("figMonthly", "figure"),
    Input("daterange", "start_date"),  # make state to prevent upate before submitting
    Input("daterange", "end_date"),  # make state to prevent upate before submitting
    Input("LAperiodSlider", "value"),
    Input("PperiodSlider", "value"),
    Input("Diseaselist", "value"),
    Input("tabs", "active_tab"),
)
def update_whatever(
    start_date,
    end_date,
    LAperiodClick,
    PperiodClick,
    diseaselist,
    tabs,
):
    starttime_general = datetime.now()

    global firstrun, \
        ddDList, \
        path, \
        variab, \
        subDistM, \
        title, \
        sub_bahis_sourcedata, \
        subDist

    if firstrun is True:  # inital settings
        ddDList = fetchdata.fetchdiseaselist(sub_bahis_sourcedata)
        path = path3
        title = "upazila"
        variab = "upazila"
        subDistM = subDist[subDist["loc_type"] == 3]
        firstrun = False

    subDist = bahis_geodata.loc[bahis_geodata["value"].astype("string").str.startswith(str(SelUpa))]
    sub_bahis_sourcedata = bahis_data.loc[bahis_data["upazila"] == SelUpa]
    sub_bahis_sourcedata4yc = fetchdata.disease_subset(diseaselist, sub_bahis_sourcedata)

    dates = [start_date, end_date]
    sub_bahis_sourcedata = fetchdata.date_subset(dates, sub_bahis_sourcedata)
    sub_bahis_sourcedata = fetchdata.disease_subset(diseaselist, sub_bahis_sourcedata)

    figMonthly = yearly_comparison.yearlyComp(sub_bahis_sourcedata4yc, diseaselist)

    endtime_general = datetime.now()
    print("general callback : " + str(endtime_general - starttime_general))

    if tabs == "ReportsLATab":
        lanimal = ["Buffalo", "Cattle", "Goat", "Sheep"]
        sub_bahis_sourcedataLA = sub_bahis_sourcedata[sub_bahis_sourcedata["species"].isin(lanimal)]
        figheight = 175
        figgLAR, figgLASick, figgLADead = ReportsSickDead.ReportsSickDead(sub_bahis_sourcedataLA,
                                                                          dates, LAperiodClick, figheight)
        return (
            ddDList,
            figgLAR,
            figgLASick,
            figgLADead,
            no_update,
            no_update,
            no_update,
            figMonthly,
        )

    if tabs == "ReportsPTab":
        starttime_tab1 = datetime.now()
        poultry = ["Chicken", "Duck", "Goose", "Pegion", "Quail", "Turkey"]
        sub_bahis_sourcedataP = sub_bahis_sourcedata[sub_bahis_sourcedata["species"].isin(poultry)]
        figheight = 175
        figgPR, figgPSick, figgPDead = ReportsSickDead.ReportsSickDead(sub_bahis_sourcedataP, dates,
                                                                       PperiodClick, figheight)
        endtime_tab1 = datetime.now()
        print("tabLA : " + str(endtime_tab1 - starttime_tab1))
        return (
            ddDList,
            no_update,
            no_update,
            no_update,
            figgPR,
            figgPSick,
            figgPDead,
            figMonthly,
        )

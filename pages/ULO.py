import json
from datetime import date, datetime

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import callback, dcc, html
from dash.dash import no_update
from dash.dependencies import Input, Output, State
#from components import yearly_comparison
from components import ReportsSickDead
from components import pathnames
from components import fetchdata
import plotly.express as px


starttime_start = datetime.now()
pd.options.mode.chained_assignment = None
dash.register_page(__name__, path_template="ulo/<upazilano>")  # register page to main dash app

sourcepath = "exported_data/"
geofilename, dgfilename, sourcefilename, path1, path2, path3 = pathnames.get_pathnames(sourcepath)
bahis_data = fetchdata.fetchsourcedata(sourcefilename)
ULOsub_bahis_sourcedata = bahis_data
ULOstart_date = date(2019, 1, 1)
ULOlast_date = max(bahis_data['date']).date()
ULOdates = [ULOstart_date, ULOlast_date]
ULOcreate_date = fetchdata.create_date(sourcefilename)

# ULOSelUpa = 201539

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

def layout(upazilano=None):
#    layout = html.Div(
    ULOSelUpa = int(upazilano)
    Upazila = str(bahis_geodata[bahis_geodata["value"] == ULOSelUpa]['name'].iloc[0].capitalize())
    return html.Div(
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
                                                    [
                                                    dbc.Row(html.Label(Upazila, style={"font-weight": "bold", "font-size": "150%"})),
                                                    dbc.Row(html.Label(ULOSelUpa, id="upazilano", hidden=True))
                                                    ]
                                                ),
                                                dbc.Col(
                                                    [
                                                        dcc.Dropdown(
                                                            ULOddDList,
                                                            "All Diseases",
                                                            id="ULODiseaselist",
                                                            multi=False,
                                                            clearable=False,
                                                        ),
                                                    ],
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
                                                                                    dbc.Row(dcc.Graph(id="ULOReportsLA")),
                                                                                    dbc.Row(dcc.Graph(id="ULOSickLA")),
                                                                                    dbc.Row(dcc.Graph(id="ULODeadLA")),
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
            )
        ]
    )#, ULOSelUpa

firstrun = True

endtime_start = datetime.now()
print("initialize : " + str(endtime_start - starttime_start))


@callback(
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

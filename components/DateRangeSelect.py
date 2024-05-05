from datetime import date, timedelta

from dash import dcc, html
import dash_bootstrap_components as dbc

from components import fetchdata, pathnames

sourcepath = "exported_data/"  # called also in Top10, make global or settings parameter
(
    geofilename,
    dgfilename,
    sourcefilename,
    farmdatafilename,
    AIinvestdatafilename,
    DiseaseInvestdatafilename,
    PartLSAssisdatafilename,
    medfilename,
    path1,
    path2,
    path3,
) = pathnames.get_pathnames(sourcepath)
first_date = date(2022, 1, 1)
# last_date = date(2024, 1, 1)  # max(bahis_data['date']).date()
last_date = fetchdata.create_date(sourcefilename)  # implement here

# fetchdata.create_date(sourcefilename)

Form = html.Div(
    [
        # dmc.DateRangePicker(
        dbc.Stack(
            [
                #                dbc.Col(
                html.H5(
                    "FROM:",
                    style={"textAlign": "center", "lineHeight": "0px", "fontWeight": 600},
                ),
                # width=4,
                # fluid=True,
                # style={"padding": "0px"},
                #                ),
                #                dbc.Col(
                dcc.DatePickerSingle(
                    id="start_date",
                    min_date_allowed=first_date,
                    max_date_allowed=last_date,
                    initial_visible_month=last_date - timedelta(weeks=6),
                    date=last_date - timedelta(weeks=6),
                    display_format="Do MMM 'YY",
                    clearable=False,
                    first_day_of_week=0,
                    style={"fontWeight": 700},
                ),
                # style={"padding": "0px", "fontWeight": 700},
                # fluid=True,
                # width=2,
                #                ),
                #                dbc.Col(
                html.H5(
                    "TO:",
                    style={"textAlign": "center", "lineHeight": "0px", "fontWeight": 600},
                ),
                # fluid=True,
                # width=2,
                # style={"padding": "0px"},
                #                ),
                #                dbc.Col(
                dcc.DatePickerSingle(
                    id="end_date",
                    min_date_allowed=first_date,
                    max_date_allowed=last_date,
                    initial_visible_month=last_date,
                    date=last_date,
                    display_format="Do MMM 'YY",
                    clearable=False,
                    first_day_of_week=0,
                    style={"fontWeight": 700},
                ),
                # fluid=True,
                # width=2,
                #               ),
            ],
            direction="horizontal",
            gap=2,
        )
        # dcc.DatePickerRange(
        #     id="DateRange",
        #     min_date_allowed=first_date,
        #     start_date=last_date - timedelta(weeks=6),
        #     max_date_allowed=last_date,
        #     end_date=last_date,
        #     initial_visible_month=last_date,
        #     first_day_of_week=0,
        #     display_format="Do MMM 'YY",
        #     clearable=False,
        #     # minDate=start_date,
        #     # value=[last_date - timedelta(weeks=6), last_date],
        #     # required=True,
        #     # dropdownType="modal",
        #     # firstDayOfWeek="sunday",
        # )
    ]
)

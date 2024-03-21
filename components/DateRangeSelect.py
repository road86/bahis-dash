from datetime import date, timedelta

from dash import dcc, html

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
        dcc.DatePickerRange(
            id="DateRange",
            min_date_allowed=first_date,
            start_date=last_date - timedelta(weeks=6),
            max_date_allowed=last_date,
            end_date=last_date,
            initial_visible_month=last_date,
            first_day_of_week=0,
            display_format="Do MMM 'YY",
            # minDate=start_date,
            # value=[last_date - timedelta(weeks=6), last_date],
            clearable=False,
            # required=True,
            # dropdownType="modal",
            # firstDayOfWeek="sunday",
        )
    ]
)

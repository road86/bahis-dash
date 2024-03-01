from datetime import timedelta, date
from components import fetchdata, pathnames
import dash_mantine_components as dmc
from dash import html


sourcepath = "exported_data/"  # called also in Top10, make global or settings parameter
geofilename, dgfilename, sourcefilename, farmdatafilename, medfilename, path1, path2, path3 = pathnames.get_pathnames(
    sourcepath
)
start_date = date(2022, 1, 1)
# last_date = date(2024, 1, 1)  # max(bahis_data['date']).date()
last_date = fetchdata.create_date(sourcefilename)  # implement here

# fetchdata.create_date(sourcefilename)

Form = html.Div(
    [
        dmc.DateRangePicker(
            id="DateRange",
            minDate=start_date,
            value=[last_date - timedelta(weeks=6), last_date],
            clearable=False,
            required=True,
            dropdownType="modal",
            firstDayOfWeek="sunday",
        )
    ]
)

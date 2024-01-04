from datetime import timedelta, date
import dash_mantine_components as dmc
from dash import html


start_date = date(2019, 1, 1)
last_date = date(2023, 1, 1)  # max(bahis_data['date']).date()
# fetchdata.create_date(sourcefilename)

Form = html.Div([
    dmc.DateRangePicker(
        id="DateRange",
        minDate=start_date,
        value=[last_date - timedelta(weeks=6), last_date],
        clearable=False,
        required=True,
        dropdownType="modal",
        firstDayOfWeek="sunday",
    )
])

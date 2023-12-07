from datetime import timedelta, date
from components import fetchdata
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import pandas as pd


start_date = date(2019, 1, 1)
last_date = date(2023, 1, 1)  #max(bahis_data['date']).date()
# fetchdata.create_date(sourcefilename)

Form = html.Div([
    dmc.DateRangePicker(
        id="DateRange",
        minDate =start_date,
        value=[last_date - timedelta(weeks=6), last_date],
        clearable=False,
        firstDayOfWeek="sunday",
    )

])

from datetime import timedelta, date
from components import fetchdata
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import pandas as pd


start_date = date(2019, 1, 1)
last_date = date(2023, 1, 1)  #max(bahis_data['date']).date()
# fetchdata.create_date(sourcefilename)

Form = html.Div([
    dcc.DatePickerRange(
        id="daterange",
        min_date_allowed=start_date,
        start_date=last_date - timedelta(weeks=6),  # date(2023, 1, 1),
        max_date_allowed = last_date,   # create_date,
        end_date = last_date,  # date(2023, 12, 31)
    )
])

# @callback(
#     Output("daterange", "options", allow_duplicate=True),
#     Input("cache_bahis_data", "data"),
#     prevent_initial_call=True
# )

# def Dates(bahis_data):
#     # List = fetchdata.fetchDiseaselist(pd.read_json(bahis_data, orient="split"))
#     min = pd.read_json(bahis_data, orient="split")['date'].min()
#     max = pd.read_json(bahis_data, orient="split")['date'].max()
#     print(min)
#     print(max)

#     return out
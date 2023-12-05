from components import fetchdata
import dash_bootstrap_components as dbc
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import pandas as pd


Form = html.Div([
    dcc.DatePickerRange(
        id="daterange",
        min_date_allowed=start_date,
        start_date=last_date - timedelta(weeks=6),  # date(2023, 1, 1),
        max_date_allowed=create_date,
        end_date=last_date,  # date(2023, 12, 31)
    )
])

@callback(
    Output("Diseaselist", "options", allow_duplicate=True),
    Input("cache_bahis_data", "data"),
    prevent_initial_call=True
)

def DiseaseList(bahis_data):
    List = fetchdata.fetchDiseaselist(pd.read_json(bahis_data, orient="split"))
    print("aa")
    print(List)
    print("here")
    Diseaselist = [{"label": i["Disease"], "value": i["value"]} for i in List]
    print(Diseaselist)
    return Diseaselist

# import dash
# from dash import html, dcc, callback
# import dash_bootstrap_components as dbc
# from components import fetchdata
# from dash.dependencies import Input, Output, State
# import pandas as pd
# import plotly.express as px

# # import plotly.express as px
# import json


# dash.register_page(
#     __name__,
# )  # register page to main dash app

# layout = [
#     html.Label("Antibiotics Usage"),
#     dbc.Row(
#         [
#             dbc.Col([html.Label("Full"), dcc.Graph(id="ABUsageF")]),
#             dbc.Col([html.Label("time"), dcc.Graph(id="ABUsageT")]),
#         ]
#     ),
#     html.Div(id="dummy"),
# ]


# @callback(
#     Output("ABUsageF", "figure"),
#     Output("ABUsageT", "figure"),
#     Input("cache_filenames", "data"),
#     Input("dummy", "id"),
#     State("cache_page_farmdata", "data"),
#     State("cache_page_settings", "data"),
#     prevent_initial_call=True,
# )
# def BSEntrance(filenames, dummy, data, settings):
#     farmdata = pd.read_json(data, orient="split")
#     farmdatafilename = json.loads(filenames)["farmdata"]
#     fulldata = fetchdata.fetchfarmdata(farmdatafilename)
#     medsfilename = json.loads(filenames)["meds"]
#     medsdata = fetchdata.fetchmedsdata(medsfilename)

#     if type(json.loads(settings)["upazila"]) == int:
#         fulldata = fulldata.loc[fulldata["upazila"] == json.loads(settings)["upazila"]]
#     else:
#         if type(json.loads(settings)["district"]) == int:
#             fulldata = fulldata.loc[fulldata["district"] == json.loads(settings)["district"]]
#         else:
#             if type(json.loads(settings)["division"]) == int:
#                 fulldata = fulldata.loc[fulldata["division"] == json.loads(settings)["division"]]
#             else:
#                 fulldata = fulldata

#     merge_df = pd.merge(farmdata["g1"], medsdata[["id", "aware_class"]], left_on="g1", right_on="id")
#     if len(merge_df) == 0:
#         figT = px.pie()
#         figT.add_annotation(x=0.5, y=0.5, text="No data available", showarrow=False, font=dict(size=20))
#         # figT.update_layout(title="No data available")
#     else:
#         category_counts = merge_df.groupby("aware_class").size().reset_index(name="count")
#         figT = px.pie(category_counts, values="count", names="aware_class", title="selected timeframe")
#         figT.update_layout(height=550)

#     merge_df = pd.merge(fulldata["g1"], medsdata[["id", "aware_class"]], left_on="g1", right_on="id")
#     category_counts = merge_df.groupby("aware_class").size().reset_index(name="count")
#     figF = px.pie(category_counts, values="count", names="aware_class", title="fulltime")
#     figF.update_layout(height=550)
#     return figF, figT

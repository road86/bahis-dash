import dash_bootstrap_components as dbc
from dash import html, dcc

Form = html.Div([
    dbc.Row([
            dbc.Col([
                dbc.Label("Division"),
                dcc.Dropdown(
                    id="Division",
                    clearable=True,
                    placeholder="Select Division"
                ),
            ]),
            dbc.Col([
                dbc.Label("District"),
                dcc.Dropdown(
                    id="District",
                    clearable=True,
                    placeholder="Select District"
                ),
            ]),
            dbc.Col([
                dbc.Label("Upazila"),
                dcc.Dropdown(
                    id="Upazila",
                    clearable=True,
                    placeholder="Select Upazila"
                ),
            ])  
        ]) 
    ])

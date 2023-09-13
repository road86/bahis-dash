import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(__name__, path="/")

layout = dbc.Container(

        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.Row(
                                    [
                                        html.Center(html.H1("Home: This landing page")),
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.Row(
                                    [
                                        html.Center(html.H1("ULO: Upazila Lifestock Office")),
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.Row(
                                    [
                                        html.Center(html.H1("DLS: Overview page ")),
                                    ]
                                )
                            ]
                        )
                    ]
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col([dbc.Card([dbc.Row([dbc.Button("Home", href="/", size="lg")])])]),
                dbc.Col([dbc.Card([dbc.Row([dbc.Button("ULO", href="/ulo", size="lg")])])]),
                dbc.Col([dbc.Card([dbc.Row([dbc.Button("DLS", href="/dls", size="lg")])])]),
            ]
        ),        
    )

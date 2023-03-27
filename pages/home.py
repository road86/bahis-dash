# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 07:48:14 2023

@author: yoshka
"""

# Import necessary libraries 
import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

# Define the page layout
layout = dbc.Container([
    dbc.Row([
        html.Center(html.H1("Home: This landing page")),
    ]),
    # dbc.Row([
    #     html.Center(html.H1("Alerts: Reporting status")),
    # ]),
    dbc.Row([
        html.Center(html.H1("Dls: Overview page ")),
    ]),
    # dbc.Row([
    #     html.Center(html.H1("Dlsquick: Test environment with only essential values")),
    # ]),
    # dbc.Row([
    #     html.Center(html.H1("Reporting: Another reporting view")),
    # ]),
    dbc.Row([
        html.Center(html.H1("Templates: Figures for reports")),
    ]),
    # dbc.Row([
    #     dbc.Nav([
    #         dbc.NavLink(
    #             [
    #                 html.Div(page["name"], className="ms-2"),
    #             ],
    #             href=page["path"],
    #             active="exact",
    #             )
    #     for page in dash.page_registry.values()
    #         ])
    # ])
])
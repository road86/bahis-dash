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
        html.Center(html.H1("Home: Select link on top right")),
    ])
])
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 07:43:22 2023

@author: yoshka
"""

# Import necessary libraries 
import dash
from dash import html, dcc, Dash, Output, Input
#from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


# Connect to your app pages
#from pages import dls, ulo, reports #,bahisdashpltOLD

# Connect the navbar to the index
from components import navbar

#app = Dash(__name__)

app = Dash(__name__, 
                use_pages=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP], 
                meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                suppress_callback_exceptions=True)

#app.config.suppress_callback_exceptions = True

# Define the navbar
nav = navbar.Navbar()

# Define the index page layout
# app.layout = html.Div([
# #    dcc.Location(id='url', refresh=False),
# #    nav, 
#     #dash.page_container,
#     #html.Div(id='page-content', children=[]), 
# ]) #, fluid=True,)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(
        [
            # html.Div(
            #     dcc.Link(
            #         f"{page['name']} - {page['path']}", href=page["relative_path"]
            #     )
            # )
            # for page in dash.page_registry.values()
        ]
    ),
    html.Div(id='page-1-display-value'),
	dash.page_container
])


@app.callback(
    Output('page-1-display-value', 'children'),
    Input('nav', 'value'))
def display_value(value):
    return f'You have selected {value}'


# "complete" layout
app.validation_layout = html.Div([
#     dls.layout,
#     ulo,
#     report,m
#     #app,
#     #navbar,
#     #index.layout,
#     #bahisdashpltOLD,
#     #page2,
    
])    
    


# Create the callback to handle mutlipage inputs
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dls':
        return dls.layout
    if pathname == '/ulo':
        return ulo.layout
    if pathname == '/reports':
        return reports.layout
    else: # if redirected to unknown link
        return "404 Page Error! Please choose a link"

# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=True)
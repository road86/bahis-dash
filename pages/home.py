from dash import html
import dash

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H2("Welcome to the bahis dashboard."),
    html.H2("Please select a report from the menu on the top left.")
])

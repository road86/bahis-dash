from dash import Dash, html, dcc
import dash

dash.register_page(__name__,)

layout = html.Div(
    [html.H2("Welcome to the bahis dashboard."),
     html.H2("Please select a report from the menu on the top left.")
    ])

if __name__ == '__main__':
    app.run(debug=True)
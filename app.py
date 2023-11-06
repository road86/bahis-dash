import dash
import dash_bootstrap_components as dbc
from components import navbar
from dash import Dash, Input, Output, dcc, html, State

# Connect to your app pages
# from pages import dls, ulo, reports #,bahisdashpltOLD


app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    suppress_callback_exceptions=True,
)

# Define the navbar
nav = navbar.Navbar()

# Define the index page layout
# app.layout = html.Div([
# #    dcc.Location(id='url', refresh=False),
# #    nav,
#     #dash.page_container,
#     #html.Div(id='page-content', children=[]),
# ]) #, fluid=True,)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        nav,
        html.Div([]),
        html.Div(
            [
                dbc.Button("Open Offcanvas", id="open-offcanvas", n_clicks=0),
                dbc.Offcanvas(
                    html.P(
                        "This is the content of the Offcanvas. "
                        "Close it by clicking on the close button, or "
                        "the backdrop."
                    ),
                    id="offcanvas",
                    title="Title",
                    is_open=False,
                ),
            ]
        ),
        html.Div(id="page-1-display-value"),
        dash.page_container,
        dcc.Store(id="cache_bahis_data", storage_type="memory"),
        dcc.Store(id="cache_bahis_dgdata", storage_type="memory"),
        dcc.Store(id="cache_bahis_geodata", storage_type="memory"),
    ]
)


@app.callback(
        Output("page-1-display-value", "children"), 
        Output("offcanvas", "is_open"),
        Input("nav", "value"),
        Input("open-offcanvas", "n_clicks"),
        [State("offcanvas", "is_open")],
)
def display_valueNtoggle_offcanvas(value, n1, is_open):
    if n1:
        return not is_open
    return f"You have selected {value}", is_open


# "complete" layout
app.validation_layout = html.Div(
    [
        #     dls.layout,
        #     ulo,
        #     report,m
        #     #app,
        #     #navbar,
        #     #index.layout,
        #     #bahisdashpltOLD,
        #     #page2,
    ]
)


# Create the callback to handle mutlipage inputs
# @app.callback(Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/dls':
#         return dls.layout
#     if pathname == '/ulo':
#         return ulo.layout
#     if pathname == '/reports':
#         return reports.layout
#     else: # if redirected to unknown link
#         return "404 Page Error! Please choose a link"

# Run the app on localhost:8050
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
else:
    server = app.server

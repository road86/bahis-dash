import dash
import dash_bootstrap_components as dbc
from components import navbar
from dash import Dash, Input, Output, dcc, html, State

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    suppress_callback_exceptions=True,
)

nav = navbar.Navbar()
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        nav,
        html.Div([]),
        html.Div(id="page-1-display-value"),
        dash.page_container,
        dcc.Store(id="cache_bahis_data", storage_type="memory"),
        dcc.Store(id="cache_bahis_dgdata", storage_type="memory"),
        dcc.Store(id="cache_bahis_geodata", storage_type="memory"),
    ]
)


@app.callback(
    Output("sidemenu", "is_open"),
    Input("open-sidemenu", "n_clicks"),
    [State("sidemenu", "is_open")],
)
def display_valueNtoggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


# Run the app on localhost:80
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
else:
    server = app.server

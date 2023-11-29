# create overall page
# store data in cache
# general layout: navbar and "body"

import dash
import dash_bootstrap_components as dbc
from components import navbar, pathnames, fetchdata
from dash import Dash, Input, Output, dcc, html, State

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    suppress_callback_exceptions=True,
    prevent_initial_callbacks="initial_duplicate",
)

dash.register_page(__name__)  # register page to main dash app

sourcepath = "exported_data/"
geofilename, dgfilename, sourcefilename, path1, path2, path3 = pathnames.get_pathnames(sourcepath)
bahis_data = fetchdata.fetchsourcedata(sourcefilename)
[bahis_dgdata, bahis_distypes] = fetchdata.fetchdisgroupdata(dgfilename)
bahis_geodata = fetchdata.fetchgeodata(geofilename)

create_date = fetchdata.create_date(sourcefilename) #implement here

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar.Navbar(),
#        html.Div(id="page-1-display-value"),
        html.Br(),
        dash.page_container,
        html.Br(),
        html.Div(id="dummy"),
        html.Label('Data from ' + str(create_date), style={'text-align': 'right'}),
        dcc.Store(data = bahis_data.to_json(date_format='iso', orient='split'), id="cache_bahis_data", storage_type="memory"),
        dcc.Store(data = bahis_dgdata.to_json(date_format='iso', orient='split'), id="cache_bahis_dgdata", storage_type="memory"),
        dcc.Store(data = bahis_distypes.to_json(date_format='iso', orient='split'), id="cache_bahis_distypes", storage_type="memory"),
        dcc.Store(id="cache_bahis_geodata", storage_type="memory"),
    ]
)

@app.callback(
        Output("cache_bahis_geodata", "data"),
        Input("dummy", "id")
)

def store2cache(dummy):
    return bahis_geodata.to_json(date_format='iso', orient='split')

@app.callback(
    Output("sidemenu", "is_open"),
    Input("open-sidemenu", "n_clicks"),
    [State("sidemenu", "is_open")],
)
def display_valueNtoggle_offcanvas(n1, is_open):

    if n1:
        return not is_open, 
    return is_open


# Run the app on localhost:80
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
else:
    server = app.server

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

offcanvas = html.Div(
    [
        dbc.Button("Menu", id="open-offcanvas", n_clicks=0),
        dbc.Offcanvas(
            # html.P(
            #     "This is the content of the Offcanvas. "
            #     "Close it by clicking on the close button, or "
            #     "the backdrop."
            # ),
            dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            [
                                html.P("This is the content of the first section"),
                                dbc.Button("Click here"),
                            ],
                            title="Item 1",
                        ),
                        dbc.AccordionItem(
                            [
                                dbc.Nav(
                                    [
                                        dbc.NavLink("Home", href="/", active="exact"),
                                        dbc.NavLink("ULO", href="/ulo", active="exact"),
                                    ],
                                    vertical=True,
                                    pills=True,
                                ),
                            ],
                            title="Item 2",
                        ),
                        dbc.AccordionItem(
                            [
                                dcc.Dropdown(
                                options=["Option 1", "Option 2"],
                                # id="DropOptions",
                                clearable=True,
                                placeholder="Select Option",
                            ),

                            ]                        
                        ),
                    ],
                ),

            id="offcanvas",
            title="Menu",
            is_open=False,
        ),
    ]
)

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
        offcanvas,
        html.Div(id="page-1-display-value"),
        dash.page_container,
        dcc.Store(id="cache_bahis_data", storage_type="memory"),
        dcc.Store(id="cache_bahis_dgdata", storage_type="memory"),
        dcc.Store(id="cache_bahis_geodata", storage_type="memory"),
    ]
)


@app.callback(
    Output("page-1-display-value", "children"), 
    Input("nav", "value"),
)
def display_value(value):
    return f"You have selected {value}"

@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def display_valueNtoggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open





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

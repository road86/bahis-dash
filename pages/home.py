from dash import html, dcc, callback
from dash.dependencies import Output, Input
import dash

dash.register_page(__name__, path='/')


def layout_gen(aid=None, **other_unknown_query_strings):
#    html.Div(id="dummy"),
    print(aid + "home")
    if aid is None:
        return html.Div(
            html.Div([
                html.H2("Welcome to the bahis dashboard."),
                html.H2("Please select a report from the menu on the top left."),
            ])
        )
    else:
        return html.Div([
            dcc.Store(id="cache_aid", storage_type="memory", data=aid),
            html.Div([
                html.H2("Welcome to the bahis dashboard."),
                html.H2("Please select a report from the menu on the top left."),
            ])
        ])


layout = layout_gen


# @callback(
#     Output("dummy", "id"),
#     Input("dummy", "id"))
# def set_store(id):
#     return id

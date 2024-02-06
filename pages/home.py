from dash import html, callback
from dash.dependencies import Output, Input, State
import dash

dash.register_page(__name__, path="/")


def layout_gen(aid=None, **other_unknown_query_strings):
    html.Div(id="dummy"),
    return html.Div(
        [
            html.Div(
                [
                    html.H2("Welcome to the bahis dashboard."),
                    html.H2("Please select a report from the menu on the top left."),
                ]
            )
        ]
    )


layout = layout_gen


@callback(
    Output("dummy", "id"),
    Output("cache_aid", "data"),
    Input("dummy", "id"),
    Input("url", "search"),
    State("cache_aid", "data"),
)
def set_store(id, url, prev):
    if url != "":
        aid = url.split("=")[1]
    else:
        aid = None
    if aid is None:
        return id, None
    else:
        return id, aid

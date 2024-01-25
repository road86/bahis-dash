from dash import html
import dash

dash.register_page(__name__, path='/')


def layout_gen(kid=None, **other_unknown_query_strings):
    return html.Div(
        html.Div([
            html.H2("Welcome to the bahis dashboard." + kid),
            html.H2("Please select a report from the menu on the top left."),
        ])
    )


layout = layout_gen

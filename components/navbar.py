# -*- coding: utf-8 -*-

from dash import html, dcc
import dash_bootstrap_components as dbc
import os

sourcepath = "exported_data/"
sourcefilename = os.path.join(sourcepath, "preped_data2.csv")


def Navbar():
    img_logo = "assets/Logo.png"

    surf = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col([
                        dbc.Button("Menu", id="open-sidemenu", n_clicks=0),
                        dbc.Offcanvas(
                            dbc.Accordion(
                                [
                                    dbc.AccordionItem(
                                        [
                                            dbc.Nav(
                                                [
                                                    dbc.NavLink("Home", href="/", active="exact"),
                                                    dbc.NavLink("Completeness Report", href="/completeness", active="exact"),
                                                    # dbc.NavLink("Large Animal Report", href="/largeanimal", active="exact"),
                                                    dbc.NavLink("ULO", href="/ulo", active="exact"),
                                                ],
                                                vertical=True,
                                                pills=True,
                                            ),
                                        ],
                                        title="Patient Registry Data",
                                    ),
                                    dbc.AccordionItem(
                                        [
                                            html.P("This is the content of the second section"),
                                            dbc.Button("Click here"),
                                        ],
                                        title="Buttons",
                                    ),
                                    dbc.AccordionItem(
                                        [
                                            dcc.Dropdown(
                                                options=["Option 1", "Option 2"],
                                                clearable=True,
                                                placeholder="Select Option",
                                            ),
                                        ],
                                        title="Dropdown",

                                    ),
                                ],
                            ),

                            id="sidemenu",
                            title="Menu",
                            is_open=False,
                        ),
                    ]),
                    dbc.Col(
                        html.Label("BAHIS dashboard", style={"font-weight": "bold",
                                                             "font-size": "200%"}),
                        width=5,
                    ),
                    dbc.Col(
                        html.Img(src=img_logo, height="30px"),
                        width=3,
                        # align='right'
                    )
                ],
                justify="end",
                align="center"
            )
        ]
    )
    return surf

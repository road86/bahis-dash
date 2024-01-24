# -*- coding: utf-8 -*-

from dash import html, dcc
import dash_bootstrap_components as dbc

# sourcepath = "exported_data/"
# sourcefilename = os.path.join(sourcepath, "preped_data2.csv")


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
                                                    dbc.NavLink("Home", href="/"),  # , active="exact"),
                                                    dbc.NavLink("Completeness Report",
                                                                href="/completeness", active="exact"),
                                                    dbc.NavLink("Large Animal Report",
                                                                href="/largeanimal", active="exact"),
                                                    dbc.NavLink("Poultry Report", href="/poultry", active="exact"),
                                                    dbc.NavLink("Remaining Animals Report", href="/remaining",
                                                                active="exact"),
                                                    dbc.NavLink("Top 10 Report", href="/topten", active="exact"),
                                                    dbc.NavLink("Zoonotic Reports", href="/zoonotic",
                                                                active="exact"),
                                                    dbc.NavLink("Regional Statistics Report",
                                                                href="/regionalstats", active="exact"),
                                                    dbc.NavLink("Regional Dynamics Report",
                                                                href="/regionaldyn", active="exact"),
                                                    dbc.NavLink("Yearly Comparison",
                                                                href="/yearlycomparison", active="exact"),
                                                    dbc.NavLink("Export Data", href="/export", active="exact"),
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
                                            dbc.Nav(
                                                [
                                                    dbc.NavLink("Antibiotics Usage Poultry",
                                                                href="/completeness", active="exact"),
                                                    dbc.NavLink("Antibiotics Usage Report AWaRe",
                                                                href="/completeness", active="exact"),
                                                    dbc.NavLink("Antibiotics Class",
                                                                href="/completeness", active="exact"),
                                                    dbc.NavLink("Biosecurity at entrance",
                                                                href="/bsentrance", active="exact"),
                                                    dbc.NavLink("Biosecurity between loading and production",
                                                                href="/bsproduction", active="exact"),
                                                    dbc.NavLink("Biosecurity personell management",
                                                                href="/bspersonell", active="exact"),
                                                    dbc.NavLink("Biosecurity equipment management",
                                                                href="/bsequipment", active="exact"),
                                                ],
                                                vertical=True,
                                                pills=True,
                                            ),
                                        ],
                                        title="Farm Assessment Data",
                                    ),
                                    dbc.AccordionItem(
                                        [
                                            html.P("This is the content of the second section"),
                                            dbc.Button("Click here"),
                                        ],
                                        title="Sink Surveillance",
                                    ),
                                    dbc.AccordionItem(
                                        [
                                            dcc.Dropdown(
                                                options=["Placeholder 1", "Placeholder 2"],
                                                clearable=True,
                                                placeholder="Select Option",
                                            ),
                                        ],
                                        title="AMR",

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

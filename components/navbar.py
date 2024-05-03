# -*- coding: utf-8 -*-

import dash_bootstrap_components as dbc
from dash import html  # , dcc


def Navbar(aid):
    return html.Div(
        [
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/?aid=" + aid),  # , active="exact"),
                ]
            ),
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            dbc.Nav(
                                [
                                    # dbc.NavLink("Home", href="/?aid=" + aid),  # , active="exact"),
                                    dbc.NavLink(
                                        "Completeness Report", href="/prcompleteness/?aid=" + aid, active="exact"
                                    ),
                                    dbc.NavLink(
                                        "Overall Data Reports",
                                        href="/proveralldatarep/?aid=" + aid,
                                        active="exact",
                                    ),
                                    dbc.NavLink(
                                        "Regional Dynamics Report", href="/prregionaldyn/?aid=" + aid, active="exact"
                                    ),
                                    dbc.NavLink(
                                        "Large Animal Report",
                                        href="/prlargeanimal/?aid=" + aid,
                                        active="exact",
                                        id="LA-click",
                                        n_clicks=0,
                                    ),
                                    dbc.NavLink("Poultry Report", href="/prpoultry/?aid=" + aid, active="exact"),
                                    dbc.NavLink(
                                        "Remaining Animals Report", href="/prremaining/?aid=" + aid, active="exact"
                                    ),
                                    dbc.NavLink("Top 10 Report", href="/prtopten/?aid=" + aid, active="exact"),
                                    dbc.NavLink("Zoonotic Reports", href="/przoonotic/?aid=" + aid, active="exact"),
                                    dbc.NavLink(
                                        "Yearly Comparison", href="/pryearlycomparison/?aid=" + aid, active="exact"
                                    ),
                                    dbc.NavLink(
                                        "Yearly Percentage Comparison", href="/pryearlyperc/?aid=" + aid, active="exact"
                                    ),
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
                                    dbc.NavLink(
                                        "Overall Farmdata Reports",
                                        href="/foverallfarmdatarep/?aid=" + aid,
                                        active="exact",
                                    ),
                                    dbc.NavLink(
                                        "Antibiotics Usage Poultry", href="/faabusage/?aid=" + aid, active="exact"
                                    ),
                                    dbc.NavLink(
                                        "Antibiotics Usage Report AWaRe", href="/faabaware/?aid=" + aid, active="exact"
                                    ),
                                    dbc.NavLink("Antibiotics Class", href="/faabclass/?aid=" + aid, active="exact"),
                                    dbc.NavLink(
                                        "Biosecurity at entrance", href="/fabsentrance/?aid=" + aid, active="exact"
                                    ),
                                    dbc.NavLink(
                                        "Biosecurity between loading and production",
                                        href="/fabsproduction/?aid=" + aid,
                                        active="exact",
                                    ),
                                    dbc.NavLink(
                                        "Biosecurity personell management",
                                        href="/fabspersonell/?aid=" + aid,
                                        active="exact",
                                    ),
                                    dbc.NavLink(
                                        "Biosecurity equipment management",
                                        href="/fabsequipment/?aid=" + aid,
                                        active="exact",
                                    ),
                                ],
                                vertical=True,
                                pills=True,
                            ),
                        ],
                        title="Farm Assessment Data",
                    ),
                    dbc.AccordionItem(
                        [
                            dbc.Nav(
                                [
                                    dbc.NavLink("Export Patient Data", href="/exportpr/?aid=" + aid, active="exact"),
                                    dbc.NavLink("Export Farmdata", href="/exportfa/?aid=" + aid, active="exact"),
                                ],
                                vertical=True,
                                pills=True,
                            ),
                        ],
                        title="Export Data",
                    ),
                    dbc.AccordionItem(
                        [
                            dbc.Nav(
                                [
                                    dbc.NavLink("Form Summary", href="/formsummary/?aid=" + aid, active="exact"),
                                ],
                                vertical=True,
                                pills=True,
                            ),
                        ],
                        title="Form Data",
                    ),
                ],
            ),
        ]
    )

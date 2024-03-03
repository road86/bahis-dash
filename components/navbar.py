# -*- coding: utf-8 -*-

from dash import html  # , dcc
import dash_bootstrap_components as dbc


def Navbar(aid):
    return html.Div(
<<<<<<< HEAD
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        dbc.Nav(
                            [
                                dbc.NavLink("Home", href="/?aid=" + aid),  # , active="exact"),
                                dbc.NavLink("Completeness Report", href="/completeness/?aid=" + aid, active="exact"),
                                dbc.NavLink(
                                    "Regional Statistics Report", href="/regionalstats/?aid=" + aid, active="exact"
                                ),
                                dbc.NavLink(
                                    "Regional Dynamics Report", href="/regionaldyn/?aid=" + aid, active="exact"
                                ),
                                dbc.NavLink("Large Animal Report", href="/largeanimal/?aid=" + aid, active="exact"),
                                dbc.NavLink("Poultry Report", href="/poultry/?aid=" + aid, active="exact"),
                                dbc.NavLink("Remaining Animals Report", href="/remaining/?aid=" + aid, active="exact"),
                                dbc.NavLink("Top 10 Report", href="/topten/?aid=" + aid, active="exact"),
                                dbc.NavLink("Zoonotic Reports", href="/zoonotic/?aid=" + aid, active="exact"),
                                dbc.NavLink("Yearly Comparison", href="/yearlycomparison/?aid=" + aid, active="exact"),
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
                                dbc.NavLink("Antibiotics Usage Poultry", href="/todopage/?aid=" + aid, active="exact"),
                                dbc.NavLink(
                                    "Antibiotics Usage Report AWaRe", href="/abaware/?aid=" + aid, active="exact"
                                ),
                                dbc.NavLink("Antibiotics Class", href="/todopage/?aid=" + aid, active="exact"),
                                dbc.NavLink("Biosecurity at entrance", href="/bsentrance/?aid=" + aid, active="exact"),
                                dbc.NavLink(
                                    "Biosecurity between loading and production",
                                    href="/bsproduction/?aid=" + aid,
                                    active="exact",
                                ),
                                dbc.NavLink(
                                    "Biosecurity personell management", href="/bspersonell/?aid=" + aid, active="exact"
                                ),
                                dbc.NavLink(
                                    "Biosecurity equipment management", href="/bsequipment/?aid=" + aid, active="exact"
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
                                dbc.NavLink("Export Patient Data", href="/export/?aid=" + aid, active="exact"),
                            ],
                            vertical=True,
                            pills=True,
                        ),
                    ],
                    title="Export Data",
                ),
                # dbc.AccordionItem(
                #     [
                #         html.P("This is the content of the second section"),
                #         dbc.Button("Click here"),
                #     ],
                #     title="Sink Surveillance",
                # ),
                # dbc.AccordionItem(
                #     [
                #         dcc.Dropdown(
                #             options=["Placeholder 1", "Placeholder 2"],
                #             clearable=True,
                #             placeholder="Select Option",
                #         ),
                #     ],
                #     title="AMR",
                # ),
            ],
        ),
=======
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
                                        "Completeness Report", href="/completeness/?aid=" + aid, active="exact"
                                    ),
                                    dbc.NavLink(
                                        "Regional Statistics Report", href="/regionalstats/?aid=" + aid, active="exact"
                                    ),
                                    dbc.NavLink(
                                        "Regional Dynamics Report", href="/regionaldyn/?aid=" + aid, active="exact"
                                    ),
                                    dbc.NavLink(
                                        "Large Animal Report",
                                        href="/largeanimal/?aid=" + aid,
                                        active="exact",
                                        id="LA-click",
                                        n_clicks=0,
                                    ),
                                    dbc.NavLink("Poultry Report", href="/poultry/?aid=" + aid, active="exact"),
                                    dbc.NavLink(
                                        "Remaining Animals Report", href="/remaining/?aid=" + aid, active="exact"
                                    ),
                                    dbc.NavLink("Top 10 Report", href="/topten/?aid=" + aid, active="exact"),
                                    dbc.NavLink("Zoonotic Reports", href="/zoonotic/?aid=" + aid, active="exact"),
                                    dbc.NavLink(
                                        "Yearly Comparison", href="/yearlycomparison/?aid=" + aid, active="exact"
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
                                        "Antibiotics Usage Poultry", href="/todopage/?aid=" + aid, active="exact"
                                    ),
                                    dbc.NavLink(
                                        "Antibiotics Usage Report AWaRe", href="/todopage/?aid=" + aid, active="exact"
                                    ),
                                    dbc.NavLink("Antibiotics Class", href="/todopage/?aid=" + aid, active="exact"),
                                    dbc.NavLink(
                                        "Biosecurity at entrance", href="/bsentrance/?aid=" + aid, active="exact"
                                    ),
                                    dbc.NavLink(
                                        "Biosecurity between loading and production",
                                        href="/bsproduction/?aid=" + aid,
                                        active="exact",
                                    ),
                                    dbc.NavLink(
                                        "Biosecurity personell management",
                                        href="/bspersonell/?aid=" + aid,
                                        active="exact",
                                    ),
                                    dbc.NavLink(
                                        "Biosecurity equipment management",
                                        href="/bsequipment/?aid=" + aid,
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
                                    dbc.NavLink("Export Patient Data", href="/export/?aid=" + aid, active="exact"),
                                ],
                                vertical=True,
                                pills=True,
                            ),
                        ],
                        title="Export Data",
                    ),
                    # dbc.AccordionItem(
                    #     [
                    #         html.P("This is the content of the second section"),
                    #         dbc.Button("Click here"),
                    #     ],
                    #     title="Sink Surveillance",
                    # ),
                    # dbc.AccordionItem(
                    #     [
                    #         dcc.Dropdown(
                    #             options=["Placeholder 1", "Placeholder 2"],
                    #             clearable=True,
                    #             placeholder="Select Option",
                    #         ),
                    #     ],
                    #     title="AMR",
                    # ),
                ],
            ),
        ]
>>>>>>> 100b73e (feat: Features and mods day2 (#247))
    )

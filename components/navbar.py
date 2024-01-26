# -*- coding: utf-8 -*-

from dash import html, dcc
import dash_bootstrap_components as dbc

# sourcepath = "exported_data/"
# sourcefilename = os.path.join(sourcepath, "preped_data2.csv")


def NavbarN():
    return html.Div(
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
    )


def Navbar(aid):
    return html.Div(
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        dbc.Nav(
                            [
                                dbc.NavLink("Homeee", href="/?aid=" + aid),  # , active="exact"),
                                dbc.NavLink("Completeness Report",
                                            href="/completeness/?aid=" + aid, active="exact"),
                                dbc.NavLink("Large Animal Report",
                                            href="/largeanimal/?aid=" + aid, active="exact"),
                                dbc.NavLink("Poultry Report",
                                            href="/poultry/?aid=" + aid, active="exact"),
                                dbc.NavLink("Remaining Animals Report",
                                            href="/remaining/?aid=" + aid, active="exact"),
                                dbc.NavLink("Top 10 Report",
                                            href="/topten/?aid=" + aid, active="exact"),
                                dbc.NavLink("Zoonotic Reports", href="/zoonotic/?aid=" + aid,
                                            active="exact"),
                                dbc.NavLink("Regional Statistics Report",
                                            href="/regionalstats/?aid=" + aid, active="exact"),
                                dbc.NavLink("Regional Dynamics Report",
                                            href="/regionaldyn/?aid=" + aid, active="exact"),
                                dbc.NavLink("Yearly Comparison",
                                            href="/yearlycomparison/?aid=" + aid,
                                            active="exact"),
                                dbc.NavLink("Export Data", href="/export/?aid=" + aid,
                                            active="exact"),
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
    )

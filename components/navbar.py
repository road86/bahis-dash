# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 07:56:51 2023

@author: yoshka
"""

# Import necessary libraries
import dash
from dash import html  # , dcc
import dash_bootstrap_components as dbc
# import datetime
import os
from components import fetchdata

# dash.register_page(__name__)

sourcepath = "exported_data/"
sourcefilename = os.path.join(sourcepath, "preped_data2.csv")
# create_time = os.path.getmtime(sourcefilename)
# create_date = datetime.datetime.fromtimestamp(create_time).date()
create_date = fetchdata.create_date(sourcefilename)


# Define the navbar structure
def Navbar():
    img_logo = "assets/Logo.png"

    withlinks = False

    if withlinks:
        surf = dbc.Navbar(
            dbc.Container(
                [
                    # dcc.Location(id='urloc', refresh=True),
                    dbc.Nav(
                        [
                            dbc.NavLink(
                                [
                                    html.Div(page["name"], className="ms-2"),
                                ],
                                href=page["path"],
                                active="exact",
                            )
                            for page in dash.page_registry.values()
                            # if page["path"].startswith("/topic")
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    # dbc.NavbarBrand("BAHIS Dashboard", className="ml-auto")
                                    html.Label("BAHIS dashboard", style={"font-weight": "bold",
                                                                         "font-size": "200%", "text-align": "center"}),
                                ],
                                width=9
                            ),
                            dbc.Col(
                                [
                                    html.Img(src=img_logo, height="30px")
                                ],
                                width=3),
                        ],
                        justify="left",
                        align="center"
                    ),

                ],
                # fluid=True,
            ),
            color="white",
            dark=False,
            className="mb-5",
        )
    else:
        surf = html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Label("BAHIS dashboard", style={"font-weight": "bold",
                                                                 "font-size": "200%"}),  # , "text-align": "center"}),
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

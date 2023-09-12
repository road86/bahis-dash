# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 07:56:51 2023

@author: yoshka
"""

# Import necessary libraries
import dash
from dash import html  # , dcc
import dash_bootstrap_components as dbc
import datetime
import os


# dash.register_page(__name__)

sourcepath = "exported_data/"
sourcefilename = os.path.join(sourcepath, "preped_data2.csv")
create_time = os.path.getmtime(sourcefilename)
create_date = datetime.datetime.fromtimestamp(create_time).date()


# Define the navbar structure
def Navbar():
    img_logo = "assets/Logo.png"

    surf = dbc.Navbar(
        dbc.Container(
            [
                # dcc.Location(id='urloc', refresh=True),
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=img_logo, height="30px")),
                        dbc.Col(
                            dbc.NavbarBrand("BAHIS Dashboard: database from : " + str(create_date), className="ml-2")
                        ),
                    ],
                    align="center",
                ),
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
            ],
            fluid=True,
        ),
        color="white",
        dark=False,
        className="mb-5",
    )

    return surf

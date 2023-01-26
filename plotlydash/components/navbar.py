# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 07:56:51 2023

@author: yoshka
"""

# Import necessary libraries
import dash
from dash import html #, dcc
import dash_bootstrap_components as dbc


#dash.register_page(__name__)

# Define the navbar structure
def Navbar():
  
    img_logo= 'assets/Logo.png'  
  
    surf = dbc.Navbar(
        dbc.Container(
            [
                #dcc.Location(id='urloc', refresh=True),
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=img_logo, height='30px')),
                        dbc.Col(dbc.NavbarBrand('BAHIS Dashboard', className='ml-2')),
                        ],
                    align='center',
                    #no_gutters=True,
                    ),
                dbc.Nav([
                    # dbc.NavLink('Home', href='/'), #, active='exact'),
                    # dbc.NavLink('DLS', href='/dls'), #, active='exact'),
                    # dbc.NavLink('ULO', href='/ulo'), #, active='exact'),
                    # dbc.NavLink('Reports', href='/reports'), #, active='exact'),
                    # ], className='ml-auto', navbar=True),
                    dbc.NavLink(
                        [
                            html.Div(page["name"], className="ms-2"),
                        ],
                        href=page["path"],
                        active="exact",
                        )
                for page in dash.page_registry.values()
                #if page["path"].startswith("/topic")
                ],
                #fluid=True,
                )]),
            color='dark',
            dark=True,
            className='mb-5',
        )
    
  
    return surf
  
# import dash
# from dash import html
# import dash_bootstrap_components as dbc


# def Navbar():
#     return html.Div(
#         dbc.Nav(
#             [
#                 dbc.NavLink(
#                     [
#                         html.Div(page["name"], className="ms-2"),
#                     ],
#                     href=page["path"],
#                     active="exact",
#                 )
#                 for page in dash.page_registry.values()
#                 if page["path"].startswith("/topic")
#             ],
#             vertical=True,
#             pills=True,
#             className="bg-light",
#         )
#     )
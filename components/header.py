import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

def header():
    return dbc.Navbar(
        dbc.Container(
            [
                # Logo Section
                dbc.Row(
                    [
                        dbc.Col(
                            html.A(
                                html.Img(src='/assets/img/logo_msg_global_RGB.svg', height="50px"),
                                href="/",
                            ),
                            width="auto",
                        ),
                    ],
                    align="center",
                    className="g-0", 
                ),
                # Toggler for small screens
                dbc.NavbarToggler(id="navbar-toggler"),
                
                # Collapsible navbar links
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavLink("Home", href="/", className="nav-link"),
                            dbc.NavLink("JD Preparation", href="/jdpreparation", className="nav-link"),
                            dbc.NavLink("JD Screening", href="/screening", className="nav-link"),
                            dbc.NavLink("Question Generation", href="/qfg", className="nav-link"),
                        ],
                        className="ml-auto",  # Align links to the right on large screens
                        navbar=True
                    ),
                    id="navbar-collapse",
                    is_open=False,  # Ensure the navbar is collapsed by default
                    navbar=True,
                ),
            ]
        ),
        color="white",  
        dark=False,    
        className="header-navbar"
    )



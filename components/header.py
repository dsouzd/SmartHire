from dash import html
import dash_bootstrap_components as dbc

def header():
    return dbc.Navbar(
        dbc.Container(
            [
                # Logo and Title
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src='/assets/img/logo_msg_global_RGB.svg',
                                height='50px'
                            ),
                            width='auto'
                        ),
                    ],
                    align="center",
                    className="g-0",
                ),
                # Navigation Links
                dbc.NavbarToggler(id="navbar-toggler"),
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavItem(dbc.NavLink("Home", href="/")),
                            dbc.NavItem(dbc.NavLink("JD Preparation", href="/jdpreparation")),
                            dbc.NavItem(dbc.NavLink("JS Screening", href="/screening")),
                        ],
                        className="ms-auto",
                        navbar=True,
                    ),
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True,
                ),
            ]
        ),
        color="dark",
        dark=True,
    )

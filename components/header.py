import dash
from dash import dcc, html
import dash_bootstrap_components as dbc


def header():
    header = dbc.Navbar(
        dbc.Container(
            [
                dcc.Location(id="url", refresh=False),
                dbc.Row(
                    [
                        dbc.Col(
                            html.A(
                                html.Img(
                                    src="/assets/img/logo_msg_global_RGB.svg",
                                    height="50px",
                                ),
                                href="/",
                            ),
                            width="auto",
                        ),
                    ],
                    align="center",
                    className="g-0",
                ),
                dbc.NavbarToggler(
                    id="navbar-toggler",
                    className="navbar-toggler-custom",
                    children=[
                        html.I(
                            className="fas fa-bars fa-lg", style={"color": "#a01441"}
                        )
                    ],
                ),
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavLink("Statistics", href="/", className="nav-link"),
                            dbc.NavLink(
                                "Job Description Generator",
                                href="/jdpreparation",
                                className="nav-link",
                            ),
                            dbc.NavLink(
                                "Profile Screening",
                                href="/screening",
                                className="nav-link",
                            ),
                            dbc.NavLink(
                                "Archive", href="/jdtable", className="nav-link"
                            ),
                        ],
                        className="ml-auto",
                        navbar=True,
                    ),
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True,
                ),
            ]
        ),
        color="white",
        dark=False,
        className="header-navbar",
    )
    return html.Div(header, className="header")

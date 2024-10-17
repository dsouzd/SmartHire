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
                                    src="/assets/img/new_msg_logo.svg",
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
                            className="fas fa-bars fa-lg", style={"color": "#ffffff"}
                        )
                    ],
                ),
                dbc.Collapse(
                    dbc.Nav(
                        [
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
                                "Preliminary Questions", 
                                href="/preliminaryquestions", 
                                className="nav-link"
                            ),
                            dbc.DropdownMenu(
                                children=[
                                    dbc.DropdownMenuItem("Statistics", href="/statistics"),
                                    dbc.DropdownMenuItem("JD Library", href="/archive"),
                                    dbc.DropdownMenuItem("Candidate Details", href="/candidate-details"),
                                ],
                                nav=True,
                                in_navbar=True,
                                label="Job Management",
                                className="dropdown-toggle",
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

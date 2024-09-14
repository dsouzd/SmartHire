import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

def header(app):
    return dbc.Navbar(
        dbc.Container(
            [
                # Logo on the left
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
                    className="g-0",  # No spacing between columns
                ),
                
                # Toggler for smaller screens
                dbc.NavbarToggler(id="navbar-toggler"),
                
                # Navigation links
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavLink("Home", href="/", className="nav-link"),
                            dbc.NavLink("JD Preparation", href="/jdpreparation", className="nav-link"),
                            dbc.NavLink("JD Screening", href="/screening", className="nav-link"),
                            dbc.NavLink("Question Generation", href="/qfg", className="nav-link"),
                        ],
                        className="ml-auto",  # Align links to the right
                        navbar=True
                    ),
                    id="navbar-collapse",
                    navbar=True,
                ),
            ]
        ),
        color="white",  # Background color
        dark=False,     # Text will not be white
        className="header-navbar"
    )

    # Callback to toggle navbar collapse for mobile view
    @app.callback(
        dash.dependencies.Output("navbar-collapse", "is_open"),
        [dash.dependencies.Input("navbar-toggler", "n_clicks")],
        [dash.dependencies.State("navbar-collapse", "is_open")],
    )
    def toggle_navbar(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open

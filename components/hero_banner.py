import dash_bootstrap_components as dbc
from dash import html


def hero_banner():
    """Creates a banner with a full background image, rounded text background, and padding."""
    hero_banner = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.H1(
                                    "Smart Hiring Automation", className="banner-title"
                                ),
                                html.P(
                                    "Streamlining your hiring process with smart automation.",
                                    className="banner-subtitle",
                                ),
                            ],
                            className="banner-text bg-text",
                        ),
                        md=6,
                        className="d-flex align-items-center",
                    ),
                ],
                align="center",
            )
        ],
        fluid=True,
        className="banner-container",
    )
    return html.Div(hero_banner, className="hero-banner")

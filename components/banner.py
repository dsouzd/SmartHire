import dash_bootstrap_components as dbc
from dash import html

def banner():
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.H1("Smart Hiring Automation", className="banner-title"),
                                html.P("Streamlining your hiring process with smart automation.", className="banner-subtitle"),
                                dbc.Button("Learn More", href="/news", color="primary", className="banner-button"),
                            ],
                            className="banner-text",
                        ),
                        md=6,
                    ),
                    dbc.Col(
                        html.Img(src="/assets/img/banner.webp", className="banner-image"),
                        md=6,
                        className="d-none d-md-block"  # Hide image on small screens
                    ),
                ],
                align="center",
            )
        ],
        fluid=True,
        className="banner-container",
    )

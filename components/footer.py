from dash import html
import dash_bootstrap_components as dbc

def footer():
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.P(
                                "MSG Global© 2024",
                                className="text-center mb-0",
                                style={
                                    "color": "#ffffff",  # White text for contrast
                                    "fontWeight": "bold",
                                    "fontSize": "18px"
                                }
                            ),
                            html.P(
                                "All Rights Reserved",
                                className="text-center mb-0",
                                style={
                                    "color": "#f0f0f0",  # Slightly lighter gray for secondary text
                                    "fontSize": "14px"
                                }
                            ),
                        ],
                        width=6,
                        className="d-flex flex-column justify-content-center align-items-center"
                    ),
                    dbc.Col(
                        [
                            # Social media icons
                            html.Div(
                                [
                                    html.A(
                                        html.I(className="fab fa-facebook-f"),
                                        href="https://www.facebook.com",
                                        className="text-white mx-2"
                                    ),
                                    html.A(
                                        html.I(className="fab fa-twitter"),
                                        href="https://www.twitter.com",
                                        className="text-white mx-2"
                                    ),
                                    html.A(
                                        html.I(className="fab fa-linkedin-in"),
                                        href="https://www.linkedin.com",
                                        className="text-white mx-2"
                                    ),
                                ],
                                className="d-flex justify-content-center",
                            )
                        ],
                        width=6,
                        className="d-flex justify-content-center align-items-center"
                    ),
                ],
                className="pt-3"
            )
        ],
        fluid=True,
        className="footer",
        style={
            "backgroundColor": "#a01441",  # Primary color as background
            "color": "#ffffff",  # White text for readability
            "paddingTop": "20px",
            "paddingBottom": "20px",
            "borderTop": "5px solid #ffffff",  # White top border
        }
    )

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
                                    "fontWeight": "bold",
                                    "fontSize": "18px"
                                }
                            ),
                            html.P(
                                "All Rights Reserved",
                                className="text-center mb-0",
                                style={
                                    "color": "#f0f0f0", 
                                    "fontSize": "14px"
                                }
                            ),
                        ],
                        width=6,
                        className="d-flex flex-column justify-content-center align-items-center"
                    ),
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.A(
                                        html.I(className="fab fa-facebook-f"),
                                        href="https://www.facebook.com",
                                        className="text-white mx-2",
                                        target="_blank", 
                                        **{'aria-label': 'Facebook'} 
                                    ),
                                    html.A(
                                        html.I(className="fab fa-twitter"),
                                        href="https://www.twitter.com",
                                        className="text-white mx-2",
                                        target="_blank",
                                        **{'aria-label': 'Twitter'}
                                    ),
                                    html.A(
                                        html.I(className="fab fa-linkedin-in"),
                                        href="https://www.linkedin.com",
                                        className="text-white mx-2",
                                        target="_blank",
                                        **{'aria-label': 'LinkedIn'}
                                    ),
                                ],
                                className="d-flex justify-content-center social-icons"
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
            "backgroundColor": "#a01441", 
            "color": "#ffffff",  
            "paddingTop": "20px",
            "paddingBottom": "20px",
            "position": "relative", 
            "zIndex": "1000", 
        }
    )

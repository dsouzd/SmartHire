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
                                "© 2024 msg global solutions",
                                className="text-center mb-0",
                                style={
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
            )
        ],
        fluid=True,
        className="footer",
        style={
            "backgroundColor": "#a01441", 
            "color": "#ffffff",  
            "paddingTop": "11px",
            "paddingBottom": "11px",
            "position": "relative", 
            "zIndex": "1000", 
        }
    )

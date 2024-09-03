from dash import html, dcc
import dash_bootstrap_components as dbc

def home():
    return html.Div([
        dbc.Container([
            # Header Section
            dbc.Row(
                dbc.Col(
                    html.H1('Welcome to the HR Recruitment Portal', className='display-4 text-center my-5'),
                    width=12
                )
            ),
            
            # Icon Section
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H5("JD Preparation", className="card-title text-center"),
                                    html.P(
                                        "Create and manage job descriptions with ease.",
                                        className="card-text text-center"
                                    ),
                                    html.Div(
                                        html.I(className="fas fa-file-alt", style={"fontSize": "50px"}),
                                        className="d-flex justify-content-center mb-3"
                                    ),
                                    dbc.Button("Get Started", href="/jdpreparation", className="btn btn-primary d-block mx-auto")
                                ],
                                className="d-flex flex-column align-items-center justify-content-center text-center h-100"
                            ),
                        ],
                        className="mb-4 shadow h-100",
                        style={"height": "350px"}
                    ),
                    width=4
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H5("JD Screening", className="card-title text-center"),
                                    html.P(
                                        "Screen and filter job descriptions efficiently.",
                                        className="card-text text-center"
                                    ),
                                    html.Div(
                                        html.I(className="fas fa-filter", style={"fontSize": "50px"}),
                                        className="d-flex justify-content-center mb-3"
                                    ),
                                    dbc.Button("Get Started", href="/jdscreening", className="btn btn-primary d-block mx-auto")
                                ],
                                className="d-flex flex-column align-items-center justify-content-center text-center h-100"
                            ),
                        ],
                        className="mb-4 shadow h-100",
                        style={"height": "350px"}
                    ),
                    width=4
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H5("Generate Questions", className="card-title text-center"),
                                    html.P(
                                        "Generate interview questions based on job descriptions.",
                                        className="card-text text-center"
                                    ),
                                    html.Div(
                                        html.I(className="fas fa-question", style={"fontSize": "50px"}),
                                        className="d-flex justify-content-center mb-3"
                                    ),
                                    dbc.Button("Get Started", href="/generatequestions", className="btn btn-primary d-block mx-auto")
                                ],
                                className="d-flex flex-column align-items-center justify-content-center text-center h-100"
                            ),
                        ],
                        className="mb-4 shadow h-100",
                        style={"height": "350px"}
                    ),
                    width=4
                ),
            ], justify="center"),

            # Additional Information Section
            dbc.Row(
                dbc.Col(
                    html.P(
                        "Our HR recruitment platform streamlines the hiring process, making it easier to connect with top talent and manage the entire recruitment lifecycle.",
                        className="lead text-center mt-4"
                    ),
                    width=12
                )
            )
        ])
    ])

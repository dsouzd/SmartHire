from dash import html
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
                                    html.H5("Job Postings", className="card-title"),
                                    html.P(
                                        "Create and manage job postings with ease.",
                                        className="card-text"
                                    ),
                                    html.Div(className="recruitment-icon posting-icon", style={"fontSize": "50px"}),
                                ]
                            )
                        ],
                        className="mb-4 shadow"
                    ),
                    width=4
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H5("Candidate Management", className="card-title"),
                                    html.P(
                                        "Organize and review candidate applications efficiently.",
                                        className="card-text"
                                    ),
                                    html.Div(className="recruitment-icon management-icon", style={"fontSize": "50px"}),
                                ]
                            )
                        ],
                        className="mb-4 shadow"
                    ),
                    width=4
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H5("Interviews", className="card-title"),
                                    html.P(
                                        "Schedule and conduct interviews seamlessly.",
                                        className="card-text"
                                    ),
                                    html.Div(className="recruitment-icon interview-icon", style={"fontSize": "50px"}),
                                ]
                            )
                        ],
                        className="mb-4 shadow"
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

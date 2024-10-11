from dash import dcc, html
import dash_bootstrap_components as dbc

def questions_screen():
    return html.Div(
        id="questions-form-container",
        style={"backgroundColor": "#f7f7f7", "padding": "50px", "minHeight": "100vh"},
        children=[
            dcc.Location(id="questions-url", refresh=False),
            dbc.Container(
                children=[
                    html.Div(id="questions-toast-container", className="toast-container"),
                    dbc.Row(
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H2(
                                            "Candidate Screening Form", className="form-title"
                                        ),
                                        html.Br(),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label("Business Unit", className="label-text"),
                                                    width=4,
                                                ),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id="questions-business-unit-dropdown",
                                                        options=[],
                                                        placeholder="Select a business unit",
                                                        className="custom-dropdown",
                                                    ),
                                                    width=8,
                                                ),
                                            ],
                                            className="mb-3",
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label("Job Descriptions", className="label-text"),
                                                    width=4,
                                                ),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id="questions-jd-dropdown",
                                                        options=[],
                                                        placeholder="Select a job description",
                                                        className="custom-dropdown",
                                                        disabled=True,
                                                    ),
                                                    width=8,
                                                ),
                                            ],
                                            className="mb-3",
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Button(
                                                        "Submit",
                                                        id="questions-submit-btn",
                                                        className="w-100 custom-submit-btn",
                                                        style={"display": "inline-block"},
                                                    )
                                                ),
                                                dbc.Col(
                                                    dbc.Button(
                                                        "Reset",
                                                        id="questions-reset-btn",
                                                        className="w-100 custom-reset-btn",
                                                        style={"display": "inline-block"},
                                                    )
                                                ),
                                            ],
                                            className="mt-4",
                                        ),
                                        html.Div(
                                            id="questions-results",
                                            className="mt-4",
                                        ),
                                        dbc.Row(
                                            dbc.Col(
                                                dbc.Button(
                                                    "Invite",
                                                    id="questions-invite-btn",
                                                    className="w-100 custom-invite-btn",
                                                    style={"display": "none"},
                                                ),
                                                width=6,
                                            ),
                                            justify="center",
                                            className="mt-4",
                                        ),
                                        dcc.Loading(
                                            id="loading-overlay",
                                            type="circle",
                                            fullscreen=True, 
                                            children=[html.Div(id="loading-output")]
                                        ),
                                    ]
                                ),
                                className="form-card",
                            ),
                            width=6,
                        ),
                        justify="center",
                    ),
                ]
            ),
        ],
    )

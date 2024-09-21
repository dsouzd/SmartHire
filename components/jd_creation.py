import dash_bootstrap_components as dbc
from dash import dcc, html

def jd_form():
    return html.Div(
        id="form-container",
        style={"backgroundColor": "#f7f7f7", "padding": "50px", "minHeight": "100vh"},
        children=[
            dbc.Container(
                dbc.Row(
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody([
                                html.H2("Job Description Form", className="form-title"),
                                html.Br(),

                                # Form section
                                dbc.Form([
                                    # Business Unit Dropdown
                                    dbc.Row([
                                        dbc.Col(dbc.Label("Business Unit", className="label-text"), width=4),
                                        dbc.Col(
                                            dcc.Loading(
                                                id="loading-business-unit",
                                                type="default",
                                                children=[
                                                    dcc.Dropdown(
                                                        id='business-unit-dropdown',
                                                        options=[],
                                                        placeholder="Select a business unit",
                                                        className="custom-dropdown"
                                                    )
                                                ]
                                            ), width=8
                                        ),
                                    ], className="mb-3"),

                                    # Job Title Input
                                    dbc.Row([
                                        dbc.Col(dbc.Label("Job Title", className="label-text"), width=4),
                                        dbc.Col(
                                            dbc.InputGroup([
                                                dbc.InputGroupText(html.I(className="fas fa-briefcase"), className="input-group-addon"),
                                                dbc.Input(id="job-title-input", type="text", placeholder="Enter job title"),
                                            ]), width=8
                                        ),
                                    ], className="mb-3"),

                                    # Experience Input
                                    dbc.Row([
                                        dbc.Col(dbc.Label("Experience", className="label-text"), width=4),
                                        dbc.Col(
                                            dbc.InputGroup([
                                                dbc.InputGroupText(html.I(className="fas fa-user-tie"), className="input-group-addon"),
                                                dbc.Input(id="experience-input", type="text", placeholder="Enter experience"),
                                            ]), width=8
                                        ),
                                    ], className="mb-3"),

                                    # Skills Input
                                    dbc.Row([
                                        dbc.Col(dbc.Label("Skills", className="label-text"), width=4),
                                        dbc.Col(
                                            dbc.InputGroup([
                                                dbc.InputGroupText(html.I(className="fas fa-tools"), className="input-group-addon"),
                                                dbc.Input(id="skills-input", type="text", placeholder="Enter required skills"),
                                            ]), width=8
                                        ),
                                    ], className="mb-3"),

                                    # Submit Button
                                    dbc.Row([
                                        dbc.Col(
                                            dbc.Button("Submit", id="submit-btn", color="primary", className="custom-btn"),
                                            width=12
                                        )
                                    ]),

                                ]),

                                # Response Section
                                html.Div(id="response-section", className="mt-4"),

                                # Save and Discard (formerly Reset) Buttons
                                dbc.Row([
                                    dbc.Col(dbc.Button("Save", id="save-btn", color="success", className="w-100", style={'display': 'none'}), width=6),
                                    dbc.Col(dbc.Button("Discard", id="reset-btn", color="secondary", className="w-100", style={'display': 'none'}), width=6),
                                ], className="mt-4"),

                                # Toast Notification for Save/Discard
                                dbc.Toast(
                                    id="toast-message",
                                    header="Notification",
                                    is_open=False,
                                    dismissable=True,
                                    duration=4000,
                                    style={"position": "fixed", "top": 10, "right": 10, "width": 350}
                                )
                            ]),
                            className="form-card"
                        ),
                        width=6
                    ),
                    justify="center",
                )
            )
        ]
    )

import dash_bootstrap_components as dbc
from dash import dcc, html

def jd_form():
    jd_form = html.Div(
        id="jd-creation-form-container",
        children=[
            dcc.Location(id="jd-creation-jdform-url", refresh=False),
            dbc.Container(
                children=[
                    # Toast notification
                    dbc.Toast(
                        id="jd-creation-toast-message",
                        header="Notification",
                        is_open=False,
                        dismissable=True,
                        duration=4000,
                        className="toast-message"
                    ),
                    dbc.Row(
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody([

                                    # Title
                                    html.H2("Job Description Form", className="form-title"),
                                    html.Br(),

                                    # Form with loaders
                                    dbc.Form([

                                        # Business Unit Dropdown with loader
                                        dbc.Row([
                                            dbc.Col(dbc.Label("Business Unit", className="label-text"), width=4),
                                            dbc.Col(
                                                dcc.Loading(
                                                    id="jd-creation-loading-business-unit",
                                                    type="default",
                                                    children=[
                                                        dcc.Dropdown(
                                                            id='jd-creation-business-unit-dropdown',
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
                                                    dbc.Input(id="jd-creation-job-title-input", type="text", placeholder="Enter job title"),
                                                ]), width=8
                                            ),
                                        ], className="mb-3"),

                                        # Experience Input
                                        dbc.Row([
                                            dbc.Col(dbc.Label("Experience", className="label-text"), width=4),
                                            dbc.Col(
                                                dbc.InputGroup([
                                                    dbc.InputGroupText(html.I(className="fas fa-user-tie"), className="input-group-addon"),
                                                    dbc.Input(id="jd-creation-experience-input", type="text", placeholder="Enter experience"),
                                                ]), width=8
                                            ),
                                        ], className="mb-3"),

                                        # Skills Input
                                        dbc.Row([
                                            dbc.Col(dbc.Label("Skills", className="label-text"), width=4),
                                            dbc.Col(
                                                dbc.InputGroup([
                                                    dbc.InputGroupText(html.I(className="fas fa-tools"), className="input-group-addon"),
                                                    dbc.Input(id="jd-creation-skills-input", type="text", placeholder="Enter required skills"),
                                                ]), width=8
                                            ),
                                        ], className="mb-3"),

                                        # Submit Button with loader
                                        dbc.Row([
                                            dbc.Col(
                                                dcc.Loading(
                                                    id="jd-creation-loading-submit",
                                                    type="circle",
                                                    children=[
                                                        dbc.Button("Submit", id="jd-creation-submit-btn", className="custom-btn w-100")
                                                    ]
                                                ),
                                                width=12
                                            )
                                        ]),

                                        # Full form loader (no need for a dummy div, we can trigger based on a real event)
                                        dbc.Row([
                                            dbc.Col(
                                                dcc.Loading(
                                                    id="jd-creation-loading-full-form",
                                                    type="circle",
                                                    children=[
                                                        html.Div(id="jd-creation-response-section", className="mt-4")
                                                    ],
                                                ),
                                                width=12
                                            )
                                        ]),

                                    ]),

                                    # Save and Discard Buttons
                                    dbc.Row([
                                        dbc.Col(dbc.Button("Save", id="jd-creation-save-btn", className="save-btn hide-button"), width=6),
                                        dbc.Col(dbc.Button("Discard", id="jd-creation-reset-btn", className="reset-btn hide-button"), width=6),
                                    ], className="mt-4"),

                                ]),
                                className="form-card"
                            ),
                            width=6
                        ),
                        justify="center",
                    )
                ]
            )
        ]
    )
    return html.Div(jd_form, className="jd-forms")

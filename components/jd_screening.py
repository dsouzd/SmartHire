import dash_bootstrap_components as dbc
from dash import dcc, html


def jdscreen():
    return html.Div(
        id="form-container",
        style={"backgroundColor": "#f7f7f7", "padding": "50px", "minHeight": "100vh"},
        children=[
            dcc.Location(id="jdscreen-url", refresh=False),
            dbc.Container(
                children=[
                    html.Div(id="toast-container", className="toast-container"),
                    # Form starts here
                    dbc.Row(
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H2(
                                            "Profile Screening Form", className="form-title"
                                        ),
                                        html.Br(),
                                        # Business Unit Dropdown
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        "Business Unit",
                                                        className="label-text",
                                                    ),
                                                    width=4,
                                                ),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id="jd-screen-business-unit-dropdown",
                                                        options=[],
                                                        placeholder="Select a business unit",
                                                        className="custom-dropdown",
                                                    ),
                                                    width=8,
                                                ),
                                            ],
                                            className="mb-3",
                                        ),
                                        # JD Dropdown (disabled until BU selected)
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        "Job Descriptions",
                                                        className="label-text",
                                                    ),
                                                    width=4,
                                                ),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id="jd-screen-jd-dropdown",
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
                                        # Upload Resumes Section
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        "Upload Resumes",
                                                        className="label-text",
                                                    ),
                                                    width=4,
                                                ),
                                                dbc.Col(
                                                    dcc.Upload(
                                                        id="jd-screen-upload-data",
                                                        children=html.Div(
                                                            [
                                                                "Drag and Drop or ",
                                                                html.A(
                                                                    "Select Files",
                                                                    className="upload-link",
                                                                ),
                                                            ]
                                                        ),
                                                        className="upload-container",
                                                        multiple=True,
                                                        disabled=True,
                                                    ),
                                                    width=8,
                                                ),
                                            ],
                                            className="mb-3",
                                        ),
                                        # File List Section
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.Ul(
                                                        id="jd-screen-file-list",
                                                        style={
                                                            "listStyleType": "none",
                                                            "paddingLeft": "0",
                                                        },
                                                    ),
                                                    width=12,
                                                )
                                            ]
                                        ),
                                        # Submit and Reset Buttons
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Button(
                                                        "Submit",
                                                        id="jd-screen-submit-btn",
                                                        className="w-100 custom-submit-btn",
                                                        style={"display": "none"},
                                                    )
                                                ),
                                                dbc.Col(
                                                    dbc.Button(
                                                        "Reset",
                                                        id="jd-screen-reset-btn",
                                                        className="w-100 custom-reset-btn",
                                                        style={"display": "none"},
                                                    )
                                                ),
                                            ],
                                            className="mt-4",
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dcc.Loading(
                                                        id="jd-screen-loading-spinner",
                                                        type="circle",
                                                        children=[
                                                            html.Div(
                                                                id="jd-screen-loading-placeholder",
                                                                style={"display": "none"}
                                                            )
                                                        ],
                                                    ),
                                                    className="mt-4",
                                                    width=12,
                                                )
                                            ]
                                        ),
                                        html.Div(
                                            id="jd-screen-screening-results",
                                            className="",
                                        ),
                                        html.Div(id="select-candidate-btn-container"),  # Container for the dynamic button
                                        html.Div(id="select-candidate-clicks", style={"display": "none"}),  # Hidden div for click storage
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

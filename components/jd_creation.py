import dash_bootstrap_components as dbc
from dash import dcc, html

# Define the form layout in a separate function
def jd_form():
    return html.Div(
        id="form-container",  # Styled with the #4d4d4d background
        children=[
            dbc.Container(
                dbc.Row(
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody([
                                html.H2("Job Description Form", className="form-title"),  # White form title
                                html.Br(),
                                # Wrap the entire form in dbc.Form
                                dbc.Form([
                                    # Business Unit Dropdown with a loading spinner
                                    dbc.Row([
                                        dbc.Col(dbc.Label("Business Unit", className="label-text"), width=4),
                                        dbc.Col(
                                            dcc.Loading(
                                                id="loading-business-unit",
                                                type="default",  # Show spinner while loading
                                                children=[
                                                    dcc.Dropdown(
                                                        id='business-unit-dropdown',
                                                        options=[],  # Will be populated dynamically
                                                        placeholder="Select a business unit"
                                                    )
                                                ]
                                            ), width=8
                                        ),
                                    ], className="mb-3"),

                                    # Job Title Input
                                    dbc.Row([
                                        dbc.Col(dbc.Label("Job Title", className="label-text"), width=4),
                                        dbc.Col(
                                            dbc.InputGroup(
                                                [
                                                    dbc.InputGroupText(html.I(className="fas fa-briefcase"), className="input-group-addon"),
                                                    dbc.Input(id="job-title-input", type="text", placeholder="Enter job title"),
                                                ]
                                            ), width=8
                                        ),
                                    ], className="mb-3"),

                                    # Experience Input
                                    dbc.Row([
                                        dbc.Col(dbc.Label("Experience", className="label-text"), width=4),
                                        dbc.Col(
                                            dbc.InputGroup(
                                                [
                                                    dbc.InputGroupText(html.I(className="fas fa-user-tie"), className="input-group-addon"),
                                                    dbc.Input(id="experience-input", type="text", placeholder="Enter experience"),
                                                ]
                                            ), width=8
                                        ),
                                    ], className="mb-3"),

                                    # Skills Input
                                    dbc.Row([
                                        dbc.Col(dbc.Label("Skills", className="label-text"), width=4),
                                        dbc.Col(
                                            dbc.InputGroup(
                                                [
                                                    dbc.InputGroupText(html.I(className="fas fa-tools"), className="input-group-addon"),
                                                    dbc.Input(id="skills-input", type="text", placeholder="Enter required skills"),
                                                ]
                                            ), width=8
                                        ),
                                    ], className="mb-3"),

                                    # Submit Button styled with #a01441
                                    dbc.Row([
                                        dbc.Col(
                                            dbc.Button("Submit", id="submit-btn", color="danger", className="w-100"),  # Styled in CSS to use #a01441
                                            width=12
                                        )
                                    ]),
                                ]),
                            ]),
                            className="form-card"  # Styled with #333 background
                        ),
                        width=6
                    ),
                    justify="center",
                )
            )
        ]
    )

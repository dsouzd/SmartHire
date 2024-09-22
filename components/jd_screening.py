import dash_bootstrap_components as dbc
from dash import dcc, html

def jdscreen():
    return html.Div(
        id="form-container",
        style={"backgroundColor": "#f7f7f7", "padding": "50px", "minHeight": "100vh"},
        children=[
            dcc.Location(id="jdscreen-url", refresh=False),
            dbc.Container(
                dbc.Row(
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody([
                                html.H2("JD Screening Form", className="form-title"),
                                html.Br(),

                                # Business Unit Dropdown
                                dbc.Row([
                                    dbc.Col(
                                        dbc.Label("Business Unit", className="label-text"), width=4
                                    ),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id='jd-screen-business-unit-dropdown',
                                            options=[],
                                            placeholder="Select a business unit",
                                            className="custom-dropdown"
                                        ), width=8
                                    ),
                                ], className="mb-3"),

                                # JD Dropdown (disabled until BU selected)
                                dbc.Row([
                                    dbc.Col(
                                        dbc.Label("Job Descriptions", className="label-text"), width=4
                                    ),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id='jd-screen-jd-dropdown',
                                            options=[],
                                            placeholder="Select a job description",
                                            className="custom-dropdown",
                                            disabled=True
                                        ), width=8
                                    ),
                                ], className="mb-3"),

                                # File Upload Component
                                dbc.Row([
                                    dbc.Col(
                                        dbc.Label("Upload Resumes", className="label-text"), width=4
                                    ),
                                    dbc.Col(
                                        dcc.Upload(
                                            id='jd-screen-upload-data',
                                            children=html.Div([
                                                'Drag and Drop or ',
                                                html.A('Select Files')
                                            ]),
                                            style={
                                                'width': '100%',
                                                'height': '60px',
                                                'lineHeight': '60px',
                                                'borderWidth': '1px',
                                                'borderStyle': 'dashed',
                                                'borderRadius': '5px',
                                                'textAlign': 'center',
                                                'margin': '10px 0'
                                            },
                                            multiple=True,
                                            disabled=True
                                        ), width=8
                                    ),
                                ], className="mb-3"),

                                # File list (View and Remove)
                                dbc.Row([
                                    dbc.Col(
                                        html.Ul(id="jd-screen-file-list", style={'listStyleType': 'none', 'paddingLeft': '0'}), width=12
                                    )
                                ]),

                                # Submit and Reset Buttons
                                dbc.Row([
                                    dbc.Col(dbc.Button("Submit", id="jd-screen-submit-btn", color="success", className="w-100", style={'display': 'none'})),
                                    dbc.Col(dbc.Button("Reset", id="jd-screen-reset-btn", color="secondary", className="w-100", style={'display': 'none'})),
                                ], className="mt-4"),

                                # Spinner to indicate loading (shown during API calls)
                                dcc.Loading(
                                    id="jd-screen-loading-spinner",
                                    type="circle",
                                    fullscreen=False,
                                    children=html.Div(id="jd-screen-loading-placeholder")
                                ),

                                # Table to display screening results
                                html.Div(id="jd-screen-screening-results", className="mt-4")
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
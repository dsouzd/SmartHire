import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

def candidate_table():
    return html.Div(
        id="candidate-table-container",  # Unique ID for the table container
        children=[
            dcc.Store(id='candidate-table-current-page', data=1),  # Store the current page number
            dbc.Toast(
                id="candidate-table-toast",
                header="Notification",
                is_open=False,
                dismissable=True,
                duration=4000,
                style={"position": "fixed", "top": 10, "right": 10, "width": 350}
            ),
            html.Div(
                className="table-wrapper",
                children=[
                    dcc.Dropdown(
                        id='candidate-table-business-unit-dropdown',
                        placeholder="Select a Business Unit",
                        style={'width': '100%'},
                    ),
                    dcc.Dropdown(
                        id='candidate-table-job-dropdown',
                        placeholder="Select a Job Description",
                        style={'width': '100%'},
                    ),
                    dcc.Dropdown(
                        id='candidate-table-status-dropdown',
                        placeholder="Filter by Status",
                        style={'width': '100%'},
                    ),
                    html.Div(
                        id='candidate-table',
                        className='table-responsive',
                        children=[
                            html.Table(className='table', children=[]),  # Table will be filled dynamically
                        ]
                    ),
                    html.Div(id='candidate-table-page-number', style={'textAlign': 'center'}),
                    html.Div(
                        [
                            dbc.Button("Previous", id='candidate-table-previous-page', n_clicks=0, color="primary", style={"margin-right": "5px"}),
                            dbc.Button("Next", id='candidate-table-next-page', n_clicks=0, color="primary"),
                        ],
                        style={"display": "flex", "justify-content": "center", "margin-top": "10px"},
                    ),
                ]
            )
        ]
    )

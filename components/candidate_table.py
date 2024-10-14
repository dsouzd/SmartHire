import dash
from dash import html, dcc

def candidate_table():
    return html.Div(
        id="candidate-table-container",  
        children=[
            dcc.Store(id='candidate-table-current-page', data=1),  
            html.Div(
                id="candidate-table-toast",
                children="",
                style={"display": "none"}, 
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
                        children=[
                            html.Table(children=[]),  
                        ]
                    ),
                    html.Div(id='candidate-table-page-number', style={'textAlign': 'center'}),
                    html.Div(
                        [
                            html.Button("Previous", id='candidate-table-previous-page', n_clicks=0, className="pagination-btn"),
                            html.Button("Next", id='candidate-table-next-page', n_clicks=0, className="pagination-btn"),
                        ],
                        className="pagination-btn-wrapper",
                    ),
                ]
            )
        ]
    )

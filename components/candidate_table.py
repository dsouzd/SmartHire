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
                        style={'width': '50%'},  
                    ),
                    html.Div(
                        id='candidate-table',
                        children=[
                            html.Table(children=[]),  
                        ]
                    ),
                ],
            ),
            html.Div(
                className="pagination-btn-wrapper",
                children=[
                    html.Button(
                        html.I(className="fas fa-chevron-left"),
                        id="candidate-table-previous-page",
                        className="pagination-btn",
                        n_clicks=0,
                    ),
                    html.Span(id='candidate-table-page-number'),
                    html.Button(
                        html.I(className="fas fa-chevron-right"),
                        id="candidate-table-next-page",
                        className="pagination-btn",
                        n_clicks=0,
                    ),
                ]
            ),
        ]
    )

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

def candidate_table():
    return html.Div(
        id="candidate-table-container",
        children=[
            dcc.Store(id="candidate-table-current-page", data=1),
            dcc.Store(id='candidate-table-job-options', data=[]),  # To store job options dynamically
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
                        id="candidate-table-business-unit-dropdown",
                        placeholder="Select a Business Unit",
                        style={"width": "100%"},
                    ),
                    dcc.Dropdown(
                        id="candidate-table-job-dropdown",
                        placeholder="Select a Job Description",
                        style={"width": "100%"},
                    ),
                    dcc.Dropdown(
                        id="candidate-table-status-dropdown",
                        placeholder="Filter by Status",
                        style={"width": "50%"},
                    ),
                    dcc.Loading(
                        id="candidate-table-loading",
                        type="default",
                        children=dbc.Table(id='candidate-table', bordered=True, hover=True, responsive=True)
                    ),
                    html.Div(
                        className="pagination-btn-wrapper",
                        children=[
                            dbc.Button(
                                html.I(className="fas fa-chevron-left"),
                                id="candidate-table-previous-page",
                                className="pagination-btn",
                                n_clicks=0,
                            ),
                            html.Span(id="candidate-table-page-number"),
                            dbc.Button(
                                html.I(className="fas fa-chevron-right"),
                                id="candidate-table-next-page",
                                className="pagination-btn",
                                n_clicks=0,
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

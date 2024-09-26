import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

def jd_table():
    return html.Div(
        id="jd-table-container",  # Unique ID for the table container
        children=[
            dcc.Store(id='jd-table-current-page', data=1),  # Store the current page number
            dbc.Toast(
                id="jd-table-toast",
                header="Error",
                is_open=False,
                dismissable=True,
                icon="danger",
                duration=4000,
                style={"position": "fixed", "top": 10, "right": 10, "width": 350}
            ),
            html.Div(
                className="table-wrapper",
                children=[
                    dcc.Dropdown(
                        id='jd-table-business-unit-dropdown',
                        placeholder="Select a Business Unit",
                        style={'width': '100%'},
                    ),
                    dcc.Loading(
                        id="jd-table-loading",
                        type="default",
                        children=dbc.Table(id='jd-table', bordered=True, hover=True, responsive=True)
                    )
                ],
            ),
            html.Div(
                children=[
                    dbc.Button(html.I(className="fas fa-chevron-left"), id="jd-table-previous-page", className="pagination-btn", n_clicks=0),
                    html.Span(id='jd-table-page-number', style={'margin': '10px'}),
                    dbc.Button(html.I(className="fas fa-chevron-right"), id="jd-table-next-page", className="pagination-btn", n_clicks=0)
                ], 
                style={'text-align': 'center', 'margin-top': '20px'}
            )
        ]
    )


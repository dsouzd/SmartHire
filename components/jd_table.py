import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

def jd_table():
    return html.Div(
        id="jd-table-container",  # Added unique ID to the main container
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
            dcc.Dropdown(
                id='jd-table-business-unit-dropdown',
                placeholder="Select a Business Unit",
                style={'width': '50%', 'margin': '10px auto'},
            ),
            dcc.Loading(
                id="jd-table-loading",
                type="default",
                children=dbc.Table(id='jd-table', bordered=True, hover=True, responsive=True)
            ),
            html.Div(
                children=[
                    dbc.Button("Previous", id="jd-table-previous-page", n_clicks=0, style={'margin': '10px'}),
                    html.Span(id='jd-table-page-number', style={'margin': '10px'}),
                    dbc.Button("Next", id="jd-table-next-page", n_clicks=0, style={'margin': '10px'})
                ], 
                style={'text-align': 'center', 'margin-top': '20px'}
            )
        ]
    )

from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

def jd_table():
    return html.Div([
        dcc.Store(id='jd-table-store'),  # Store to hold JD data
        
        # Container for the dropdown and table
        dbc.Container([
            # Row for Business Unit Dropdown
            dbc.Row([
                dbc.Col([
                    html.H3('Select Business Unit', className='text-center mt-3'),
                    dcc.Loading(
                        id="loading-bu-dropdown",
                        type="circle",
                        children=dcc.Dropdown(
                            id='jd-table-bu-dropdown',
                            placeholder="Select a Business Unit",
                            className="mb-3"
                        )
                    )
                ], width=12),
            ]),

            # Row for JD Table
            dbc.Row([
                dbc.Col([
                    html.H4('Job Descriptions', className='text-center mt-5'),
                    dcc.Loading(
                        id="loading-jd-table",
                        type="default",
                        children=dash_table.DataTable(
                            id='jd-table',
                            columns=[
                                {"name": "ID", "id": "jd_id"},
                                {"name": "Title", "id": "title"},
                                {"name": "Posted Date", "id": "job_posted"},
                                # Adding a Download column for direct links
                                {"name": "Download", "id": "download"},
                            ],
                            style_as_list_view=True,
                            style_header={
                                'backgroundColor': '#a01441',
                                'color': 'white',
                                'fontWeight': 'bold',
                                'fontSize': '16px',
                                'textAlign': 'center'
                            },
                            style_cell={
                                'backgroundColor': '#f5f5f5',
                                'color': '#34495e',
                                'textAlign': 'center',
                                'fontSize': '14px',
                                'padding': '10px',
                                'border': '1px solid #ddd',
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': '#f9f9f9'
                                }
                            ],
                            page_size=5,
                        ),
                    ),
                    html.Div(id='jd-table-output')  # For displaying additional content if needed
                ], width=12),
            ]),
        ], fluid=True)
    ])

from dash import html
import dash_bootstrap_components as dbc

def footer():
    return dbc.Container(
        dbc.Row(
            dbc.Col(
                html.P(
                    'MSG Global© 2024',
                    className='text-center mb-0'
                ),
                width=12
            ),
            className='pt-3'
        ),
        fluid=True,
        className='footer bg-dark text-white mt-auto py-3'
    )

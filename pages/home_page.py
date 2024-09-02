from dash import html
from components.home import home

def home_page():
    return html.Div([
        home()
    ])

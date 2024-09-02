from dash import html
from components.jdforms import jd_form

def jd_creation_page():
    return html.Div([
        jd_form()
    ])

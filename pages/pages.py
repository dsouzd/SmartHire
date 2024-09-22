from dash import html
from components.hero_text import hero_text
from components.hero_banner import hero_banner
from components.jd_creation import jd_form
from components.jd_screening import jdscreen

def home_page():
    return html.Div([
        hero_banner(),
        hero_text(),
    ])

def jd_creation_page():
    return html.Div([
        jd_form(),
    ])
    
def jd_screning_page():
    return html.Div([
        jdscreen(),
    ])
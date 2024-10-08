from dash import html
from components.hero_text import hero_text
from components.hero_banner import hero_banner
from components.jd_creation import jd_form
from components.jd_screening import jdscreen
from components.jd_table import jd_table
from components.carousel import carousel

def home_page():
    return html.Div([
        #carousel(),
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
    
def jd_table_page():
    return html.Div([
        jd_table(),
    ])
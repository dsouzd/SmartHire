from dash import html
from components.hero_text import hero_text
from components.hero_banner import hero_banner
from components.home import home
from components.jdforms import jd_form

def home_page():
    return html.Div([
        hero_banner(),
        hero_text(),
        home()
    ])

def jd_creation_page():
    return html.Div([
        jd_form()
    ])
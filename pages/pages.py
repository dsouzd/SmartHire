from dash import html
from components.banner import banner
from components.hero import hero
from components.hero_banner import hero_banner
from components.home import home
from components.jdforms import jd_form

def home_page():
    return html.Div([
        hero_banner(),
        hero(),
        home()
    ])

def jd_creation_page():
    return html.Div([
        jd_form()
    ])
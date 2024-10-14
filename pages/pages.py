from dash import html
from components.candidate_table import candidate_table
from components.hero_text import hero_text
from components.hero_banner import hero_banner
from components.jd_creation import jd_form
from components.jd_screening import jdscreen
from components.jd_table import jd_table
from components.carousel import carousel
from components.question_generation import questions_screen
from components.statistics import statistics

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
    
def preliminaryquestions_page():
    return html.Div([
        questions_screen(),
    ])
    
def statistics_page():
    return html.Div([
        statistics(),
    ])
    
def candidate_details_page():
    return html.Div([
        candidate_table(),
    ])
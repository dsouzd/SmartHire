from dash import Output, Input
from components.candidate_table import candidate_table
from components.question_generation import questions_screen
from components.statistics import statistics
from pages.pages import home_page, jd_creation_page, jd_screning_page, jd_table_page


def display_page(app):
    @app.callback(Output("page-content", "children"), [Input("route-url", "pathname")])
    def callback(pathname="/"):
        if pathname == "/jdpreparation":
            return candidate_table()
        elif pathname == "/screening":
            return statistics()
        elif pathname == "/jdtable":
            return jd_table_page()
        elif pathname == "/preliminaryquestions":
            return questions_screen()
        else:
            return home_page()

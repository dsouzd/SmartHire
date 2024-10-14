from dash import Output, Input
from pages.pages import candidate_details_page, home_page, jd_creation_page, jd_screning_page, jd_table_page, preliminaryquestions_page, statistics_page


def display_page(app):
    @app.callback(Output("page-content", "children"), [Input("route-url", "pathname")])
    def callback(pathname="/"):
        if pathname == "/jdpreparation":
            return jd_creation_page()
        elif pathname == "/screening":
            return jd_screning_page()
        elif pathname == "/archive":
            return jd_table_page()
        elif pathname == "/candidate-details":
            return candidate_details_page()
        elif pathname == "/statistics":
            return statistics_page()
        elif pathname == "/preliminaryquestions":
            return preliminaryquestions_page()
        else:
            return home_page()

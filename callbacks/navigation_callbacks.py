from dash import Output, Input
from pages.pages import home_page, jd_creation_page, jd_screning_page, jd_table_page


def display_page(app):
    @app.callback(Output("page-content", "children"), [Input("route-url", "pathname")])
    def callback(pathname="/"):
        if pathname == "/jdpreparation":
            return jd_creation_page()
        elif pathname == "/screening":
            return jd_screning_page()
        elif pathname == "/jdtable":
            return jd_table_page()
        else:
            return home_page()

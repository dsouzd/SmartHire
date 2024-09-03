from dash import Output, Input
from pages.home_page import home_page
from pages.jdcreation_page import jd_creation_page

def display_page(app):
    @app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')]
    )
    def callback(pathname='/'):
        if pathname == '/jdpreparation':
            return jd_creation_page()
        else:
            return home_page()
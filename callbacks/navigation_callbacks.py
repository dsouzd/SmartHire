from dash import Output, Input
from pages.pages import home_page, jd_creation_page

def display_page(app):
    @app.callback(
        Output('page-content', 'children'),
        [Input('route-url', 'pathname')]
    )
    def callback(pathname='/'):
        if pathname == '/jdpreparation':
            return jd_creation_page()
        else:
            return home_page()
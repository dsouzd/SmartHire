import dash
from dash import html

def header_callback(app):
    @app.callback(
        [dash.dependencies.Output("navbar-collapse", "is_open"),
         dash.dependencies.Output("navbar-toggler", "children")],
        [dash.dependencies.Input("navbar-toggler", "n_clicks")],
        [dash.dependencies.State("navbar-collapse", "is_open")]
    )
    def toggle_navbar(n_clicks, is_open):
        if n_clicks:
            # Switch between hamburger and "X" icon based on whether navbar is open
            icon = html.I(className="fas fa-times fa-lg", style={"color": "#a01441"}) if not is_open else html.I(className="fas fa-bars fa-lg", style={"color": "#a01441"})
            return not is_open, icon
        return is_open, html.I(className="fas fa-bars fa-lg", style={"color": "#a01441"})

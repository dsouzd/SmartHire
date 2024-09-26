import dash
from dash import html, Input, Output, State, callback_context
import requests


def header_callback(app):
    @app.callback(
        [Output("navbar-collapse", "is_open"), Output("navbar-toggler", "children")],
        [Input("navbar-toggler", "n_clicks"), Input("url", "pathname")],
        [State("navbar-collapse", "is_open")],
    )
    def toggle_navbar(n_clicks_toggler, pathname, is_open):
        ctx = callback_context
        if ctx.triggered and ctx.triggered[0]["prop_id"] == "navbar-toggler.n_clicks":
            icon = (
                html.I(className="fas fa-times fa-lg", style={"color": "#a01441"})
                if not is_open
                else html.I(className="fas fa-bars fa-lg", style={"color": "#a01441"})
            )
            return not is_open, icon
        if pathname:
            return False, html.I(
                className="fas fa-bars fa-lg", style={"color": "#a01441"}
            )
        return is_open, html.I(
            className="fas fa-bars fa-lg", style={"color": "#a01441"}
        )

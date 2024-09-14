import dash

def header_callback(app):
    @app.callback(
        dash.dependencies.Output("navbar-collapse", "is_open"),
        [dash.dependencies.Input("navbar-toggler", "n_clicks")],
        [dash.dependencies.State("navbar-collapse", "is_open")],
    )
    def toggle_navbar(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open
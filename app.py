import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from callbacks.candidate_table import candidate_table_callback
from callbacks.components_callbacks import header_callback
from callbacks.jd_table_callback import jd_table_callback
from callbacks.jf_creation_callbacks import generate_jd
from callbacks.js_screenig_callback import jd_screening_callbacks
from callbacks.navigation_callbacks import display_page
from callbacks.question_gen_callbacks import questions_screen_callbacks
from components.footer import footer
from components.header import header

# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css",
        "https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap",
    ],
    suppress_callback_exceptions=True,
)
# Define the app layout

app.title = "Smart Hire"
app._favicon = "favico.ico"

app.layout = html.Div(
    [
        dcc.Location(id="route-url", refresh=False),
        header(),
        html.Div(id="page-content"),
        footer(),
    ]
)

header_callback(app)
generate_jd(app)
display_page(app)
jd_screening_callbacks(app)
jd_table_callback(app)
questions_screen_callbacks(app)
candidate_table_callback(app)


if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=8080)

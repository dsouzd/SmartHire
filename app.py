import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from callbacks.navigation_callbacks import display_page
from callbacks.jdform_callbacks import generate_jd
from components.header import header
from components.footer import footer

# Initialize the Dash app
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP, 
                                      "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css"], 
                suppress_callback_exceptions=True)
# Define the app layout

app.title = 'Smart Hire' 

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    header(), 
    html.Div(id='page-content'),
    # footer()
])


generate_jd(app)
display_page(app)


if __name__ == '__main__':
    app.run_server(debug=True)

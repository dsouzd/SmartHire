from dash.dependencies import Input, Output, State
import requests
from dash import html

def generate_jd(app):
    @app.callback(
        Output('business-unit-dropdown', 'options'),
        Input('submit-btn', 'n_clicks')  
    )
    def load_business_units(n_clicks):
        url = 'https://smarthire-e32r.onrender.com/businessunits'
    
        response = requests.get(url)
    
        if response.status_code == 200:
            business_units = response.json()['data']
            return [{'label': unit['name'], 'value': unit['id']} for unit in business_units]
    
        return []  
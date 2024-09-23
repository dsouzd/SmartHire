import requests
from dash import Input, Output, State
import dash
from dash import html

def jd_table_callback(app):

    # Callback to populate the Business Unit dropdown with loading spinner
    @app.callback(
        Output('jd-table-bu-dropdown', 'options'),
        Output('jd-table-bu-dropdown', 'disabled'),  # Disable dropdown during loading
        Input('jd-table-bu-dropdown', 'value')
    )
    def update_business_unit_dropdown(_):
        try:
            # Disable the dropdown while loading
            response = requests.get('https://smarthire-e32r.onrender.com/businessunits')
            if response.status_code == 200:
                data = response.json()['data']
                options = [{'label': bu['name'], 'value': bu['id']} for bu in data]
                return options, False  # Enable dropdown after data loads
        except requests.RequestException:
            return [], False  # Return empty options in case of failure

    # Callback to populate the JD Table when a Business Unit is selected
    @app.callback(
        Output('jd-table', 'data'),
        Input('jd-table-bu-dropdown', 'value'),
        prevent_initial_call=True
    )
    def update_jd_table(bu_id):
        if bu_id is None:
            return []
        
        # Show loading spinner while fetching JD data
        try:
            response = requests.get(f'https://smarthire-e32r.onrender.com/businessunits/{bu_id}/jds')
            if response.status_code == 200:
                data = response.json()['data']
                return [
                    {
                        "jd_id": jd['jd_id'], 
                        "title": jd['title'], 
                        "job_posted": jd['job_posted'],
                        # Return HTML anchor tag for the download link
                        "download": f'<a href="https://smarthire-e32r.onrender.com/download?f_name={jd["title"].replace(".docx", "")}&f_type=docx&bu_id={jd["bu_id"]}" target="_blank">Download</a>'
                    }
                    for jd in data
                ]
        except requests.RequestException:
            return []  # Return empty in case of failure

import dash
from dash.dependencies import Input, Output, State
import requests
from dash import html, dcc, callback_context, no_update


def generate_jd(app):
    # Load Business Units
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

    # Combined callback to handle generate JD, view, save, and reset actions
    @app.callback(
        [
            Output('response-section', 'children'),  # To show messages like JD saved/discarded
            Output('save-btn', 'style'),             # Control the visibility of the Save button
            Output('reset-btn', 'style'),            # Control the visibility of the Discard button
            Output('job-title-input', 'value'),      # To reset the Job Title field
            Output('experience-input', 'value'),     # To reset the Experience field
            Output('skills-input', 'value'),         # To reset the Skills field
            Output('business-unit-dropdown', 'value'),  # To reset the Business Unit dropdown
            Output('toast-message', 'is_open'),      # Open/Close the toast notification
            Output('toast-message', 'children'),     # Set the content of the toast message
        ],
        [
            Input('submit-btn', 'n_clicks'),
            Input('save-btn', 'n_clicks'),
            Input('reset-btn', 'n_clicks'),
            Input('response-section', 'children'),  # Dynamically added content for view icon
        ],
        [
            State('job-title-input', 'value'),
            State('experience-input', 'value'),
            State('skills-input', 'value'),
            State('business-unit-dropdown', 'value'),
        ]
    )
    def handle_actions(submit_clicks, save_clicks, reset_clicks, response_section, job_title, experience, skills, bu_id):
        ctx = callback_context
        if not ctx.triggered:
            return no_update, {'display': 'none'}, {'display': 'none'}, no_update, no_update, no_update, no_update, False, ""

        # Get the ID of the triggering input
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # Handle Submit action (generate JD)
        if trigger_id == 'submit-btn' and submit_clicks:
            payload = {
                "job_title": job_title,
                "experience": experience,
                "skills": skills,
                "bu_id": bu_id
            }
            url = "https://smarthire-e32r.onrender.com/generatejd"
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                file_name = response.json().get('file_name')
                # Display file name with icons for viewing and downloading
                return (
                    html.Div([
                        html.P(f"Generated File: {file_name}.docx"),
                        html.I(className="fas fa-eye fa-lg", id='view-file-icon', style={'cursor': 'pointer', 'marginRight': '10px'}, n_clicks=0),
                        html.I(className="fas fa-download fa-lg", id='download-file-icon', style={'cursor': 'pointer', 'marginRight': '10px'})
                    ]),
                    {'display': 'inline-block'},  # Show the save button
                    {'display': 'inline-block'},  # Show the discard button
                    no_update, no_update, no_update, no_update,  # Don't reset form inputs on submit
                    False, "",  # No toast on submit
                )
            return "Error generating JD. Please enter Fill the form", {'display': 'none'}, {'display': 'none'}, no_update, no_update, no_update, no_update, False, ""

        # Handle Save action
        elif trigger_id == 'save-btn' and save_clicks:
            children_list = response_section['props']['children']
            file_name_section = children_list[0]['props']['children']
            file_name = file_name_section.split(": ")[1]
            url = f'https://smarthire-e32r.onrender.com/savejd?bu_id={bu_id}&jd_title={file_name}&is_save=true'
            response = requests.get(url)
            if response.status_code == 200:
                # Reset the form inputs and show success message in toast
                return (
                    "",  # Clear the response section
                    {'display': 'none'},  # Hide the save button
                    {'display': 'none'},  # Hide the discard button
                    "",  # Clear Job Title field
                    "",  # Clear Experience field
                    "",  # Clear Skills field
                    None,  # Clear Business Unit dropdown
                    True,  # Show toast message
                    "JD saved successfully!"  # Toast message content
                )
            return "Error saving JD.", no_update, no_update, no_update, no_update, no_update, no_update, False, ""

        # Handle Reset (Discard) action
        elif trigger_id == 'reset-btn' and reset_clicks:
            children_list = response_section['props']['children']
            file_name_section = children_list[0]['props']['children']
            file_name = file_name_section.split(": ")[1]
            url = f'https://smarthire-e32r.onrender.com/savejd?bu_id={bu_id}&jd_title={file_name}&is_save=false'
            response = requests.get(url)
            if response.status_code == 200:
                # Reset the form inputs and show discard message in toast
                return (
                    "",  # Clear the response section
                    {'display': 'none'},  # Hide the save button
                    {'display': 'none'},  # Hide the discard button
                    "",  # Clear Job Title field
                    "",  # Clear Experience field
                    "",  # Clear Skills field
                    None,  # Clear Business Unit dropdown
                    True,  # Show toast message
                    "JD discarded successfully!"  # Toast message content
                )
            return "Error discarding JD.", no_update, no_update, no_update, no_update, no_update, no_update, False, ""

        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, False, ""

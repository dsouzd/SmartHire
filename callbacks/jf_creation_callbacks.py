import requests
from dash.dependencies import Input, Output, State
from dash import html, dcc, no_update, callback_context
import dash_bootstrap_components as dbc

def generate_jd(app):
    # Load Business Units (on page load)
    @app.callback(
        Output('jd-creation-business-unit-dropdown', 'options'),
        Input('jd-creation-submit-btn', 'n_clicks')
    )
    def load_business_units(n_clicks):
        url = 'https://smarthire-e32r.onrender.com/businessunits'
        try:
            response = requests.get(url, timeout=500)
            print(response)
            if response.status_code == 200:
                business_units = response.json()['data']
                return [{'label': unit['name'], 'value': unit['id']} for unit in business_units]
            return []
        except requests.exceptions.RequestException as e:
            print(f"Error fetching business units: {e}")
            return []

    # Handle JD submission, save/discard actions, and resetting the form
    @app.callback(
        [
            Output('jd-creation-response-section', 'children'),
            Output('jd-creation-save-btn', 'style'),
            Output('jd-creation-reset-btn', 'style'),
            Output('jd-creation-toast-message', 'is_open'),
            Output('jd-creation-toast-message', 'children'),
            Output('jd-creation-toast-message', 'header'),
            Output('jd-creation-business-unit-dropdown', 'disabled'),
            Output('jd-creation-job-title-input', 'disabled'),
            Output('jd-creation-experience-input', 'disabled'),
            Output('jd-creation-skills-input', 'disabled'),
            Output('jd-creation-business-unit-dropdown', 'value'),
            Output('jd-creation-job-title-input', 'value'),
            Output('jd-creation-experience-input', 'value'),
            Output('jd-creation-skills-input', 'value'),
        ],
        [
            Input('jd-creation-submit-btn', 'n_clicks'),
            Input('jd-creation-save-btn', 'n_clicks'),
            Input('jd-creation-reset-btn', 'n_clicks')
        ],
        [
            State('jd-creation-job-title-input', 'value'),
            State('jd-creation-experience-input', 'value'),
            State('jd-creation-skills-input', 'value'),
            State('jd-creation-business-unit-dropdown', 'value')
        ]
    )
    def handle_form_actions(submit_clicks, save_clicks, reset_clicks, job_title, experience, skills, bu_id):
        ctx = callback_context

        # No action triggered
        if not ctx.triggered:
            return no_update, {'display': 'none'}, {'display': 'none'}, False, "", "", False, False, False, False, no_update, no_update, no_update, no_update

        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # Handle Save Button Click (reset form and clear View/Download section)
        if trigger_id == 'jd-creation-save-btn' and save_clicks:
            file_name = f"{job_title}.docx"
            url = f'https://smarthire-e32r.onrender.com/savejd?bu_id={bu_id}&jd_title={file_name}&is_save=true'
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    return (
                        "", {'display': 'none'}, {'display': 'none'},  # Clear the response section and hide buttons
                        True, "Job description saved successfully!", "Success",  # Toast notification
                        False, False, False, False,  # Re-enable inputs
                        None, "", "", ""  # Clear form fields
                    )
                else:
                    return (
                        no_update, no_update, no_update,
                        True, "Failed to save the job description.", "Error",
                        False, False, False, False,
                        no_update, no_update, no_update, no_update
                    )
            except requests.exceptions.RequestException as e:
                return (
                    no_update, no_update, no_update,
                    True, f"Error: {str(e)}", "Request Failed",
                    False, False, False, False,
                    no_update, no_update, no_update, no_update
                )

        # Handle Discard Button Click (reset form and clear View/Download section)
        if trigger_id == 'jd-creation-reset-btn' and reset_clicks:
            file_name = f"{job_title}.docx"
            url = f'https://smarthire-e32r.onrender.com/savejd?bu_id={bu_id}&jd_title={file_name}&is_save=false'
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    return (
                        "", {'display': 'none'}, {'display': 'none'},  # Clear the response section and hide buttons
                        True, "Job description discarded successfully!", "Success",  # Toast notification
                        False, False, False, False,  # Re-enable inputs
                        None, "", "", ""  # Clear form fields
                    )
                else:
                    return (
                        no_update, no_update, no_update,
                        True, "Failed to discard the job description.", "Error",
                        False, False, False, False,
                        no_update, no_update, no_update, no_update
                    )
            except requests.exceptions.RequestException as e:
                return (
                    no_update, no_update, no_update,
                    True, f"Error: {str(e)}", "Request Failed",
                    False, False, False, False,
                    no_update, no_update, no_update, no_update
                )

        # Handle JD Generation (Submit Button)
        if trigger_id == 'jd-creation-submit-btn' and submit_clicks:
            if not job_title or not experience or not skills or not bu_id:
                # Handle empty field errors
                return (
                    no_update, no_update, no_update,
                    True, "Please fill in all the fields!", "Error",
                    False, False, False, False,
                    no_update, no_update, no_update, no_update
                )

            # Disable input fields and show loading animation during processing
            return_list = [no_update] * 13
            return_list[6:] = [True] * 4  # Disable input fields during loading

            # Proceed with the API call after disabling inputs
            payload = {
                "job_title": job_title,
                "experience": experience,
                "skills": skills,
                "bu_id": bu_id
            }

            try:
                url = "https://smarthire-e32r.onrender.com/generatejd"
                response = requests.post(url, json=payload, timeout=30)

                if response.status_code == 200:
                    file_name = response.json().get('file_name')
                    response_content = html.Div([
                        html.P(f"Generated File: {file_name}.docx", className="generated-file-text"),
                        html.Div([
                            html.A(
                                html.I(className="fas fa-eye action-icon text-info"),  # Eye icon for view
                                href=f"https://smarthire-e32r.onrender.com/download?f_name={file_name}&f_type=pdf&bu_id={bu_id}",
                                target="_blank",
                                title="View as PDF"
                            ),
                            html.A(
                                html.I(className="fas fa-download action-icon text-primary"),  # Download icon
                                href=f"https://smarthire-e32r.onrender.com/download?f_name={file_name}&f_type=docx&bu_id={bu_id}",
                                target="_blank",
                                title="Download DOCX"
                            )
                        ], style={'display': 'inline-flex', 'justify-content': 'center', 'align-items': 'center'})
                    ])
                    # Show save and discard buttons after JD generation
                    return (
                        response_content,
                        {'display': 'inline-block'},  # Show save button
                        {'display': 'inline-block'},  # Show discard button
                        True, "Job description generated successfully!", "Success",
                        False, False, False, False,  # Re-enable inputs after success
                        no_update, no_update, no_update, no_update  # Keep form values intact after JD generation
                    )
                else:
                    # Handle non-200 responses
                    return (
                        no_update, no_update, no_update,
                        True, "Failed to generate JD. Please try again.", "Error",
                        False, False, False, False,
                        no_update, no_update, no_update, no_update
                    )

            except requests.exceptions.RequestException as e:
                # Handle request timeout or connection issues
                return (
                    no_update, no_update, no_update,
                    True, f"Error: {str(e)}", "Request Failed",
                    False, False, False, False,
                    no_update, no_update, no_update, no_update
                )

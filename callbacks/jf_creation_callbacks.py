# import dash
# from dash.dependencies import Input, Output, State
# import requests
# from dash import html, dcc, callback_context, no_update

# def generate_jd(app):

#     # Load Business Units
#     @app.callback(
#         Output('business-unit-dropdown', 'options'),
#         Input('submit-btn', 'n_clicks')
#     )
#     def load_business_units(n_clicks):
#         url = 'https://smarthire-e32r.onrender.com/businessunits'

#         response = requests.get(url)
#         if response.status_code == 200:
#             business_units = response.json()['data']
#             return [{'label': unit['name'], 'value': unit['id']} for unit in business_units]

#         return []

#     # Combined callback to handle generate JD, view, save, and reset actions
#     @app.callback(
#         Output('response-section', 'children'),
#         Output('save-btn', 'style'),
#         Output('reset-btn', 'style'),
#         Input('submit-btn', 'n_clicks'),
#         Input('save-btn', 'n_clicks'),
#         Input('reset-btn', 'n_clicks'),
#         Input('response-section', 'children'),  # Dynamically added content for view icon
#         State('job-title-input', 'value'),
#         State('experience-input', 'value'),
#         State('skills-input', 'value'),
#         State('business-unit-dropdown', 'value'),
#     )
#     def handle_actions(submit_clicks, save_clicks, reset_clicks, response_section, job_title, experience, skills, bu_id):
#         ctx = callback_context
#         if not ctx.triggered:
#             return no_update, {'display': 'none'}, {'display': 'none'}

#         # Get the ID of the triggering input
#         trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

#         # Handle Submit action (generate JD)
#         if trigger_id == 'submit-btn' and submit_clicks:
#             payload = {
#                 "job_title": job_title,
#                 "experience": experience,
#                 "skills": skills,
#                 "bu_id": bu_id
#             }
#             url = "http://smarthire-e32r.onrender.com/generatejd"
#             response = requests.post(url, json=payload)

#             if response.status_code == 200:
#                 file_name = response.json().get('file_name')
#                 # Display file name with icons for viewing and downloading
#                 return html.Div([
#                     html.P(f"Generated File: {file_name}.pdf"),
#                     html.I(className="fas fa-eye fa-lg", id='view-file-icon', style={'cursor': 'pointer', 'marginRight': '10px'}, n_clicks=0),
#                     html.I(className="fas fa-download fa-lg", id='download-file-icon', style={'cursor': 'pointer', 'marginRight': '10px'})
#                 ]), {'display': 'inline-block'}, {'display': 'inline-block'}

#             return "Error generating JD.", {'display': 'none'}, {'display': 'none'}

#         # Handle View action (view the file)
#         elif trigger_id == 'response-section' and 'view-file-icon' in response_section:
#             file_name = response_section[0]['props']['children'].split(": ")[1].replace(".pdf", "")
#             url = f'http://smarthire-e32r.onrender.com/download?f_name={file_name}&f_type=pdf&bu_id={bu_id}'

#             # Fetch PDF file from the API
#             response = requests.get(url)
#             if response.status_code == 200:
#                 pdf_data = response.content
#                 return html.Embed(src=f"data:application/pdf;base64,{pdf_data}", type="application/pdf", width="100%", height="600px"), no_update, no_update
#             return "Error fetching the PDF.", no_update, no_update

#         # Handle Save action
#         elif trigger_id == 'save-btn' and save_clicks:
#             file_name = response_section[0]['props']['children'].split(": ")[1].replace(".pdf", "")
#             url = f'http://smarthire-e32r.onrender.com/savejd?bu_id={bu_id}&jd_title={file_name}.docx&is_save=true'
#             response = requests.post(url)
#             if response.status_code == 200:
#                 return "JD saved successfully.", no_update, no_update
#             return "Error saving JD.", no_update, no_update

#         # Handle Reset action
#         elif trigger_id == 'reset-btn' and reset_clicks:
#             file_name = response_section[0]['props']['children'].split(": ")[1].replace(".pdf", "")
#             url = f'http://smarthire-e32r.onrender.com/savejd?bu_id={bu_id}&jd_title={file_name}.docx&is_save=false'
#             response = requests.post(url)
#             if response.status_code == 200:
#                 return "", {'display': 'none'}, {'display': 'none'}
#             return "Error resetting form.", no_update, no_update

#         return no_update, no_update, no_update

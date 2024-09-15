# # jd_creation_callback.py

# from dash import Input, Output, State, callback, html
# import requests

# # Callback for form submission and JD generation
# @callback(
#     [Output('file-output', 'children'),
#      Output('error-output', 'children')],
#     [Input('submit-button', 'n_clicks')],
#     [State('business-unit-dropdown', 'value'),
#      State('job-title', 'value'),
#      State('experience', 'value'),
#      State('skills', 'value')]
# )
# def handle_form_submission(n_clicks, bu_id, job_title, experience, skills):
#     if n_clicks:
#         # Check if all fields are filled
#         if not bu_id or not job_title or not experience or not skills:
#             return '', "Please fill out all fields."
        
#         # Call API to generate JD
#         payload = {
#             "job_title": job_title,
#             "experience": experience,
#             "skills": skills,
#             "bu_id": bu_id
#         }
        
#         response = requests.post('http://smarthire-e32r.onrender.com/generatejd', json=payload)
#         if response.status_code == 200:
#             result = response.json()
#             file_name = result['file_name']
#             return html.Div([
#                 html.P(f"Generated file: {file_name}"),
#                 html.A(html.I(className="fas fa-eye"), href="#", id='eye-icon', style={"margin-left": "10px"}),
#                 html.Div(id='file-preview'),
#                 dbc.Button("Save", id="save-button", color="success", className='ml-2'),
#                 dbc.Button("Reset", id="reset-button", color="danger", className='ml-2')
#             ]), ""
#         else:
#             return '', "Failed to generate JD."
    
#     return '', ''  # Initial state

# # Callback to preview the file
# @callback(
#     Output('file-preview', 'children'),
#     [Input('eye-icon', 'n_clicks')],
#     [State('business-unit-dropdown', 'value'),
#      State('file-output', 'children')]
# )
# def preview_file(n_clicks, bu_id, file_output):
#     if n_clicks:
#         # Extract file name from the file output
#         file_name = file_output[0]['props']['children'][0]
        
#         # Call the download API
#         response = requests.get(f"http://smarthire-e32r.onrender.com/download?f_name={file_name}&f_type=pdf&bu_id={bu_id}")
#         if response.status_code == 200:
#             # Assuming you get a downloadable file, return a download link or file preview
#             file_url = response.content  # Placeholder for the actual file
#             return html.Embed(src=file_url, width="800px", height="600px")  # Embedding PDF in UI
#         else:
#             return "Failed to fetch the file."

#     return ""

# # Callback to handle Save or Reset actions
# @callback(
#     [Output('business-unit-dropdown', 'value'),
#      Output('job-title', 'value'),
#      Output('experience', 'value'),
#      Output('skills', 'value')],
#     [Input('save-button', 'n_clicks'),
#      Input('reset-button', 'n_clicks')],
#     [State('file-output', 'children'),
#      State('business-unit-dropdown', 'value')]
# )
# def handle_save_or_reset(save_clicks, reset_clicks, file_output, bu_id):
#     ctx = dash.callback_context

#     if ctx.triggered and ctx.triggered[0]['prop_id'].split('.')[0] == 'save-button':
#         # Save JD API call
#         file_name = file_output[0]['props']['children'][0] + ".docx"
#         requests.get(f"http://smarthire-e32r.onrender.com/savejd?bu_id={bu_id}&jd_title={file_name}&is_save=true")
#         return None, '', '', ''
    
#     if ctx.triggered and ctx.triggered[0]['prop_id'].split('.')[0] == 'reset-button':
#         # Reset form
#         return None, '', '', ''

#     return dash.no_update

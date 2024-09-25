import base64
import requests
from dash.dependencies import Input, Output, State, ALL
from dash import html, no_update, callback_context, dcc
import dash_bootstrap_components as dbc
import json

def jd_screening_callbacks(app):

    @app.callback(
        Output('jd-screen-business-unit-dropdown', 'options'),
        Input('jdscreen-url', 'pathname')
    )
    def load_business_units(pathname):
        url = 'https://smarthire-e32r.onrender.com/businessunits'
        try:
            response = requests.get(url, timeout=300)
            if response.status_code == 200:
                business_units = response.json()['data']
                return [{'label': unit['name'], 'value': unit['id']} for unit in business_units]
            return []
        except requests.exceptions.RequestException as e:
            print(f"Error fetching business units: {e}")
            return []

    @app.callback(
        [
            Output('jd-screen-jd-dropdown', 'options'),
            Output('jd-screen-jd-dropdown', 'disabled'),
            Output('jd-screen-upload-data', 'disabled'),
            Output('jd-screen-file-list', 'children'),
            Output('jd-screen-submit-btn', 'style'),
            Output('jd-screen-reset-btn', 'style'),
            Output('jd-screen-screening-results', 'children'),
            Output('jd-screen-upload-data', 'filename'),
            Output('jd-screen-upload-data', 'contents'),
            Output('toast-container', 'children'),  # Toast for feedback
            Output('jd-screen-loading-spinner', 'children'),  # For loader
            Output('jd-screen-business-unit-dropdown', 'value'),  # Added Business Unit Dropdown Reset
            Output('jd-screen-jd-dropdown', 'value')  # Added Job Description Dropdown Reset
        ],
        [
            Input('jd-screen-business-unit-dropdown', 'value'),
            Input('jd-screen-jd-dropdown', 'value'),
            Input('jd-screen-upload-data', 'filename'),
            Input('jd-screen-upload-data', 'contents'),
            Input('jd-screen-submit-btn', 'n_clicks'),
            Input('jd-screen-reset-btn', 'n_clicks'),
            Input({'type': 'remove-file-btn', 'index': ALL}, 'n_clicks')
        ],
        [
            State('jd-screen-upload-data', 'filename'),
            State('jd-screen-upload-data', 'contents'),
            State('jd-screen-file-list', 'children')  # Keep track of current file list
        ]
    )
    def handle_actions(bu_id, jd_id, filenames, contents, submit_clicks, reset_clicks, remove_clicks, state_filenames, state_contents, current_file_list):
        ctx = callback_context
        trigger = ctx.triggered[0] if ctx.triggered else None
        trigger_id = trigger['prop_id'].split('.')[0] if trigger else None
        toast_message = []
        loading_output = None

        print(f"trigger id: {trigger_id}")  # Debugging: log the trigger ID

        # Handle Business Unit Dropdown Population
        if trigger_id and 'jd-screen-business-unit-dropdown' in trigger_id and bu_id:
            url = f'https://smarthire-e32r.onrender.com/businessunits/{bu_id}/jds'
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    jd_options = [{'label': jd['title'], 'value': jd['jd_id']} for jd in response.json()['data']]
                    return jd_options, False, True, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
            except requests.exceptions.RequestException:
                toast_message.append(dbc.Toast("Failed to load Business Units", header="Error", duration=4000, is_open=True))
                return [], True, True, no_update, no_update, no_update, no_update, no_update, no_update, toast_message, no_update, no_update, no_update 

        # Enable Job Description and Upload when JD is selected
        if trigger_id == 'jd-screen-jd-dropdown' and jd_id:
            return no_update, no_update, False, no_update, {'display': 'inline-block'}, {'display': 'inline-block'}, no_update, no_update, no_update, no_update, no_update, no_update, no_update

        # Reset the entire form, including Business Unit, JD, and uploaded files
        if trigger_id == 'jd-screen-reset-btn' and reset_clicks:
            toast_message.append(dbc.Toast("Form reset successfully", header="Info", duration=3000, is_open=True))
            return (
                [],  # Clear BU options
                True,  # Disable JD dropdown
                True,  # Disable upload
                [],  # Clear file list
                {'display': 'none'},  # Hide submit button
                {'display': 'none'},  # Hide reset button
                "",  # Clear table
                [],  # Clear filenames
                [],  # Clear contents
                toast_message,  # Show toast message
                no_update,  # No change to spinner
                None,
                None
            )

        # Handle file uploads (triggered by jd-screen-upload-data)
        if trigger_id == 'jd-screen-upload-data' and filenames and contents:
            file_list = []

            # Initialize current_file_list as an empty list if it's None (on first upload)
            if current_file_list is None or len(current_file_list) == 0:
                print("Initializing current_file_list as an empty list")
                current_file_list = []

            # Combine newly uploaded files and existing files for duplicate check
            all_uploaded_filenames = [f['props']['children'][0]['props']['children'] for f in current_file_list] if current_file_list else []

            # Print extracted filenames from current file list for debugging
            print(f"Existing Filenames: {all_uploaded_filenames}")

            # Track if new files are uploaded and if duplicates are found
            duplicates_found = False
            new_files_uploaded = False

            # Loop over the newly uploaded files and check for duplicates
            for filename, content in zip(filenames, contents):
                print(f"Processing uploaded file: {filename}")

                if filename in all_uploaded_filenames:
                    # Show a warning toast if the filename already exists (duplicate detection)
                    print(f"Duplicate file detected: {filename}")
                    toast_message.append(dbc.Toast(f"File {filename} already exists.", header="Duplicate File", duration=3000, is_open=True))
                    duplicates_found = True
                else:
                    # If the file is not a duplicate, add it to the file list
                    content_type = content.split(',')[0]
                    content_string = content.split(',')[1]
                    href_value = f"{content_type};base64,{content_string}"

                    # Append the new file to the file list
                    file_list.append(
                        html.Li([
                            html.Span(filename),
                            html.A(html.I(className="fas fa-download"), href=href_value, download=filename, className="ml-3 btn-icon"),
                            html.Button(html.I(className="fas fa-trash"), id={'type': 'remove-file-btn', 'index': filename}, n_clicks=0, className="ml-3 btn-icon")
                        ])
                    )
                    print(f"Added file: {filename} to the list")
                    all_uploaded_filenames.append(filename)  # Add this file to the overall list
                    current_file_list.append(  # Append to current_file_list for future submissions
                        html.Li([
                            html.Span(filename),
                            html.A(html.I(className="fas fa-download"), href=href_value, download=filename, className="ml-3 btn-icon"),
                            html.Button(html.I(className="fas fa-trash"), id={'type': 'remove-file-btn', 'index': filename}, n_clicks=0, className="ml-3 btn-icon")
                        ])
                    )
                    new_files_uploaded = True

            # If new files are uploaded, update the file list and show the submit button
            if new_files_uploaded:
                return no_update, no_update, False, current_file_list, {'display': 'inline-block'}, no_update, no_update, filenames, contents, toast_message, no_update, no_update, no_update

            # If duplicates are found and no new files, don't show the submit button
            return no_update, no_update, False, current_file_list, no_update, no_update, no_update, filenames, contents, toast_message, no_update, no_update, no_update

        # Handle form submission (triggered by jd-screen-submit-btn)
        if trigger_id == 'jd-screen-submit-btn' and submit_clicks and (current_file_list or filenames):
            # Combine state_filenames with any previously uploaded files
            combined_filenames = state_filenames if state_filenames else []
            combined_contents = state_contents if state_contents else []

            # Print filenames and contents for debugging
            print(f"Submitting all files: {combined_filenames}") 

            url = f"https://smarthire-e32r.onrender.com/screenjd?jd_id={jd_id}&bu_id={bu_id}"
            loading_output = dbc.Spinner(size="md")
            try:
                # Submit all current files (both previously submitted and newly added)
                files = [('profiles', (filename, base64.b64decode(content.split(',')[1]))) for filename, content in zip(combined_filenames, combined_contents)]
                response = requests.post(url, files=files)

                if response.status_code == 200:
                    data = response.json()['data']
                    rows = []
                    for result in data:
                        tooltip_content = " ".join(result['details'])
                        rows.append(
                            html.Tr([
                                html.Td(result['name']),
                                html.Td(result['email']),
                                html.Td(result['score']),
                                dbc.Tooltip(tooltip_content, target=result['email'], placement='right')
                            ])
                        )

                    table = dbc.Table([html.Thead(html.Tr([html.Th("Name"), html.Th("Email"), html.Th("Score")])), html.Tbody(rows)], bordered=True, className="table")
                    table_responsive = html.Div(table, className="table-responsive")
                    toast_message.append(dbc.Toast("Submission successful", header="Success", duration=3000, is_open=True))

                    # Keep the files in the list and allow new files to be appended later
                    return no_update, no_update, False, current_file_list, {'display': 'none'}, {'display': 'inline-block'}, table_responsive, [], [], toast_message, None, no_update, no_update

            except requests.exceptions.RequestException as e:
                toast_message.append(dbc.Toast(f"Error: {str(e)}", header="Error", duration=4000, is_open=True))
                return no_update, no_update, no_update, no_update, no_update, no_update, f"Error: {str(e)}", no_update, no_update, toast_message, None, no_update, no_update

        # Handle file removal
        if trigger_id and trigger_id.startswith('{"index":'):
            try:
                trigger_temp = trigger['prop_id']
                trigger_json = trigger_temp.rsplit('.n_clicks', 1)[0]
                remove_trigger = json.loads(trigger_json)
                remove_index = remove_trigger['index']
                new_filenames = [f for f in state_filenames if f != remove_index]
                new_contents = [c for f, c in zip(state_filenames, state_contents) if f != remove_index]

                file_list = [
                    html.Li([
                        html.Span(filename),
                        html.A(html.I(className="fas fa-download"), href=f"data:{content.split(',')[0]};base64,{content.split(',')[1]}", download=filename, className="ml-3 btn-icon"),
                        html.Button(html.I(className="fas fa-trash"), id={'type': 'remove-file-btn', 'index': filename}, n_clicks=0, className="ml-3 btn-icon")
                    ]) for filename, content in zip(new_filenames, new_contents)
                ]
                return no_update, no_update, False, file_list, no_update, no_update, no_update, new_filenames, new_contents, no_update, no_update, no_update, no_update
            except json.JSONDecodeError:
                return no_update, no_update, no_update, no_update, no_update, no_update, no_update, state_filenames, state_contents, no_update, no_update, no_update

        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

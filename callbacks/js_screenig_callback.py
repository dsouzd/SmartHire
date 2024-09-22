import base64
import requests
from dash.dependencies import Input, Output, State, ALL
from dash import html, no_update, callback_context, dcc
import dash_bootstrap_components as dbc

def jd_screening_callbacks(app):
    # Callback to load Business Units when the page loads
    @app.callback(
        Output('jd-screen-business-unit-dropdown', 'options'),
        Input('jdscreen-url', 'pathname')  # Trigger on page load
    )
    def load_business_units(pathname):
        print("Loading business units...")  # Debugging print
        url = 'https://smarthire-e32r.onrender.com/businessunits'
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                business_units = response.json()['data']
                print("Business Units Loaded:", business_units)  # Debugging print
                return [{'label': unit['name'], 'value': unit['id']} for unit in business_units]
            print("Failed to load business units. Status Code:", response.status_code)
            return []
        except requests.exceptions.RequestException as e:
            print(f"Error fetching business units: {str(e)}")
            return []

    # Handle file uploads, removal, reset, submit, and dropdowns
    @app.callback(
        [
            Output('jd-screen-jd-dropdown', 'options'),
            Output('jd-screen-jd-dropdown', 'disabled'),
            Output('jd-screen-upload-data', 'disabled'),
            Output('jd-screen-file-list', 'children'),  # File list with remove and view options
            Output('jd-screen-submit-btn', 'style'),
            Output('jd-screen-reset-btn', 'style'),
            Output('jd-screen-screening-results', 'children'),
            Output('jd-screen-upload-data', 'filename'),  # Properly update filenames after removal
            Output('jd-screen-upload-data', 'contents'),  # Properly update contents after removal
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
            State('jd-screen-upload-data', 'contents')
        ]
    )
    def handle_actions(bu_id, jd_id, filenames, contents, submit_clicks, reset_clicks, remove_clicks, state_filenames, state_contents):
        ctx = callback_context
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

        print("Triggered by:", trigger_id)  # Log to identify what caused the callback

        # Handle Business Unit Dropdown Population
        if trigger_id == 'jd-screen-business-unit-dropdown' and bu_id:
            print(f"Selected BU ID: {bu_id}")  # Debugging print
            url = f'https://smarthire-e32r.onrender.com/businessunits/{bu_id}/jds'
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    jd_options = [{'label': jd['title'], 'value': jd['jd_id']} for jd in response.json()['data']]
                    print("Job Descriptions Loaded:", jd_options)  # Debugging print
                    return jd_options, False, True, no_update, no_update, no_update, no_update, no_update, no_update
            except requests.exceptions.RequestException as e:
                print(f"Error loading job descriptions: {str(e)}")  # Debugging print
                return [], True, True, no_update, no_update, no_update, no_update, no_update, no_update

        # Handle JD Selection and enable file upload
        if trigger_id == 'jd-screen-jd-dropdown' and jd_id:
            print(f"Selected JD ID: {jd_id}")  # Debugging print
            return no_update, no_update, False, no_update, {'display': 'inline-block'}, {'display': 'inline-block'}, no_update, no_update, no_update

        # Handle file uploads and show uploaded files
        if filenames and contents:
            print(f"Uploaded Files: {filenames}")  # Log uploaded filenames
            file_list = []
            for filename, content in zip(filenames, contents):
                content_type, content_string = content.split(',')
                file_list.append(html.Li([
                    html.Span(filename),
                    dcc.Link("View", href=f"data:{content_type};base64,{content_string}", target="_blank", className="ml-3"),  # Ensure view URL is correct
                    html.Button("Remove", id={'type': 'remove-file-btn', 'index': filename}, n_clicks=0, className="ml-3")
                ]))
            print("Updated file list after upload:", file_list)  # Debugging print
            return no_update, no_update, False, file_list, no_update, no_update, no_update, filenames, contents

        # Handle file removal (check for valid `trigger_id`)
        if trigger_id and trigger_id.startswith('{"index":'):
            remove_trigger = eval(trigger_id)  # Get the index (filename) of the file to remove
            remove_index = remove_trigger['index']

            print(f"File to Remove: {remove_index}")  # Log the file to be removed
            new_filenames = [f for f in state_filenames if f != remove_index]
            new_contents = [c for f, c in zip(state_filenames, state_contents) if f != remove_index]

            file_list = []
            for filename, content in zip(new_filenames, new_contents):
                content_type, content_string = content.split(',')
                file_list.append(html.Li([
                    html.Span(filename),
                    dcc.Link("View", href=f"data:{content_type};base64,{content_string}", target="_blank", className="ml-3"),
                    html.Button("Remove", id={'type': 'remove-file-btn', 'index': filename}, n_clicks=0, className="ml-3")
                ]))

            print("Updated file list after removal:", new_filenames)  # Debugging print
            return no_update, no_update, False, file_list, no_update, no_update, no_update, new_filenames, new_contents

        # Handle reset button click
        if trigger_id == 'jd-screen-reset-btn':
            print("Resetting form...")  # Log for reset
            return [], True, True, [], {'display': 'none'}, {'display': 'none'}, "", [], []  # Clear filenames and contents

        # Handle submit button click
        if trigger_id == 'jd-screen-submit-btn' and state_filenames and state_contents:
            print("Submitting form...")  # Log for submit
            url = f"https://smarthire-e32r.onrender.com/screenjd?jd_id={jd_id}&bu_id={bu_id}"
            print(f"Submit URL: {url}")  # Log the URL being called
            try:
                # Decoding file content from base64 for submission
                files = [('file', (filename, base64.b64decode(content.split(',')[1]))) for filename, content in zip(state_filenames, state_contents)]
                response = requests.post(url, files=files)
                if response.status_code == 200:
                    data = response.json()['data']
                    print("Screening Results:", data)  # Log the results
                    rows = []
                    for result in data:
                        rows.append(html.Tr([
                            html.Td(result['name']),
                            html.Td(result['email']),
                            html.Td(result['score']),
                        ]))
                    table = dbc.Table([html.Thead(html.Tr([html.Th("Name"), html.Th("Email"), html.Th("Score")])), html.Tbody(rows)], bordered=True)
                    return no_update, no_update, False, [], {'display': 'none'}, {'display': 'none'}, table, [], []  # Clear filenames and contents after submit
            except requests.exceptions.RequestException as e:
                print(f"Error submitting form: {str(e)}")  # Log for any submission error
                return no_update, no_update, no_update, no_update, no_update, no_update, f"Error: {str(e)}", no_update, no_update

        # Fallback return to ensure no issue if no conditions are triggered
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

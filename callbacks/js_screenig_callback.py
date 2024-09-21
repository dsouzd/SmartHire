import base64
import io
import requests
from dash import html, dcc
from dash.dependencies import Input, Output, State, ALL
import dash

def jd_screening(app):
    # Callback to fetch and display Business Units
    @app.callback(
        Output('bu-dropdown', 'options'),
        Input('bu-dropdown', 'value')
    )
    def fetch_business_units(_):
        response = requests.get("https://smarthire-e32r.onrender.com/businessunits")
        bu_data = response.json()['data']
        
        if bu_data:
            return [{"label": bu["name"], "value": bu["id"]} for bu in bu_data]
        else:
            return [{"label": "No Business Units Available", "value": ""}]
    
    # Callback to fetch and display Job Descriptions for the selected BU
    @app.callback(
        [Output('jd-dropdown', 'options'), Output('jd-container', 'style')],
        Input('bu-dropdown', 'value')
    )
    def fetch_job_descriptions(bu_id):
        if bu_id:
            response = requests.get(f"http://smarthire-e32r.onrender.com/businessunits/{bu_id}/jds")
            jd_data = response.json()['data']

            if jd_data:
                return [{"label": jd["title"], "value": jd["jd_id"]} for jd in jd_data], {"display": "block"}
            else:
                return [{"label": "No Job Descriptions for this BU", "value": "", "disabled": True}], {"display": "block"}
        return [], {"display": "none"}

    # Callback for handling file uploads, file removal, and updating the display
    @app.callback(
        [Output("file-list", "children"), Output("file-upload-container", "style"), Output("submit-container", "style"), Output("uploaded-files-store", "data"), Output("upload-loading", "style")],
        [Input("upload-data", "contents"), State("upload-data", "filename"), State("upload-data", "last_modified"),
         Input({'type': 'remove-file', 'index': ALL}, 'n_clicks')],
        [State("uploaded-files-store", "data")]
    )
    def handle_files(contents, filenames, last_modified, n_clicks, current_uploaded_files):
        print("handle_files callback triggered")
        print(f"Contents: {contents}")
        print(f"Filenames: {filenames}")

        if current_uploaded_files is None:
            current_uploaded_files = []  # Initialize empty if the store is empty

        loading_style = {"display": "none"}  # Default loading style is hidden

        ctx = dash.callback_context  # Access dash callback context
        if contents is not None:
            # Handle file uploads
            print("Received contents:")
            print(contents)
            print("Filenames:")
            print(filenames)

            # Encode the binary file as a Base64 string before storing in dcc.Store
            for content, filename in zip(contents, filenames):
                content_type, content_string = content.split(',')

                # Store Base64 content instead of binary data
                current_uploaded_files.append({
                    'filename': filename,
                    'content': content_string  # Store Base64 string
                })

            loading_style = {"display": "none"}  # Hide the loading spinner after upload
        elif ctx.triggered and 'remove-file' in ctx.triggered[0]['prop_id']:
            # Handle file removal
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            remove_index = eval(button_id)['index']
            if n_clicks[remove_index]:
                current_uploaded_files.pop(remove_index)

        # Generate the file list with "X" buttons for removal
        file_list = [
            html.Div([
                html.Span(file['filename']),
                html.Button('X', id={'type': 'remove-file', 'index': i}, n_clicks=0)
            ], className='file-item')
            for i, file in enumerate(current_uploaded_files)
        ]
        
        # Debugging: Check what files are stored after upload
        print("Updated stored files in dcc.Store:")
        print(current_uploaded_files)

        # Return the updated file list and update the store with the new files
        return file_list, {"display": "block"}, {"display": "block"}, current_uploaded_files, loading_style

    # Callback for handling form submission
    @app.callback(
        [Output("loading-animation", "children"), Output("output-table", "children")],
        Input("submit-button", "n_clicks"),
        State("jd-dropdown", "value"),
        State("bu-dropdown", "value"),
        State("uploaded-files-store", "data")  # Read uploaded files from the store
    )
    def submit_data(n_clicks, jd_id, bu_id, uploaded_files):
        if n_clicks and jd_id and bu_id:
            loading_animation = html.Div(className="spinner")  # Show spinner during processing

            # Check if uploaded_files has any content
            if not uploaded_files:
                error_message = "No files uploaded. Please upload files before submitting."
                return loading_animation, html.Div(error_message, className="error-message")

            # Prepare the files for the API request
            files_payload = [
                # Decode Base64 back into bytes when sending to the API
                ('profiles', (file['filename'], io.BytesIO(base64.b64decode(file['content']))))
                for file in uploaded_files
            ]

            # Debugging: Output the filenames and payload structure before sending
            print(f"Sending files: {[file['filename'] for file in uploaded_files]}")
            print(f"Payload: {files_payload}")

            # Send the request with files
            response = requests.post(
                f"http://smarthire-e32r.onrender.com/screenjd?jd_id={jd_id}&bu_id={bu_id}",
                files=files_payload
            )

            # Debugging: Output the server response for debugging purposes
            print(f"Response Status: {response.status_code}")
            print(f"Response Content: {response.text}")

            # Check if the response contains the 'data' key
            if response.status_code == 200 and 'data' in response.json():
                candidates = response.json()['data']

                # Build results table
                table = html.Table(
                    [
                        html.Tr([html.Th("Candidate Name"), html.Th("Score"), html.Th("Details")]),
                        *[
                            html.Tr([
                                html.Td(candidate["name"]),
                                html.Td(candidate["score"]),
                                html.Td(html.Span([
                                    "Hover for details",  # The visible text
                                    html.Span(candidate["details"], className="tooltip-text")  # The tooltip content
                                ], className="tooltip"))
                            ]) for candidate in candidates
                        ]
                    ],
                )
                return loading_animation, table
            else:
                # Gracefully handle the error when 'data' is missing
                error_message = f"Error: {response.status_code} - {response.reason}. No data returned from the server."
                return loading_animation, html.Div(error_message, className="error-message")

        return None, None

from dash import dcc, html

def jd_screnning():
    return html.Div(
        className="main-container",
        children=[
            dcc.Store(id="uploaded-files-store"),  # Store to hold uploaded files
            html.Div(
                className="form-container",
                children=[
                    html.Div(
                        id="bu-container",  # Wrapper for BU dropdown
                        className="dropdown-container",
                        children=[
                            dcc.Dropdown(
                                id="bu-dropdown",
                                placeholder="Loading Business Units...",
                                clearable=False,
                                className="dropdown-style"
                            ),
                        ],
                    ),
                    html.Div(
                        id="jd-container",  # Wrapper for JD dropdown
                        className="dropdown-container",
                        children=[
                            dcc.Dropdown(
                                id="jd-dropdown",
                                placeholder="Select Job Description",
                                clearable=False,
                                className="dropdown-style"
                            ),
                        ],
                        style={"display": "none"},  # Initially hidden
                    ),
                    html.Div(
                        id="file-upload-container",
                        className="file-upload-container",
                        children=[
                            dcc.Upload(
                                id="upload-data",
                                children=html.Div(
                                    ["Drag and Drop or ", html.A("Select Files")],
                                ),
                                multiple=True,
                                className="upload-box"
                            ),
                            html.Div(id="upload-loading", className="loading-animation", style={"display": "none"}),  # Spinner for loading animation
                            html.Div(id="file-list", className="file-list-container"),  # Uploaded files will be shown here
                        ],
                        style={"display": "none"},  # Initially hidden
                    ),
                    html.Div(
                        id="submit-container",
                        className="submit-container",
                        children=[
                            html.Button("Submit", id="submit-button", className="submit-button"),
                            html.Button("Reset", id="reset-button", className="reset-button"),
                        ],
                        style={"display": "none"},  # Initially hidden, shown when file is uploaded
                    ),
                    html.Div(id="loading-animation"),  # Animation during submit process
                    html.Div(id="output-table"),  # Table with results
                ],
            ),
        ],
    )

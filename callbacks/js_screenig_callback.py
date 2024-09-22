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
        except requests.exceptions.RequestException:
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
        trigger = ctx.triggered[0] if ctx.triggered else None
        trigger_id = trigger['prop_id'].split('.')[0] if trigger else None

        if trigger_id and 'jd-screen-business-unit-dropdown' in trigger_id and bu_id:
            url = f'https://smarthire-e32r.onrender.com/businessunits/{bu_id}/jds'
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    jd_options = [{'label': jd['title'], 'value': jd['jd_id']} for jd in response.json()['data']]
                    return jd_options, False, True, no_update, no_update, no_update, no_update, no_update, no_update
            except requests.exceptions.RequestException:
                return [], True, True, no_update, no_update, no_update, no_update, no_update, no_update

        if trigger_id == 'jd-screen-jd-dropdown' and jd_id:
            return no_update, no_update, False, no_update, {'display': 'inline-block'}, {'display': 'inline-block'}, no_update, no_update, no_update

        if trigger_id == 'jd-screen-reset-btn' and reset_clicks:
            return [], True, True, [], {'display': 'none'}, {'display': 'none'}, "", [], []

        if trigger_id == 'jd-screen-submit-btn' and submit_clicks and state_filenames and state_contents:
            url = f"https://smarthire-e32r.onrender.com/screenjd?jd_id={jd_id}&bu_id={bu_id}"
            try:
                files = [('profiles', (filename, base64.b64decode(content.split(',')[1]))) for filename, content in zip(state_filenames, state_contents)]
                response = requests.post(url, files=files)

                if response.status_code == 200:
                    data = response.json()['data']
                    rows = [
                        html.Tr([
                            html.Td(result['name']),
                            html.Td(result['email']),
                            html.Td(result['score'])
                        ]) for result in data
                    ]
                    table = dbc.Table([html.Thead(html.Tr([html.Th("Name"), html.Th("Email"), html.Th("Score")])), html.Tbody(rows)], bordered=True)
                    return no_update, no_update, False, [], {'display': 'none'}, {'display': 'none'}, table, [], []
            except requests.exceptions.RequestException as e:
                return no_update, no_update, no_update, no_update, no_update, no_update, f"Error: {str(e)}", no_update, no_update

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
                        dcc.Link("View", href=f"data:{content.split(',')[0]};base64,{content.split(',')[1]}", target="_blank", className="ml-3"),
                        html.Button("Remove", id={'type': 'remove-file-btn', 'index': filename}, n_clicks=0, className="ml-3")
                    ]) for filename, content in zip(new_filenames, new_contents)
                ]
                return no_update, no_update, False, file_list, no_update, no_update, no_update, new_filenames, new_contents
            except json.JSONDecodeError:
                return no_update, no_update, no_update, no_update, no_update, no_update, no_update, state_filenames, state_contents

        if filenames and contents:
            file_list = []

            for filename, content in zip(filenames, contents):
                content_type = content.split(',')[0]  
                content_string = content.split(',')[1]  

                href_value = f"{content_type};base64,{content_string}"


                file_list.append(
                    html.Li([
                        html.Span(filename),
                        html.A("Download", href=href_value, download=filename, className="ml-3"),
                        html.Button("Remove", id={'type': 'remove-file-btn', 'index': filename}, n_clicks=0, className="ml-3")
                    ])
                )

            return no_update, no_update, False, file_list, no_update, no_update, no_update, filenames, contents


        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

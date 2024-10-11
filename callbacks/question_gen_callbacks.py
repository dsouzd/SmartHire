import base64
import json
import os

import dash_bootstrap_components as dbc
import requests
from dash import callback_context, dcc, html, no_update
from dash.dependencies import ALL, Input, Output, State
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

def questions_screen_callbacks(app):

    @app.callback(
        Output("questions-business-unit-dropdown", "options"),
        Input("questions-url", "pathname"),
    )
    def load_business_units(pathname):
        # Fetch business units
        url = f"{API_BASE_URL}/businessunits"
        try:
            response = requests.get(url, timeout=300)
            if response.status_code == 200:
                business_units = response.json()["data"]
                return [{"label": unit["name"], "value": unit["id"]} for unit in business_units]
            return []
        except requests.exceptions.RequestException as e:
            print(f"Error fetching business units: {e}")
            return []

    @app.callback(
        [
            Output("questions-jd-dropdown", "options"),
            Output("questions-jd-dropdown", "disabled"),
        ],
        Input("questions-business-unit-dropdown", "value"),
    )
    def load_jds(business_unit_id):
        if not business_unit_id:
            return [], True
        url = f"{API_BASE_URL}/businessunits/{business_unit_id}/jds"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                jds = response.json()["data"]
                return [{"label": jd["title"], "value": jd["jd_id"]} for jd in jds], False
            return [], True
        except requests.exceptions.RequestException:
            return [], True

    @app.callback(
        Output("questions-results", "children"),
        [
            Input("questions-submit-btn", "n_clicks"),
            Input("questions-reset-btn", "n_clicks"),
        ],
        [
            State("questions-business-unit-dropdown", "value"),
            State("questions-jd-dropdown", "value")
        ]
    )
    def handle_form_actions(submit_clicks, reset_clicks, business_unit_id, jd_id):
        ctx = callback_context
        trigger = ctx.triggered[0]["prop_id"].split(".")[0]

        # Handle reset action
        if trigger == "questions-reset-btn":
            return no_update

        # Handle submit action
        if trigger == "questions-submit-btn" and business_unit_id and jd_id:
            url = f"{API_BASE_URL}/screenedcandidates?jd_id={jd_id}&bu_id={business_unit_id}"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    candidates = response.json()["data"]
                    rows = []
                    for candidate in candidates:
                        rows.append(html.Tr([
                            html.Td(dcc.Checklist(
                                id={"type": "candidate-select-checkbox", "index": candidate["id"]},
                                options=[{"label": "", "value": "selected"}],
                                value=[], className="candidate-checkbox"
                            )),
                            html.Td(candidate["name"]),
                            html.Td(candidate["email"]),
                            html.Td(candidate["phone"]),
                            html.Td(candidate["status"])
                        ]))
                    table = dbc.Table([html.Thead(html.Tr([html.Th("Select"), html.Th("Name"), html.Th("Email"), html.Th("Phone"), html.Th("Status")])), html.Tbody(rows)], bordered=True)
                    invite_button = dbc.Button("Invite", id="questions-invite-btn", className="w-100 custom-submit-btn")
                    return [table, invite_button]
            except requests.exceptions.RequestException as e:
                print(f"Error fetching candidates: {e}")
                return []

        return no_update

    @app.callback(
        Output("questions-toast-container", "children"),
        Input("questions-invite-btn", "n_clicks"),
        [
            State("questions-jd-dropdown", "value"),
            State("questions-business-unit-dropdown", "value"),
            State({"type": "candidate-select-checkbox", "index": ALL}, "value"),
            State({"type": "candidate-select-checkbox", "index": ALL}, "id")
        ]
    )
    def send_invites(n_clicks, jd_id, bu_id, selected_values, candidate_ids):
        if not n_clicks or not jd_id or not bu_id:
            return no_update
    
        selected_candidates = [candidate_id["index"] for value, candidate_id in zip(selected_values, candidate_ids) if value]
        
        if selected_candidates:
            body = {
                "jd_id": jd_id,
                "bu_id": bu_id,
                "candidate_list": selected_candidates
            }
            url = f"{API_BASE_URL}/sendpreliminaryquestions"
            
            try:
                response = requests.post(url, json=body)
                if response.status_code == 200:
                    return dbc.Toast("Invite sent successfully!", header="Success", duration=3000, is_open=True)
                else:
                    return dbc.Toast("Error sending invite! Please try again", header="Error", duration=3000, is_open=True)
            except requests.exceptions.RequestException as e:
                return dbc.Toast(f"Request failed: {str(e)}", header="Error", duration=3000, is_open=True)
        
        return no_update


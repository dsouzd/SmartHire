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
        url = f"{API_BASE_URL}/businessunits"
        try:
            response = requests.get(url, timeout=30)
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
        print(f"Business Unit ID selected: {business_unit_id}")
        if not business_unit_id:
            return [], True
        url = f"{API_BASE_URL}/businessunits/{business_unit_id}/jds"
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                jds = response.json()["data"]
                return [{"label": jd["title"], "value": jd["jd_id"]} for jd in jds], False
            return [], True
        except requests.exceptions.RequestException:
            return [], True

    @app.callback(
        [
            Output("questions-results", "children"),
            Output("questions-jd-dropdown", "value"),
            Output("questions-business-unit-dropdown", "value"),
            Output("questions-invite-btn", "disabled"),
            Output("questions-toast-container", "children"),
            Output("questions-submit-btn", "disabled"),
            Output("questions-reset-btn", "disabled"),
            Output("questions-invite-btn", "style"),
            Output("loading-output", "children"),
        ],
        [
            Input("questions-submit-btn", "n_clicks"),
            Input("questions-reset-btn", "n_clicks"),
            Input("questions-invite-btn", "n_clicks"),
            Input("questions-business-unit-dropdown", "value"),  
            Input("questions-jd-dropdown", "value"),            
        ],
        State({"type": "candidate-select-checkbox", "index": ALL}, "value"),
        State({"type": "candidate-select-checkbox", "index": ALL}, "id")
    )
    def handle_form_actions(submit_clicks, reset_clicks, invite_clicks, business_unit_id, jd_id, selected_values, candidate_ids):
        ctx = callback_context
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
        print(f"Triggered ID: {triggered_id}")
        print(f"Business Unit ID: {business_unit_id}, Job Description ID: {jd_id}")
    
        invite_style = {"display": "none"}
        invite_disabled = True
        loading_message = None  # Initialize loading message
    
        if triggered_id == "questions-reset-btn":
            print("Reset button clicked.")
            return [], None, None, True, no_update, True, True, invite_style, no_update
    
        if triggered_id == "questions-submit-btn":
            print("Submit button clicked.")
            if business_unit_id and jd_id:
                print("Business unit and Job Description selected. Making API call.")
                url = f"{API_BASE_URL}/screenedcandidates?jd_id={jd_id}&bu_id={business_unit_id}"
                try:
                    response = requests.get(url, timeout=30)
                    if response.status_code == 200:
                        candidates = response.json()["data"]
                        if not candidates:
                            print("No candidates found.")
                            return ["No candidates screened for this Job Description and Business Unit."], no_update, business_unit_id, invite_disabled, no_update, True, True, invite_style, no_update
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
                        invite_style = {"display": "block"}
                        print("Candidates loaded successfully.")
                        return [table], no_update, business_unit_id, False, no_update, False, False, invite_style, no_update
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching candidates: {e}")
                    return [], no_update, business_unit_id, invite_disabled, no_update, True, True, invite_style, no_update
    
        if triggered_id == "questions-invite-btn":
            print("Invite button clicked.")
            selected_candidates = [candidate_id["index"] for value, candidate_id in zip(selected_values, candidate_ids) if value]
            print(f"Selected Candidates: {selected_candidates}")
        
            if not selected_candidates:
                invite_style = {"display": "block"}
                toast_message = dbc.Toast("Please select at least one candidate.", header="Warning", duration=3000, is_open=True)
                print("No candidates selected. Showing warning toast.")
                return no_update, no_update, business_unit_id, False, toast_message, False, False, invite_style, no_update
        
            body = {
                "jd_id": jd_id,
                "bu_id": business_unit_id,
                "candidate_list": selected_candidates
            }
            url = f"{API_BASE_URL}/sendpreliminaryquestions"
        
            # Disable buttons when API call is made
            invite_disabled = True
            submit_disabled = True
            reset_disabled = True
            loading_message = dcc.Loading(type="circle")    
            print("Disabling buttons for API call.")
        
            try:
                response = requests.post(url, json=body, timeout=30)
                if response.status_code == 200:
                    print("Invite sent successfully.")
                    return [], None, None, True, dbc.Toast("Invite sent successfully!", header="Success", duration=3000, is_open=True), False, False, invite_style, no_update
                else:
                    invite_disabled = False  # Re-enable the invite button on error
                    invite_style = {"display": "block"}
                    print("Failed to send invite.")
                    return no_update, no_update, business_unit_id, invite_disabled, dbc.Toast("Error sending invite! Please try again.", header="Error", duration=3000, is_open=True), False, False, invite_style, no_update
        
            except requests.exceptions.RequestException as e:
                invite_disabled = False  # Re-enable the invite button on exception
                invite_style = {"display": "block"}
                print(f"Request failed: {str(e)}")
                return no_update, no_update, business_unit_id, invite_disabled, dbc.Toast(f"Request failed: {str(e)}. Please try again.", header="Error", duration=3000, is_open=True), False, False, invite_style, no_update

        # Check and set submit and reset button states
        submit_disabled = not (business_unit_id and jd_id)
        reset_disabled = not (business_unit_id and jd_id)

        # Debug print for button states
        print(f"Submit Disabled: {submit_disabled}, Reset Disabled: {reset_disabled}, Invite Disabled: {invite_disabled}")
        return no_update, no_update, business_unit_id, invite_disabled, no_update, submit_disabled, reset_disabled, invite_style, loading_message

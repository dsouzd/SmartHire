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
        [State({"type": "candidate-select-checkbox", "index": ALL}, "value"),
         State({"type": "candidate-select-checkbox", "index": ALL}, "id")]
    )
    def handle_form_actions(submit_clicks, reset_clicks, invite_clicks, business_unit_id, jd_id, selected_values, candidate_ids):
        ctx = callback_context
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

        invite_style = {"display": "none"}
        invite_disabled = True
        loading_message = None

        if triggered_id == "questions-reset-btn":
            return [], None, None, True, no_update, True, True, invite_style, no_update

        if triggered_id == "questions-submit-btn":
            if business_unit_id and jd_id:
                url = f"{API_BASE_URL}/screenedcandidates?jd_id={jd_id}&bu_id={business_unit_id}&status=Screening: Selected"
                try:
                    response = requests.get(url, timeout=30)
                    if response.status_code == 200:
                        candidates = response.json()["data"]
                        if not candidates:
                            return ["No candidates screened for this Job Description and Business Unit."], no_update, business_unit_id, invite_disabled, no_update, True, True, invite_style, no_update

                        table_header = html.Thead(html.Tr([
                            html.Th(dcc.Checklist(
                                id="select-all-checkbox",  
                                options=[{"label": "", "value": "all"}],
                                value=[],  
                                className="candidate-checkbox"
                            )),
                            html.Th("Name"),
                            html.Th("Email"),
                            html.Th("Phone"),
                            html.Th("Screen Score")
                        ]))

                        rows = []
                        for candidate in candidates:
                            rows.append(html.Tr([
                                html.Td(dcc.Checklist(
                                    id={"type": "candidate-select-checkbox", "index": candidate["id"]},
                                    options=[{"label": "", "value": "selected"}],
                                    value=[],  # Individual checkboxes initially unselected
                                    className="candidate-checkbox"
                                )),
                                html.Td(candidate["name"]),
                                html.Td(candidate["email"]),
                                html.Td(candidate["phone"]),
                                html.Td(candidate["screen_score"]),
                            ]))

                        table = dbc.Table(
                            [table_header, html.Tbody(rows)],
                            bordered=True
                        )

                        invite_style = {"display": "block"}
                        return [table], no_update, business_unit_id, False, no_update, False, False, invite_style, no_update

                except requests.exceptions.RequestException as e:
                    return [], no_update, business_unit_id, invite_disabled, no_update, True, True, invite_style, no_update

        if triggered_id == "questions-invite-btn":
            selected_candidates = [candidate_id["index"] for value, candidate_id in zip(selected_values, candidate_ids) if value]

            if not selected_candidates:
                invite_style = {"display": "block"}
                toast_message = dbc.Toast("Please select at least one candidate.", header="Warning", duration=3000, is_open=True)
                return no_update, no_update, business_unit_id, False, toast_message, False, False, invite_style, no_update

            body = {
                "jd_id": jd_id,
                "bu_id": business_unit_id,
                "candidate_list": selected_candidates
            }
            url = f"{API_BASE_URL}/sendpreliminaryquestions"

            loading_message = dcc.Loading(type="circle", fullscreen=True)

            try:
                response = requests.post(url, json=body, timeout=300)
                if response.status_code == 200:
                    return [], None, None, True, dbc.Toast("Invite sent successfully!", header="Success", duration=3000, is_open=True), False, False, invite_style, no_update
                else:
                    invite_disabled = False
                    invite_style = {"display": "block"}
                    return no_update, no_update, business_unit_id, invite_disabled, dbc.Toast("Error sending invite! Please try again.", header="Error", duration=3000, is_open=True), False, False, invite_style, no_update

            except requests.exceptions.RequestException as e:
                invite_disabled = False
                invite_style = {"display": "block"}
                return no_update, no_update, business_unit_id, invite_disabled, dbc.Toast(f"Request failed: {str(e)}. Please try again.", header="Error", duration=3000, is_open=True), False, False, invite_style, no_update

        submit_disabled = not (business_unit_id and jd_id)
        reset_disabled = not (business_unit_id and jd_id)

        return no_update, no_update, business_unit_id, invite_disabled, no_update, submit_disabled, reset_disabled, invite_style, loading_message

    @app.callback(
        Output({"type": "candidate-select-checkbox", "index": ALL}, "value"),
        Input("select-all-checkbox", "value"),
        [State({"type": "candidate-select-checkbox", "index": ALL}, "id")]
    )
    def update_all_checkboxes(select_all, candidate_ids):
        if "all" in select_all:
            return [["selected"]] * len(candidate_ids)  
        return [[]] * len(candidate_ids)  
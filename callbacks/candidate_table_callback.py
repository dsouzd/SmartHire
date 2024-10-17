import os
from datetime import datetime

import dash
import requests
from dash import html
from dash.dependencies import Input, Output, State
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

ROWS_PER_PAGE = 5

def candidate_table_callback(app):

    @app.callback(
        [
            Output("candidate-table-business-unit-dropdown", "options"),
            Output("candidate-table-job-dropdown", "options"),
            Output("candidate-table-status-dropdown", "options"),
            Output("candidate-table", "children"),
            Output("candidate-table-page-number", "children"),
            Output("candidate-table-current-page", "data"),
            Output("candidate-table-toast", "is_open"),
            Output("candidate-table-toast", "children"),
            Output("candidate-table-previous-page", "style"),
            Output("candidate-table-next-page", "style"),
            Output("candidate-table-page-number", "style"),
        ],
        [
            Input("candidate-table-business-unit-dropdown", "value"),
            Input("candidate-table-job-dropdown", "value"),
            Input("candidate-table-status-dropdown", "value"),
            Input("candidate-table-previous-page", "n_clicks"),
            Input("candidate-table-next-page", "n_clicks"),
        ],
        [State("candidate-table-current-page", "data")],
    )
    def candidate_table_update(bu_id, jd_id, status_filter, prev_clicks, next_clicks, current_page):
        # Initialize toast properties
        toast_open = False
        toast_message = ""

        # Initialize dropdown options
        dropdown_options_bu = []
        dropdown_options_jd = []
        status_options = [
            {"label": "All", "value": ""},
            {"label": "Screening: Rejected", "value": "Screening: Rejected"},
            {"label": "Screening: Selected", "value": "Screening: Selected"},
            {"label": "Applied", "value": "Applied"},
            {"label": "Screened", "value": "Screened"},
            {"label": "Preliminary: Attended", "value": "Preliminary: Attended"},
            {"label": "Preliminary: Invite Sent", "value": "Preliminary: Invite Sent"},
        ]

        # Fetch Business Units
        try:
            response_bu = requests.get(f"{API_BASE_URL}/businessunits")
            response_bu.raise_for_status()
            business_units = response_bu.json().get("data", [])
            dropdown_options_bu = [
                {"label": bu["name"], "value": bu["id"]} for bu in business_units
            ]
        except requests.exceptions.RequestException:
            toast_open = True
            toast_message = "Business Unit loading failed."
            return (
                [],  # Business Units options
                [],  # Job Description options
                [],  # Status options
                html.Div("Error loading data.", className='docs-message'),
                "",
                1,
                toast_open,
                toast_message,
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
            )

        # If Business Unit not selected
        if bu_id is None:
            return (
                dropdown_options_bu,
                [],  # No job options yet
                status_options,  # Status options
                html.Div("Please select a Business Unit.", className='docs-message'),
                "",
                1,
                False,
                "",
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
            )

        # Fetch Job Descriptions based on Business Unit
        try:
            url = f"{API_BASE_URL}/businessunits/{bu_id}/jds"
            response_jds = requests.get(url, timeout=10)
            response_jds.raise_for_status()
            jds = response_jds.json().get("data", [])
            dropdown_options_jd = [
                {"label": jd["title"], "value": jd["jd_id"]} for jd in jds
            ]
        except requests.exceptions.RequestException:
            toast_open = True
            toast_message = "Job Descriptions loading failed."
            return (
                dropdown_options_bu,
                [],  # No job options if fetching fails
                status_options,
                html.Div("Error loading Job Descriptions.", className='docs-message'),
                "",
                1,
                toast_open,
                toast_message,
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
            )

        # If Job Description not selected
        if jd_id is None:
            return (
                dropdown_options_bu,
                dropdown_options_jd,
                status_options,
                html.Div("Please select a Job Description.", className='docs-message'),
                "",
                1,
                False,
                "",
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
            )

        # Fetch Candidate Details based on selected Business Unit and Job Description
        try:
            url_candidates = f"{API_BASE_URL}/screenedcandidates?jd_id={jd_id}&bu_id={bu_id}"
            response_candidates = requests.get(url_candidates, timeout=10)
            response_candidates.raise_for_status()
            candidates = response_candidates.json().get("data", [])

            # Filter candidates based on status
            if status_filter:
                candidates = [c for c in candidates if c["status"] == status_filter]

            total_candidates = len(candidates)
            total_pages = (total_candidates // ROWS_PER_PAGE) + (
                1 if total_candidates % ROWS_PER_PAGE > 0 else 0
            )

            if total_candidates == 0:
                return (
                    dropdown_options_bu,
                    dropdown_options_jd,
                    status_options,
                    html.Div("No candidates available for the selected Job Description.", className='docs-message'),
                    "",
                    1,
                    False,
                    "",
                    {"display": "none"},
                    {"display": "none"},
                    {"display": "none"},
                )

            # Determine which input triggered the callback
            ctx = dash.callback_context
            if ctx.triggered:
                button_id = ctx.triggered[0]["prop_id"].split(".")[0]
                if button_id == "candidate-table-next-page" and current_page < total_pages:
                    current_page += 1
                elif button_id == "candidate-table-previous-page" and current_page > 1:
                    current_page -= 1

            current_page = min(current_page, total_pages)

            start_idx = (current_page - 1) * ROWS_PER_PAGE
            end_idx = start_idx + ROWS_PER_PAGE
            paginated_candidates = candidates[start_idx:end_idx]

            # Define table headers
            headers = [
                html.Th("Name"),
                html.Th("Email"),
                html.Th("Phone"),
                html.Th("Status"),
                html.Th("Screen Score"),
                html.Th("Prelim Score"),
                html.Th("Last Update Date"),
            ]

            # Create table rows
            rows = []
            for candidate in paginated_candidates:
                try:
                    date_updated = datetime.strptime(
                        candidate["last_update_date"].split(".")[0],
                        "%Y-%m-%dT%H:%M:%S"
                    ).strftime("%d-%m-%Y")
                except (ValueError, KeyError):
                    date_updated = "N/A"

                rows.append(
                    html.Tr(
                        [
                            html.Td(candidate.get("name", "N/A")),
                            html.Td(candidate.get("email", "N/A")),
                            html.Td(candidate.get("phone", "N/A")),
                            html.Td(candidate.get("status", "N/A")),
                            html.Td(candidate.get("screen_score", "N/A")),
                            html.Td(candidate.get("prelim_score", "N/A")),
                            html.Td(date_updated),
                        ]
                    )
                )

            # Determine visibility of pagination buttons and page number
            prev_button_style = {"display": "none"} if current_page == 1 else {}
            next_button_style = {"display": "none"} if current_page == total_pages else {}
            page_number_style = {"display": "none"} if total_candidates <= ROWS_PER_PAGE else {}

            page_number_display = f"Page {current_page} of {total_pages}"

            return (
                dropdown_options_bu,
                dropdown_options_jd,
                status_options,
                [html.Thead(html.Tr(headers)), html.Tbody(rows)],
                page_number_display,
                current_page,
                False,
                "",
                prev_button_style,
                next_button_style,
                page_number_style,
            )

        except requests.exceptions.RequestException:
            toast_open = True
            toast_message = "Candidates data failed to load."
            return (
                dropdown_options_bu,
                dropdown_options_jd,
                status_options,
                html.Div("Error loading candidates data.", className='docs-message'),
                "",
                1,
                toast_open,
                toast_message,
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
            )

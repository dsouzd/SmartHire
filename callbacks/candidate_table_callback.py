import os
from datetime import datetime

import dash
import requests
from dash import html
from dash.dependencies import Input, Output, State
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

ROWS_PER_PAGE = 10

def candidate_table_callback(app):

    @app.callback(
        [
            Output("candidate-table-business-unit-dropdown", "options"),
            Output("candidate-table-job-dropdown", "options"),
            Output("candidate-table-status-dropdown", "options"),
            Output("candidate-table", "children"),
            Output("candidate-table-page-number", "children"),
            Output("candidate-table-current-page", "data"),
            Output("candidate-table-toast", "style"),  # Changed to 'style' for visibility
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
        # Initialize toast style and message
        toast_style = {'display': 'none'}
        toast_message = ''
        
        try:
            # Fetch Business Units
            response_bu = requests.get(f"{API_BASE_URL}/businessunits")
            response_bu.raise_for_status()
            business_units = response_bu.json().get("data", [])
            dropdown_options_bu = [
                {"label": bu["name"], "value": bu["id"]} for bu in business_units
            ]
        except requests.exceptions.RequestException:
            toast_style = {
                'display': 'block',
                'position': 'fixed',
                'top': 10,
                'right': 10,
                'width': 350,
                'background-color': '#fff',
                'padding': '10px',
                'border': '1px solid #ccc',
                'border-radius': '5px',
                'zIndex': 1000
            }
            toast_message = "Business Unit loading failed."
            return (
                [],  # Business Units options
                [],  # Job Description options
                [],  # Status options
                [],  # Candidate table children
                "",  # Page number display
                1,  # Current page
                toast_style,
                toast_message,
                {"display": "none"},  # Previous page button style
                {"display": "none"},  # Next page button style
                {"display": "none"},  # Page number style
            )

        if bu_id is None:
            return (
                dropdown_options_bu,
                [],  # No job options yet
                [],  # No status options yet
                [],  # No candidates yet
                "", 
                1,
                {'display': 'none'},  # Toast style
                "",
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
            )

        try:
            # Fetch Job Descriptions based on Business Unit
            url = f"{API_BASE_URL}/businessunits/{bu_id}/jds"
            response_jds = requests.get(url, timeout=10)
            response_jds.raise_for_status()
            jds = response_jds.json().get("data", [])
            dropdown_options_jd = [
                {"label": jd["title"], "value": jd["jd_id"]} for jd in jds
            ]
        except requests.exceptions.RequestException:
            toast_style = {
                'display': 'block',
                'position': 'fixed',
                'top': 10,
                'right': 10,
                'width': 350,
                'background-color': '#fff',
                'padding': '10px',
                'border': '1px solid #ccc',
                'border-radius': '5px',
                'zIndex': 1000
            }
            toast_message = "Job Descriptions loading failed."
            return (
                dropdown_options_bu,
                [],  # No job options if fetching fails
                [],
                [],
                "", 
                1,
                toast_style,
                toast_message,
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
            )

        # Status filter options
        status_options = [
            {"label": "All", "value": ""},
            {"label": "Screening: Rejected", "value": "Screening: Rejected"},
            {"label": "Preliminary: Attended", "value": "Preliminary: Attended"},
            {"label": "Preliminary: Invite Sent", "value": "Preliminary: Invite Sent"},
        ]

        if jd_id is None:
            return (
                dropdown_options_bu,
                dropdown_options_jd,
                status_options,  # Status options
                [],  # No candidates yet
                "",
                1,
                {'display': 'none'},  # Toast style
                "",
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
            )

        try:
            # Fetch Candidate Details based on selected Business Unit and Job Description
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
                    {'display': 'none'},  # Toast style
                    "",
                    {"display": "none"},
                    {"display": "none"},
                    {"display": "none"},
                )

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

            headers = [
                html.Th("Name"),
                html.Th("Email"),
                html.Th("Phone"),
                html.Th("Status"),
                html.Th("Screen Score"),
                html.Th("Prelim Score"),
                html.Th("Last Update Date"),
            ]

            rows = []
            for candidate in paginated_candidates:
                date_updated = datetime.strptime(
                    candidate["last_update_date"].split(".")[0],
                    "%Y-%m-%dT%H:%M:%S"
                ).strftime("%d-%m-%Y")
                rows.append(
                    html.Tr(
                        [
                            html.Td(candidate["name"]),
                            html.Td(candidate["email"]),
                            html.Td(candidate["phone"]),
                            html.Td(candidate["status"]),
                            html.Td(candidate["screen_score"]),
                            html.Td(candidate["prelim_score"]),
                            html.Td(date_updated),
                        ]
                    )
                )

            prev_button_style = {"display": "none"} if current_page == 1 else {}
            next_button_style = {"display": "none"} if current_page == total_pages else {}
            page_number_style = {"display": "none"} if total_candidates <= ROWS_PER_PAGE else {}

            page_number_display = f"Page {current_page} of {total_pages}"

            return (
                dropdown_options_bu,
                dropdown_options_jd,
                status_options,
                [html.Thead(html.Tr(headers)), html.Tbody(rows)],
                html.Span(page_number_display),  # Wrapped in html.Span for consistency
                current_page,
                {'display': 'none'},  # Toast style
                "",
                prev_button_style,
                next_button_style,
                page_number_style,
            )

        except requests.exceptions.RequestException:
            toast_style = {
                'display': 'block',
                'position': 'fixed',
                'top': 10,
                'right': 10,
                'width': 350,
                'background-color': '#fff',
                'padding': '10px',
                'border': '1px solid #ccc',
                'border-radius': '5px',
                'zIndex': 1000
            }
            toast_message = "Candidates data failed to Load."
            return (
                dropdown_options_bu,
                dropdown_options_jd,
                status_options,
                html.Div("Error loading candidates data", className='docs-message'),
                "",
                1,
                toast_style,
                toast_message,
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
            )

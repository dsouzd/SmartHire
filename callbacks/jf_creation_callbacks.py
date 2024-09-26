import os
import requests
from dash.dependencies import Input, Output, State
from dash import html, dcc, no_update, callback_context
import dash_bootstrap_components as dbc
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")


def generate_jd(app):
    @app.callback(
        Output("jd-creation-business-unit-dropdown", "options"),
        Input("jd-creation-submit-btn", "n_clicks"),
    )
    def load_business_units(n_clicks):
        url = f"{API_BASE_URL}/businessunits"
        try:
            response = requests.get(url, timeout=300)
            if response.status_code == 200:
                business_units = response.json()["data"]
                return [
                    {"label": unit["name"], "value": unit["id"]}
                    for unit in business_units
                ]
            return []
        except requests.exceptions.RequestException as e:
            print(f"Error fetching business units: {e}")
            return []

    @app.callback(
        [
            Output("jd-creation-response-section", "children"),
            Output("jd-creation-save-btn", "className"),
            Output("jd-creation-reset-btn", "className"),
            Output("jd-creation-toast-message", "is_open"),
            Output("jd-creation-toast-message", "children"),
            Output("jd-creation-toast-message", "header"),
            Output("jd-creation-business-unit-dropdown", "disabled"),
            Output("jd-creation-job-title-input", "disabled"),
            Output("jd-creation-experience-input", "disabled"),
            Output("jd-creation-skills-input", "disabled"),
            Output("jd-creation-business-unit-dropdown", "value"),
            Output("jd-creation-job-title-input", "value"),
            Output("jd-creation-experience-input", "value"),
            Output("jd-creation-skills-input", "value"),
        ],
        [
            Input("jd-creation-submit-btn", "n_clicks"),
            Input("jd-creation-save-btn", "n_clicks"),
            Input("jd-creation-reset-btn", "n_clicks"),
        ],
        [
            State("jd-creation-job-title-input", "value"),
            State("jd-creation-experience-input", "value"),
            State("jd-creation-skills-input", "value"),
            State("jd-creation-business-unit-dropdown", "value"),
        ],
    )
    def handle_form_actions(
        submit_clicks, save_clicks, reset_clicks, job_title, experience, skills, bu_id
    ):
        ctx = callback_context

        if not ctx.triggered:
            return (
                no_update,
                "hide-button",
                "hide-button",
                False,
                "",
                "",
                False,
                False,
                False,
                False,
                no_update,
                no_update,
                no_update,
                no_update,
            )

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger_id == "jd-creation-save-btn" and save_clicks:
            file_name = f"{job_title}.docx"
            url = (
                f"{API_BASE_URL}/savejd?bu_id={bu_id}&jd_title={file_name}&is_save=true"
            )
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    return (
                        "",
                        "hide-button",
                        "hide-button",
                        True,
                        "Job description saved successfully!",
                        "Success",
                        False,
                        False,
                        False,
                        False,
                        None,
                        "",
                        "",
                        "",
                    )
                else:
                    return (
                        no_update,
                        "hide-button",
                        "hide-button",
                        True,
                        "Failed to save the job description.",
                        "Error",
                        False,
                        False,
                        False,
                        False,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                    )
            except requests.exceptions.RequestException as e:
                return (
                    no_update,
                    "hide-button",
                    "hide-button",
                    True,
                    f"Error: {str(e)}",
                    "Request Failed",
                    False,
                    False,
                    False,
                    False,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                )

        if trigger_id == "jd-creation-reset-btn" and reset_clicks:
            file_name = f"{job_title}.docx"
            url = f"{API_BASE_URL}/savejd?bu_id={bu_id}&jd_title={file_name}&is_save=false"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    return (
                        "",
                        "hide-button",
                        "hide-button",
                        True,
                        "Job description discarded successfully!",
                        "Success",
                        False,
                        False,
                        False,
                        False,
                        None,
                        "",
                        "",
                        "",
                    )
                else:
                    return (
                        no_update,
                        "hide-button",
                        "hide-button",
                        True,
                        "Failed to discard the job description.",
                        "Error",
                        False,
                        False,
                        False,
                        False,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                    )
            except requests.exceptions.RequestException as e:
                return (
                    no_update,
                    "hide-button",
                    "hide-button",
                    True,
                    f"Error: {str(e)}",
                    "Request Failed",
                    False,
                    False,
                    False,
                    False,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                )

        if trigger_id == "jd-creation-submit-btn" and submit_clicks:
            if not job_title or not experience or not skills or not bu_id:
                return (
                    no_update,
                    "hide-button",
                    "hide-button",
                    True,
                    "Please fill in all the fields!",
                    "Error",
                    False,
                    False,
                    False,
                    False,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                )

            return_list = [no_update] * 13
            return_list[6:] = [True] * 4

            payload = {
                "job_title": job_title,
                "experience": experience,
                "skills": skills,
                "bu_id": bu_id,
            }

            try:
                url = f"{API_BASE_URL}/generatejd"
                response = requests.post(url, json=payload, timeout=30)

                if response.status_code == 200:
                    file_name = response.json().get("file_name")
                    response_content = html.Div(
                        [
                            html.Div(
                                [
                                    html.Span(
                                        f"{file_name}.docx", className="file-name"
                                    ),
                                    html.Div(
                                        [
                                            html.A(
                                                html.I(className="fas fa-eye btn-icon"),
                                                href=f"{API_BASE_URL}/download?f_name={file_name}&f_type=pdf&bu_id={bu_id}",
                                                target="_blank",
                                                title="View as PDF",
                                                className="mr-2",
                                            ),
                                            html.A(
                                                html.I(
                                                    className="fas fa-download btn-icon"
                                                ),
                                                href=f"{API_BASE_URL}/download?f_name={file_name}&f_type=docx&bu_id={bu_id}",
                                                target="_blank",
                                                title="Download DOCX",
                                            ),
                                        ],
                                        className="icon-wrapper",
                                    ),
                                ],
                                className="d-flex align-items-center justify-content-between generated-file-item",
                            )
                        ]
                    )
                    return (
                        response_content,
                        "save-btn show-button",
                        "reset-btn show-button",
                        True,
                        "Job description generated successfully!",
                        "Success",
                        False,
                        False,
                        False,
                        False,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                    )
                else:
                    return (
                        no_update,
                        "hide-button",
                        "hide-button",
                        True,
                        "Failed to generate JD. Please try again.",
                        "Error",
                        False,
                        False,
                        False,
                        False,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                    )

            except requests.exceptions.RequestException as e:
                return (
                    no_update,
                    "hide-button",
                    "hide-button",
                    True,
                    f"Error: {str(e)}",
                    "Request Failed",
                    False,
                    False,
                    False,
                    False,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                )

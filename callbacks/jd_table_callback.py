import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import requests
from datetime import datetime

ROWS_PER_PAGE = 10  # Define 10 rows per page

def jd_table_callback(app):

    @app.callback(
        [Output('jd-table-business-unit-dropdown', 'options'),
         Output('jd-table', 'children'),
         Output('jd-table-page-number', 'children'),
         Output('jd-table-current-page', 'data'),
         Output('jd-table-toast', 'is_open'),
         Output('jd-table-toast', 'children')],
        [Input('jd-table-business-unit-dropdown', 'value'),
         Input('jd-table-previous-page', 'n_clicks'),
         Input('jd-table-next-page', 'n_clicks')],
        [State('jd-table-current-page', 'data')]
    )
    def jd_table_update(bu_id, prev_clicks, next_clicks, current_page):
        # Initialize for business unit loading
        try:
            response_bu = requests.get('https://smarthire-e32r.onrender.com/businessunits')
            response_bu.raise_for_status()
            business_units = response_bu.json().get('data', [])
            dropdown_options = [{'label': bu['name'], 'value': bu['id']} for bu in business_units]
        except requests.exceptions.RequestException:
            return [], [], "", 1, True, "Business Unit loading failed."

        # If no BU is selected, return empty table and page info
        if bu_id is None:
            return dropdown_options, html.Tr([html.Td("Please select a Business Unit")]), "Page 1", 1, False, ""

        # Handle loading JDs and pagination
        try:
            # Fetch JDs for the selected business unit
            url = f'https://smarthire-e32r.onrender.com/businessunits/{bu_id}/jds'
            response_jds = requests.get(url, timeout=10)  # Add timeout to prevent long waits
            response_jds.raise_for_status()

            jds = response_jds.json().get('data', [])

            # Pagination logic (10 rows per page)
            total_jds = len(jds)
            total_pages = (total_jds // ROWS_PER_PAGE) + (1 if total_jds % ROWS_PER_PAGE > 0 else 0)

            # Handle page number based on button clicks
            ctx = dash.callback_context
            if ctx.triggered:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]
                if button_id == 'jd-table-next-page' and current_page < total_pages:
                    current_page += 1
                elif button_id == 'jd-table-previous-page' and current_page > 1:
                    current_page -= 1

            current_page = min(current_page, total_pages)  # Ensure current page doesn't exceed total pages

            start_idx = (current_page - 1) * ROWS_PER_PAGE
            end_idx = start_idx + ROWS_PER_PAGE
            paginated_jds = jds[start_idx:end_idx]

            # Create table headers
            headers = [html.Th(col) for col in ["JD ID", "Title", "Posted Date", "Download"]]

            # Create table rows and format date
            rows = []
            for jd in paginated_jds:
                download_link = f"https://smarthire-e32r.onrender.com/download?f_name={jd['title'].split('.')[0]}&f_type={jd['title'].split('.')[1]}&bu_id={jd['bu_id']}"
                
                # Refactor the date to dd-mm-yyyy format
                date_posted = datetime.strptime(jd['job_posted'].split('.')[0], "%Y-%m-%dT%H:%M:%S").strftime("%d-%m-%Y")
                
                rows.append(html.Tr([
                    html.Td(jd['jd_id']),
                    html.Td(jd['title']),
                    html.Td(date_posted),
                    html.Td(html.A("Download", href=download_link, target="_blank"))
                ]))

            # Handle pagination display and page number
            page_number_display = f"Page {current_page} of {total_pages}"

            return dropdown_options, [html.Thead(html.Tr(headers)), html.Tbody(rows)], html.Span(page_number_display), current_page, False, ""

        except requests.exceptions.RequestException as e:
            # Return error toast in case of failure to load data for the table
            return html.Tr([html.Td("Error loading data")]), "", current_page, True, "Data failed to Load."

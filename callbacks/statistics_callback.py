import dash
from dash.dependencies import Input, Output
import requests
import plotly.graph_objs as go
from dash import dcc, html

def register_callbacks(app):
    @app.callback(
        Output('statistics-total-open-positions', 'children'),
        Output('statistics-total-candidates-sourced', 'children'),
        Output('statistics-offer-acceptance-rate', 'children'),
        Input('statistics-kpis-update', 'n_intervals')
    )
    def update_kpis(n):
        try:
            response = requests.get('https://smarthire-hvsy.onrender.com/analytics/kpis')
            response.raise_for_status()
            data = response.json()['data']
            return data['total_open_positions'], data['total_candidates_sourced'], f"{data['offer_acceptance_rate']}%"
        except (requests.exceptions.RequestException, KeyError, ValueError) as e:
            print(f"Error fetching KPIs: {e}")
            return 'Error', 'Error', 'Error'

    @app.callback(
        Output('statistics-job-select', 'options'),
        Input('statistics-job-select-update', 'n_intervals')
    )
    def update_job_options(n):
        try:
            response = requests.get('https://smarthire-hvsy.onrender.com/api/jobs')
            response.raise_for_status()
            data = response.json()['data']['jobs']
            return [{'label': job['job_title'], 'value': job['job_id']} for job in data]
        except (requests.exceptions.RequestException, KeyError, ValueError) as e:
            print(f"Error fetching job options: {e}")
            return []

    @app.callback(
        Output('statistics-pipelineChart', 'figure'),
        Input('statistics-job-select', 'value')
    )
    def update_job_analytics(job_id):
        if not job_id:
            return {}
        try:
            response = requests.get(f'https://smarthire-hvsy.onrender.com/analytics/jobs/{job_id}')
            response.raise_for_status()
            data = response.json()['data']
            pipeline_labels = list(data['pipeline_health'].keys())
            pipeline_counts = list(data['pipeline_health'].values())
            return {
                'data': [go.Bar(x=pipeline_labels, y=pipeline_counts)],
                'layout': go.Layout(title='Candidates in Pipeline')
            }
        except (requests.exceptions.RequestException, KeyError, ValueError) as e:
            print(f"Error fetching job analytics: {e}")
            return {}

    @app.callback(
        Output('statistics-sourceChart', 'figure'),
        Output('statistics-sourceChart-info', 'children'),
        Input('statistics-sourcing-update', 'n_intervals')
    )
    def update_sourcing_analytics(n):
        try:
            response = requests.get('https://smarthire-hvsy.onrender.com/analytics/sourcing')
            response.raise_for_status()
            data = response.json()['data']
            info = response.json()['info']
            source_labels = list(data['source_breakdown'].keys())
            source_counts = list(data['source_breakdown'].values())
            return {
                'data': [go.Pie(labels=source_labels, values=source_counts)],
                'layout': go.Layout(title='Candidates by Source')
            }, info['source_breakdown_summary'] + "\n\n" + info['cost_per_source_summary']
        except (requests.exceptions.RequestException, KeyError, ValueError) as e:
            print(f"Error fetching sourcing analytics: {e}")
            return {}, 'Error fetching data'

    @app.callback(
        Output('statistics-costPerSourceChart', 'figure'),
        Input('statistics-sourcing-update', 'n_intervals')
    )
    def update_cost_per_source_analytics(n):
        try:
            response = requests.get('https://smarthire-hvsy.onrender.com/analytics/sourcing')
            response.raise_for_status()
            data = response.json()['data']
            cost_labels = list(data['cost_per_source'].keys())
            cost_values = list(data['cost_per_source'].values())
            return {
                'data': [go.Bar(x=cost_labels, y=cost_values)],
                'layout': go.Layout(title='Cost per Source')
            }
        except (requests.exceptions.RequestException, KeyError, ValueError) as e:
            print(f"Error fetching cost per source analytics: {e}")
            return {}

    @app.callback(
        Output('statistics-geoSourcingChart', 'figure'),
        Input('statistics-sourcing-update', 'n_intervals')
    )
    def update_geo_sourcing_analytics(n):
        try:
            response = requests.get('https://smarthire-hvsy.onrender.com/analytics/sourcing')
            response.raise_for_status()
            data = response.json()['data']
            geo_labels = list(data['geographical_sourcing'].keys())
            geo_counts = list(data['geographical_sourcing'].values())
            return {
                'data': [go.Pie(labels=geo_labels, values=geo_counts)],
                'layout': go.Layout(title='Geographical Sourcing')
            }
        except (requests.exceptions.RequestException, KeyError, ValueError) as e:
            print(f"Error fetching geographical sourcing analytics: {e}")
            return {}

    @app.callback(
        Output('statistics-screeningChart', 'figure'),
        Input('statistics-screening-update', 'n_intervals')
    )
    def update_screening_analytics(n):
        try:
            response = requests.get('https://smarthire-hvsy.onrender.com/analytics/screeninginterview')
            response.raise_for_status()
            data = response.json()['data']
            screening_labels = ['Passed Screening', 'Passed Interview']
            screening_counts = [data['passed_screening'], data['interview_conversion_rate']]
            return {
                'data': [go.Bar(x=screening_labels, y=screening_counts)],
                'layout': go.Layout(title='Screening & Interview Analytics')
            }
        except (requests.exceptions.RequestException, KeyError, ValueError) as e:
            print(f"Error fetching screening analytics: {e}")
            return {}

    @app.callback(
        Output('statistics-diversityChart', 'figure'),
        Input('statistics-diversity-update', 'n_intervals')
    )
    def update_diversity_analytics(n):
        try:
            response = requests.get('https://smarthire-hvsy.onrender.com/analytics/diversity')
            response.raise_for_status()
            data = response.json()['data']
            gender_labels = list(data['gender_diversity'].keys())
            gender_counts = list(data['gender_diversity'].values())
            return {
                'data': [go.Pie(labels=gender_labels, values=gender_counts)],
                'layout': go.Layout(title='Gender Diversity')
            }
        except (requests.exceptions.RequestException, KeyError, ValueError) as e:
            print(f"Error fetching diversity analytics: {e}")
            return {}

    @app.callback(
        Output('statistics-gdpr-compliance-rate', 'children'),
        Output('statistics-gender-distribution', 'children'),
        Output('statistics-ethnicity-distribution', 'children'),
        Output('statistics-compliance-info', 'children'),
        Input('statistics-compliance-update', 'n_intervals')
    )
    def update_compliance_analytics(n):
        try:
            response = requests.get('https://smarthire-hvsy.onrender.com/analytics/compliance')
            response.raise_for_status()
            data = response.json()['data']
            info = response.json()['info']
            gdpr_compliance_rate = f"{data['gdpr_compliance_rate']}%"
            gender_distribution = ', '.join([f"{gender}: {count}" for gender, count in data['gender_distribution'].items()])
            ethnicity_distribution = ', '.join([f"{ethnicity}: {count}" for ethnicity, count in data['ethnicity_distribution'].items()])
            return gdpr_compliance_rate, gender_distribution, ethnicity_distribution, info
        except (requests.exceptions.RequestException, KeyError, ValueError) as e:
            print(f"Error fetching compliance analytics: {e}")
            return 'Error', 'Error', 'Error', 'Error fetching data'

    @app.callback(
        Output('statistics-recruiterPerformanceChart', 'figure'),
        Output('statistics-task-completion-table', 'children'),
        Input('statistics-efficiency-update', 'n_intervals')
    )
    def update_efficiency_analytics(n):
        try:
            response = requests.get('https://smarthire-hvsy.onrender.com/analytics/efficiency')
            response.raise_for_status()
            data = response.json()['data']
            recruiter_labels = list(data['recruiter_performance'].keys())
            recruiter_counts = list(data['recruiter_performance'].values())
            task_completion_rows = [
                html.Tr([html.Td(recruiter), html.Td(f"{rate}%")])
                for recruiter, rate in data['task_completion_rate'].items()
            ]
            return {
                'data': [go.Bar(x=recruiter_labels, y=recruiter_counts)],
                'layout': go.Layout(title='Recruiter Performance')
            }, task_completion_rows
        except (requests.exceptions.RequestException, KeyError, ValueError) as e:
            print(f"Error fetching efficiency analytics: {e}")
            return {}, []

    @app.callback(
        Output('statistics-average-nps', 'children'),
        Output('statistics-recent-feedback', 'children'),
        Input('statistics-experience-update', 'n_intervals')
    )
    def update_experience_analytics(n):
        try:
            response = requests.get('https://smarthire-hvsy.onrender.com/analytics/candidateexperience')
            response.raise_for_status()
            data = response.json()['data']
            average_nps = f"{data['average_nps']}"
            recent_feedback = 'No recent feedback available.'
            return average_nps, recent_feedback
        except (requests.exceptions.RequestException, KeyError, ValueError) as e:
            print(f"Error fetching experience analytics: {e}")
            return 'Error', 'Error'

    @app.callback(
        Output('statistics-offerHireRatioChart', 'figure'),
        Output('statistics-candidate-drop-off-rate', 'children'),
        Input('statistics-offers-update', 'n_intervals')
    )
    def update_offers_analytics(n):
        try:
            response = requests.get('https://smarthire-hvsy.onrender.com/analytics/offers')
            response.raise_for_status()
            data = response.json()['data']
            offer_hire_ratio = data['offer_to_hire_ratio']
            candidate_drop_off_rate = f"{data['candidate_drop_off_rate']}%"
            return {
                'data': [go.Pie(labels=['Offers Accepted', 'Offers Rejected'], values=[offer_hire_ratio, 100 - offer_hire_ratio])],
                'layout': go.Layout(title='Offer to Hire Ratio')
            }, candidate_drop_off_rate
        except (requests.exceptions.RequestException, KeyError, ValueError) as e:
            print(f"Error fetching offers analytics: {e}")
            return {}, 'Error'
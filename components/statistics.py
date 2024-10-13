from dash import dcc, html

def statistics():

    return html.Div([
    html.Link(rel='stylesheet', href='/assets/styles/statistics.css'),
    html.Div(className='statistics-sidebar', children=[
        html.H2('Analytics Dashboard'),  # Updated title
        html.Ul([
            html.Li(html.A('KPIs', href='#statistics-kpis')),
            html.Li(html.A('Job Analytics', href='#statistics-job-analytics')),
            html.Li(html.A('Sourcing Analytics', href='#statistics-sourcing-analytics')),
            html.Li(html.A('Cost per Source', href='#statistics-cost-per-source-analytics')),
            html.Li(html.A('Geographical Sourcing', href='#statistics-geo-sourcing-analytics')),
            html.Li(html.A('Screening & Interview Analytics', href='#statistics-screening-analytics')),
            html.Li(html.A('Diversity & Inclusion', href='#statistics-diversity-analytics')),
            html.Li(html.A('Compliance & Legal', href='#statistics-compliance-analytics')),
            html.Li(html.A('Recruitment Efficiency', href='#statistics-efficiency-analytics')),
            html.Li(html.A('Candidate Experience', href='#statistics-experience-analytics')),
            html.Li(html.A('Offer & Hiring Analytics', href='#statistics-offer-hiring-analytics'))
        ])
    ]),
    html.Div(className='statistics-main-content', children=[
        html.Section(id='statistics-kpis', className='statistics-panel', children=[
            html.H3('Key Performance Indicators'),
            html.Div(className='statistics-kpi-container', children=[
                html.Div(className='statistics-kpi-card', children=[
                    html.H4('Total Open Positions'),
                    html.P(id='statistics-total-open-positions', children='Loading...')
                ]),
                html.Div(className='statistics-kpi-card', children=[
                    html.H4('Total Candidates Sourced'),
                    html.P(id='statistics-total-candidates-sourced', children='Loading...')
                ]),
                html.Div(className='statistics-kpi-card', children=[
                    html.H4('Offer Acceptance Rate'),
                    html.P(id='statistics-offer-acceptance-rate', children='Loading...')
                ])
            ]),
            dcc.Interval(id='statistics-kpis-update', interval=10000)
        ]),
        html.Section(id='statistics-job-analytics', className='statistics-panel', children=[
            html.H3('Job-Specific Analytics'),
            html.Label('Select Job:'),
            dcc.Dropdown(
                id='statistics-job-select',
                options=[],
                value=''
            ),
            dcc.Graph(id='statistics-pipelineChart'),
            dcc.Interval(id='statistics-job-select-update', interval=10000)
        ]),
        html.Section(id='statistics-sourcing-analytics', className='statistics-panel', children=[
            html.H3('Candidate Sourcing Analytics'),
            dcc.Graph(id='statistics-sourceChart'),
            html.Div(id='statistics-sourceChart-info', children='Loading...'),
            dcc.Graph(id='statistics-costPerSourceChart'),
            dcc.Graph(id='statistics-geoSourcingChart'),
            dcc.Interval(id='statistics-sourcing-update', interval=10000)
        ]),
        html.Section(id='statistics-screening-analytics', className='statistics-panel', children=[
            html.H3('Screening & Interview Analytics'),
            dcc.Graph(id='statistics-screeningChart'),
            dcc.Interval(id='statistics-screening-update', interval=10000)
        ]),
        html.Section(id='statistics-diversity-analytics', className='statistics-panel', children=[
            html.H3('Diversity & Inclusion Metrics'),
            dcc.Graph(id='statistics-diversityChart'),
            dcc.Interval(id='statistics-diversity-update', interval=10000)
        ]),
        html.Section(id='statistics-compliance-analytics', className='statistics-panel', children=[
            html.H3('Compliance & Legal Metrics'),
            html.Div(className='statistics-metrics-container', children=[
                html.Div(className='statistics-metric-card', children=[
                    html.H4('GDPR Compliance Rate'),
                    html.P(className='statistics-metric-value', children=[html.Span(id='statistics-gdpr-compliance-rate', children='Loading...')])
                ]),
                html.Div(className='statistics-metric-card', children=[
                    html.H4('Gender Distribution'),
                    html.P(className='statistics-metric-value', children=[html.Span(id='statistics-gender-distribution', children='Loading...')])
                ]),
                html.Div(className='statistics-metric-card', children=[
                    html.H4('Ethnicity Distribution'),
                    html.P(className='statistics-metric-value', children=[html.Span(id='statistics-ethnicity-distribution', children='Loading...')])
                ])
            ]),
            html.Div(id='statistics-compliance-info', children='Loading...'),
            dcc.Interval(id='statistics-compliance-update', interval=10000)
        ]),
        html.Section(id='statistics-efficiency-analytics', className='statistics-panel', children=[
            html.H3('Recruiter Efficiency'),
            html.H4('Recruiter Performance (Applications Handled)'),
            dcc.Graph(id='statistics-recruiterPerformanceChart'),
            html.H4('Task Completion Rates'),
            html.Div(className='statistics-table-container', children=[
                html.Table(id='statistics-task-completion-table', children=[
                    html.Thead(children=[
                        html.Tr([
                            html.Th('Recruiter Name'),
                            html.Th('Task Completion Rate (%)')
                        ])
                    ]),
                    html.Tbody(id='statistics-task-completion-table-body')
                ])
            ]),
            dcc.Interval(id='statistics-efficiency-update', interval=10000)
        ]),
        html.Section(id='statistics-experience-analytics', className='statistics-panel', children=[
            html.H3('Candidate Experience & Feedback'),
            html.H4('Average NPS Score:'),
            html.P(id='statistics-average-nps', children='Loading...'),
            html.H4('Recent Candidate Feedback'),
            html.Div(id='statistics-recent-feedback', children=[
                html.P('Loading feedback...')
            ]),
            dcc.Interval(id='statistics-experience-update', interval=10000)
        ]),
        html.Section(id='statistics-offer-hiring-analytics', className='statistics-panel', children=[
            html.H3('Offer & Hiring Analytics'),
            html.H4('Offer to Hire Ratio:'),
            dcc.Graph(id='statistics-offerHireRatioChart'),
            html.H4('Candidate Drop-Off Rate:'),
            html.P(id='statistics-candidate-drop-off-rate', children='Loading...'),
            dcc.Interval(id='statistics-offers-update', interval=10000)
        ])
    ])
])
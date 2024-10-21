from dash import dcc, html

def statistics():
    return html.Div([
        html.Div(id='page-load-trigger-kpis', style={'display': 'none'}),
        html.Div(id='page-load-trigger-job-select', style={'display': 'none'}),
        html.Div(id='page-load-trigger-sourcing', style={'display': 'none'}),
        html.Div(id='page-load-trigger-screening', style={'display': 'none'}),
        html.Div(id='page-load-trigger-diversity', style={'display': 'none'}),
        html.Div(id='page-load-trigger-compliance', style={'display': 'none'}),
        html.Div(id='page-load-trigger-efficiency', style={'display': 'none'}),
        html.Div(id='page-load-trigger-experience', style={'display': 'none'}),
        html.Div(id='page-load-trigger-offers', style={'display': 'none'}),
        html.Link(rel='stylesheet', href='/assets/styles/statistics.css'),
        html.Div(className='statistics-sidebar', children=[
            html.H2('Analytics Dashboard'),  
            html.Ul([
                html.Li(html.A('KPIs', href='#statistics-kpis')),
                html.Li(html.A('Job Analytics', href='#statistics-job-analytics')),
                html.Li(html.A('Sourcing Analytics', href='#statistics-sourcing-analytics')),
                html.Li(html.A('Geographical Sourcing', href='#statistics-geo-sourcing-analytics')),
                html.Li(html.A('Screening & Interview Analytics', href='#statistics-screening-analytics')),
                html.Li(html.A('Diversity & Inclusion', href='#statistics-diversity-analytics')),
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
                ])
            ]),
            html.Section(id='statistics-job-analytics', className='statistics-panel', children=[
                html.H3('Job-Specific Analytics'),
                html.Label('Select Job:'),
                dcc.Dropdown(
                    id='statistics-job-select',
                    options=[],
                    value=''
                ),
                dcc.Graph(id='statistics-pipelineChart')
            ]),
            html.Section(id='statistics-sourcing-analytics', className='statistics-panel', children=[
                html.H3('Candidate Sourcing Analytics'),
                dcc.Graph(id='statistics-geoSourcingChart')
            ]),
            html.Section(id='statistics-screening-analytics', className='statistics-panel', children=[
                html.H3('Screening & Interview Analytics'),
                dcc.Graph(id='statistics-screeningChart')
            ]),
            html.Section(id='statistics-diversity-analytics', className='statistics-panel', children=[
                html.H3('Diversity & Inclusion Metrics'),
                dcc.Graph(id='statistics-diversityChart')
            ]),
            html.Section(id='statistics-efficiency-analytics', className='statistics-panel', children=[
                html.H3('Recruiter Efficiency'),
                html.H4('Recruiter Performance (Applications Handled)'),
                dcc.Graph(id='statistics-recruiterPerformanceChart'),
                html.H4('Task Completion Rates'),
                html.Div(className='statistics-table-container', children=[
                    html.Table(children=[
                        html.Thead(children=[
                            html.Tr([
                                html.Th('Recruiter Name'),
                                html.Th('Task Completion Rate (%)')
                            ])
                        ]),
                        html.Tbody(id='statistics-task-completion-table-body')
                    ])
                ])
            ]),
            html.Section(id='statistics-experience-analytics', className='statistics-panel', children=[
                html.H3('Candidate Experience & Feedback'),
                html.H4('Average NPS Score:'),
                html.P(id='statistics-average-nps', children='Loading...'),
                html.H4('Recent Candidate Feedback'),
                html.Div(id='statistics-recent-feedback', children=[
                    html.P('Loading feedback...')
                ])
            ]),
            html.Section(id='statistics-offer-hiring-analytics', className='statistics-panel', children=[
                html.H3('Offer & Hiring Analytics'),
                html.H4('Offer to Hire Ratio:'),
                dcc.Graph(id='statistics-offerHireRatioChart'),
                html.H4('Candidate Drop-Off Rate:'),
                html.P(id='statistics-candidate-drop-off-rate', children='Loading...')
            ])
        ])
    ])

import dash_bootstrap_components as dbc
from dash import html, dcc

def jd_form():
    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.Div(
                        [
                            # Header
                            html.H3('Job Description Preparation', className='text-center mb-4 text-white'),

                            # Job Title Input
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupText(html.I(className="fas fa-briefcase")),
                                    dbc.Input(id='job-title-input', type='text', placeholder='Enter Job Title', className='form-control-lg')
                                ],
                                className='mb-3'
                            ),

                            # Experience Input
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupText(html.I(className="fas fa-calendar-alt")),
                                    dbc.Input(id='experience-input', type='text', placeholder='Enter Experience', className='form-control-lg')
                                ],
                                className='mb-3'
                            ),

                            # Skills Input
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupText(html.I(className="fas fa-tools")),
                                    dbc.Input(id='skill-input', type='text', placeholder='Enter Skills', className='form-control-lg')
                                ],
                                className='mb-3'
                            ),

                            # Submit Button
                            dbc.Button('Submit', id='submit-button', color='info', className='btn-block btn-lg mb-3',
                                       style={"background": "linear-gradient(90deg, rgba(0,123,255,1) 0%, rgba(23,162,184,1) 100%)"}),

                            # Loading Spinner and Output
                            dcc.Loading(
                                id="loading-output",
                                type="circle",
                                children=[
                                    html.Div(id='output-state', className='mt-3 text-white'),
                                    html.Div(id='download-link', className='text-white')
                                ]
                            )
                        ],
                        className='p-5 border rounded shadow-lg bg-secondary',
                        style={"border": "2px solid #007bff"}
                    ),
                    width=6,
                    className='mx-auto'
                ),
                className='justify-content-center align-items-center vh-100',
            )
        ],
        fluid=True,
        className='bg-dark',
        style={"background": "linear-gradient(to right, #0f2027, #203a43, #2c5364)"}
    )

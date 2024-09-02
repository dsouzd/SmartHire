from dash import html
import dash_bootstrap_components as dbc

def jd_form():
    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.Div(
                        [
                            html.H3('Job Description Preparation', className='text-center mb-4'),
                            dbc.Input(id='skill-input', type='text', placeholder='Enter Skills', className='mb-3', size='lg'),
                            dbc.Input(id='experience-input', type='number', placeholder='Enter Experience', className='mb-3', size='lg'),
                            dbc.Input(id='job-title', type='text', placeholder='Enter Job Title', className='mb-3', size='lg'),
                            dbc.Button('Submit', id='submit-button', color='primary', className='me-2 mb-3', size='lg'),
                            dbc.Button('Clear', id='clear-button', color='secondary', className='mb-3', size='lg'),
                            html.Div(id='output-state', className='mt-3'),
                            html.Div(id='pdf-container', className='mt-3'),
                        ],
                        className='p-5 border rounded bg-light shadow-lg',
                    ),
                    width=6,
                    className='mx-auto'
                ),
                className='justify-content-center align-items-center vh-100',
            )
        ],
        fluid=True,
        className='bg-dark'
    )

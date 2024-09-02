from dash import Output, Input, State, html
import requests
import base64

def generate_pdf(app):
    @app.callback(
        Output('output-state', 'children'),
        Output('pdf-container', 'children'),
        [Input('submit-button', 'n_clicks')],
        [State('skill-input', 'value'), State('experience-input', 'value')]
    )
    def update_output(n_clicks, skill, experience):
        print(n_clicks, skill, experience)
        if n_clicks:
            api_url = 'https://localhose:4758/api/generate-pdf'
            payload = {'skill': skill, 'experience': experience}
            response = requests.get(api_url, json=payload)
            print(f"API Response Status Code: {response.status_code}")

            if response.status_code == 200:
                pdf_content = response.content
                pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
                pdf_src = f'data:application/pdf;base64,{pdf_base64}'
                pdf_display = html.Iframe(src=pdf_src, style={'width': '100%', 'height': '600px'})
                return 'Form submitted successfully!', pdf_display
            else:
                return 'Failed to generate PDF. Please try again.', ''
        return '', ''
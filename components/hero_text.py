# hero.py
from dash import html

def hero_text():
    hero_text = html.Div(
        className="hero-container",
        children=[
            html.Div(
                className="hero-content",
                children=[
                    html.H1("Automated Hiring System", className="hero-title"),
                    html.P(
                        """
                        Welcome to the Future of Hiring Automation. Our platform simplifies the recruitment process:
                        """,
                        className="hero-description"
                    ),
                    html.Ul(
                        children=[
                            html.Li("Create job descriptions by skills, position, and experience."),
                            html.Li("Upload resumes and receive match scores for quick candidate screening."),
                            html.Li("Automatically generate interview questions tailored to job descriptions."),
                        ],
                        className="hero-list"
                    ),
                ]
            ),
            html.Div(
                className="hero-animation",
                children=[
                    # Use your image here
                    html.Img(src="/assets/img/hero_banner.webp", className="hero-image"),
                ]
            ),
        ]
    )
    return html.Div(hero_text, className="hero-text")

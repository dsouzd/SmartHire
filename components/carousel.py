from dash import html
import dash_bootstrap_components as dbc

def carousel():
    return dbc.Container(
        [
            dbc.Carousel(
                items=[
                    {
                        "key": "1",
                        "src": "/assets/img/hero_banner_res.webp",
                        "header": "AI-Powered JD Generation",
                        "caption": "Generate job descriptions by taking inputs like skills, experience, and roles.",
                        "img_style": {"width": "100%", "height": "400px", "objectFit": "cover"}
                    },
                    {
                        "key": "2",
                        "src": "/assets/img/banner.webp",
                        "header": "Automated Resume Screening",
                        "caption": "Screen resumes efficiently and compare them with generated JDs.",
                        "img_style": {"width": "100%", "height": "400px", "objectFit": "cover"}
                    },
                    {
                        "key": "3",
                        "src": "/assets/img/hero_banner_res.webp",
                        "header": "First-Round Question Generation",
                        "caption": "Generate intelligent questions for the first-round interviews.",
                        "img_style": {"width": "100%", "height": "400px", "objectFit": "cover"}
                    }
                ],
                controls=True,
                indicators=True,
                interval=3000,
                ride="carousel",
                className="carousel-fade",
                style={"width": "100%", "margin": "0 auto"}
            )
        ],
        fluid=True,
        style={"padding": "0", "backgroundColor": "#f8f9fa"}
    )

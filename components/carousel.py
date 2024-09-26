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
                        "header": html.H3("AI-Powered JD Generation", style={
                            "backgroundColor": "rgba(255, 255, 255, 0.6)",
                            "backdropFilter": "blur(10px)", 
                            "padding": "10px",
                            "borderRadius": "8px",
                            "color": "#000", 
                        }),
                        "caption": html.P("Generate job descriptions by taking inputs like skills, experience, and roles.", style={
                            "backgroundColor": "rgba(255, 255, 255, 0.6)",
                            "backdropFilter": "blur(10px)",  
                            "padding": "10px",
                            "borderRadius": "8px",
                            "color": "#000",  
                        }),
                        "img_style": {"width": "100%", "height": "400px", "objectFit": "cover"}  
                    },
                    {
                        "key": "2",
                        "src": "/assets/img/banner.webp",  
                        "header": html.H3("Automated Resume Screening", style={
                            "backgroundColor": "rgba(255, 255, 255, 0.6)",
                            "backdropFilter": "blur(10px)",
                            "padding": "10px",
                            "borderRadius": "8px",
                            "color": "#000", 
                        }),
                        "caption": html.P("Screen resumes efficiently and compare them with generated JDs.", style={
                            "backgroundColor": "rgba(255, 255, 255, 0.6)",
                            "backdropFilter": "blur(10px)",
                            "padding": "10px",
                            "borderRadius": "8px",
                            "color": "#000",  
                        }),
                        "img_style": {"width": "100%", "height": "400px", "objectFit": "cover"}  
                    },
                    {
                        "key": "3",
                        "src": "/assets/img/hero_banner_res.webp",  
                        "header": html.H3("First-Round Question Generation", style={
                            "backgroundColor": "rgba(255, 255, 255, 0.6)",
                            "backdropFilter": "blur(10px)",
                            "padding": "10px",
                            "borderRadius": "8px",
                            "color": "#000",  
                        }),
                        "caption": html.P("Generate intelligent questions for the first-round interviews.", style={
                            "backgroundColor": "rgba(255, 255, 255, 0.6)",
                            "backdropFilter": "blur(10px)",
                            "padding": "10px",
                            "borderRadius": "8px",
                            "color": "#000",  
                        }),
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

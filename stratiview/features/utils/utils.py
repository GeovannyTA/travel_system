from django.http import HttpResponse


def soft_redirect(url):
    return HttpResponse(
        f"""
        <html>
            <head>
                <style>
                    body {{
                        margin: 0;
                        background: white;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        font-family: Arial, sans-serif;
                        opacity: 1;
                        transition: opacity 0.8s ease-out;
                    }}
                    body.fade-out {{
                        opacity: 0;
                    }}
                </style>
                <script type="text/javascript">
                    document.addEventListener("DOMContentLoaded", function() {{
                        setTimeout(function() {{
                            document.body.classList.add('fade-out');
                            setTimeout(function() {{
                                window.location.href = "{url}";
                            }}, 800); // Espera a que termine el efecto
                        }}, 200); // Pequeño retardo para asegurar que la página cargó
                    }});
                </script>
            </head>
        </html>
    """
    )

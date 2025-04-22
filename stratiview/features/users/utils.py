from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_credentials_email(temp_password, first_name, last_name, email):
    full_name = f"{first_name} {last_name}"
    temp_password = temp_password

    subject = "Bienvenido a Stratiview"

    html_content = render_to_string(
        "emails/template_credentials_email.html",
        {
            "full_name": full_name,
            "email": email,
            "temp_password": temp_password,
            "login_url": "http://127.0.0.1:8000/auth/sign_in/",
        },
    )

    email_msg = EmailMultiAlternatives(
        subject=subject,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email]
    )
    email_msg.attach_alternative(html_content, "text/html")
    email_msg.send()
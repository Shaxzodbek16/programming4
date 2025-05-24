import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from celery import shared_task

from app.core.settings import get_settings, Settings
from app.api.tasks.email_template import EMAIL_TEMPLATE
from app.core.celery import celery

settings: Settings = get_settings()


@celery.task
def send_verification_email(email: str, code: int):
    sender_email = settings.EMAIL
    sender_password = settings.EMAIL_PASSWORD

    html_body = EMAIL_TEMPLATE.replace("{{CODE}}", str(code)).replace(
        "{{EMAIL}}", str(email)
    )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Your verification code: {code}"
    msg["From"] = sender_email
    msg["To"] = email

    html_part = MIMEText(html_body, "html")
    msg.attach(html_part)

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

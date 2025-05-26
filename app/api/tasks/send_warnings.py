import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core.settings import get_settings, Settings
from app.api.tasks.email_template import EMAIL_TEMPLATE_FOR_WARNINGS
from app.core.celery import celery

settings: Settings = get_settings()


@celery.task
def send_warnings(email: str, product_name: str):
    sender_email = settings.EMAIL
    sender_password = settings.EMAIL_PASSWORD

    html_body = EMAIL_TEMPLATE_FOR_WARNINGS.replace(
        "{{PRODUCT_NAME}}", product_name
    ).replace("{{EMAIL}}", email)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"⚠️ Low Stock Alert: {product_name}"
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
        print(f"Error sending warning email: {e}")
        return False

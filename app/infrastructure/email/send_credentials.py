import smtplib
import os
from email.mime.text import MIMEText
from app.core.config import settings

def send_credentials_email(to: str, subject: str, body: str):
    from_email = settings.EMAIL_USER
    password = settings.EMAIL_PASS

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, [to], msg.as_string())
    except Exception as e:
        print(f"❌ Error al enviar correo: {e}")
        raise

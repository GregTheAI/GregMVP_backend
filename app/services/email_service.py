from email.message import EmailMessage
import certifi
import ssl
from aiosmtplib import SMTP
from fastapi import BackgroundTasks

from app.core.config import get_settings

settings = get_settings()


class EmailService:
    def __init__(self, background_tasks: BackgroundTasks):
        self.background_tasks : BackgroundTasks = background_tasks

    @staticmethod
    async def _send_email_sync(to_email: str, subject: str, html_body: str):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        smtp = SMTP(hostname=settings.SMTP_HOST, port=settings.SMTP_PORT, start_tls=settings.SMTP_TLS, tls_context=ssl_context)

        try:
            message = EmailMessage()
            message["From"] = settings.EMAILS_FROM_EMAIL
            message["To"] = to_email
            message["Subject"] = subject
            message.set_content("Sent from GregAI")
            message.add_alternative(html_body, subtype="html")

            await smtp.connect()
            await smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            smtp_response = await smtp.send_message(message)
            return smtp_response

        except Exception as e:
            print(f"Failed to send email: {e}")
            return None

    def send_email_background(self, to_email: str, subject: str, html_content: str):
        self.background_tasks.add_task(self._send_email_sync, to_email, subject, html_content)

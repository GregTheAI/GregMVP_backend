from email.message import EmailMessage

import boto3
import certifi
import ssl
from aiosmtplib import SMTP
from botocore.client import BaseClient
from botocore.exceptions import ClientError
from fastapi import BackgroundTasks

from app.core.config import get_settings

settings = get_settings()


class EmailService:

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
            # await smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            await smtp.login("ses-smtp-user.20250703-111313", "BFkvgWwvPT83A2nHTjm1Lunf9sSgv9CM2TdSieXLmukk")
            smtp_response = await smtp.send_message(message)
            return smtp_response

        except ClientError as e:
            print(f"Failed to send email: {e.response['Error']['Message']}")
            return await smtp.quit()
        except Exception as e:
            print(f"Failed to send email: {e}")
            return await smtp.quit()

    def send_email_background(self, background_tasks: BackgroundTasks, to_email: str, subject: str, html_content: str):
        background_tasks.add_task(self._send_email_sync, to_email, subject, html_content)

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError
from fastapi import BackgroundTasks

from app.core.config import get_settings

settings = get_settings()


class EmailService:
    def __init__(self):
        self.ses_client: BaseClient = boto3.client(
            "ses",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY
        )

    def _send_email_sync(self, to_email: str, subject: str, html_body: str):
        try:
            response = self.ses_client.send_email(
                Source=settings.EMAILS_FROM_EMAIL,
                Destination={"ToAddresses": [to_email]},
                Message={
                    "Subject": {"Data": subject, "Charset": "UTF-8"},
                    "Body": {
                        "Html": {"Data": html_body, "Charset": "UTF-8"},
                        "Text": {"Data": "Please use an HTML-compatible viewer", "Charset": "UTF-8"},
                    },
                },
            )
            return response
        except ClientError as e:
            print(f"Failed to send email: {e.response['Error']['Message']}")
            return None

    def send_email_background(self, background_tasks: BackgroundTasks, to_email: str, subject: str, html_content: str):
        background_tasks.add_task(self._send_email_sync, to_email, subject, html_content)

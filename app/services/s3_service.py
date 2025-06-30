import uuid
from typing import BinaryIO

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from app.core.config import get_settings
from app.dtos.s3_response_dto import S3UploadResponse

settings = get_settings()
class S3Service:
    def __init__(self):
        self.s3_client: BaseClient = boto3.client(
    "s3",
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY
)

    def upload_file(self, file_data: BinaryIO, filename: str, content_type: str) -> S3UploadResponse:
        """Upload a file to an S3 bucket."""
        unique_filename = f"{uuid.uuid4()}_{filename}"
        try:
            self.s3_client.put_object(
                Bucket=settings.AWS_S3_BUCKET,
                Key=unique_filename,
                Body=file_data,
                ContentType=content_type,
                ACL='private'
            )
            return S3UploadResponse(unique_filename, f"https://{settings.AWS_S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{unique_filename}")
        except ClientError as e:
            raise Exception(f"S3 upload failed: {e}")
        except Exception as e:
            print(f"Error uploading file: {e}")
            return S3UploadResponse()

    def generate_presigned_url(self, key: str, expires_in: int = 3600) -> str | None:
        try:
            return self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.AWS_S3_BUCKET, 'Key': key},
                ExpiresIn=expires_in
            )
        except ClientError as e:
            raise Exception(f"Failed to generate presigned URL: {e}")
        except Exception as e:
            print(f"Error generating presigned URL: {e}")
            return None

    def download_file(self, bucket, object_name, file_name):
        """Download a file from an S3 bucket."""
        try:
            self.s3_client.download_file(bucket, object_name, file_name)
        except Exception as e:
            print(f"Error downloading file: {e}")
            return None
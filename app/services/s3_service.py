import boto3

from app.core.config import settings


class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY
)

    def upload_file(self, file_name, bucket, object_name=None):
        """Upload a file to an S3 bucket."""
        if object_name is None:
            object_name = file_name
        try:
            response = self.s3_client.upload_file(file_name, bucket, object_name)
            return response
        except Exception as e:
            print(f"Error uploading file: {e}")
            return None

    def download_file(self, bucket, object_name, file_name):
        """Download a file from an S3 bucket."""
        try:
            self.s3_client.download_file(bucket, object_name, file_name)
        except Exception as e:
            print(f"Error downloading file: {e}")
            return None
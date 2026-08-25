# Service responsible for uploading files to AWS S3.

import os
import boto3

from dotenv import load_dotenv


# Load variables from backend/.env
load_dotenv()


# Read AWS configuration by VARIABLE NAME.
AWS_REGION = os.getenv("AWS_REGION")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


# Fail early if configuration is missing.
if not AWS_REGION:
    raise ValueError("AWS_REGION is missing from the .env file.")

if not AWS_S3_BUCKET_NAME:
    raise ValueError("AWS_S3_BUCKET_NAME is missing from the .env file.")

if not AWS_ACCESS_KEY_ID:
    raise ValueError("AWS_ACCESS_KEY_ID is missing from the .env file.")

if not AWS_SECRET_ACCESS_KEY:
    raise ValueError("AWS_SECRET_ACCESS_KEY is missing from the .env file.")


# Create authenticated AWS S3 client.
s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def upload_file_to_s3(file_path: str, object_name: str) -> str:
    """
    Uploads a local file to the configured AWS S3 bucket.
    """

    s3_client.upload_file(
        file_path,
        AWS_S3_BUCKET_NAME,
        object_name
    )

    return object_name
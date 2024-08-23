import boto3
import os
from dotenv import load_dotenv #not needed for terminal usage, but needed for usage from script

# Load environment variables from .env file
load_dotenv()

s3Client = boto3.client(
    's3',
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
)
"""Quick manual test of the S3 upload. Fill the keys in from .env, never here."""
import boto3

AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)
print(s3.list_buckets())

from dotenv import load_dotenv
import os
import boto3

# Load environment variables from .env file
load_dotenv()

# Access credentials
access_key = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region = os.getenv('AWS_DEFAULT_REGION')

# Initialize S3 client using environment variables
s3 = boto3.client('s3',
                  aws_access_key_id=access_key,
                  aws_secret_access_key=secret_key,
                  region_name=region)

# Test: List buckets
response = s3.list_buckets()


if region == 'us-east-1':
    print("✅ Connected to S3 in us-east-1 region")




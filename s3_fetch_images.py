import boto3
import pandas as pd
from dotenv import load_dotenv
import pickle
import os

load_dotenv()

# AWS Credentials
access_key = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region = os.getenv('AWS_DEFAULT_REGION')

# Init S3
s3 = boto3.client('s3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
)

bucket = 'utkface-aligned-cropped-bhaskar-0424'
prefix = 'utkface_aligned_cropped/'  # Folder path in S3

# List files
response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)

age = []
gender = []
file_list = []

for obj in response.get('Contents', []):
    file_key = obj['Key']
    if not file_key.endswith('.jpg.chip.jpg'):
        continue
    file_list.append(file_key)

    img_name = file_key.split('/')[-1]
    parts = img_name.split('_')

    try:
        age.append(int(parts[0]))
        gender.append(int(parts[1]))
    except:
        print(f"Skipping file with bad name: {file_key}")
        continue

# ✅ Create full S3 URI for each image
df1 = pd.DataFrame({
    'img': ['s3://' + bucket + '/' + key for key in file_list],
    'age': age,
    'gender': gender
})



with open('df1.pkl', 'wb') as f:
    pickle.dump(df1, f)

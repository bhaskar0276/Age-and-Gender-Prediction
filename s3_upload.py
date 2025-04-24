from s3_connector import s3
import os

# Access credentials
access_key = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region = os.getenv('AWS_DEFAULT_REGION')


local_folder = r"C:\Users\tbhas\Downloads\Face_Images\utkface_aligned_cropped"  # Relative path to your local folder
bucket_name = 'utkface-aligned-cropped-bhaskar-0424'

 # Your S3 bucket name


try:
    if region == 'us-east-1':
        s3.create_bucket(Bucket=bucket_name)
    else:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
    print(f"Created bucket: {bucket_name}")
except s3.exceptions.BucketAlreadyOwnedByYou:
    print(f"Bucket {bucket_name} already exists and is owned by you.")
except Exception as e:
    print(f"Bucket creation failed: {e}")



# Optional S3 folder name inside the bucket
s3_prefix = 'utkface_aligned_cropped/'

# Upload all files in the folder recursively
for root, dirs, files in os.walk(local_folder):
    for filename in files:
        local_path = os.path.join(root, filename)
        relative_path = os.path.relpath(local_path, local_folder).replace("\\", "/")
        s3_key = f"{s3_prefix}{relative_path}"  # key = folder/filename.jpg

        try:
            s3.upload_file(local_path, bucket_name, s3_key)
            print(f"Uploaded: {local_path} → s3://{bucket_name}/{s3_key}")
        except Exception as e:
            print(f"Failed to upload {local_path}: {e}")


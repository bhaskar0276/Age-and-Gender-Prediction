import boto3
import os
import sagemaker
from sagemaker.tensorflow import TensorFlow
from dotenv import load_dotenv

load_dotenv()

# ✅ Load credentials from .env
access_key = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region = os.getenv('AWS_DEFAULT_REGION')

# ✅ Setup role and bucket
role = "arn:aws:iam::123456789012:role/service-role/AmazonSageMaker-ExecutionRole-20240715T151805"
bucket = "utkface-aligned-cropped-bhaskar-0424"

# ✅ Create boto3 session with credentials
boto_sess = boto3.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
)

# ✅ Use this session in SageMaker
session = sagemaker.Session(boto_session=boto_sess)

# ✅ Upload your data
input_path = session.upload_data(path='df1.pkl', bucket=bucket, key_prefix='sagemaker/input-data')

# ✅ Launch SageMaker training job
estimator = TensorFlow(
    entry_point='train.py',
    source_dir='.',
    role=role,
    instance_type='ml.m5.large',
    framework_version='2.10',
    py_version='py39',
    dependencies=['requirements.txt'],
    output_path=f's3://{bucket}/sagemaker/output',
    sagemaker_session=session
)

estimator.fit({'train': input_path})

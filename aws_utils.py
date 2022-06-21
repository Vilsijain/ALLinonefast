import os
import boto3
import botocore

s3 = boto3.resource('s3',aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
)
def download_from_s3(bucket_name,key_name,download_file_name):
    try:
        s3 = boto3.resource('s3')
        obj = s3.Object(bucket_name,download_file_name)
        body = obj.get()['Body'].read()   
    except botocore.exceptions.ClientError as error:
        print(error)
    except Exception as e:
        print(e)



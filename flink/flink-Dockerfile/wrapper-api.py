import boto3
import zipfile
import os
import shutil
from io import BytesIO
from urllib.parse import urlparse

def unzip():
    try:
        # url = "https://custom-jobs.s3.us-east-2.amazonaws.com/application.zip"
        url = os.environ.get("FILEPATH")
        parsed_url = urlparse(url)
        bucket=parsed_url.netloc.split('.')[0]
        file=parsed_url.path.lstrip('/')
        print("Bucket: ",bucket," File: ",file)
        # session = boto3.Session(profile_name='your_profile_name')
        resource = boto3.resource('s3', region_name='us-east-2')
        obj = resource.Object(bucket_name=bucket, key=file)
        buffer = BytesIO(obj.get()["Body"].read()) 
        tmp = '/temp' # ADD UUID 
        if not os.path.exists(tmp):
            os.makedirs(tmp, exist_ok=True)
        with zipfile.ZipFile(buffer, "r") as zip_ref:
            zip_ref.extractall(tmp)
        if len(os.listdir(tmp))==0:
            print("Failed to extract!")
        else:
            print(f"Extracted.")
        for root, dirs, files in os.walk(tmp):
            for file in files:
                if file.endswith(".jar"):
                    source_path = os.path.join(root, file)
                    destination_dir = '/opt/flink/lib'
                    print(os.path.abspath(destination_dir))
                    if not os.path.exists(destination_dir):
                        os.makedirs(destination_dir, exist_ok=True)
                    shutil.copy(source_path, destination_dir)
                    print(f"Copied {file} to {destination_dir}")
    except Exception as e:
        print(e)
        print("Error occurred: ",str(e))
    
if __name__ == '__main__':
    unzip()
    
import boto3
import zipfile
import os
import shutil
from io import BytesIO
from urllib.parse import urlparse
import logging
import requests

def unzip():
        url = os.environ.get("FILEPATH")
        parsed_url = urlparse(url)
        bucket=parsed_url.netloc.split('.')[0]
        file=parsed_url.path.lstrip('/')
        print("Bucket: ",bucket," File: ",file)
        resource = boto3.resource('s3', region_name='us-east-2')
        obj = resource.Object(bucket_name=bucket, key=file)
        buffer = BytesIO(obj.get()["Body"].read()) 
        tmp = '/tmp' # ADD UUID 
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
                    destination_dir = '/opt/bitnami/spark/jars/'
                    print(os.path.abspath(destination_dir))
                    if not os.path.exists(destination_dir):
                        os.makedirs(destination_dir, exist_ok=True)
                    shutil.copy(source_path, destination_dir)
                    print(f"Copied {file} to {destination_dir}")
        curl_url='http://localhost:8998/batches/'
        print(1)
        headers = {"Content-Type": "application/json"}
        data =  {
                    "file": "local:/opt/bitnami/spark/jars/data-products-1.0.0.jar",
                    "args": [
                    "/opt/bitnami/spark/conf/jobconfig.conf"
                    ],
                    "className": "org.sunbird.obsrv.dataproducts.MasterDataProcessorIndexer",
                    "conf": {
                        "spark.master": "spark://master-data-indexer-spark-master-svc.spark.svc.cluster.local:7077",
                        "spark.executor.memory":"10g"
                    }
                }
        response = requests.post(url=curl_url, json=data, headers=headers)
        if response.status_code == 200:
             print("Request successful!")
             print(response.text)  # Print the response text
        else:
             print("Error occurred!")
             print("Status code:", response.status_code)
             print("Error message:", response.text)
    
if __name__ == '__main__':
    unzip()

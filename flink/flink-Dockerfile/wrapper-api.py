import boto3
import zipfile
import os
import shutil
from io import BytesIO
from flask import Flask, jsonify, request, make_response
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def unzip():
    try:
        request_data = request.get_json()
        url = request_data.get('s3_url')
        parsed_url = urlparse(url)
        bucket=parsed_url.netloc.split('.')[0]
        file=parsed_url.path.lstrip('/')
        print("Bucket: ",bucket," File: ",file)
        resource = boto3.resource('s3', region_name='us-east-2')
        obj = resource.Object(bucket_name=bucket, key=file)
        buffer = BytesIO(obj.get()["Body"].read()) 
        tmp = 'tmp/'
        if not os.path.exists(tmp):
            os.makedirs(tmp, exist_ok=True)
        with zipfile.ZipFile(buffer, "r") as zip_ref:
            zip_ref.extractall(tmp)
        if len(os.listdir(tmp))==0:
            print("Failed to extract!")
        else:
            print("Extracted.")
        for root, dirs, files in os.walk(tmp):
            for file in files:
                if file.endswith(".jar"):
                    source_path = os.path.join(root, file)
                    destination_dir = 'lib/'
                    if not os.path.exists(destination_dir):
                        os.makedirs(destination_dir, exist_ok=True)
                    shutil.copy(source_path, destination_dir)
                    print(f"Copied {file} to {destination_dir}")
        return make_response("Copied jars", 200)
    except Exception as e:
        print(e)
        return make_response("Error occurred: ",str(e), 500)
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
    
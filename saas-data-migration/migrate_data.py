import os
import gzip
import json
import logging
import requests

from azure.storage.blob import BlobClient, ContainerClient

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, filename='onest_data_transfer.log', encoding='utf-8', level=logging.INFO)

api_url = "http://localhost:9000/data/v2/in/onest-ingest" # need to update with correct topic name
headers = {
  'Content-Type': 'application/json'
}

azure_storage_account_name=os.getenv("AZURE_ACCOUNT_NAME")
azure_storage_account_key=os.getenv("AZURE_ACCOUNT_KEY")

connection_string = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix=core.windows.net".format(azure_storage_account_name, azure_storage_account_key)
container_name = "obsrv-onest"
container = ContainerClient.from_connection_string(conn_str=connection_string, container_name=container_name)
blob_list = container.list_blob_names(name_starts_with="telemetry-data/ingest/")
for blob_ in blob_list:
    blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name=blob_)
    blob_data = blob.download_blob()
    data = gzip.decompress(blob_data.readall())
    json_data = json.loads(data)
    response = requests.request("POST", api_url, headers=headers, json=json_data)
    logging.info("File %s, API response code: %s, API response msg: %s", blob_, response.status_code, response.text)


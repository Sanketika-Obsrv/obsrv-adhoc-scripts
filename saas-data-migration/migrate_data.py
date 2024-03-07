import os
import gzip
import json
import time
import logging
from pathlib import Path

import requests
import pandas as pd
from azure.storage.blob import BlobClient, ContainerClient

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, filename='onest_data_transfer.log', encoding='utf-8', level=logging.INFO)

api_url = "http://localhost:3000/network-observability/v1/in/onest-network-telemetry-v3" # need to update with correct topic name
headers = {
  'Content-Type': 'application/json'
}

azure_storage_account_name=os.getenv("AZURE_ACCOUNT_NAME")
azure_storage_account_key=os.getenv("AZURE_ACCOUNT_KEY")

older_files = []
older_data = Path("logger.log")
if older_data.exists():
    df = pd.read_csv(older_data, names=["file", "status_code", "response_text"])
    df = df[df["status_code"]==200]
    older_files = df["file"].unique().tolist()
connection_string = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix=core.windows.net".format(azure_storage_account_name, azure_storage_account_key)
container_name = "obsrv-onest"
container = ContainerClient.from_connection_string(conn_str=connection_string, container_name=container_name)
blob_list = container.list_blob_names(name_starts_with="telemetry-data/ingest/onest-network-telemetry/")
event_counter = 0
file_counter = 0
for blob_ in blob_list:
    if blob_ not in older_files:
        blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name=blob_)
        blob_data = blob.download_blob()
        data = gzip.decompress(blob_data.readall())
        event_counter_inner = 0
        batch_counter = 0
        for batch in data.splitlines():
            json_data = {"data": json.loads(batch)}
            batch_len = len(json_data["data"]["events"])
            event_counter_inner += batch_len    
            response = requests.request("POST", api_url, headers=headers, json=json_data)
            batch_counter += 1
            logging.info("File %s, Batch id %s, batch size: %s, API response code: %s, API response msg: %s", blob_, json_data["data"]["id"], batch_len, response.status_code, response.text)
            with open("logger.log", "a+") as f:
                f.writeline("{},{},{},{}".format(blob_, json_data["data"]["id"], batch_len, response.status_code))
            print(blob_, json_data["data"]["id"], batch_len, response.status_code)
        file_counter += 1
        event_counter += event_counter_inner
    else:
        print(blob_, "already processed, skipping")
print("total files processed: ", file_counter)
print("total batches processed: ", batch_counter)
print("total events processed: ", event_counter)

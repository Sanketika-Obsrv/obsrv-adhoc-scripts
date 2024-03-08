import gzip
import json
import yaml
import logging
import datetime
from multiprocessing import Pool

import requests
from azure.storage.blob import BlobClient, ContainerClient

start_ = datetime.datetime.now()
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, filename='onest_data_transfer.log', encoding='utf-8', level=logging.INFO)

with open("config.yaml", "r") as f:
    config = yaml.load(f, yaml.FullLoader)

api_url = config["endpoint"] + config["dataset"]
headers = {
  'Content-Type': 'application/json'
}

def process_blob(blob_):
    blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=config["container_name"], blob_name=blob_)
    blob_data = blob.download_blob()
    data = gzip.decompress(blob_data.readall())
    for batch in data.splitlines():
        json_data = {"data": json.loads(batch)}
        batch_len = len(json_data["data"]["events"])
        if batch_len == 0:
            continue
        response = requests.post(api_url, headers=headers, json=json_data)
        logging.info("File %s, Batch id %s, batch size: %s, API response code: %s, API response msg: %s", blob_, json_data["data"]["id"], batch_len, response.status_code, response.text)
        with open("logger.log", "a+") as f:
            f.writelines("{},{},{},{}\n".format(blob_, json_data["data"]["id"], batch_len, response.status_code))
        print(blob_, json_data["data"]["id"], batch_len, response.status_code)

connection_string = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix=core.windows.net".format(config["azure_storage_account_name"], config["azure_storage_account_key"])
container = ContainerClient.from_connection_string(conn_str=connection_string, container_name=config["container_name"])
start_date = config["start_date"]
end_date = config["end_date"]
while start_date < end_date:
    blob_list = container.list_blob_names(name_starts_with=config["prefix"] + start_date.strftime("%Y-%m-%d"))
    with Pool(config["cpus"]) as p:
        p.map(process_blob, [blob_ for blob_ in blob_list])
    start_date += datetime.timedelta(1)
end_ = datetime.datetime.now()
print("time taken: ", end_-start_)

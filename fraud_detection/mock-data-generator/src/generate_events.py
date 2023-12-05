from argparse import ArgumentParser
import requests
import time
import uuid
import pandas as pd

# port forward your API service to push events
BASE_URL = "http://localhost:3000"
DATA_INGEST_ENDPOINT = "http://localhost:3000/obsrv/v1/data/create/"

# no of events per batch
CHUNK_SIZE = 10

# wait time after pushing one batch (in seconds)
WAIT_TIME = 5

def send_events(dataset_id, payload):
    print("pushing events to", dataset_id)
    url = f"{DATA_INGEST_ENDPOINT}{dataset_id}"
    response = requests.post(url, json=payload)
    return response

def sleep(seconds):
    print(f"Waiting for {seconds} seconds...")
    time.sleep(seconds)

def process_records(dataset_id, file_path):
    try:
        df = pd.read_json(file_path, lines=True, orient="records", dtype=False)
        records = df.to_dict(orient="records")
        chunk_size = CHUNK_SIZE
        for i in range(0, len(records), chunk_size):
            chunk = records[i:i + chunk_size]
            id = uuid.uuid4()
            send_events(dataset_id, {"data":{"id": str(id), "events": chunk}})
            if i + chunk_size < len(records):
                sleep(WAIT_TIME)     
    except Exception as e:
        print(f"Error while sending events: {e}")

if __name__ == "__main__":
    parser = ArgumentParser('Mock Data Generator')
    parser.add_argument('-did', '--dataset_id', required=True, help='Specify dataset name to send events')
    parser.add_argument('-path', '--file_path', required=True, help='Specify file path to fetch data')
    args = parser.parse_args()
    dataset_id= args.dataset_id 
    file_path = args.file_path
    process_records(dataset_id, file_path)
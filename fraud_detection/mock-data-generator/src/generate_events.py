from argparse import ArgumentParser
import requests
import time
import uuid
import pandas as pd


# url of obsrv api service
BASE_URL = "http://localhost:4000"

# no of events per batch
CHUNK_SIZE = 10

def send_events(dataset_id, payload):
    print("pushing events to", dataset_id)
    # end point of obsrv data ingest API /obsrv/v1/data/create/:datasetId
    # request body structure for batch events {data: {id: "", events: []}}
    url = f"{BASE_URL}/obsrv/v1/data/create/{dataset_id}"
    response = requests.post(url, json=payload)
    return response

def sleep(seconds):
    print(f"Waiting for {seconds} seconds...")
    time.sleep(seconds)

def process_records(dataset_id, file_path):
    try:
        df = pd.read_json(file_path, compression="gzip", lines=True, orient="records", dtype=False)
        records = df.to_dict(orient="records")
        chunk_size = CHUNK_SIZE
        for i in range(0, len(records), chunk_size):
            print("index", i)
            chunk = records[i:i + chunk_size]
            id = uuid.uuid4()
            send_events(dataset_id, {"data":{"id": str(id), "events": chunk}})
            if i + chunk_size < len(records):
                sleep(60)    # sleep for 60 seconds after pushing one batch
    except Exception as e:
        print(f"Error while sending events: {e}")
if __name__ == "__main__":
    parser = ArgumentParser('Mock Data Generator')
    parser.add_argument('-did', '--dataset_id', required=True, default='test_dataset', help='Specify dataset name to send events')
    parser.add_argument('-path', '--file_path', required=True, default='./sample-files/urcs-events.json.gz', help='Specify file path to fetch data')
    args = parser.parse_args()
    dataset_id= args.dataset_id  
    file_path = args.file_path
    process_records(dataset_id, file_path)

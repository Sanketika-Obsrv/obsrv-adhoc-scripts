## read file name from args and write the events to kafka


import sys
import json
from kafka import KafkaProducer
import time
from argparse import ArgumentParser
import uuid

def parse_args():
    parser = ArgumentParser(description="Ingest data into Kafka")
    parser.add_argument("--file_name", help="Name of the file to ingest", default=None)
    parser.add_argument("--file_prefix", help="Prefix of the file to ingest", default="chunk")
    parser.add_argument("--file_suffix", help="Suffix of the file to ingest", default=1)
    parser.add_argument("--topic", help="Name of the Kafka topic to write to", default="local.ingest")
    parser.add_argument("--bootstrap_servers", help="Kafka bootstrap servers", default="localhost:9092")
    parser.add_argument("--batch", help="Batch size for sending messages", action='store_true')
    parser.add_argument("--batch_name", help="Batch size for sending messages", default="events")
    parser.add_argument("--batch_id", help="Batch size for sending messages", default="id")
    parser.add_argument("--dataset_id", help="Dataset ID", default="new-york-taxi-data")
    parser.add_argument("--verbose", help="Print debug messages", action='store_true')

    args = parser.parse_args()

    if args.file_name is None:
        args.file_name = "{}-{}.json".format(args.file_prefix, args.file_suffix)

    return args

def main():
    args = parse_args()
    producer = KafkaProducer(bootstrap_servers=args.bootstrap_servers)

    print("Ingesting data from file: ", args.file_name)

    with open(f"events/{args.file_name}", 'r') as f:
        events = json.loads(f.read())

    if args.batch:
        batch = {
            args.batch_id: str(uuid.uuid4()),
            args.batch_name: events,
            "obsrv_meta": _get_obsrv_meta(),
            "dataset":args.dataset_id
        }

        if args.verbose:
            print("Sending Batch to Kafka: ", json.dumps(batch))

        producer.send(args.topic, json.dumps(batch).encode('utf-8'))
    else:
        for event in events:
            e = {
                "event": event,
                "obsrv_meta": _get_obsrv_meta(),
                "dataset":args.dataset_id
            }

            if args.verbose:
                print("Sending Event to Kafka: ", json.dumps(e))

            producer.send(args.topic, json.dumps(e).encode('utf-8'))

    producer.flush()
    producer.close()

def _get_obsrv_meta():
    syncts = int(time.time() * 1000)
    obsrv_meta = {
        "syncts": syncts,
        "flags": {},
        "timespans": {},
        "error": {},
        "source":{"entry_source":"python"}
    }

    return obsrv_meta

if __name__ == "__main__":
    main()
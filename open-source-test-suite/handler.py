import config
import requests
from resources.defaults import dataset_defaults, datasource_defaults
from app import rootLogger
import uuid
import os
import json

session = requests.Session()

class DatasetHandler():
    def __init__(self, env) -> None:
        self.master_datasets_schemas_path = "stubs/schemas/master-datasets"
        self.datasets_schemas_path = "stubs/schemas/datasets"
        self.env = env
        print("Creating master dataset...")
        self.create_master_dataset()
        print("Creating dataset...")
        self.create_dataset()
        rootLogger.info("Successfully created Master dataset and dataset...")
        print("Successfully created Master dataset and dataset...")
    
    def create_master_dataset(self):
        schemas = os.listdir(self.master_datasets_schemas_path)
        for schema in schemas:
            with open(f"{self.master_datasets_schemas_path}/{schema}", "r") as f:
                schema_def = json.load(f)
            dataset_payload = dataset_defaults(schema_def["dataset_type"], schema_def["id"], schema_def["schema"], schema_def["ts_key"], schema_def["data_key"], schema_def["denorm_config"], self.env)
            response = session.post(f"{config.API_HOST}{config.ROUTES['CREATE_DATASETS']}", json=dataset_payload)
            if response.raise_for_status():
                print("API Call failed for create master dataset...")
                raise response.json()
            if self.verify_dataset_created(dataset_id=dataset_payload["dataset_id"]):
                pass
            else:
                print("Master Dataset is not found in the list datasets...")
                rootLogger.info("Dataset not listed in response...")
                raise "Dataset missing from list"

    def create_dataset(self):
        schemas = os.listdir(self.datasets_schemas_path)
        for schema in schemas:
            with open(f"{self.datasets_schemas_path}/{schema}", "r") as f:
                schema_def = json.load(f)
            dataset_payload = dataset_defaults(schema_def["dataset_type"], schema_def["id"], schema_def["schema"], schema_def["ts_key"], schema_def["data_key"], schema_def["denorm_config"], self.env)
            response = session.post(f"{config.API_HOST}{config.ROUTES['CREATE_DATASETS']}", json=dataset_payload)
            if response.raise_for_status():
                print("API Call failed for create master dataset...")
                raise response.json()
            if self.verify_dataset_created(dataset_id=dataset_payload["dataset_id"]):
                pass
            else:
                print("Master Dataset is not found in the list datasets...")
                rootLogger.info("Dataset not listed in response...")
                raise "Dataset missing from list"
        
    def verify_dataset_created(self, dataset_id):
        response = session.post(f"{config.API_HOST}{config.ROUTES['LIST_DATASETS']}", json={
            "filters": {
                "status": [
                    "Live"
                ]
            }
        })
        if response.raise_for_status():
            raise response.json()
        return any(dataset.get('dataset_id') == dataset_id for dataset in response.json()["result"])

    def push_data(self, dataset_id, eventsArray):
        request_data = {
            "data": {
                "id": str(uuid.uuid4()),
                "events": eventsArray
            }
        }
        response = session.post(f"{config.API_HOST}{config.ROUTES['PUSH_DATA']}/{dataset_id}", json=request_data)
        if response.raise_for_status():
            raise response.json()
        print(f"Data pushed for {dataset_id}")
        return True

class DatasourceHandler():
    def __init__(self) -> None:
        self.datasets_schemas_path = "stubs/schemas/datasets"
        print("Creating datasource...")
        self.create_datasource()
        rootLogger.info("Successfully created datasource for telemetry dataset...")
        print("Successfully created datasource for telemetry dataset...")

    def create_datasource(self):
        schemas = os.listdir(self.datasets_schemas_path)
        for schema in schemas:
            with open(f"{self.datasets_schemas_path}/{schema}", "r") as f:
                schema_def = json.load(f)
            dataset_payload = datasource_defaults(schema_def["id"], schema_def["ingestion_spec"], schema_def["ts_key"])
            response = session.post(f"{config.API_HOST}{config.ROUTES['CREATE_DATASOURCES']}", json=dataset_payload)
            if response.raise_for_status():
                print("API Call failed for create master dataset...")
                raise response.json()
            if self.verify_datasource_created(dataset_id=dataset_payload["dataset_id"]):
                pass
            else:
                print("Datasource not listed in response...")
                rootLogger.info("Datasource not listed in response...")
                raise "Datasource missing from list"

    def verify_datasource_created(self, dataset_id):
        response = session.post(f"{config.API_HOST}{config.ROUTES['LIST_DATASOURCES']}", json={
            "filters": {
                "status": [
                    "Live"
                ]
            }
        })
        if response.raise_for_status():
            print("API Call failed for listing datasources...")
            raise response.json()
        return any(dataset.get('dataset_id') == dataset_id for dataset in response.json()["result"])

class IngestionHandler():
    def __init__(self) -> None:
        self.datasets_schemas_path = "stubs/schemas/datasets"
        self.submit_dataset_ingestion()
    
    def submit_dataset_ingestion(self):
        print("Submit Ingestion for dataset")
        schemas = os.listdir(self.datasets_schemas_path)
        for schema in schemas:
            with open(f"{self.datasets_schemas_path}/{schema}", "r") as f:
                schema_def = json.load(f)
            dataset_payload = datasource_defaults(schema_def["id"], schema_def["ingestion_spec"], schema_def["ts_key"])
            response = session.post(f"{config.DRUID_HOST}{config.ROUTES['SUBMIT_INGESTION']}", json=dataset_payload["ingestion_spec"])
            if response.raise_for_status():
                print("Failed to submit ingestion spec..")
                raise response.json()
            else:
                print("Ingestion submitted for dataset")

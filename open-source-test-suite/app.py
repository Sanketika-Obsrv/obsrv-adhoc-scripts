import os
import logging
import json
import handler
import subprocess
import re
import time
from config import ENV

cwd = os.getcwd()
rootLogger = logging.getLogger()
logFormatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
fileHandler = logging.FileHandler("{0}.log".format(os.path.join(cwd, __name__)))
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)
rootLogger.setLevel("DEBUG")

def find_pods_and_delete():
    get_pods = subprocess.run(["kubectl", "get", "all", "-n", "flink"], capture_output=True)
    reg = re.compile(r"pod/[\w+-]+")
    pods = re.findall(reg, str(get_pods))
    if(len(pods) < 4 and len(pods) == 4):
        rootLogger.info("Not found 4 pods for the 2 flink jobs")
        print(f"Found {len(pods)} flink processes running")
        raise "All required pods not found"
    else:
        print("Refreshing jobs...")
        for pod in pods:
            rootLogger.info(f"Refreshed pod {pod}")
            subprocess.run(["kubectl", "delete", pod, "-n", "flink"], capture_output=True)
        print("Refreshed jobs...")
        return True

def init():
    rootLogger.info("Initializing...")
    try:
        datasetHandler = handler.DatasetHandler(ENV)
        datasourceHandler = handler.DatasourceHandler()
        ingestionHandler = handler.IngestionHandler()
        rootLogger.info(f"Pushing data for datasets")
        find_pods_and_delete()
        time.sleep(2)
        print(f"Pushing data for Telemetry devices events")
        master_datasets_samples = os.listdir("stubs/sample-data/master-datasets")
        for master_dataset in master_datasets_samples:
            with open(f"stubs/sample-data/master-datasets/{master_dataset}", "r") as f:
                masterDatasetData = json.load(f)
                for x in masterDatasetData:
                    x["api_last_updated_on"] = int(time.time())
            datasetHandler.push_data(dataset_id=masterDatasetData, eventsArray=masterDatasetData)
        datasets_samples = os.listdir("stubs/sample-data/datasets")
        for dataset in datasets_samples:
            with open(f"stubs/sample-data/datasets/{dataset}", "r") as f:
                datasetData = json.load(f)
                for x in datasetData:
                    x["ets"] = int(time.time())
            datasetHandler.push_data(dataset_id=dataset, eventsArray=datasetData)
        rootLogger.info("Datasets have been created and data push was successful.")
        print("Data has been pushed for querying")
    except Exception as e:
        rootLogger.exception(e)
        rootLogger.error("Error occured, exiting...")
        exit()

if __name__ == "__main__":
    init()

import requests
import time
import logging
import datetime
import json
import os
DIR = os.getcwd()
TODAY_TS = round(time.time())
READABLE_TS = datetime.datetime.fromtimestamp(TODAY_TS).strftime("%Y-%m-%d-%H:%M")
LOG_FILE = "logs/log-"+READABLE_TS
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
# 10 datasources
DATASOURCES_LIST = [
    "ingestion-bm-5n-ds9-1",
    "ingestion-bm-5n-ds9-2",
    "ingestion-bm-5n-ds9-3",
    "ingestion-bm-5n-ds9-4",
    "ingestion-bm-5n-ds9-5",
    "ingestion-bm-5n-ds9-6",
    "ingestion-bm-5n-ds9-7",
    "ingestion-bm-5n-ds9-8",
    "ingestion-bm-5n-ds9-9",
    #"ingestion-bm-5n-ds10-10",
]
fileHandler = logging.FileHandler("{0}/{1}.log".format(DIR, LOG_FILE))
DRUID_HOST = "http://10.244.1.28:8888"
logger = logging.getLogger()
logger.addHandler(fileHandler)

def get_supervisor_status(DATASOURCE):
    try:
        DRUID_ROUTERS_URL = f"{DRUID_HOST}/druid/indexer/v1/supervisor/{DATASOURCE}/status"
        result = requests.get(DRUID_ROUTERS_URL)
        result.raise_for_status()
        result = result.json()
        logger.info(f"Current druid lag - {result}")
        write_druid_status(result, DATASOURCE)
        return None
    except Exception as e:
        logger.error("Error getting supervisor status: {}".format(e))
        return None
def write_druid_status(data, DATASOURCE):
    try:
        TODAY_TS = round(time.time())
        READABLE_TS = datetime.datetime.fromtimestamp(TODAY_TS).strftime("%Y-%m-%d-%H:%M")
        FILENAME = f"druid-metrics/{DATASOURCE}/{DATASOURCE}-druid-data-"+READABLE_TS+".json"
        if os.path.exists(FILENAME):
            with open(FILENAME, "w") as file:
                json.dump(data, file)
        else:
            if not os.path.exists(f"druid-metrics/{DATASOURCE}"):
                os.makedirs(f"druid-metrics/{DATASOURCE}")
            with open(FILENAME, "w") as file:
                json.dump(data, file)
        return None
    except Exception as e:
        logger.error("Error writing druid data to file: {}".format(e))
        return None
if __name__ == "__main__":
    for DATASOURCE in DATASOURCES_LIST:
        get_supervisor_status(DATASOURCE=DATASOURCE)


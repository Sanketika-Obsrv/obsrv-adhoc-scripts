import os
import time
import datetime
import logging
import json
import requests
import argparse

DIR = os.getcwd()
TODAY_TS = round(time.time())
READABLE_TS = datetime.datetime.fromtimestamp(TODAY_TS).strftime("%Y-%m-%d-%H:%M")
LOG_FILE = "logs/log-"+READABLE_TS
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()
DRUID_HOST = "http://192.168.67.2:8888"

class IngestionBenchmark():
    def __init__(self, b_number, b_description, b_rows, cpu, events_count):
        self.DRUID_HOST = DRUID_HOST
        self.submitted_ingestions = SubmitIngestions()
        self.DATASOURCES_LIST = self.submitted_ingestions.DATASOURCES_LIST
        self.b_number = b_number
        self.b_description = b_description
        self.b_rows = b_rows
        self.cpu = cpu
        self.run_id = f"ingestion-bm-{self.b_number}-{self.b_rows}"
        self.benchmark_status = {}
        self.start_time = datetime.datetime.now()
        self.events_count = events_count

    def check_if_ingestion_complete(self, DATASOURCE, result):
        try:
            if result["payload"]["aggregateLag"] > 0:
                logging.info(f"Ingestion for {DATASOURCE} is not complete yet")
                return False
            elif result["payload"]["aggregateLag"] == 0 and len(result["payload"]["publishingTasks"]) > 0:
                logging.info(f"Ingestion for {DATASOURCE} is complete and publishing is in progress")
                return False
            elif result["payload"]["aggregateLag"] == 0 and len(result["payload"]["publishingTasks"]) == 0:
                if len(result["payload"]["activeTasks"]) > 0 and result["payload"]["activeTasks"][0]["currentOffsets"]["0"] == self.events_count:
                    logging.info(f"Ingestion and publishing of segments for {DATASOURCE} is complete")
                    return True
                else:
                    return False
        except Exception as e:
            logging.error(f"Error checking if ingestion is complete: {e}")
            return False
        
    def timer(self, DATASOURCE, result):
        # Check if it's been 1hr since ingestion started
        try:
            current_time = datetime.datetime.now()
            time_diff = current_time - self.start_time
            if time_diff.total_seconds() >= 3900:
                logging.info(f"1hr has passed since ingestion started for {DATASOURCE}, terminating supervisor and dropping segments")
                return True
            else:
                return False
        except Exception as e:
            logging.error(f"Error checking if 1hr has passed since ingestion started: {e}")
            return False
        
    def terminate_supervisor(self, DATASOURCE):
        try:
            DRUID_ROUTERS_URL = f"{self.DRUID_HOST}/druid/indexer/v1/supervisor/{DATASOURCE}/terminate"
            result = requests.post(DRUID_ROUTERS_URL)
            result.raise_for_status()
            logging.info(f"Terminated supervisor for {DATASOURCE}")
            return True
        except Exception as e:
            logging.error(f"Error terminating supervisor: {e}")
            return None
        
    def drop_segments(self, DATASOURCE):
        try:
            DRUID_ROUTERS_URL = f"{self.DRUID_HOST}/druid/coordinator/v1/datasources/{DATASOURCE}"
            result = requests.delete(DRUID_ROUTERS_URL)
            result.raise_for_status()
            logging.info(f"Dropped segments for {DATASOURCE}")
            return True
        except Exception as e:
            logging.error(f"Error dropping segments: {e}")
            return None
        
    def kill_tasks(self, DATASOURCE):
        try:
            DRUID_ROUTERS_URL = f"{self.DRUID_HOST}/druid/indexer/v1/tasks"
            result = requests.get(DRUID_ROUTERS_URL)
            result.raise_for_status()
            result = result.json()
            for task in result:
                if task["status"] == "RUNNING"  and (task["dataSource"] == DATASOURCE or task["dataSource"] in DATASOURCE):
                    task_id = task["id"]
                    kill_task_url = f"{self.DRUID_HOST}/druid/indexer/v1/task/{task_id}/shutdown"
                    kill_task = requests.post(kill_task_url)
                    logging.info(f"Killed task {task_id} for {DATASOURCE}")
                    kill_task.raise_for_status()
            logging.info(f"Killed tasks for {DATASOURCE}")
            return True
        except Exception as e:
            logging.error(f"Error killing tasks: {e}")
            return None

    def get_supervisor_status(self, DATASOURCE, ds_key, cpu):
        try:
            DRUID_ROUTERS_URL = f"{self.DRUID_HOST}/druid/indexer/v1/supervisor/{DATASOURCE}/status"
            result = requests.get(DRUID_ROUTERS_URL)
            result.raise_for_status()
            result = result.json()
            logging.info(f"Current druid lag - {result}")
            self.write_druid_status(result, DATASOURCE, ds_key, cpu)
            if self.timer(DATASOURCE, result) or self.check_if_ingestion_complete(DATASOURCE, result):
                kill_supervisor = self.terminate_supervisor(DATASOURCE)
                drop_segments = self.drop_segments(DATASOURCE)
                kill_tasks = self.kill_tasks(DATASOURCE)
                if kill_supervisor and drop_segments:
                    self.benchmark_status[DATASOURCE] = "complete"
                    logging.info(f"Terminated supervisor and dropped segments for {DATASOURCE}")
            return None
        except Exception as e:
            logging.error("Error getting supervisor status: {}".format(e))
            return None

    def write_druid_status(self, data, DATASOURCE, ds_key, cpu):
        try:
            TODAY_TS = round(time.time())
            READABLE_TS = datetime.datetime.fromtimestamp(TODAY_TS).strftime("%Y-%m-%d-%H:%M:%S")
            FILENAME = f"{cpu}-cpu-{self.b_rows}/{ds_key}/{self.run_id}/{DATASOURCE}/{DATASOURCE}-druid-data-"+READABLE_TS+".json"
            if os.path.exists(FILENAME):
                with open(FILENAME, "w") as file:
                    json.dump(data, file)
            else:
                if not os.path.exists(f"{cpu}-cpu-{self.b_rows}/{ds_key}/{self.run_id}/{DATASOURCE}"):
                    os.makedirs(f"{cpu}-cpu-{self.b_rows}/{ds_key}/{self.run_id}/{DATASOURCE}")
                with open(FILENAME, "w") as file:
                    json.dump(data, file)
            
            description_file = f"{cpu}-cpu-{self.b_rows}/{ds_key}/{self.run_id}/{DATASOURCE}/description.txt"
            if not os.path.exists(description_file):
                with open(description_file, "w") as file:
                    file.write(self.b_description)
            return None
        except Exception as e:
            logging.error("Error writing druid data to file: {}".format(e))
            return None
    
    def run(self):
        for ds_key in self.DATASOURCES_LIST.keys():
            # Submit ingestions
            self.submitted_ingestions.run(ds_key, self.b_number, b_rows)
            # Get supervisor status
            self.start_time = datetime.datetime.now()
            
            while True:
                for ds in self.DATASOURCES_LIST[ds_key].keys():
                    logging.info(f"Checking supervisor status for {ds}")
                    self.get_supervisor_status("{}_{}".format(ds, self.b_number), ds_key, self.cpu)
                    final_ds = []
                    for ds in self.DATASOURCES_LIST[ds_key].keys():
                        final_ds.append("{}_{}".format(ds, b_number))
                if set(final_ds).issubset(set(self.benchmark_status.keys())):
                    break
                else:
                    time.sleep(5)
            logging.info(f"Completed benchmark for {ds_key}")
        logging.info(f"Completed benchmark for all datasources")

class SubmitIngestions():
    def __init__(self):
        self.DRUID_HOST = DRUID_HOST
        self.DATASOURCES_LIST = {
            "1-datasources": {
                "ingestions-bm-1-1": "ingestion-bm-ROWS-events-1",
            },
            "2-datasources": {
                "ingestions-bm-2-1": "ingestion-bm-ROWS-events-1",
                "ingestions-bm-2-2": "ingestion-bm-ROWS-events-2",
            },
            "3-datasources": {
                "ingestions-bm-3-1": "ingestion-bm-ROWS-events-1",
                "ingestions-bm-3-2": "ingestion-bm-ROWS-events-2",
                "ingestions-bm-3-3": "ingestion-bm-ROWS-events-3",
            },
            "4-datasources": {
                "ingestions-bm-4-1": "ingestion-bm-ROWS-events-1",
                "ingestions-bm-4-2": "ingestion-bm-ROWS-events-2",
                "ingestions-bm-4-3": "ingestion-bm-ROWS-events-3",
                "ingestions-bm-4-4": "ingestion-bm-ROWS-events-4",
            },
            "5-datasources": {
                "ingestions-bm-5-1": "ingestion-bm-ROWS-events-1",
                "ingestions-bm-5-2": "ingestion-bm-ROWS-events-2",
                "ingestions-bm-5-3": "ingestion-bm-ROWS-events-3",
                "ingestions-bm-5-4": "ingestion-bm-ROWS-events-4",
                "ingestions-bm-5-5": "ingestion-bm-ROWS-events-5",
            },
            "6-datasources": {
                "ingestions-bm-6-1": "ingestion-bm-ROWS-events-1",
                "ingestions-bm-6-2": "ingestion-bm-ROWS-events-2",
                "ingestions-bm-6-3": "ingestion-bm-ROWS-events-3",
                "ingestions-bm-6-4": "ingestion-bm-ROWS-events-4",
                "ingestions-bm-6-5": "ingestion-bm-ROWS-events-5",
                "ingestions-bm-6-6": "ingestion-bm-ROWS-events-6",
            },
            "7-datasources": {
                "ingestions-bm-7-1": "ingestion-bm-ROWS-events-1",
                "ingestions-bm-7-2": "ingestion-bm-ROWS-events-2",
                "ingestions-bm-7-3": "ingestion-bm-ROWS-events-3",
                "ingestions-bm-7-4": "ingestion-bm-ROWS-events-4",
                "ingestions-bm-7-5": "ingestion-bm-ROWS-events-5",
                "ingestions-bm-7-6": "ingestion-bm-ROWS-events-6",
                "ingestions-bm-7-7": "ingestion-bm-ROWS-events-7",
            },
            "8-datasources": {
                "ingestions-bm-8-1": "ingestion-bm-ROWS-events-1",
                "ingestions-bm-8-2": "ingestion-bm-ROWS-events-2",
                "ingestions-bm-8-3": "ingestion-bm-ROWS-events-3",
                "ingestions-bm-8-4": "ingestion-bm-ROWS-events-4",
                "ingestions-bm-8-5": "ingestion-bm-ROWS-events-5",
                "ingestions-bm-8-6": "ingestion-bm-ROWS-events-6",
                "ingestions-bm-8-7": "ingestion-bm-ROWS-events-7",
                "ingestions-bm-8-8": "ingestion-bm-ROWS-events-8",
            },
            "9-datasources": {
                "ingestions-bm-9-1": "ingestion-bm-ROWS-events-1",
                "ingestions-bm-9-2": "ingestion-bm-ROWS-events-2",
                "ingestions-bm-9-3": "ingestion-bm-ROWS-events-3",
                "ingestions-bm-9-4": "ingestion-bm-ROWS-events-4",
                "ingestions-bm-9-5": "ingestion-bm-ROWS-events-5",
                "ingestions-bm-9-6": "ingestion-bm-ROWS-events-6",
                "ingestions-bm-9-7": "ingestion-bm-ROWS-events-7",
                "ingestions-bm-9-8": "ingestion-bm-ROWS-events-8",
                "ingestions-bm-9-9": "ingestion-bm-ROWS-events-9",
            },
            "10-datasources": {
                "ingestions-bm-10-1": "ingestion-bm-ROWS-events-1",
                "ingestions-bm-10-2": "ingestion-bm-ROWS-events-2",
                "ingestions-bm-10-3": "ingestion-bm-ROWS-events-3",
                "ingestions-bm-10-4": "ingestion-bm-ROWS-events-4",
                "ingestions-bm-10-5": "ingestion-bm-ROWS-events-5",
                "ingestions-bm-10-6": "ingestion-bm-ROWS-events-6",
                "ingestions-bm-10-7": "ingestion-bm-ROWS-events-7",
                "ingestions-bm-10-8": "ingestion-bm-ROWS-events-8",
                "ingestions-bm-10-9": "ingestion-bm-ROWS-events-9",
                "ingestions-bm-10-10": "ingestion-bm-ROWS-events-10",
            },
        }

    def submit_ingestion(self, spec, datasource, topic, b_rows):
        spec_copy = spec
        spec_copy["spec"]["dataSchema"]["dataSource"] = datasource
        spec_copy["spec"]["ioConfig"]["topic"] = topic.replace("ROWS", b_rows)

        # Submit ingestion
        try:
            response = requests.post(
                f"{self.DRUID_HOST}/druid/indexer/v1/supervisor",
                json=spec_copy
            )
            response.raise_for_status()
            logging.info(f"Successfully submitted ingestion for {datasource}")
            return None
        except Exception as e:
            logging.error(f"Error submitting ingestion for {datasource}: {e}")
            return None
    
    def run(self, ds_key, b_number, b_rows):
        with open(f"telemetry.json", "r") as file:
            spec = json.load(file)
        for ds, topic in self.DATASOURCES_LIST[ds_key].items():
            self.submit_ingestion(spec, "{}_{}".format(ds, b_number), topic, b_rows)

if __name__ == "__main__":
    rows_choices = ["1m", "2m", "3m", "4m", "5m"]
    parser = argparse.ArgumentParser(description='Run Ingestion benchmark')
    parser.add_argument('-n', '--number', help='Benchmark number', type=int, required=True)
    parser.add_argument('-d', '--description', help='Description for the benchmark', type=str, required=False)
    parser.add_argument('-r', '--rows', help='No. of rows per segment in millions', type=str, choices=rows_choices, required=True)
    parser.add_argument('-c', '--cpu', help='no. of cpus', type=str, required=True)
    args = parser.parse_args()

    b_number = args.number
    b_description = args.description
    b_rows = args.rows
    cpu = args.cpu

    if b_rows == "1m":
        events_count = 1000000
    elif b_rows == "2m":
        events_count = 2000000
    elif b_rows == "3m":
        events_count = 3000000
    elif b_rows == "4m":
        events_count = 4000000
    elif b_rows == "5m":
        events_count = 5000000
    else:
        events_count = 0

    # match b_rows:
    #     case "1m":
    #         events_count = 1000000
    #     case "2m":
    #         events_count = 2000000
    #     case "3m":
    #         events_count = 3000000
    #     case "4m":
    #         events_count = 4000000
    #     case "5m":
    #         events_count = 5000000
    #     case _:
    #         events_count = 0

    folder = f"{cpu}-cpu-{b_rows}"
    folder = os.path.join(DIR, folder)

    if not os.path.exists(folder):
        os.makedirs(folder)
        os.makedirs(folder + "/logs")

    fileHandler = logging.FileHandler("{}/{}.log".format(folder, LOG_FILE))
    logger.addHandler(fileHandler)
    
    ingestion_benchmark = IngestionBenchmark(b_number, b_description, b_rows, cpu, events_count)
    ingestion_benchmark.run()
    logging.info("Ingestion benchmark completed")


# 100mb maxBytesinMemory
# 100217728

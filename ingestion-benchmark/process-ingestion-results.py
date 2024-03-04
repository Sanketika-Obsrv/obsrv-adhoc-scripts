import pandas as pd
from glob import glob
from pathlib import Path
import os
import json
import datetime
pd.set_option("display.max_columns", 100)
json_dir_name = Path("/home/ubuntu/Downloads/benchmarks_data/ingestion_benchmark/cpu-1/10-datasources/ingestion-bm-6-1m")
file_list = sorted(json_dir_name.glob("ingestion-*/*.json"))
# print(file_list)
# Read all folders for json files
result = []
appended = {}
for f_name in file_list:
    data = json.load(open(f_name))
    datasource = data['id']
    for task in data['payload']['activeTasks']:
        if task['currentOffsets'] == {}:
            continue
        if 'currentOffsets' in task and task['currentOffsets']["0"] <= 1000000:
            if task['currentOffsets']["0"] <= 1000000:
                if datasource in appended and task['currentOffsets']["0"] == 1000000:
                    continue
                elif task['currentOffsets']["0"] <= 1000000:
                    task['id'] = datasource
                    task['captureTime'] = data['generationTime']
                    result.append(task)
                    if task['currentOffsets']["0"] == 1000000:
                        appended[datasource] = True
            else:
                continue

df = pd.DataFrame(result)
df = df[df['currentOffsets']!={}]
df['currentOffsets'] = df['currentOffsets'].apply(lambda x: x['0'])
# time_taken_for_5m = df[df['currentOffsets'] <= 5000000]
time_taken_for_5m = df.sort_values(by='captureTime').reset_index(drop=True)
# Aggregate the time taken to ingest 5 million events and compute difference between min and max
result = time_taken_for_5m.groupby('id')['captureTime'].agg(['min', 'max'])
result['time_taken'] = result.apply(lambda x: (datetime.datetime.strptime(x['max'], '%Y-%m-%dT%H:%M:%S.%fZ').timestamp() - datetime.datetime.strptime(x['min'], '%Y-%m-%dT%H:%M:%S.%fZ').timestamp())/3600, axis=1)
# If result['time_taken'] is 0, then set it to 1
result['time_taken'] = result['time_taken'].apply(lambda x: 0.083335 if x == 0 else x)
result['throughput'] = 1000000/result['time_taken']
# Print min of throughput
print(result['throughput'].min())
result.to_csv('ingestion_time.csv')

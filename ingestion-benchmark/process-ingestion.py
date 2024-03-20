import json
import glob
import datetime
import argparse
import statistics

total_events = 3000000


def read_metric_data(dir):
    metrics = []
    for file_name in glob.glob(f"{dir}/*.json"):
        with open(file_name) as file:
            metric_json = json.load(file)
            metric_dict = {}
            if (
                metric_json["payload"]["detailedState"] == "RUNNING"
                and metric_json["payload"]["activeTasks"]
            ):
                metric_dict["generationTime"] = metric_json["generationTime"]
                metric_dict["id"] = metric_json["id"]
                metric_dict["aggregateLag"] = metric_json["payload"]["aggregateLag"]
                current_offsets = 0
                if metric_json["payload"]["activeTasks"][0]["currentOffsets"]:
                    for rec in metric_json["payload"]["activeTasks"]:
                        for key in rec["currentOffsets"]:
                            current_offsets = (
                                current_offsets + rec["currentOffsets"][key]
                            )
                    # metric_dict['currentOffsets'] = metric_json['payload']['activeTasks'][0]['currentOffsets']['0']
                metric_dict["currentOffsets"] = current_offsets
                metrics.append(metric_dict)

    metrics.sort(key=lambda item: item["generationTime"], reverse=False)
    return metrics


def compute_throughput(metrics):
    start_time = datetime.datetime.strptime(
        metrics[0]["generationTime"], "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    # start_agg_lag = metrics[0]['aggregateLag']
    if metrics[0]["currentOffsets"] != 0:
        data = {
            "generationTime": datetime.datetime.strftime(start_time - datetime.timedelta(seconds=5), "%Y-%m-%dT%H:%M:%S.%fZ"),
            "id": metrics[0]["id"],
            "aggregateLag": 0,
            "currentOffsets": 0,
        }
        metrics.insert(0, data)
        start_time = datetime.datetime.strptime(metrics[0]["generationTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
    start_agg_lag = total_events
    throughput_list = []

    for metric in metrics:
        throughput_data = {}
        end_time = datetime.datetime.strptime(metric["generationTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
        if (
            metric["currentOffsets"] == total_events or metric["currentOffsets"] != 0
        ) and metric["aggregateLag"] != start_agg_lag:
            # if (metric['aggregateLag'] != start_agg_lag):
            total_events_processed = abs(start_agg_lag - metric["aggregateLag"])
            time_delta = end_time - start_time
            total_time_elapsed = round(time_delta.total_seconds())
            throughput = total_events_processed * 3600 / total_time_elapsed
            throughput_data["total_events_processed"] = total_events_processed
            throughput_data["total_time_elapsed"] = total_time_elapsed
            throughput_data["throughput"] = throughput
            throughput_list.append(throughput_data)
            start_time = end_time
            start_agg_lag = metric["aggregateLag"]

    sum = 0
    final_data = []
    data_2 = []
    for data in throughput_list:
        print(data)
        final_data.append(data["throughput"])
    sd = statistics.stdev(final_data)
    avg = statistics.mean(final_data)
    high = avg + 1 * sd
    low = avg - 1 * sd
    for num in final_data:
        if low < num < high:
            data_2.append(num)
    print(data_2)
    output_avg = round(statistics.mean(data_2))
    print(output_avg)
    # avg_throughput = round(sum/len(throughput_list))
    # print(f'Avg Throughput: {avg_throughput}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", help="Enter the metrics data directory", required=True)
    args = parser.parse_args()
    dir = args.dir
    metrics_data = read_metric_data(dir)
    compute_throughput(metrics_data)

import argparse
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as fn


class FraudProfileGenerator:
    def __init__(self, data_dir_, source_file_name_, sink_file_name_) -> None:
        self.data_dir = data_dir_
        self.source_file_name = source_file_name_
        self.sink_file_name = sink_file_name_
        self.process_txns()

    def process_txns(self):
        spark = SparkSession.builder.getOrCreate()

        txn_data = spark.read.json(
            str(self.data_dir.joinpath(self.source_file_name))
        ).filter(
            fn.col("txn_status").isin(["DEEMED", "PARTIAL", "SUCCESS"])
        )

        sender_group_1 = txn_data.groupby("sender_account_number").agg(
            fn.count("*").alias("net_transactions"),
            fn.sum("txn_amount").alias("net_amount_spent"),
            fn.stddev_pop("txn_amount").alias("std_dev_net_amount_spent"),
            fn.max("txn_date").alias("latest_txn_date")
        )

        sender_group_2 = txn_data.groupby(["sender_account_number", "txn_date"]).agg(
            fn.sum("txn_amount").alias("daily_amount_spent"),
            fn.count("*").alias("daily_transactions")
        ).groupby("sender_account_number").agg(
            fn.avg("daily_amount_spent").alias("daily_avg_amount_spent"),
            fn.avg("daily_transactions").alias("daily_avg_transactions")
        )

        sender_group = sender_group_1.join(
            sender_group_2, on="sender_account_number", how="fullouter"
        )
        
        receiver_group_1 = txn_data.groupby("receiver_account_number").agg(
            fn.avg("txn_amount").alias("net_amount_received")
        )

        receiver_group_2 = txn_data.groupby(["receiver_account_number", "txn_date"]).agg(
            fn.sum("txn_amount").alias("daily_amount_received")
        ).groupby("receiver_account_number").agg(
            fn.avg("daily_amount_received").alias("daily_avg_amount_received")
        )

        receiver_group = receiver_group_1.join(
            receiver_group_2, on="receiver_account_number", how="fullouter" 
        )
        fraud_profile = sender_group.join(
            receiver_group, 
            on=sender_group.sender_account_number==receiver_group.receiver_account_number, 
            how="fullouter"
        ).withColumn(
            "net_cashflow",
            fn.try_subtract(fn.col("net_amount_spent"), fn.col("net_amount_received"))
        ).withColumn(
            "daily_avg_cashflow",
            fn.try_subtract(fn.col("daily_avg_amount_spent"), fn.col("daily_avg_amount_received"))
        )

        fraud_profile.write.json(
            str(self.data_dir.joinpath(self.sink_file_name)), 
            compression="gzip", mode="overwrite"
        )

        print(str(self.data_dir.joinpath(self.sink_file_name)))
        spark.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", 
        help="the directory path where source and sink file will be located")
    parser.add_argument("--source_file_name", 
        help="the name with which source file exists")
    parser.add_argument("--sink_file_name", 
        help="the name with which output file will be created")
    args = parser.parse_args()
    data_dir__ = Path(args.data_dir)
    source_file_name__ = args.source_file_name
    sink_file_name__ = args.sink_file_name
    fraud_profile = FraudProfileGenerator(
        data_dir_=data_dir__, 
        source_file_name_=source_file_name__, 
        sink_file_name_=sink_file_name__)

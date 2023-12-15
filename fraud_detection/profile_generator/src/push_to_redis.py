import json
from datetime import date, datetime

import redis2
from pyspark.sql import SparkSession

def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s is not serializable" % type(obj))

def to_redis(partition):
    redisClient = redis2.Redis(host="localhost", port=6379, db=3)
    for row in partition:
        data = row.asDict(True)
        row_data = json.dumps(data, indent=4, default=json_serial)
        redisClient.set(data.get("sender_account_number"), row_data)

spark = SparkSession.builder.getOrCreate()
data = spark.read.json("/home/aniket/documents/fraud-detection/mock-data-generator/resources/fraud_profile")
data.rdd.foreachPartition(to_redis)
spark.stop()

from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import functions as fn

from pyspark.sql.types import StringType, FloatType
import datetime
import uuid
import requests
import time

FROM_DATE = "2024-01-31"
TO_DATE = "2024-02-01"

if __name__ == "__main__":
    conf = SparkConf().setAppName("command-service")
    conf.set("fs.s3a.access.key", "b55kAStsLGc973mWiCgY")
    conf.set("fs.s3a.secret.key", "RB0ocdc4jdwPQkLyvJ0JSKLX0acN1m1M3RfIZRow")
    conf.set("fs.s3a.endpoint", "http://192.168.1.2:9000")
    conf.set("fs.s3a.path.style.access", "true")
    conf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    # Region
    conf.set("fs.s3a.endpoint.region", "ap-south-1")
    spark = SparkSession.builder.config(conf=conf).getOrCreate()

    # Get how many days are in the date range
    from_date = datetime.datetime.strptime(FROM_DATE, "%Y-%m-%d")
    to_date = datetime.datetime.strptime(TO_DATE, "%Y-%m-%d")
    date_range = to_date - from_date
    date_range = date_range.days
    # Read JSON files from the input directory
    #df = spark.read.json("/home/sanketika/Downloads/2024-01-02")
    df2 = spark.read.json("file:///Users/praveen/Documents/work/sanketika/obsrv-adhoc-scripts/data-generation/templates/telemetry/output")
    timerange = {}
    timerange_rollup = {}
    @fn.udf(StringType())
    def uuidstr():
        return str(uuid.uuid4())

    @fn.udf(FloatType())
    def getts(current_date):
        return timerange[current_date].pop()

    @fn.udf(FloatType())
    def gettsrollup(current_date):
        return timerange_rollup[current_date].pop()

    for date in range(date_range):
        # Generate 5M events per day within the given date range
        current_date = from_date + datetime.timedelta(days=date)
        timerange_rollup[current_date.strftime("%Y-%m-%d")] = [((current_date + datetime.timedelta(milliseconds=i*17)).timestamp()*1000) for i in range(5000000)]
        timerange_rollup[current_date.strftime("%Y-%m-%d")] = ",".join(str(x) for x in timerange_rollup[current_date.strftime("%Y-%m-%d")])
        #timerange[current_date.strftime("%Y-%m-%d")] = [((current_date + datetime.timedelta(milliseconds=i*17)).timestamp()*1000) for i in range(5000000)]

    for date in range(date_range):
        current_date = from_date + datetime.timedelta(days=date)
        #df = df.withColumn("mid", uuidstr())
        #df = df.withColumn("syncts", getts(fn.lit(current_date.strftime("%Y-%m-%d"))))
        #df = df.withColumn("ets", fn.col("syncts"))
        df2 = df2.drop("syncts")
        df2 = df2.withColumn("mid", uuidstr())
        df2 = df2.withColumn("syncts", fn.lit(timerange_rollup[current_date.strftime("%Y-%m-%d")]))
        df2 = df2.withColumn("syncts", fn.split(df2.syncts, ","))
        df2 = df2.withColumn("syncts", fn.col("syncts").getItem(0).cast(FloatType()))
        df2 = df2.withColumn("ets", fn.col("syncts"))
        #df.write.option("compression", "gzip").json("s3a://ingestion-data/raw-2/{}".format(current_date.strftime("%Y-%m-%d")), mode="overwrite")
        df2.write.option("compression", "gzip").json("file:///Users/praveen/Documents/work/sanketika/obsrv-adhoc-scripts/data-generation/templates/telemetry/output-2/{}".format(current_date.strftime("%Y-%m-%d")), mode="overwrite")
    
    spark.stop()


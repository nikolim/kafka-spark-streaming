import os
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

KAFKA_BROKER = os.environ['KAFKA_BROKER'] if "KAFKA_BROKER" in os.environ else "localhost:9092"

conf = SparkConf()

conf.setAll(
    [
        ('spark.jars.packages',
         'org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0')
    ]
)

spark = SparkSession.builder.config(conf=conf).getOrCreate()
# read stream to kafka broker
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", "raw") \
    .load()

# write stream to console
values = df.selectExpr("CAST(value AS STRING)")

values.writeStream.format("console").start()

# write stream to other kafka topic (publish to broker)
df.writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("topic", "processed") \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .start().awaitTermination()

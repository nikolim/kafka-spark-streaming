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

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", "raw") \
    .load()

# write stream to console
values = df.selectExpr("CAST(value AS STRING)")

schema = StructType().add('btc_price', DoubleType(), False).add('hash_rate', DoubleType(), False).add('event_time', DoubleType(), False)
df_casted = df.selectExpr('CAST(value AS STRING)').select(from_json('value', schema).alias('temp')).select('temp.*')

df_casted = df_casted.withColumn('event_time', current_timestamp())

def compute_correlation(df, id):
    df.withColumn("corr", lit(df.corr("btc_price", "hash_rate"))).show()

def compute_avarage(df, id):
    df.withColumn("avg", lit(df.avg("btc_price"))).show()

# write stream to console
df_casted.writeStream \
    .foreachBatch(compute_correlation) \
    .trigger(processingTime='10 seconds').start()

df_casted.writeStream \
    .foreachBatch(compute_avarage) \
    .trigger(processingTime='10 seconds').start()

# add a watermark to the stream
# df_casted = df_casted.withWatermark("event_time", "1 minute")

# reduce by window and compute correlation
# df_casted \
#     .groupBy(window("event_time", "1 minute"), "event_time") \
#     .agg(corr("btc_price", "hash_rate").alias("corr"), avg("btc_price").alias("avg")) \
#     .selectExpr("to_json(struct(*)) AS value") \
#     .writeStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", KAFKA_BROKER) \
#     .option("topic", "processed") \
#     .option("checkpointLocation", "/tmp/checkpoint1") \
#     .start().awaitTermination()

df_casted.selectExpr("to_json(struct(*)) AS value") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("topic", "processed") \
    .option("checkpointLocation", "/tmp/checkpoint1") \
    .start().awaitTermination()

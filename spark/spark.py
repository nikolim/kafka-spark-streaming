import os
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.functions import from_json, corr, lit, to_json
from pyspark.sql.types import StructType, DoubleType
import pyspark.sql.functions as F
from pyspark.sql.window import Window



KAFKA_BROKER = os.environ['KAFKA_BROKER'] if "KAFKA_BROKER" in os.environ else "localhost:9092"

conf = SparkConf()

conf.setAll(
    [
        ('spark.jars.packages',
         'org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0')
    ]
)

spark = SparkSession.builder.config(conf=conf).getOrCreate()

# read stream from kafka broker
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", "raw") \
    .load()


# to create a DF out of a json object, we need a schema 
schema = StructType().add('btc_price', DoubleType(), False).add('hash_rate', DoubleType(), False).add('timestamp', TimestampType(), False)
df_casted = df.selectExpr('CAST(value AS STRING)').select(from_json('value', schema).alias('temp')).select('temp.*')

df_casted = df_casted.withColumn('doubled_btc_price', col('btc_price') * 2)

# create a moving window
# window = Window.partitionBy().orderBy('timestamp').rowsBetween(-10, 0)

# calculate the average btc price over the last 10 seconds
# df_casted = df_casted.withColumn('avg_btc_price', F.avg('btc_price').over(window))


df_casted.selectExpr("to_json(struct(*)) AS value") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("topic", "processed") \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .start().awaitTermination()

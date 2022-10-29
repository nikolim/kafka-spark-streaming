import os
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.functions import from_json, corr, lit, to_json
from pyspark.sql.types import StructType, DoubleType
import pyspark.sql.functions as F


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
schema = StructType().add('btc_price', DoubleType(), False).add('hash_rate', DoubleType(), False)
df_casted = df.selectExpr('CAST(value AS STRING)').select(from_json('value', schema).alias('temp')).select('temp.*')

# add col and calculate corr
def compute_correlation(df, id):
    df.withColumn("corr", lit(df.corr("btc_price", "hash_rate"))).show()

    # CONVERT BACK TO JSON HERE


df_casted.writeStream \
    .foreachBatch(compute_correlation) \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("topic", "processed") \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .start() \
    .awaitTermination()


# return df with the avatage bitcoin price every 10 seconds
def compute_avarage(df, id):
    resDF = df.select(avg('btc_price')).show()

    # CONVERT BACK TO JSON HERE

    #resDF.select(to_json(struct($"battery_level", "c02_level")).alias("value"))

df_casted.writeStream \
    .foreachBatch(compute_avarage) \
    .trigger(processingTime='10 seconds') \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("topic", "processed") \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .start() \
    .awaitTermination()

# write stream to other kafka topic (publish to broker)
df.writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("topic", "processed") \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .start().awaitTermination()



'''

 OLD CODE

def aggData(df, id):
    df.groupBy(
    window(df.timestamp, "10 seconds", "5 seconds"),
    df.value).show()

df2.writeStream.foreachBatch(aggData).start()
# df_casted = df.selectExpr('CAST(value AS DOUBLE)')
#df2 = df_casted \
#    .withWatermark("timestamp", "10 seconds") \
#    .select(avg('btc_price')).collect()
   # df2.withColumn("id", monotonically_increasing_id())
    #df.withColumn("id", monotonically_increasing_id())

# Previous try. Didn't work. Need to add writeStream to actually write to the stream
# df_casted.withColumn("corr", df_casted.corr("btc_price", "hash_rate")).show()

# But this works?
#df_casted = df_casted.withColumn("corr", col('btc_price')+100)

# write stream to console
#df_hej.writeStream.format("console").start()
    #print(corr)
    #df.withColumn('correlation', lit(df.corr('btc_price', 'hash_rate')))
    #print(corr_value)ç

    #('correlation', corr_value).start()  #lit(df_casted.stat.corr('btc_price', 'hash_rate'))).show()

 '''
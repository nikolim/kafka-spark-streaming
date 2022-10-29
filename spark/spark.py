import os
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.functions import from_json, corr, lit
from pyspark.sql.types import StructType, StringType, IntegerType, DoubleType
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
# read stream to kafka broker
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", "raw") \
    .load()

# to create a DF out of a json object, we need a schema 
schema = StructType().add('btc_price', DoubleType(), False).add('hash_rate', DoubleType(), False)
df_casted = df.selectExpr('CAST(value AS STRING)').select(from_json('value', schema).alias('temp')).select('temp.*')
# df_casted = df.selectExpr('CAST(value AS DOUBLE)')

def processRow(df, id):
    #print("rad", df)
    print("df typ", type(df))
    print("btc price type", type(df['btc_price']))
    df.withColumn("corr", lit(df.corr("btc_price", "hash_rate"))).show()
    #print(corr)
    #df.withColumn('correlation', lit(df.corr('btc_price', 'hash_rate')))
    #print(corr_value)ç
#    return df

# add col and calculate corr
df_casted.writeStream.foreachBatch(processRow).start() #('correlation', corr_value).start()  #lit(df_casted.stat.corr('btc_price', 'hash_rate'))).show()

# write stream to console
df_casted.writeStream.format("console").start()

# write stream to other kafka topic (publish to broker)
df.writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("topic", "processed") \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .start().awaitTermination()

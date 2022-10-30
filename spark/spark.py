import os
import random
import secrets
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
# json_schema = StructType().add('value', StringType(), True)


# add col and calculate corr
# def compute_correlation(df: DataFrame, id):
#     df = df.withColumn("corr", lit(df.corr("btc_price", "hash_rate") + random.uniform(-1,1)))
#     # CONVERT BACK TO JSON HERE

#     # 2. of the data is
#     final_df = df.selectExpr("to_json(struct(*)) AS value")
#     return final_df

    # btc_price = data[0]
    # hash_rate = data[1]
    # corr = data[2]

    # print(btc_price)
    # print(hash_rate)
    # print(corr)

    # df_with_json = spark.createDataFrame(data, ("key", "value"))
    # test = df_with_json.select(to_json(df_with_json.value).alias("json")).collect()
    # print(test)
    # hi = df_with_json.select(to_json(df_with_json.value).alias("json")).collect()
    # print(hi)
    #print(df_cast_string.collect())
    #df_cast_string.select(to_json(df_cast_string.first()).alias("value")).collect()
    #temp.select(to_json(temp.test).alias("json")).show()
    # df.select(to_json(df.first(), schema)).show()
    
# Remove these comments if you wanna run
# df_casted.writeStream \
#    .foreachBatch(compute_correlation).start()

# return df with the avatage bitcoin price every 10 seconds
# def compute_avarage(df, id):
#     df.select(avg('btc_price')).show()

    # CONVERT BACK TO JSON HERE
    #df.select(to_json("avg('btc_price)".cast("string"), schema).alias("value"))
    #resDF.select(to_json(struct($"battery_level", "c02_level")).alias("value"))


# Remove these comments if you wanna run
#df_casted.writeStream \
#    .foreachBatch(compute_avarage) \
#    .trigger(processingTime='10 seconds').start()

# test = df_casted.writeStream.format("console").start()

# # Add comments to line 50-57 if you wanna run
# ds2 = df_casted
    
ds1 = df.selectExpr('CAST(value AS STRING)').select(from_json('value', schema).alias('temp')).select('temp.*')
query1 = ds1.writeStream.format("console").start()

ds2 = ds1.withColumn("corr", lit(ds1.corr("btc_price", "hash_rate") + random.uniform(-1,1))) 
query2 = ds2.writeStream.format("console").start()

# .selectExpr("to_json(struct(*)) AS value") \
# .writeStream \
# .format("kafka") \
# .option("kafka.bootstrap.servers", KAFKA_BROKER) \
# .option("topic", "processed") \
# .option("checkpointLocation", "/tmp/checkpoint") \
# .start();

query1.awaitTermination()
query2.awaitTermination()

    
# Add comments to line 76-84 if you wanna run
# df_casted.writeStream \
#     .foreachBatch(compute_avarage) \
#     .trigger(processingTime='10 seconds') \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", KAFKA_BROKER) \
#     .option("topic", "processed") \
#     .option("checkpointLocation", "/tmp/checkpoint") \
#     .start() \
#     .awaitTermination()

# write stream to other kafka topic (publish to broker)
# this works
# df.writeStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", KAFKA_BROKER) \
#     .option("topic", "processed") \
#     .option("checkpointLocation", "/tmp/checkpoint") \
#     .start().awaitTermination()



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
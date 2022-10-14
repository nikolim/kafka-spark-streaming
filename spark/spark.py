from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

conf = SparkConf()

# Note you have to set set spark-home folder
# export SPARK_HOME=/usr/local/spark

# REMOTE CONFIG (docker-compose)
# docker inspect spark-master | grep IPAddress -> spark-master ip
# conf.setAll(
#     [
#         ("spark.master", "spark://172.19.0.3:7077"),
#         ("spark.driver.host", "local[*]"),
#         ("spark.submit.deployMode", "client"),
#         ("spark.driver.bindAddress", "0.0.0.0"),
#         ('spark.jars.packages',
#          'org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0')
#     ]

# LOCAL CONFIG (local testing)
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
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "raw") \
    .load()

# write stream to console
# values = df.selectExpr("CAST(value AS STRING)")
# values.writeStream.format("console").start().awaitTermination()

# multiply the values in the stream by 2
# processed = df.selectExpr("CAST(value AS DOUBLE)").withColumn("value", col("value") * 2)

# write stream to other kafka topic
df.writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "processed") \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .start().awaitTermination()

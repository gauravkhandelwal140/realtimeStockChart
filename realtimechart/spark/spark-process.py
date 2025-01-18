import os

import yaml
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import time

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.yml")
with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

# Kafka Cluster/Server Details
kafka_host_name = config['kafka'].get('host')
kafka_port_no = config['kafka'].get('port_no')
input_kafka_topic_name = config['kafka'].get('input_topic_name')
output_kafka_topic_name = config['kafka'].get('output_topic_name')
kafka_bootstrap_servers = kafka_host_name + ':' + kafka_port_no

# Postgres Database Server Details
postgres_host_name = config['postgres'].get('host')
postgres_port_no = config['postgres'].get('port_no')
postgres_user_name = config['postgres'].get('username')
postgres_password = config['postgres'].get('password')
postgres_database_name = config['postgres'].get('db_name')
postgres_driver = config['postgres'].get('driver')
postgres_stock_table_name = config.get('postgres_chartsStock_tbl')
postgres_jdbc_url = "jdbc:postgresql://" + postgres_host_name + ":" + str(postgres_port_no) + "/" + postgres_database_name

# https://mvnrepository.com/artifact/mysql/mysql-connector-java
# --packages mysql:mysql-connector-java:5.1.49
# spark-submit --master local[*] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,mysql:mysql-connector-java:5.1.49 --files /home/datamaking/workarea/code/course_download/ecom-real-time-case-study/realtime_data_processing/datamaking_app.conf /home/datamaking/workarea/code/course_download/ecom-real-time-case-study/realtime_data_processing/realtime_data_processing.py

#Create the Database properties
db_properties = {}
db_properties['user'] = postgres_user_name
db_properties['password'] = postgres_password
db_properties['driver'] = postgres_driver

db_properties = {
    "user": postgres_user_name,  # PostgreSQL username
    "password": postgres_password,  # PostgreSQL password
    "driver": "org.postgresql.Driver"  # PostgreSQL JDBC driver
}


def save_to_postgres_table(current_df,postgres_table_name):
    # PostgreSQL connection properties, replace with your actual database details
    # Save the DataFrame to PostgreSQL table
    current_df.write.jdbc(url=postgres_jdbc_url,
                          table=postgres_table_name,
                          mode='append',          # Mode to append to the table
                          properties=db_properties)
    current_df.show()
    print("Exit out of save_to_postgres_table function")

if __name__ == "__main__":
    spark = (SparkSession \
             .builder \
             .appName("Real-Time Data Processing with Kafka Source and Message Format as JSON") \
             .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0") \
             .config("spark.jars", '/opt/spark/postgresql-42.5.1.jar') \
             .master("local[*]")
             .getOrCreate())
    spark.sparkContext.setLogLevel("ERROR")

    schema=(StructType()
            .add("Symbol",StringType())
            .add('Open',FloatType())
            .add('High', FloatType())
            .add('Low', FloatType())
            .add('Close', FloatType())
            .add('Volume', FloatType())
            .add('Adj Close', FloatType())
            .add('Datetime', StringType())
            )

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", input_kafka_topic_name) \
        .option("startingOffsets", "latest") \
        .load()

    df.printSchema()
    # key, value, topic, partition, offset, timestamp

    df1 = df.selectExpr("CAST(value AS STRING)", "timestamp")

    df2 = df1 \
        .select(from_json(col("value"), schema) \
                .alias("data"), "timestamp")

    df3=df2.select("data.*")

    df3=df3.withColumn("Datetime", col("Datetime").cast(LongType()))
    df4=df3.drop("Adj Close")
    df5 = df4 \
        .writeStream \
        .trigger(processingTime='3 seconds') \
        .outputMode("update") \
        .foreachBatch(lambda current_df, epoc_id: save_to_postgres_table(current_df, postgres_stock_table_name)) \
        .start()

    # query = df4 \
    #     .writeStream \
    #     .trigger(processingTime='1 seconds') \
    #     .outputMode("update") \
    #     .option("truncate", "false")\
    #     .format("console") \
    #     .start()
    df5.awaitTermination()


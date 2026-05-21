from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import boto3
import os
from pyspark.sql import SparkSession

def load_covid_to_raw(**context):
    import psycopg2

    s3 = boto3.client(
        "s3",
        endpoint_url="http://minio:9000",
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin"
    )

    
    spark = SparkSession.builder.appName("covid_raw_load").getOrCreate()

    date_path = datetime.now().strftime("%Y/%m/%d")
    objects = s3.list_objects(Bucket="covid-data", Prefix=f"parquet/{date_path}/")

    for obj in objects.get("Contents", []):
        key = obj["Key"]
        filename = key.split("/")[-1]
        s3.download_file("covid-data", key, f"/tmp/{filename}")

    df = spark.read.parquet("/tmp/*.parquet")

    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", "raw.covid") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

    spark.stop()


def load_countries_to_raw(**context):
    s3 = boto3.client(
        "s3",
        endpoint_url="http://minio:9000",
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin"
    )


    spark = SparkSession.builder.appName("countries_raw_load").getOrCreate()

    date_path = datetime.now().strftime("%Y/%m")
    objects = s3.list_objects(Bucket="countries-data", Prefix=f"parquet/{date_path}/")

    for obj in objects.get("Contents", []):
        key = obj["Key"]
        filename = key.split("/")[-1]
        s3.download_file("countries-data", key, f"/tmp/{filename}")

    df = spark.read.parquet("/tmp/*.parquet")

    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", "raw.countries") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

    spark.stop()


with DAG(
    dag_id="raw_load_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False
) as dag:

    t1 = PythonOperator(task_id="load_covid_to_raw",     python_callable=load_covid_to_raw)
    t2 = PythonOperator(task_id="load_countries_to_raw", python_callable=load_countries_to_raw)

    t1 >> t2
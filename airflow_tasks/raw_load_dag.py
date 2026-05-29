"""
Daily pipeline: download Parquet from MinIO → load into PostgreSQL raw schema.
Flow: create_covid_table >> load_covid_to_raw
      create_countries_table >> load_countries_to_raw
"""

from datetime import datetime
import os
import shutil
from airflow import DAG
from airflow.operators.python import PythonOperator
import boto3
from pyspark.sql import SparkSession
from airflow.providers.postgres.operators.postgres import PostgresOperator


def load_covid_to_raw(**context):
    """Download today's COVID Parquet from MinIO and write to raw.covid_data via JDBC."""
    download_dir = "/tmp/covid_data"
    if os.path.exists(download_dir):
        shutil.rmtree(download_dir)
    os.makedirs(download_dir)

    s3 = boto3.client(
        "s3",
        endpoint_url="http://minio:9000",
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin"
    )

    spark = SparkSession.builder \
        .appName("covid_raw_load") \
        .config("spark.jars", "/home/airflow/jars/postgresql-42.6.0.jar") \
        .config("spark.driver.extraClassPath", "/home/airflow/jars/postgresql-42.6.0.jar") \
        .getOrCreate()

    date_path = datetime.now().strftime("%Y/%m/%d")
    objects = s3.list_objects(Bucket="covid-data", Prefix=f"parquet/{date_path}/")

    for obj in objects.get("Contents", []):
        key = obj["Key"]
        filename = key.split("/")[-1]
        s3.download_file("covid-data", key, f"{download_dir}/{filename}")

    df = spark.read.parquet(f"{download_dir}/*.parquet")

    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", "raw.covid_data") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()

    spark.stop()


def load_countries_to_raw(**context):
    """Download current month's countries Parquet from MinIO and write to raw.countries_data via JDBC."""
    download_dir = "/tmp/countries_data"
    if os.path.exists(download_dir):
        shutil.rmtree(download_dir)
    os.makedirs(download_dir)

    s3 = boto3.client(
        "s3",
        endpoint_url="http://minio:9000",
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin"
    )

    spark = SparkSession.builder \
        .appName("country_raw_load") \
        .config("spark.jars", "/home/airflow/jars/postgresql-42.6.0.jar") \
        .config("spark.driver.extraClassPath", "/home/airflow/jars/postgresql-42.6.0.jar") \
        .getOrCreate()

    date_path = datetime.now().strftime("%Y/%m")
    objects = s3.list_objects(Bucket="countries-data", Prefix=f"parquet/{date_path}/")

    for obj in objects.get("Contents", []):
        key = obj["Key"]
        filename = key.split("/")[-1]
        s3.download_file("countries-data", key, f"{download_dir}/{filename}")

    df = spark.read.parquet(f"{download_dir}/*.parquet")

    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", "raw.countries_data") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()

    spark.stop()


with DAG(
    dag_id="raw_load_dag",
    start_date=datetime(2026, 5, 28),
    schedule="@daily",
    catchup=False
) as dag:

    t1 = PostgresOperator(
        task_id="create_covid_table",
        postgres_conn_id="postgre_conn",
        sql="""CREATE TABLE IF NOT EXISTS raw.covid_data (
            date DATE,
            country TEXT,
            cases INT,
            death INT,
            recovered INT
        );""")

    t3 = PostgresOperator(
        task_id="create_countries_table",
        postgres_conn_id="postgre_conn",
        sql="""CREATE TABLE IF NOT EXISTS raw.countries_data (
            country_name TEXT,
            country_code TEXT,
            population BIGINT,
            region TEXT
        );""")

    t2 = PythonOperator(task_id="load_covid_to_raw",     python_callable=load_covid_to_raw)
    t4 = PythonOperator(task_id="load_countries_to_raw", python_callable=load_countries_to_raw)

    t1 >> t2
    t3 >> t4

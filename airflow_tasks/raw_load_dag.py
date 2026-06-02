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
from airflow.hooks.base import BaseHook

def load_from_minio_to_raw(bucket: str,prefix: str,download_dir: str,app_name: str,target_table: str, **context):
    """Download today's COVID Parquet from MinIO and write to raw.covid_data via JDBC."""
    conn = BaseHook.get_connection("postgre_conn")
    
    if os.path.exists(download_dir):
        shutil.rmtree(download_dir)
    os.makedirs(download_dir)

    conn_minio = BaseHook.get_connection("minio_conn")
    s3 = boto3.client(
        "s3",
        endpoint_url=f"http://{conn_minio.host}:{conn_minio.port}",
        aws_access_key_id=conn_minio.login,
        aws_secret_access_key=conn_minio.password
    )

    spark = SparkSession.builder \
        .appName(app_name) \
        .config("spark.jars", "/home/airflow/jars/postgresql-42.6.0.jar") \
        .config("spark.driver.extraClassPath", "/home/airflow/jars/postgresql-42.6.0.jar") \
        .getOrCreate()

    objects = s3.list_objects(Bucket=bucket, Prefix=prefix)

    for obj in objects.get("Contents", []):
        key = obj["Key"]
        filename = key.split("/")[-1]
        s3.download_file(bucket, key, f"{download_dir}/{filename}")

    df = spark.read.parquet(download_dir)



    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", target_table) \
        .option("user", conn.login) \
        .option("password", conn.password) \
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
            deaths INT,
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

    t2 = PythonOperator(
        task_id="load_covid_to_raw",
        python_callable=load_from_minio_to_raw,
        op_kwargs = {
            "bucket": "covid-data",
            "prefix": f"processed/{datetime.now().strftime('%Y/%m/%d')}/",
            "download_dir": "/tmp/covid_data",
            "app_name": "covid_raw_load",
            "target_table": "raw.covid_data"
        }
    )
    t4 = PythonOperator(
        task_id="load_countries_to_raw",
        python_callable=load_from_minio_to_raw,
        op_kwargs={
            "bucket": "countries-data",
            "prefix": f"processed/{datetime.now().strftime('%Y/%m/%d')}/",
            "download_dir": "/tmp/countries_data",
            "app_name": "country_raw_load",
            "target_table": "raw.countries_data"
        }
    )

    t1 >> t2
    t3 >> t4

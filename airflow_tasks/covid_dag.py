import json
import requests
import boto3
import os
from pyspark.sql import SparkSession, Row
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.hooks.base import BaseHook

BUCKET_NAME = "covid-data"

def get_s3_client():
    """Return a boto3 S3 client using credentials from Airflow Connection 'minio_conn'."""
    conn_minio = BaseHook.get_connection("minio_conn")
    return boto3.client(
        "s3",
        endpoint_url=f"http://{conn_minio.host}:{conn_minio.port}",
        aws_access_key_id=conn_minio.login,
        aws_secret_access_key=conn_minio.password
    )

def extract_covid():
    """Fetch COVID-19 stats for all countries from disease.sh API and save raw JSON to MinIO."""
    url = "https://disease.sh/v3/covid-19/countries"
    data = requests.get(url).json()
    s3 = get_s3_client()
    s3.put_object(Bucket=BUCKET_NAME, Key="raw/covid_data.json", Body=json.dumps(data))

def transform_covid():
    """Read raw COVID JSON from MinIO, transform with PySpark, and upload Parquet files."""
    s3 = get_s3_client()
    obj = s3.get_object(Bucket=BUCKET_NAME, Key="raw/covid_data.json")
    data = json.loads(obj['Body'].read().decode('utf-8'))

    spark = SparkSession.builder.appName("covid_transform").getOrCreate()
    rows = [Row(
        country=str(item.get("country", "")),
        cases=int(item.get("cases", 0)),
        deaths=int(item.get("deaths", 0)),
        recovered=int(item.get("recovered", 0)),
        date=datetime.now().strftime("%Y/%m/%d")
    ) for item in data]

    df = spark.createDataFrame(rows)

    tmp_path = "/tmp/transformed_covid"
    df.write.mode("overwrite").parquet(tmp_path)

    date_path = datetime.now().strftime("%Y/%m/%d")
    for file in os.listdir(tmp_path):
        if file.endswith(".parquet"):
            s3.upload_file(f"{tmp_path}/{file}", BUCKET_NAME, f"processed/{date_path}/{file}")

    spark.stop()

with DAG(
        dag_id="covid_dag",
        start_date=datetime(2026, 5, 28),
        schedule="@daily",
        catchup=False
) as dag:
    t1 = PythonOperator(task_id="extract_covid", python_callable=extract_covid)
    t2 = PythonOperator(task_id="transform_covid", python_callable=transform_covid)

    t1 >> t2
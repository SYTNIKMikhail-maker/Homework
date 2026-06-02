import json
import requests
import boto3
import os
from pyspark.sql import SparkSession, Row
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.hooks.base import BaseHook

BUCKET_NAME = "countries-data"


def get_s3_client():
    """Return a boto3 S3 client using credentials from Airflow Connection 'minio_conn'."""
    conn_minio = BaseHook.get_connection("minio_conn")
    return boto3.client(
        "s3",
        endpoint_url=f"http://{conn_minio.host}:{conn_minio.port}",
        aws_access_key_id=conn_minio.login,
        aws_secret_access_key=conn_minio.password
    )


def extract_countries():
    """Fetch all countries from the World Bank API and save raw JSON to MinIO."""
    url = "https://api.worldbank.org/v2/country?format=json&per_page=300"
    data = requests.get(url).json()[1]
    s3 = get_s3_client()
    s3.put_object(Bucket=BUCKET_NAME, Key="raw/countries.json", Body=json.dumps(data))


def transform_countries():
    """Read raw countries JSON from MinIO, transform with PySpark, and upload Parquet files."""
    s3 = get_s3_client()
    obj = s3.get_object(Bucket=BUCKET_NAME, Key="raw/countries.json")
    data = json.loads(obj['Body'].read().decode('utf-8'))

    spark = SparkSession.builder.appName("countries_transform").getOrCreate()
    rows = [Row(
        country_name=str(item.get("name", "")),
        country_code=str(item.get("id", "")),
        population=int(item.get("population", 0)),
        region=str(item.get("region", {}).get("value", ""))
    ) for item in data]

    df = spark.createDataFrame(rows)

    tmp_path = "/tmp/transformed_countries"
    df.write.mode("overwrite").parquet(tmp_path)

    date_path = datetime.now().strftime("%Y/%m")
    for file in os.listdir(tmp_path):
        if file.endswith(".parquet"):
            s3.upload_file(f"{tmp_path}/{file}", BUCKET_NAME, f"processed/{date_path}/{file}")

    spark.stop()


with DAG(
        dag_id="countries_dag",
        start_date=datetime(2026, 5, 28),
        schedule="@monthly",
        catchup=False
) as dag:
    t1 = PythonOperator(task_id="extract_countries", python_callable=extract_countries)
    t2 = PythonOperator(task_id="transform_countries", python_callable=transform_countries)

    t1 >> t2
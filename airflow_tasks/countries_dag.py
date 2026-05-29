"""
Monthly ETL pipeline: World Bank API → PySpark transform → MinIO (Parquet).
Flow: extract_countries >> transform_countries >> load_to_minio
"""
import os
import shutil
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
import boto3



def extract_countries(**context):
    """Fetch all countries from World Bank API and push raw list to XCom."""
    url = "https://api.worldbank.org/v2/country?format=json&per_page=300"
    response = requests.get(url)
    data = response.json()
    countries = data[1]
    context["ti"].xcom_push(key="countries_raw", value=countries)


def transform_countries(**context):
    """Pull raw countries from XCom, build Spark DataFrame, push as JSON strings."""
    from pyspark.sql import SparkSession, Row

    data = context["ti"].xcom_pull(task_ids="extract_countries", key="countries_raw")

    spark = SparkSession.builder \
        .appName("countries_transform") \
        .getOrCreate()

    rows = []
    for item in data:
        rows.append(Row(
            country_id=str(item.get("id", "")),
            country_name=str(item.get("name", "")),
            capital=str(item.get("capitalCity", "")),
            region=str(item.get("region", {}).get("value", "")),
            income_level=str(item.get("incomeLevel", {}).get("value", "")),
            date=datetime.now().strftime("%Y/%m")
        ))

    df = spark.createDataFrame(rows)
    context["ti"].xcom_push(key="countries_transformed", value=df.toJSON().collect())
    spark.stop()


def load_to_minio(**context):
    """Write transformed data to local Parquet, then upload to MinIO bucket."""
    from pyspark.sql import SparkSession

    local_output_dir = "/tmp/countries_parquet_local"
    if os.path.exists(local_output_dir):
        shutil.rmtree(local_output_dir)
    os.makedirs(local_output_dir)

    data = context["ti"].xcom_pull(task_ids="transform_countries", key="countries_transformed")

    spark = SparkSession.builder.appName("countries_load").getOrCreate()
    df = spark.read.json(spark.sparkContext.parallelize(data))

    df.write.mode("overwrite").parquet(local_output_dir)
    spark.stop()

    s3 = boto3.client(
        "s3",
        endpoint_url="http://minio:9000",
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin"
    )

    date_path = datetime.now().strftime("%Y/%m")
    for file in os.listdir(local_output_dir):
        if file.endswith(".parquet"):
            filepath = f"{local_output_dir}/{file}"
            s3.upload_file(filepath, "countries-data", f"parquet/{date_path}/{file}")
    shutil.rmtree(local_output_dir)


with DAG(
        dag_id="countries_dag",
        start_date=datetime(2026, 5, 28),
        schedule="@monthly",
        catchup=False
) as dag:
    t1 = PythonOperator(task_id="extract_countries", python_callable=extract_countries)
    t2 = PythonOperator(task_id="transform_countries", python_callable=transform_countries)
    t3 = PythonOperator(task_id="load_to_minio", python_callable=load_to_minio)

    t1 >> t2 >> t3

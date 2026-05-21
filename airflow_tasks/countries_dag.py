from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import boto3
import os

def extract_countries(**context):
    url = "https://api.worldbank.org/v2/country?format=json&per_page=300"
    response = requests.get(url)
    data = response.json()
    countries = data[1]
    context["ti"].xcom_push(key="countries_raw", value=countries)


def transform_countries(**context):
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


    data = context["ti"].xcom_pull(task_ids="transform_countries", key="countries_transformed")

    from pyspark.sql import SparkSession
    spark = SparkSession.builder.appName("countries_load").getOrCreate()
    df = spark.read.json(spark.sparkContext.parallelize(data))
    df.write.mode("overwrite").parquet("/tmp/countries_parquet")
    spark.stop()

    s3 = boto3.client(
        "s3",
        endpoint_url="http://minio:9000",
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin"
    )

    date_path = datetime.now().strftime("%Y/%m")
    for file in os.listdir("/tmp/countries_parquet"):
        if file.endswith(".parquet"):
            filepath = f"/tmp/countries_parquet/{file}"
            s3.upload_file(filepath, "countries-data", f"parquet/{date_path}/{file}")


with DAG(
    dag_id="countries_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@monthly",
    catchup=False
) as dag:

    t1 = PythonOperator(task_id="extract_countries",   python_callable=extract_countries)
    t2 = PythonOperator(task_id="transform_countries", python_callable=transform_countries)
    t3 = PythonOperator(task_id="load_to_minio",       python_callable=load_to_minio)

    t1 >> t2 >> t3
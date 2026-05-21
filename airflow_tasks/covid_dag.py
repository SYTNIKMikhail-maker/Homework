from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests


def extract_covid(**context):
    url = "https://disease.sh/v3/covid-19/countries"
    response = requests.get(url)
    data = response.json()
    print(f"Extracted {len(data)} records")
    context["ti"].xcom_push(key="covid_raw", value=data)


def transform_covid(**context):
    from pyspark.sql import SparkSession
    from pyspark.sql import Row
    from pyspark.sql.functions import lit

    data = context["ti"].xcom_pull(task_ids="extract_covid", key="covid_raw")

    spark = SparkSession.builder \
        .appName("covid_transform") \
        .getOrCreate()


    rows = []
    for item in data:
        rows.append(Row(
            country=str(item.get("country", "")),
            cases=int(item.get("cases", 0)),
            deaths=int(item.get("deaths", 0)),
            recovered=int(item.get("recovered", 0)),
            active=int(item.get("active", 0)),
            date=datetime.now().strftime("%Y/%m/%d")
        ))

    df = spark.createDataFrame(rows)
    df.show(5)

    context["ti"].xcom_push(key="covid_transformed", value=df.toJSON().collect())
    spark.stop()


def load_to_minio(**context):
    import boto3
    import os
    import json

    data = context["ti"].xcom_pull(task_ids="transform_covid", key="covid_transformed")

    from pyspark.sql import SparkSession
    spark = SparkSession.builder.appName("covid_load").getOrCreate()
    df = spark.read.json(spark.sparkContext.parallelize(data))
    df.write.mode("overwrite").parquet("/tmp/covid_parquet")
    spark.stop()


    s3 = boto3.client(
        "s3",
        endpoint_url="http://minio:9000",
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin"
    )

    date_path = datetime.now().strftime("%Y/%m/%d")
    for file in os.listdir("/tmp/covid_parquet"):
        if file.endswith(".parquet"):
            filepath = f"/tmp/covid_parquet/{file}"
            s3.upload_file(filepath, "covid-data", f"parquet/{date_path}/{file}")
            print(f"Загружен: {file}")


with DAG(
    dag_id="covid_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False
) as dag:

    t1 = PythonOperator(task_id="extract_covid",   python_callable=extract_covid)
    t2 = PythonOperator(task_id="transform_covid", python_callable=transform_covid)
    t3 = PythonOperator(task_id="load_to_minio",   python_callable=load_to_minio)

    t1 >> t2 >> t3
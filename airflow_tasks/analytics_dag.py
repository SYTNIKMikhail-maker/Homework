from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def run_analytics(**context):
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.appName("analytics").getOrCreate()

    covid = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", "warehouse.covid") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .option("driver", "org.postgresql.Driver") \
        .load()

    countries = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", "warehouse.countries") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .option("driver", "org.postgresql.Driver") \
        .load()

    df = covid.join(countries, covid.country == countries.country_name, "left")

    df.show(10)

    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", "warehouse.covid_countries") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()

    spark.stop()


with DAG(
    dag_id="analytics_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False
) as dag:

    t1 = PythonOperator(task_id="run_analytics", python_callable=run_analytics)
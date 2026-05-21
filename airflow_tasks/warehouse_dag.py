from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def load_covid_to_warehouse(**context):
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.appName("warehouse_covid").getOrCreate()

    df = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", "raw.covid") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .option("driver", "org.postgresql.Driver") \
        .load()

    df = df.dropDuplicates()

    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", "warehouse.covid") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()

    spark.stop()


def load_countries_to_warehouse(**context):
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.appName("warehouse_countries").getOrCreate()

    df = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", "raw.countries") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .option("driver", "org.postgresql.Driver") \
        .load()

    df = df.dropDuplicates()

    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", "warehouse.countries") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()

    spark.stop()


with DAG(
    dag_id="warehouse_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False
) as dag:

    t1 = PythonOperator(task_id="load_covid_to_warehouse",     python_callable=load_covid_to_warehouse)
    t2 = PythonOperator(task_id="load_countries_to_warehouse", python_callable=load_countries_to_warehouse)

    t1 >> t2
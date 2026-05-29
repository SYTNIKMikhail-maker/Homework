"""
Daily pipeline: deduplicate raw schema tables and load into warehouse schema.
Flow: create_covid_table >> load_covid_to_warehouse
      create_countries_table >> load_countries_to_warehouse
"""

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator


def load_covid_to_warehouse(**context):
    """Read raw.covid_data via JDBC, deduplicate, and write to warehouse.covid_data."""
    from pyspark.sql import SparkSession

    spark = SparkSession.builder \
        .appName("warehouse_covid") \
        .config("spark.jars", "/home/airflow/jars/postgresql-42.6.0.jar") \
        .config("spark.driver.extraClassPath", "/home/airflow/jars/postgresql-42.6.0.jar") \
        .getOrCreate()

    df = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", "raw.covid_data") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .option("driver", "org.postgresql.Driver") \
        .load()

    df = df.dropDuplicates()

    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", "warehouse.covid_data") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()

    spark.stop()


def load_countries_to_warehouse(**context):
    """Read raw.countries_data via JDBC, deduplicate, and write to warehouse.countries_data."""
    from pyspark.sql import SparkSession

    spark = SparkSession.builder \
        .appName("warehouse_countries") \
        .config("spark.jars", "/home/airflow/jars/postgresql-42.6.0.jar") \
        .config("spark.driver.extraClassPath", "/home/airflow/jars/postgresql-42.6.0.jar") \
        .getOrCreate()

    df = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", "raw.countries_data") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .option("driver", "org.postgresql.Driver") \
        .load()

    df = df.dropDuplicates()

    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", "warehouse.countries_data") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()

    spark.stop()


with DAG(
    dag_id="warehouse_dag",
    start_date=datetime(2026, 5, 28),
    schedule="@daily",
    catchup=False
) as dag:

    t1 = PostgresOperator(
        task_id="create_covid_table",
        postgres_conn_id="postgre_conn",
        sql="""CREATE TABLE IF NOT EXISTS warehouse.covid_data (
            date DATE,
            country TEXT,
            cases INT
        );""")

    t3 = PostgresOperator(
        task_id="create_countries_table",
        postgres_conn_id="postgre_conn",
        sql="""CREATE TABLE IF NOT EXISTS warehouse.countries_data (
            country_name TEXT,
            country_code TEXT,
            population BIGINT,
            region TEXT
        );""")

    t2 = PythonOperator(task_id="load_covid_to_warehouse",     python_callable=load_covid_to_warehouse)
    t4 = PythonOperator(task_id="load_countries_to_warehouse", python_callable=load_countries_to_warehouse)

    t1 >> t2
    t3 >> t4

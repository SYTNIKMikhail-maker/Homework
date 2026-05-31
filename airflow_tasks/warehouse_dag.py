"""
Daily pipeline: deduplicate raw schema tables and load into warehouse schema.
Flow: create_covid_table >> load_covid_to_warehouse
      create_countries_table >> load_countries_to_warehouse
"""

from datetime import datetime
from airflow import DAG
from pyspark.sql import SparkSession
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.base import BaseHook



def load_raw_data_to_warehouse(raw_table: str, dwh_table: str,app_name:str,**context):
    """Read raw.covid_data via JDBC, deduplicate, and write to warehouse.covid_data."""

    conn = BaseHook.get_connection("postgre_conn")

    spark = SparkSession.builder \
        .appName(app_name) \
        .config("spark.jars", "/home/airflow/jars/postgresql-42.6.0.jar") \
        .config("spark.driver.extraClassPath", "/home/airflow/jars/postgresql-42.6.0.jar") \
        .getOrCreate()

    df = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", raw_table) \
        .option("user", conn.login) \
        .option("password", conn.password) \
        .option("driver", "org.postgresql.Driver") \
        .load()

    df = df.dropDuplicates(["date","country"])

    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", dwh_table) \
        .option("user", conn.login) \
        .option("password", conn.password) \
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
            cases INT,
            deaths INT,
            recovered INT,
            active INT
        );""")

    t3 = PostgresOperator(
        task_id="create_countries_table",
        postgres_conn_id="postgre_conn",
        sql="""CREATE TABLE IF NOT EXISTS warehouse.countries_data (
            country_name TEXT,
            country_code TEXT,
            population BIGINT,
            region TEXT,
            income_level TEXT
        );""")

    t2 = PythonOperator(
        task_id="load_covid_to_warehouse",
        python_callable=load_raw_data_to_warehouse,
        op_kwargs = {
            "app_name": "warehouse_covid",
            "raw_table" : "raw.covid_data",
            "dwh_table" : "warehouse.covid_data"
        }
                        )
    t4 = PythonOperator(
        task_id="load_countries_to_warehouse",
        python_callable=load_raw_data_to_warehouse,
        op_kwargs={
            "app_name": "warehouse_countries",
            "raw_table": "raw.countries_data",
            "dwh_table": "warehouse.countries_data"
        }
        )


    t1 >> t2
    t3 >> t4

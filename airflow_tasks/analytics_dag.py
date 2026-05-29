"""
Daily pipeline: join warehouse.covid_data with warehouse.countries_data and write to warehouse.covid_countries_data.
Flow: create_covid_countries_table >> run_analytics
"""

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator


def run_analytics(**context):
    """Join covid and countries warehouse tables and write result to warehouse.covid_countries_data."""
    from pyspark.sql import SparkSession

    spark = SparkSession.builder \
        .appName("analytics") \
        .config("spark.jars", "/home/airflow/jars/postgresql-42.6.0.jar") \
        .config("spark.driver.extraClassPath", "/home/airflow/jars/postgresql-42.6.0.jar") \
        .getOrCreate()

    covid = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", "warehouse.covid_data") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .option("driver", "org.postgresql.Driver") \
        .load()

    countries = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", "warehouse.countries_data") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .option("driver", "org.postgresql.Driver") \
        .load()

    df = covid.join(countries, covid.country == countries.country_name, "left")

    final_df = df.select(
        covid["country"],
        covid["date"],
        covid["cases"].alias("covid_cases"),
        covid["deaths"],
        covid["recovered"],
        covid["active"],
        countries["region"],
        countries["income_level"]
    )

    final_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", "warehouse.covid_countries_data") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()

    spark.stop()


with DAG(
    dag_id="analytics_dag",
    start_date=datetime(2026, 5, 28),
    schedule="@daily",
    catchup=False
) as dag:

    t1 = PostgresOperator(
        task_id="create_covid_countries_table",
        postgres_conn_id="postgre_conn",
        sql="""CREATE TABLE IF NOT EXISTS warehouse.covid_countries_data (
            country_name TEXT,
            country_code TEXT,
            population BIGINT,
            region TEXT
        );""")

    t2 = PythonOperator(task_id="run_analytics", python_callable=run_analytics)

    t1 >> t2

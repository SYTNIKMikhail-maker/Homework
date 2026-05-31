"""
Daily pipeline: join warehouse.covid_data with warehouse.countries_data and write to warehouse.covid_countries_data.
Flow: create_covid_countries_table >> run_analytics
"""

from datetime import datetime
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

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
            country TEXT,
            date DATE,
            cases INT,
            deaths INT,
            recovered INT,
            region TEXT,
            income_level TEXT
        );""")

    t2 = SparkSubmitOperator(
        task_id="run_analytics",
        application="/opt/airflow/airflow_tasks/spark_jobs/analytics_job.py",
        conn_id="spark_default",
        name="covid_countries_join",
        verbose=True,
        env_vars = {
        "POSTGRES_USER": "{{ conn.postgre_conn.login }}",
        "POSTGRES_PASSWORD": "{{ conn.postgre_conn.password }}",
        "POSTGRES_URL": "jdbc:postgresql://postgres:5432/airflow"
    }

    )

    t1 >> t2

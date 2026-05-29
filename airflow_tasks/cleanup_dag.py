"""
Manual DAG: truncates raw.covid_data and raw.countries_data.
Triggered on-demand via schedule=None.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook


def cleanup_raw(**context):
    """Truncate both raw schema tables to free space before next load."""
    hook = PostgresHook(postgres_conn_id="postgre_conn")
    sql = """
        TRUNCATE TABLE raw.covid_data;
        TRUNCATE TABLE raw.countries_data;
    """
    hook.run(sql)


with DAG(
    dag_id="cleanup_dag",
    start_date=datetime(2026, 5, 28),
    schedule=None,
    catchup=False
) as dag:

    t1 = PythonOperator(task_id="cleanup_raw", python_callable=cleanup_raw)
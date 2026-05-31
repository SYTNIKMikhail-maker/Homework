"""
Manual DAG: truncates raw.covid_data and raw.countries_data.
Triggered on-demand via schedule=None.
"""

from datetime import datetime
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator


with DAG(
    dag_id="cleanup_dag",
    start_date=datetime(2026, 5, 28),
    schedule=None,
    catchup=False
) as dag:

    t1 = PostgresOperator(
        task_id="cleanup_raw",
        postgres_conn_id="postgre_conn",
        sql = """
        TRUNCATE TABLE raw.conid_data;
        TRUNCATE TABLE raw.countries_data;
        """
    )

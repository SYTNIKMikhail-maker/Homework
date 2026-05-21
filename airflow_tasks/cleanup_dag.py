from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def cleanup_raw(**context):
    import psycopg2

    conn = psycopg2.connect(
        host="postgres",
        database="airflow",
        user="airflow",
        password="airflow"
    )

    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE raw.covid;")
    cursor.execute("TRUNCATE TABLE raw.countries;")
    conn.commit()
    cursor.close()
    conn.close()

with DAG(
    dag_id="cleanup_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    t1 = PythonOperator(task_id="cleanup_raw", python_callable=cleanup_raw)
FROM apache/airflow:2.7.1

USER root

RUN apt-get update && apt-get install -y openjdk-11-jdk && apt-get clean

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

RUN mkdir -p /home/airflow/jars && \
    curl -o /home/airflow/jars/postgresql-42.6.0.jar \
    https://jdbc.postgresql.org/download/postgresql-42.6.0.jar

USER airflow

RUN pip install pyspark==3.4.0 apache-airflow-providers-amazon boto3
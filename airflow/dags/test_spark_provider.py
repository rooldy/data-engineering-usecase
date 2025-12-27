from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from pendulum import datetime

with DAG(
    dag_id="test_spark_provider",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["test", "spark"],
) as dag:

    spark_test_task = SparkSubmitOperator(
        task_id="spark_test_task",
        application="/opt/airflow/dags/scripts/test_spark.py",
        conn_id="spark_default",
    )

from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator

# Import depuis dags/orchestration (PAS DE sys.path!)
from orchestration.bronze_taskgroup import bronze_taskgroup


DEFAULT_ARGS = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="raw_to_bronze_dag",
    description="Chargement RAW → BRONZE (Spark local)",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["spark", "bronze", "etl"],
) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    bronze = bronze_taskgroup()

    start >> bronze >> end
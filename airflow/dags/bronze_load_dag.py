from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from orchestration.bronze_taskgroup import bronze_taskgroup

DEFAULT_ARGS = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,  # Mettre True si vous configurez les emails
    "email_on_retry": False,
    "execution_timeout": timedelta(hours=2),  # Timeout max pour une task
}

with DAG(
    dag_id="raw_to_bronze_dag",
    description="Chargement RAW → BRONZE (Spark local) - Exécution quotidienne",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2025, 1, 1),
    schedule="@daily",  # Exécution quotidienne à minuit UTC
    catchup=False,  # Ne pas rattraper les runs passés
    max_active_runs=1,  # Empêcher les runs concurrents
    tags=["spark", "bronze", "etl", "production"],
    doc_md="""
    ## Pipeline RAW → BRONZE
    
    **Description:** Transformation des données CSV (RAW) vers Parquet (BRONZE)
    
    **Fréquence:** Quotidienne (minuit UTC)
    
    **Tables traitées:**
    - Dimensions: clients, produits, fournisseurs, entrepôts, moyens_paiement
    - Facts: commandes, produits_commandes, paiements
    - SCD: prix_produits
    
    **Volume:** ~829 MB de données
    """,
) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")
    
    bronze = bronze_taskgroup()
    
    start >> bronze >> end
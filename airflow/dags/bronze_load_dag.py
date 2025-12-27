from datetime import datetime, timedelta

from airflow import DAG
from airflow.utils.task_group import TaskGroup
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

# ============================================================
# CONFIGURATION GÉNÉRALE
# ============================================================

DEFAULT_ARGS = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

SPARK_CONN_ID = "spark_default"
SPARK_APP_BASE_PATH = "/app/src/bronze"

SPARK_CONF = {
    "executor_memory": "2g",
    "driver_memory": "2g",
    "executor_cores": 1,
}

# ============================================================
# DÉFINITION DU DAG
# ============================================================

with DAG(
    dag_id="raw_to_bronze_dag",
    description="Chargement des données RAW vers BRONZE (Dimensions, Facts, SCD)",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,  # déclenchement manuel
    catchup=False,
    tags=["spark", "bronze", "etl"],
) as dag:

    # ========================================================
    # TASK GROUP - DIMENSIONS
    # ========================================================

    with TaskGroup(group_id="dimensions") as dimensions:

        load_dim_clients = SparkSubmitOperator(
            task_id="load_dim_clients",
            conn_id=SPARK_CONN_ID,
            application=f"{SPARK_APP_BASE_PATH}/load_dim_clients.py",
            **SPARK_CONF,
        )

        load_dim_produits = SparkSubmitOperator(
            task_id="load_dim_produits",
            conn_id=SPARK_CONN_ID,
            application=f"{SPARK_APP_BASE_PATH}/load_dim_produits.py",
            **SPARK_CONF,
        )

        load_dim_fournisseurs = SparkSubmitOperator(
            task_id="load_dim_fournisseurs",
            conn_id=SPARK_CONN_ID,
            application=f"{SPARK_APP_BASE_PATH}/load_dim_fournisseurs.py",
            **SPARK_CONF,
        )

        load_dim_entrepots = SparkSubmitOperator(
            task_id="load_dim_entrepots",
            conn_id=SPARK_CONN_ID,
            application=f"{SPARK_APP_BASE_PATH}/load_dim_entrepots.py",
            **SPARK_CONF,
        )

        load_dim_promotions = SparkSubmitOperator(
            task_id="load_dim_promotions",
            conn_id=SPARK_CONN_ID,
            application=f"{SPARK_APP_BASE_PATH}/load_dim_promotions.py",
            **SPARK_CONF,
        )

        load_dim_moyens_paiement = SparkSubmitOperator(
            task_id="load_dim_moyens_paiement",
            conn_id=SPARK_CONN_ID,
            application=f"{SPARK_APP_BASE_PATH}/load_dim_moyens_paiement.py",
            **SPARK_CONF,
        )

    # ========================================================
    # TASK GROUP - FAITS
    # ========================================================

    with TaskGroup(group_id="facts") as facts:

        load_fact_commandes = SparkSubmitOperator(
            task_id="load_fact_commandes",
            conn_id=SPARK_CONN_ID,
            application=f"{SPARK_APP_BASE_PATH}/load_fact_commandes.py",
            **SPARK_CONF,
        )

        load_fact_produits_commandes = SparkSubmitOperator(
            task_id="load_fact_produits_commandes",
            conn_id=SPARK_CONN_ID,
            application=f"{SPARK_APP_BASE_PATH}/load_fact_produits_commandes.py",
            **SPARK_CONF,
        )

        load_fact_panier = SparkSubmitOperator(
            task_id="load_fact_panier",
            conn_id=SPARK_CONN_ID,
            application=f"{SPARK_APP_BASE_PATH}/load_fact_panier.py",
            **SPARK_CONF,
        )

        load_fact_paiements = SparkSubmitOperator(
            task_id="load_fact_paiements",
            conn_id=SPARK_CONN_ID,
            application=f"{SPARK_APP_BASE_PATH}/load_fact_paiements.py",
            **SPARK_CONF,
        )

        load_fact_livraisons_detaillees = SparkSubmitOperator(
            task_id="load_fact_livraisons_detaillees",
            conn_id=SPARK_CONN_ID,
            application=f"{SPARK_APP_BASE_PATH}/load_fact_livraisons_detaillees.py",
            **SPARK_CONF,
        )

        load_fact_evenements_logs = SparkSubmitOperator(
            task_id="load_fact_evenements_logs",
            conn_id=SPARK_CONN_ID,
            application=f"{SPARK_APP_BASE_PATH}/load_fact_evenements_logs.py",
            **SPARK_CONF,
        )

        load_fact_produits_livres = SparkSubmitOperator(
            task_id="load_fact_produits_livres",
            conn_id=SPARK_CONN_ID,
            application=f"{SPARK_APP_BASE_PATH}/load_fact_produits_livres.py",
            **SPARK_CONF,
        )

        load_fact_produits_retournes = SparkSubmitOperator(
            task_id="load_fact_produits_retournes",
            conn_id=SPARK_CONN_ID,
            application=f"{SPARK_APP_BASE_PATH}/load_fact_produits_retournes.py",
            **SPARK_CONF,
        )

    # ========================================================
    # TASK GROUP - SCD / HISTORIQUE
    # ========================================================

    with TaskGroup(group_id="scd") as scd:

        load_scd_prix_produits = SparkSubmitOperator(
            task_id="load_scd_prix_produits",
            conn_id=SPARK_CONN_ID,
            application=f"{SPARK_APP_BASE_PATH}/load_scd_prix_produits.py",
            **SPARK_CONF,
        )

    # ========================================================
    # DÉPENDANCES ENTRE GROUPES
    # ========================================================

    dimensions >> facts >> scd

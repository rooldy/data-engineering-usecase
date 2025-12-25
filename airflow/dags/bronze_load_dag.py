from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

# =========================
# CONFIG GÉNÉRALE
# =========================

DEFAULT_ARGS = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

SPARK_APP_BASE_PATH = "/app/src/bronze"

# =========================
# DAG
# =========================

with DAG(
    dag_id="raw_to_bronze_dag",
    description="Chargement RAW → BRONZE (Dimensions & Facts)",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,  # déclenché manuellement
    catchup=False,
    tags=["bronze", "spark", "etl"],
) as dag:

    # =========================
    # DIMENSIONS
    # =========================

    load_dim_clients = SparkSubmitOperator(
        task_id="load_dim_clients",
        application=f"{SPARK_APP_BASE_PATH}/load_clients.py",
        conn_id="spark_default",
        verbose=True,
    )

    load_dim_produits = SparkSubmitOperator(
        task_id="load_dim_produits",
        application=f"{SPARK_APP_BASE_PATH}/load_produits.py",
        conn_id="spark_default",
        verbose=True,
    )

    load_dim_fournisseurs = SparkSubmitOperator(
        task_id="load_dim_fournisseurs",
        application=f"{SPARK_APP_BASE_PATH}/load_fournisseurs.py",
        conn_id="spark_default",
        verbose=True,
    )

    load_dim_entrepots = SparkSubmitOperator(
        task_id="load_dim_entrepots",
        application=f"{SPARK_APP_BASE_PATH}/load_entrepots.py",
        conn_id="spark_default",
        verbose=True,
    )

    load_dim_promotions = SparkSubmitOperator(
        task_id="load_dim_promotions",
        application=f"{SPARK_APP_BASE_PATH}/load_promotions.py",
        conn_id="spark_default",
        verbose=True,
    )

    load_dim_moyens_paiement = SparkSubmitOperator(
        task_id="load_dim_moyens_paiement",
        application=f"{SPARK_APP_BASE_PATH}/load_moyens_paiement.py",
        conn_id="spark_default",
        verbose=True,
    )

    # =========================
    # FAITS
    # =========================

    load_fact_commandes = SparkSubmitOperator(
        task_id="load_fact_commandes",
        application=f"{SPARK_APP_BASE_PATH}/load_commandes.py",
        conn_id="spark_default",
        verbose=True,
    )

    load_fact_produits_commandes = SparkSubmitOperator(
        task_id="load_fact_produits_commandes",
        application=f"{SPARK_APP_BASE_PATH}/load_produits_commandes.py",
        conn_id="spark_default",
        verbose=True,
    )

    load_fact_panier = SparkSubmitOperator(
        task_id="load_fact_panier",
        application=f"{SPARK_APP_BASE_PATH}/load_panier.py",
        conn_id="spark_default",
        verbose=True,
    )

    load_fact_produits_dans_panier = SparkSubmitOperator(
        task_id="load_fact_produits_dans_panier",
        application=f"{SPARK_APP_BASE_PATH}/load_produits_dans_panier.py",
        conn_id="spark_default",
        verbose=True,
    )

    load_fact_notation_produit = SparkSubmitOperator(
        task_id="load_fact_notation_produit",
        application=f"{SPARK_APP_BASE_PATH}/load_notation_produit.py",
        conn_id="spark_default",
        verbose=True,
    )

    load_fact_paiements = SparkSubmitOperator(
        task_id="load_fact_paiements",
        application=f"{SPARK_APP_BASE_PATH}/load_paiements.py",
        conn_id="spark_default",
        verbose=True,
    )

    load_fact_livraisons_detaillees = SparkSubmitOperator(
        task_id="load_fact_livraisons_detaillees",
        application=f"{SPARK_APP_BASE_PATH}/load_livraisons_detaillees.py",
        conn_id="spark_default",
        verbose=True,
    )

    load_fact_evenements_logs = SparkSubmitOperator(
        task_id="load_fact_evenements_logs",
        application=f"{SPARK_APP_BASE_PATH}/load_evenements_logs.py",
        conn_id="spark_default",
        verbose=True,
    )

    load_fact_produits_livres = SparkSubmitOperator(
        task_id="load_fact_produits_livres",
        application=f"{SPARK_APP_BASE_PATH}/load_produits_livres.py",
        conn_id="spark_default",
        verbose=True,
    )

    load_fact_produits_retournes = SparkSubmitOperator(
        task_id="load_fact_produits_retournes",
        application=f"{SPARK_APP_BASE_PATH}/load_produits_retournes.py",
        conn_id="spark_default",
        verbose=True,
    )

    # =========================
    # HISTORIQUE (SCD)
    # =========================

    load_scd_prix_produits = SparkSubmitOperator(
        task_id="load_scd_prix_produits",
        application=f"{SPARK_APP_BASE_PATH}/load_historique_prix_produits.py",
        conn_id="spark_default",
        verbose=True,
    )

    # =========================
    # DÉPENDANCES
    # =========================

    (
        load_dim_clients
        >> load_fact_commandes
        >> load_fact_produits_commandes
        >> load_fact_produits_livres
        >> load_fact_produits_retournes
    )

    load_dim_produits >> load_fact_produits_commandes
    load_dim_moyens_paiement >> load_fact_paiements
    load_dim_entrepots >> load_fact_livraisons_detaillees
    load_dim_clients >> load_fact_panier

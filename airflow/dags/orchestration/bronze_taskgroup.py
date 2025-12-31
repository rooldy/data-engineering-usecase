from airflow.sdk import TaskGroup
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

SPARK_CONF = {
    "spark.executor.memory": "2g",
    "spark.executor.cores": "1",
    "spark.driver.memory": "1g",
    "spark.sql.shuffle.partitions": "4",
}

SPARK_APP_PATH = "/opt/airflow/src/bronze"


def bronze_taskgroup():
    with TaskGroup(group_id="bronze_layer") as bronze_layer:

        load_dim_clients = SparkSubmitOperator(
            task_id="load_dim_clients",
            application=f"{SPARK_APP_PATH}/load_dim_clients.py",
            conf=SPARK_CONF,
            conn_id="spark_default",
        )

        load_dim_produits = SparkSubmitOperator(
            task_id="load_dim_produits",
            application=f"{SPARK_APP_PATH}/load_dim_produits.py",
            conf=SPARK_CONF,
            conn_id="spark_default",
        )

        load_dim_fournisseurs = SparkSubmitOperator(
            task_id="load_dim_fournisseurs",
            application=f"{SPARK_APP_PATH}/load_dim_fournisseurs.py",
            conf=SPARK_CONF,
            conn_id="spark_default",
        )

        load_dim_entrepots = SparkSubmitOperator(
            task_id="load_dim_entrepots",
            application=f"{SPARK_APP_PATH}/load_dim_entrepots.py",
            conf=SPARK_CONF,
            conn_id="spark_default",
        )

        load_dim_moyens_paiement = SparkSubmitOperator(
            task_id="load_dim_moyens_paiement",
            application=f"{SPARK_APP_PATH}/load_dim_moyens_paiement.py",
            conf=SPARK_CONF,
            conn_id="spark_default",
        )

        load_fact_commandes = SparkSubmitOperator(
            task_id="load_fact_commandes",
            application=f"{SPARK_APP_PATH}/load_fact_commandes.py",
            conf=SPARK_CONF,
            conn_id="spark_default",
        )

        load_fact_produits_commandes = SparkSubmitOperator(
            task_id="load_fact_produits_commandes",
            application=f"{SPARK_APP_PATH}/load_fact_produits_commandes.py",
            conf=SPARK_CONF,
            conn_id="spark_default",
        )

        load_fact_paiements = SparkSubmitOperator(
            task_id="load_fact_paiements",
            application=f"{SPARK_APP_PATH}/load_fact_paiements.py",
            conf=SPARK_CONF,
            conn_id="spark_default",
        )

        load_scd_prix_produits = SparkSubmitOperator(
            task_id="load_scd_prix_produits",
            application=f"{SPARK_APP_PATH}/load_scd_prix_produits.py",
            conf=SPARK_CONF,
            conn_id="spark_default",
        )

        (
            [load_dim_clients, load_dim_produits]
            >> load_fact_commandes
            >> load_fact_produits_commandes
        )

        load_dim_moyens_paiement >> load_fact_paiements
        load_dim_produits >> load_scd_prix_produits

    return bronze_layer

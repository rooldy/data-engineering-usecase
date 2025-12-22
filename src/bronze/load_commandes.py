"""
=========================================
LOAD COMMANDES - BRONZE LAYER
=========================================
Ce script charge la table commandes depuis la couche RAW (CSV)
vers la couche BRONZE (Parquet) en conservant les données quasi brutes.
=========================================
"""

import sys
from pyspark.sql import DataFrame
from pyspark.sql.functions import col

# =========================
# AJOUT DE src DANS sys.path
# =========================
if "/app/src" not in sys.path:
    sys.path.append("/app/src")

# =========================
# IMPORTS
# =========================
from common.spark_session import get_spark_session
from common.paths import raw_table_path, bronze_table_path

# =========================
# CONSTANTES
# =========================
TABLE_NAME = "fact_commandes"  # correspond au dossier RAW/fact_commandes

# =========================
# FONCTION DE CHARGEMENT
# =========================
def load_commandes() -> None:
    """
    Charge les données commandes depuis la couche RAW vers la couche BRONZE.
    - Source : CSV
    - Destination : Parquet
    """

    spark = get_spark_session("bronze_load_commandes")

    raw_path = raw_table_path(TABLE_NAME)
    bronze_path = bronze_table_path(TABLE_NAME)

    print(f"[INFO] Lecture des données RAW depuis : {raw_path}")
    print(f"[INFO] Écriture des données BRONZE vers : {bronze_path}")

    # Lecture CSV (RAW)
    df_raw: DataFrame = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(raw_path)
    )

    # (Bronze = données quasi brutes → pas de transformation lourde)
    df_bronze: DataFrame = df_raw.select(col("*"))

    # Écriture BRONZE en Parquet avec compression snappy
    (
        df_bronze.write
        .mode("overwrite")
        .option("compression", "snappy")
        .parquet(bronze_path)
    )

    print(f"[SUCCESS] Table BRONZE '{TABLE_NAME}' chargée avec succès !")

    spark.stop()
    print("[INFO] SparkSession arrêtée.")

# =========================
# POINT D’ENTRÉE
# =========================
if __name__ == "__main__":
    load_commandes()

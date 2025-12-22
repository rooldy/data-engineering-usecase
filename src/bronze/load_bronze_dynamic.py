"""
Script central dynamique pour le chargement de toutes les tables BRONZE
à partir des fichiers RAW (CSV).

- Compatible : Docker, local, Airflow
- Détecte automatiquement toutes les tables présentes dans /raw
"""

import sys
from pathlib import Path

PROJECT_ROOT = "/app/src"
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from common.spark_session import get_spark_session
from common.paths import raw_table_path, bronze_table_path

from pyspark.sql import DataFrame
from pyspark.sql.functions import col

# =========================
# FONCTION DE CHARGEMENT DYNAMIQUE
# =========================
def load_table_bronze(spark, table_name: str) -> None:
    """
    Charge une table RAW (CSV) vers BRONZE (Parquet)
    """
    raw_path = raw_table_path(table_name)
    bronze_path = bronze_table_path(table_name)

    print(f"[INFO] Lecture RAW : {raw_path}")
    print(f"[INFO] Écriture BRONZE : {bronze_path}")

    df: DataFrame = spark.read.option("header", True).option("inferSchema", True).csv(raw_path)

    df.select(col("*")).write.mode("overwrite").parquet(bronze_path)

    print(f"[SUCCESS] Table BRONZE '{table_name}' chargée \n")


# =========================
# MAIN
# =========================
def main():
    spark = get_spark_session("Bronze_Layer_Load_Dynamic")
    raw_base = Path("/app/data/raw")

    try:
        print("Démarrage du chargement BRONZE dynamique")

        # Lister tous les dossiers dans /raw
        tables = [d.name for d in raw_base.iterdir() if d.is_dir()]
        tables.sort()

        for table in tables:
            load_table_bronze(spark, table)

        print("Chargement BRONZE dynamique terminé avec succès")

    except Exception as e:
        print("Erreur lors du chargement BRONZE dynamique")
        raise e

    finally:
        spark.stop()
        print("SparkSession arrêtée")


# =========================
# POINT D’ENTRÉE
# =========================
if __name__ == "__main__":
    main()

from common.spark_session import get_spark_session
from common.paths import (
    RAW_CLIENTS_PATH,
    BRONZE_CLIENTS_PATH
)

def load_clients():
    """
    Chargement de la table clients
    Raw CSV  → Bronze Parquet
    """

    spark = get_spark_session("bronze_clients")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(RAW_CLIENTS_PATH)
    )

    (
        df.write
        .mode("overwrite")
        .parquet(BRONZE_CLIENTS_PATH)
    )

    print("Bronze clients chargé avec succès")


if __name__ == "__main__":
    load_clients()

from common.spark_session import get_spark_session
from common.paths import (
    RAW_COMMANDES_PATH,
    BRONZE_COMMANDES_PATH
)

def load_commandes():
    """
    Chargement de la table commandes
    """

    spark = get_spark_session("bronze_commandes")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(RAW_COMMANDES_PATH)
    )

    (
        df.write
        .mode("overwrite")
        .parquet(BRONZE_COMMANDES_PATH)
    )

    print("Bronze commandes chargé avec succès")


if __name__ == "__main__":
    load_commandes()

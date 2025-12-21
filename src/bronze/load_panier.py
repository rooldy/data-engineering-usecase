from common.spark_session import get_spark_session
from common.paths import (
    RAW_PANIER_PATH,
    BRONZE_PANIER_PATH
)

def load_panier():
    """
    Chargement de la table panier
    """

    spark = get_spark_session("bronze_panier")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(RAW_PANIER_PATH)
    )

    (
        df.write
        .mode("overwrite")
        .parquet(BRONZE_PANIER_PATH)
    )

    print("Bronze panier chargé avec succès")


if __name__ == "__main__":
    load_panier()

from common.spark_session import get_spark_session
from common.paths import (
    RAW_PRODUITS_PATH,
    BRONZE_PRODUITS_PATH
)

def load_produits():
    """
    Chargement de la table produits
    """

    spark = get_spark_session("bronze_produits")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(RAW_PRODUITS_PATH)
    )

    (
        df.write
        .mode("overwrite")
        .parquet(BRONZE_PRODUITS_PATH)
    )

    print("Bronze produits chargé avec succès")


if __name__ == "__main__":
    load_produits()

from common.spark_session import get_spark_session
from common.paths import (
    RAW_PRODUITS_DANS_PANIERS_PATH,
    BRONZE_PRODUITS_DANS_PANIERS_PATH
)

def load_produits_dans_paniers():
    """
    Chargement de la table produits dans paniers
    """

    spark = get_spark_session("bronze_produits_dans_paniers")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(RAW_PRODUITS_DANS_PANIERS_PATH)
    )

    (
        df.write
        .mode("overwrite")
        .parquet(BRONZE_PRODUITS_DANS_PANIERS_PATH)
    )

    print("Bronze produits dans paniers chargé avec succès")


if __name__ == "__main__":
    load_produits_dans_paniers()

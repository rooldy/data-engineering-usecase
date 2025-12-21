from common.spark_session import get_spark_session
from common.paths import (
    RAW_PRODUITS_COMMANDES_PATH,
    BRONZE_PRODUITS_COMMANDES_PATH
)

def load_produits_commandes():
    """
    Chargement de la table produits commandes
    """

    spark = get_spark_session("bronze_produits_commandes")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(RAW_PRODUITS_COMMANDES_PATH)
    )

    (
        df.write
        .mode("overwrite")
        .parquet(BRONZE_PRODUITS_COMMANDES_PATH)
    )

    print("Bronze produits commandes chargé avec succès")


if __name__ == "__main__":
    load_produits_commandes()

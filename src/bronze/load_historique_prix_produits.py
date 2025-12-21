from common.spark_session import get_spark_session
from common.paths import (
    RAW_HISTORIQUE_PRIX_PRODUITS_PATH,
    BRONZE_HISTORIQUE_PRIX_PRODUITS_PATH
)

def load_historique_prix_produits():
    """
    Chargement de la table historique prix produits
    """

    spark = get_spark_session("bronze_historique_prix_produits")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(RAW_HISTORIQUE_PRIX_PRODUITS_PATH)
    )

    (
        df.write
        .mode("overwrite")
        .parquet(BRONZE_HISTORIQUE_PRIX_PRODUITS_PATH)
    )

    print("Bronze historique prix produits chargé avec succès")


if __name__ == "__main__":
    load_historique_prix_produits()

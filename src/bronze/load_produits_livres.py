from common.spark_session import get_spark_session
from common.paths import (
    RAW_PRODUITS_LIVRES_PATH,
    BRONZE_PRODUITS_LIVRES_PATH
)

def load_produits_livres():
    """
    Chargement de la table produits livres
    """

    spark = get_spark_session("bronze_produits_livres")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(RAW_PRODUITS_LIVRES_PATH)
    )

    (
        df.write
        .mode("overwrite")
        .parquet(BRONZE_PRODUITS_LIVRES_PATH)
    )

    print("Bronze produits livres chargé avec succès")


if __name__ == "__main__":
    load_produits_livres()

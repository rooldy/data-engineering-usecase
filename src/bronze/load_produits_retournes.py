from common.spark_session import get_spark_session
from common.paths import (
    RAW_PRODUITS_RETOURNES_PATH,
    BRONZE_PRODUITS_RETOURNES_PATH
)

def load_produits_retournes():
    """
    Chargement de la table produits retournes
    """

    spark = get_spark_session("bronze_produits_livres")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(RAW_PRODUITS_RETOURNES_PATH)
    )

    (
        df.write
        .mode("overwrite")
        .parquet(BRONZE_PRODUITS_RETOURNES_PATH)
    )

    print("Bronze produits retournes chargé avec succès")


if __name__ == "__main__":
    load_produits_retournes()

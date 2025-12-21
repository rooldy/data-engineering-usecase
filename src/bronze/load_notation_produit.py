from common.spark_session import get_spark_session
from common.paths import (
    RAW_NOTATION_PRODUIT_PATH,
    BRONZE_NOTATION_PRODUIT_PATH
)

def load_notation_produit():
    """
    Chargement de la table notation produit
    """

    spark = get_spark_session("bronze_notation_produit")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(RAW_NOTATION_PRODUIT_PATH)
    )

    (
        df.write
        .mode("overwrite")
        .parquet(BRONZE_NOTATION_PRODUIT_PATH)
    )

    print("Bronze notation produit chargé avec succès")


if __name__ == "__main__":
    load_notation_produit()

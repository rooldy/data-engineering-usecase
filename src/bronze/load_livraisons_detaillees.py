from common.spark_session import get_spark_session
from common.paths import (
    RAW_LIVRAISONS_DETAILLEES_PATH,
    BRONZE_LIVRAISONS_DETAILLEES_PATH
)

def load_livraisons_detaillees():
    """
    Chargement de la table livraisons detaillees
    """

    spark = get_spark_session("bronze_livraisons_detaillees")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(RAW_LIVRAISONS_DETAILLEES_PATH)
    )

    (
        df.write
        .mode("overwrite")
        .parquet(BRONZE_LIVRAISONS_DETAILLEES_PATH)
    )

    print("Bronze livraisons detaillees chargé avec succès")


if __name__ == "__main__":
    load_livraisons_detaillees()

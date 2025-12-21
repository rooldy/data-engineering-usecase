from common.spark_session import get_spark_session
from common.paths import (
    RAW_MOYENS_PAIEMENT_PATH,
    BRONZE_MOYENS_PAIEMENT_PATH
)

def load_moyens_paiement():
    """
    Chargement de la table moyens paiement
    """

    spark = get_spark_session("bronze_moyens_paiement")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(RAW_MOYENS_PAIEMENT_PATH)
    )

    (
        df.write
        .mode("overwrite")
        .parquet(BRONZE_MOYENS_PAIEMENT_PATH)
    )

    print("Bronze moyens paiement chargé avec succès")


if __name__ == "__main__":
    load_moyens_paiement()

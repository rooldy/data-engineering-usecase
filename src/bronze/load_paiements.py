from common.spark_session import get_spark_session
from common.paths import (
    RAW_PAIEMENTS_PATH,
    BRONZE_PAIEMENTS_PATH
)

def load_paiements():
    """
    Chargement de la table paiements
    """

    spark = get_spark_session("bronze_paiements")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(RAW_PAIEMENTS_PATH)
    )

    (
        df.write
        .mode("overwrite")
        .parquet(BRONZE_PAIEMENTS_PATH)
    )

    print("Bronze paiements chargé avec succès")


if __name__ == "__main__":
    load_paiements()

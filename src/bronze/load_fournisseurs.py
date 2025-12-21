from common.spark_session import get_spark_session
from common.paths import (
    RAW_FOURNISSEURS_PATH,
    BRONZE_FOURNISSEURS_PATH
)

def load_fournisseurs():
    """
    Chargement de la table fournisseurs
    """

    spark = get_spark_session("bronze_fournisseurs")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(RAW_FOURNISSEURS_PATH)
    )

    (
        df.write
        .mode("overwrite")
        .parquet(BRONZE_FOURNISSEURS_PATH)
    )

    print("Bronze fournisseurs chargé avec succès")


if __name__ == "__main__":
    load_fournisseurs()

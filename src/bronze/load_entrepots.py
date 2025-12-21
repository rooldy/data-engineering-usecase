from common.spark_session import get_spark_session
from common.paths import (
    RAW_ENTREPOTS_PATH,
    BRONZE_ENTREPOTS_PATH
)

def load_entrepots():
    """
    Chargement de la table entrepots
    """

    spark = get_spark_session("bronze_entrepots")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(RAW_ENTREPOTS_PATH)
    )

    (
        df.write
        .mode("overwrite")
        .parquet(BRONZE_ENTREPOTS_PATH)
    )

    print("Bronze entrepots chargé avec succès")


if __name__ == "__main__":
    load_entrepots()

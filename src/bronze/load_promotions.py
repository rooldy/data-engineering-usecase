from common.spark_session import get_spark_session
from common.paths import (
    RAW_PROMOTIONS_PATH,
    BRONZE_PROMOTIONS_PATH
)

def load_promotions():
    """
    Chargement de la table promotions
    """

    spark = get_spark_session("bronze_promotions")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(RAW_PROMOTIONS_PATH)
    )

    (
        df.write
        .mode("overwrite")
        .parquet(BRONZE_PROMOTIONS_PATH)
    )

    print("Bronze promotions chargé avec succès")


if __name__ == "__main__":
    load_promotions()

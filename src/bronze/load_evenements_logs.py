from common.spark_session import get_spark_session
from common.paths import (
    RAW_EVENEMENTS_LOGS_PATH,
    BRONZE_EVENEMENTS_LOGS_PATH
)

def load_evenements_logs():
    """
    Chargement de la table EVENEMENTS_LOGS
    """

    spark = get_spark_session("bronze_evenements_logs")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(RAW_EVENEMENTS_LOGS_PATH)
    )

    (
        df.write
        .mode("overwrite")
        .parquet(BRONZE_EVENEMENTS_LOGS_PATH)
    )

    print("Bronze evenements logs chargé avec succès")


if __name__ == "__main__":
    load_evenements_logs()

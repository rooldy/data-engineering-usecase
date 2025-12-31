from pyspark.sql import SparkSession


def get_spark_session(app_name: str = "DataEngineeringProject") -> SparkSession:
    """
    Crée et retourne une SparkSession configurée pour le projet.
    
    Le master (local, yarn, k8s...) est volontairement défini
    dans SparkSubmitOperator (Airflow) et NON ici.
    """

    spark = (
        SparkSession.builder
        .appName(app_name)
        .config("spark.sql.shuffle.partitions", "200")
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.sql.execution.arrow.enabled", "true")
        .getOrCreate()
    )

    return spark


if __name__ == "__main__":
    spark = get_spark_session()
    print("SparkSession créée avec succès")
    print(f"Spark version : {spark.version}")
    spark.stop()

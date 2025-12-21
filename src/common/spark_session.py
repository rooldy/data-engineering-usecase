from pyspark.sql import SparkSession

def get_spark_session(app_name: str = "DataEngineeringProject"):
    """
    Crée et retourne une SparkSession configurée pour notre projet.
    
    Args:
        app_name (str): Nom de l'application Spark.
    
    Returns:
        SparkSession
    """
    spark = (
        SparkSession.builder
        .appName(app_name)
        .config("spark.sql.shuffle.partitions", "200")  # Ajustable selon ton cluster
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.sql.execution.arrow.enabled", "true")  # Pour optimiser Pandas <-> Spark
        .getOrCreate()
    )
    return spark

if __name__ == "__main__":
    spark = get_spark_session()
    print("SparkSession créée avec succès !")
    print(f"Version Spark : {spark.version}")
    spark.stop()

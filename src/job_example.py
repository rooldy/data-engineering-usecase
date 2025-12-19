from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("job-example").getOrCreate()

df = spark.range(100)
df.write.mode("overwrite").parquet("/app/data/output")

spark.stop()


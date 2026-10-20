from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip


def get_spark(app="medlake"):
    builder = (
        SparkSession.builder.appName(app)
        .master("local[*]")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog",
                "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.sql.shuffle.partitions", "8")
    )
    return configure_spark_with_delta_pip(builder).getOrCreate()

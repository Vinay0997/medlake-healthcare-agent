from pyspark.sql import functions as F


def to_bronze(spark, raw_path, bronze_path):
    df = (spark.read.option("header", True).csv(raw_path)
          .withColumn("_ingest_ts", F.current_timestamp())
          .withColumn("_source_file", F.input_file_name()))
    df.write.format("delta").mode("overwrite").save(bronze_path)
    return df.count()

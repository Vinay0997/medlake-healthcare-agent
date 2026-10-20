from pyspark.sql import DataFrame, functions as F

AMOUNTS = ["billed_amount", "allowed_amount", "paid_amount"]


def transform_silver(bronze: DataFrame):
    df = bronze
    for c in AMOUNTS:
        df = df.withColumn(c, F.col(c).cast("double"))
    df = df.withColumn("service_date", F.to_date("service_date"))

    valid = (
        F.col("claim_id").isNotNull() & F.col("member_id").isNotNull()
        & F.col("service_date").isNotNull()
        & (F.col("paid_amount") >= 0) & (F.col("billed_amount") > 0)
        & (F.col("paid_amount") <= F.col("billed_amount"))
    )
    good = df.filter(valid)
    rejects = df.filter(~valid).withColumn("_reject_reason", F.lit("failed_validation"))

    good = good.dropDuplicates(["claim_id"])
    good = (good
        .withColumn("member_key", F.sha2(F.col("member_id"), 256))
        .withColumn("member_name_masked", F.lit("***"))
        .withColumn("member_ssn_masked",
                    F.concat(F.lit("***-**-"), F.substring("member_ssn", -4, 4)))
        .drop("member_id", "member_name", "member_ssn")
        .withColumn("service_month", F.date_trunc("month", "service_date").cast("date")))
    return good, rejects


def to_silver(spark, bronze_path, silver_path, quarantine_path):
    good, rejects = transform_silver(spark.read.format("delta").load(bronze_path))
    good.write.format("delta").mode("overwrite").save(silver_path)
    rejects.write.format("delta").mode("overwrite").save(quarantine_path)
    return good.count(), rejects.count()

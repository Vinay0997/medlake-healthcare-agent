from pyspark.sql import functions as F


def to_gold(spark, silver_path, gold_path):
    s = spark.read.format("delta").load(silver_path)

    fact = s.select("claim_id", "member_key", "provider_id", "service_date",
                    "service_month", "procedure_code", "diagnosis_code",
                    "place_of_service", "billed_amount", "allowed_amount", "paid_amount")
    fact.write.format("delta").mode("overwrite").save(f"{gold_path}/fact_claims")

    monthly = (s.groupBy("service_month", "procedure_code")
        .agg(F.count("*").alias("claim_count"),
             F.sum("paid_amount").alias("total_paid"),
             F.avg("paid_amount").alias("avg_paid"),
             F.expr("percentile_approx(paid_amount, 0.5)").alias("median_paid")))
    monthly.write.format("delta").mode("overwrite").save(f"{gold_path}/agg_monthly_cost")

    provider = (s.groupBy("provider_id")
        .agg(F.count("*").alias("claim_count"),
             F.sum("paid_amount").alias("total_paid"),
             F.avg("paid_amount").alias("avg_paid")))
    provider.write.format("delta").mode("overwrite").save(f"{gold_path}/dim_provider_stats")

from medlake.spark import get_spark
from medlake import bronze, silver, gold, quality

RAW, LAKE = "data/raw/claims.csv", "data/lake"


def main():
    spark = get_spark()
    n = bronze.to_bronze(spark, RAW, f"{LAKE}/bronze/claims")
    good, bad = silver.to_silver(spark, f"{LAKE}/bronze/claims",
                                 f"{LAKE}/silver/claims", f"{LAKE}/quarantine/claims")
    s = spark.read.format("delta").load(f"{LAKE}/silver/claims")
    print(quality.check(s, "silver.claims", quality.silver_rules()))
    quality.assert_unique(s, "claim_id")
    gold.to_gold(spark, f"{LAKE}/silver/claims", f"{LAKE}/gold")
    print(f"bronze={n} silver={good} quarantined={bad}")


if __name__ == "__main__":
    main()

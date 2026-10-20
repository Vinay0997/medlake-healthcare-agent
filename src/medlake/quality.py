from pyspark.sql import functions as F


class DataQualityError(Exception):
    pass


def check(df, name, rules: dict):
    failures = []
    total = df.count()
    for rule, cond in rules.items():
        bad = df.filter(~cond).count()
        if bad:
            failures.append(f"{name}.{rule}: {bad}/{total} rows failed")
    if failures:
        raise DataQualityError("; ".join(failures))
    return {"table": name, "rows": total, "status": "pass"}


def silver_rules():
    return {
        "claim_id_not_null": F.col("claim_id").isNotNull(),
        "paid_non_negative": F.col("paid_amount") >= 0,
        "paid_le_billed": F.col("paid_amount") <= F.col("billed_amount"),
        "no_raw_pii": ~F.col("member_ssn_masked").rlike(r"^\d{3}-\d{2}-\d{4}$"),
    }


def assert_unique(df, col):
    d = df.count() - df.dropDuplicates([col]).count()
    if d:
        raise DataQualityError(f"{col}: {d} duplicate keys")

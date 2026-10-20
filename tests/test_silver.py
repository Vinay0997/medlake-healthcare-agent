from medlake.silver import transform_silver

COLS = ["claim_id", "member_id", "member_name", "member_ssn", "provider_id",
        "service_date", "procedure_code", "diagnosis_code", "place_of_service",
        "billed_amount", "allowed_amount", "paid_amount"]


def row(cid, mid="M1", paid="80", billed="100"):
    return (cid, mid, "Jane Doe", "123-45-6789", "P1", "2025-03-14",
            "99213", "I10", "11", billed, "90", paid)


def test_dedupe_quarantine_and_masking(spark):
    df = spark.createDataFrame(
        [row("C1"), row("C1"), row("C2", paid="-1"), row("C3", mid=None)], COLS)
    good, rejects = transform_silver(df)
    assert good.count() == 1
    assert rejects.count() == 2
    r = good.first()
    assert r.member_ssn_masked == "***-**-6789"
    assert "member_name" not in good.columns

import argparse, random
from pathlib import Path
import numpy as np, pandas as pd
from faker import Faker

PROCS = {"99213": 120, "99214": 180, "70450": 650, "80053": 45,
         "93000": 70, "27447": 14000, "45378": 1200, "71046": 150}
DX = ["E11.9", "I10", "J45.909", "M54.5", "N39.0", "K21.9", "F41.1"]
POS = ["11", "21", "22", "23"]


def generate(n=50_000, seed=42):
    rng = np.random.default_rng(seed)
    random.seed(seed)
    fake = Faker()
    Faker.seed(seed)
    members = [(f"M{i:06d}", fake.name(), fake.ssn()) for i in range(5_000)]
    providers = [f"P{i:04d}" for i in range(300)]
    rows = []
    for i in range(n):
        m = members[rng.integers(len(members))]
        code = random.choice(list(PROCS))
        billed = PROCS[code] * rng.lognormal(0, 0.25)
        allowed = billed * rng.uniform(0.4, 0.9)
        rows.append({
            "claim_id": f"C{i:08d}", "member_id": m[0], "member_name": m[1],
            "member_ssn": m[2], "provider_id": random.choice(providers),
            "service_date": fake.date_between("-2y", "today").isoformat(),
            "procedure_code": code, "diagnosis_code": random.choice(DX),
            "place_of_service": random.choice(POS),
            "billed_amount": round(billed, 2),
            "allowed_amount": round(allowed, 2),
            "paid_amount": round(allowed * rng.uniform(0.7, 1.0), 2),
        })
    df = pd.DataFrame(rows)
    dupes = df.sample(frac=0.01, random_state=seed)
    df = pd.concat([df, dupes], ignore_index=True)
    bad = df.sample(frac=0.005, random_state=1).index
    df.loc[bad[: len(bad) // 2], "paid_amount"] = -1
    df.loc[bad[len(bad) // 2:], "member_id"] = None
    return df.sample(frac=1, random_state=seed).reset_index(drop=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=50_000)
    ap.add_argument("--out", default="data/raw/claims.csv")
    a = ap.parse_args()
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    generate(a.rows).to_csv(a.out, index=False)
    print(f"wrote {a.rows} synthetic rows (+dupes/bad rows) to {a.out}")

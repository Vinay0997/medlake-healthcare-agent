# Architecture

raw CSV -> bronze (Delta) -> silver (clean, dedupe, mask, quarantine) -> gold (fact + aggregates)

Data-quality gates run on silver before gold is built.

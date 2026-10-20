# MedLake Agent

Governed multi-agent healthcare cost intelligence on a Delta Lake medallion pipeline, with hybrid RAG, MCP tools and LLM evaluation.

> All data is synthetic or public. No PHI is used.

## Status
- [x] Week 1: synthetic claims, bronze/silver/gold Delta pipeline, PII masking, quarantine, data-quality gates, tests
- [ ] Week 2: cost model, SHAP, MLflow, scoring API
- [ ] Week 3: hybrid RAG, LangGraph agents, MCP tools, guardrails
- [ ] Week 4: Kubernetes, Terraform, CI/CD, observability, evaluation report

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate
make setup
make data
make pipeline
make test
```
Requires Java 17 for Spark.

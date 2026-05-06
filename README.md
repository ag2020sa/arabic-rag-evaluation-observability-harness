# Arabic RAG Evaluation & Observability Harness

[![Arabic RAG Evaluation Gates](https://github.com/ag2020sa/arabic-rag-evaluation-observability-harness/actions/workflows/evaluation.yml/badge.svg)](https://github.com/ag2020sa/arabic-rag-evaluation-observability-harness/actions/workflows/evaluation.yml)
[![Release](https://img.shields.io/github/v/release/ag2020sa/arabic-rag-evaluation-observability-harness)](https://github.com/ag2020sa/arabic-rag-evaluation-observability-harness/releases/tag/v1.0.0)
[![GitHub Pages](https://img.shields.io/badge/portfolio-GitHub%20Pages-blue)](https://ag2020sa.github.io/arabic-rag-evaluation-observability-harness/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Production-minded portfolio MVP for Arabic RAG quality evaluation, lightweight observability, audit history, and release gates.

This repository is a portfolio-ready implementation blueprint and working MVP codebase for evaluating Arabic-first Retrieval-Augmented Generation systems in regulated Saudi enterprise use cases such as HR, labor-law, compliance, cybersecurity governance, and internal knowledge assistants.

The project is designed to wrap around an existing Arabic RAG application, such as a Saudi Labor Law & HR Compliance RAG platform, and continuously answer these questions:

- Are retrieved chunks relevant and complete?
- Are generated Arabic answers grounded in the retrieved sources?
- Are citations accurate and traceable?
- Did a model, prompt, retriever, or dataset change regress quality?
- Are responses safe against prompt injection, jailbreaks, PII leakage, and policy violations?
- Should a candidate release be promoted, blocked, or routed to human review?

---

## Why this project matters

Most RAG demos stop at answering a question. Enterprise RAG systems need repeatable evaluation, monitoring, and release governance. This harness demonstrates production-minded GenAI engineering by combining:

- Arabic-specific preprocessing and quality checks
- Retrieval metrics: Precision@k, Recall@k, MRR, nDCG, Hit Rate
- Generation metrics: rule-based/proxy groundedness, answer relevance, completeness
- Citation validation: source match, coverage, retrieved-source support, and optional page/span checks when metadata is available
- Safety checks: prompt injection, jailbreaks, PII leakage, unsafe tool-use signals
- Observability: structured logs, lightweight trace spans, latency, token/cost accounting, and report diagnostics
- CI/CD decision gates: block release, promote to staging, or require human review
- Registry and audit: dataset/model/prompt/retriever metadata, append-only SQLite run history by run ID, JSON reports, and JSONL feedback events

---

## Project status

This is a **portfolio MVP / production-minded evaluation harness, not a production deployment**.

It is designed to show how an Arabic RAG system could be evaluated, observed, gated, and reported before release. It runs locally, in CI, through a FastAPI demo endpoint, and in a Streamlit dashboard. It does not claim live enterprise deployment, certified compliance, or full replacement for legal/security review.

## Known limitations

- LLM-as-Judge is disabled by default and currently implemented as a placeholder unless replaced with a provider-backed judge.
- Generation scoring uses rule-based/proxy metrics unless a real judge model or claim-level evaluator is configured.
- Citation validation checks source match, citation coverage, unsupported citations, missing citations, retrieved-source support, and span/page metadata when available. It does not prove authoritative legal page/span correctness without authoritative source metadata.
- Observability is lightweight structured logging, local span events, and Prometheus-compatible metric helpers unless a full OpenTelemetry backend/export path is configured.
- SQLite evaluation history is append-only by run ID for portfolio/demo traceability, but it is not a certified immutable audit ledger.
- The included RAG adapter is deterministic and mock-based for CI/demo. Use `HTTPRAGAdapter` or a custom adapter to evaluate a real RAG backend.

---

## Repository layout

```text
.
├── README.md
├── AGENTS.md
├── agent.md
├── pyproject.toml
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── .env.example
├── configs/
│   ├── harness.yaml
│   ├── thresholds.yaml
│   ├── models.yaml
│   └── prompts/
├── data/
│   ├── golden/
│   ├── replay/
│   ├── corpus/
│   └── policies/
├── docs/
├── assets/visuals/
├── src/rag_eval_harness/
├── scripts/
├── dashboard/
├── deploy/
├── monitoring/
├── reports/
└── tests/
```

---

## Quick start

Use the `Makefile` workflow. It creates/uses `.venv` and avoids direct system `pip` installs, which can fail on PEP 668 externally managed Python environments.

### 1. Install the local demo environment

```bash
make install
```

### 2. Run the sample evaluation

```bash
make evaluate
```

### 3. Generate a Markdown release report

```bash
make report
```

### 4. Run tests

```bash
make test
```

### 5. Run the local portfolio demo path

```bash
make demo
```

This runs the sample evaluation, generates the release report, and executes the unit tests.

### 6. Start the API locally

```bash
make api
```

Open:

```text
http://localhost:8080/docs
```

### 7. Start the dashboard locally

```bash
make dashboard
```

Open:

```text
http://localhost:8501
```

### 8. Start with Docker Compose

```bash
docker compose up --build
```

Docker Compose reads safe local defaults from `.env.example`. To override values, copy it to `.env` and edit local-only values such as ports or demo database credentials.

### CI release gates

The GitHub Actions workflow in `.github/workflows/evaluation.yml` runs tests, evaluates the Arabic golden dataset, generates a release report, uploads artifacts, and fails the workflow if the release decision is `BLOCK_RELEASE`.

---

## Portfolio proof

This project is designed to be demoed as a working release-governance loop, not only as an architecture diagram.

For the final presentation path, use `docs/final_demo_walkthrough.md`.

### Local proof commands

```bash
make install
make demo
make human-review-demo
make failure-demo
make lint
make api
make dashboard
```

Open:

```text
API docs:  http://localhost:8080/docs
Dashboard: http://localhost:8501
```

### Verified sample run

Latest sample evaluation over `data/golden/arabic_hr_golden_set.jsonl`:

| Evidence | Result |
|---|---:|
| Release decision | `PROMOTE_TO_STAGING` |
| Passed | `True` |
| Cases evaluated | 6 |
| Pass rate | 100% |
| Unit tests | 17 passed |
| Lint | Passed |
| API health | `200 OK` |
| Dashboard entrypoint | Present |

Intentional human-review demo:

| Evidence | Result |
|---|---:|
| Degraded behavior | low generation quality |
| Expected decision | `HUMAN_REVIEW_REQUIRED` |
| Review report | `reports/human_review_release_report.md` |

Intentional block demo:

| Evidence | Result |
|---|---:|
| Broken behavior | citations removed |
| Expected decision | `BLOCK_RELEASE` |
| Failure report | `reports/failure_release_report.md` |

Generated artifacts:

- `reports/latest_evaluation_report.json`
- `reports/latest_release_report.md`
- `reports/human_review_evaluation_report.json`
- `reports/human_review_release_report.md`
- `reports/failure_evaluation_report.json`
- `reports/failure_release_report.md`
- `reports/api_evaluation_report.json`
- `reports/api_release_report.md`

### What the reviewer should notice

- The RAG system is adapter-based, so the harness can wrap an existing Arabic RAG backend.
- Citation validation, append-only run history, Arabic normalization, structured evaluation errors, and explicit release gates are first-class behavior.
- The same evaluation path runs locally, through the API, and in GitHub Actions.
- The dashboard summarizes decision status, pass rate, gates, metric averages, model version, and retriever version.
- The dashboard compares the three canonical release outcomes from the generated reports.
- The human-review demo proves non-critical quality degradation can be routed to manual review.
- The failure demo proves the gate can block an unsafe or ungrounded candidate release.

---

## Core architecture

The harness has five layers:

1. **Inputs & Test Assets**
   - Golden Arabic dataset
   - Production replay samples
   - Synthetic test cases
   - Ground truth answers
   - Policy and safety rules
   - Prompt/model/retriever versions
   - Document corpus and citation metadata
   - User feedback

2. **RAG System Under Test**
   - User query
   - Arabic preprocessing and normalization
   - Prompt builder
   - Embedding model
   - Hybrid retriever
   - Reranker
   - Vector DB
   - Document store
   - LLM inference
   - Answer with citations

3. **Evaluation Harness**
   - Retrieval evaluation
   - Generation evaluation
   - Citation validation
   - Arabic quality checks
   - Safety and security checks
   - Regression and comparison
   - Rule-based validators
   - Disabled LLM-as-judge placeholder that can be replaced with a provider-backed evaluator

4. **Observability & Registry**
   - Structured logs
   - Lightweight local trace spans
   - Query/session IDs
   - Latency breakdown
   - Token/cost usage
   - Retrieval diagnostics
   - Hallucination flags
   - Append-only run history and feedback audit events
   - Dataset/model/prompt/retriever versioning

5. **CI/CD Decision Gates**
   - Pull request or nightly run
   - Automated evaluation
   - Quality gates
   - Promote to staging, block, or require human review

---

## MVP output

A successful evaluation run produces:

- `reports/latest_evaluation_report.json`
- `reports/latest_release_report.md`
- per-case metric breakdowns
- failed gate explanations
- suggested remediation actions
- audit metadata for reproducibility

---

## Example CV bullet after implementation

> Built an Arabic RAG evaluation and observability harness with golden-set regression tests, retrieval metrics, citation validation, Arabic quality scoring, safety checks, lightweight structured traces, append-only run history, and CI/CD release gates for source-grounded Arabic enterprise AI systems.

---

This package is designed as a strong MVP and implementation starter. It includes working baseline code, sample data, tests, docs, Docker/CI scaffolding, and a complete `agent.md` for coding-agent implementation.

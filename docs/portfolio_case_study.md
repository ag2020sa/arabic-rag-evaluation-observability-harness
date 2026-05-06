# Portfolio Case Study

## Project title

Arabic RAG Evaluation & Observability Harness

## One-line summary

Built a production-minded portfolio evaluation, lightweight observability, and release-gating harness for Arabic RAG systems, with retrieval metrics, proxy groundedness checks, citation validation, Arabic quality scoring, safety tests, traceability, and CI/CD gates.

## Problem

RAG systems can produce fluent answers while still failing in retrieval quality, citation accuracy, source grounding, or safety. In regulated Arabic enterprise domains such as HR, labor-law, and cybersecurity governance, these failures create trust, compliance, and operational risk.

## Solution

A working MVP evaluation harness that tests a RAG system against Arabic golden datasets, replay samples, safety policies, and versioned model/prompt/retriever configurations.

## Technical scope

- Python package
- FastAPI API
- Typer CLI
- Pydantic schemas
- Rule-based evaluation metrics
- Adapter pattern for external RAG systems
- JSON/Markdown reports
- Append-only SQLite run history by run ID
- Docker and CI/CD workflow
- Observability instrumentation

## Outcome

The project demonstrates practical GenAI engineering skills beyond simple chatbot creation: quality measurement, release governance, demo audit history, and secure AI design patterns.

## Portfolio proof

The local demo path runs end to end:

```bash
make demo
make lint
make api
make dashboard
```

Verified sample output:

| Evidence | Result |
|---|---:|
| Release decision | `PROMOTE_TO_STAGING` |
| Cases evaluated | 6 |
| Pass rate | 100% |
| Unit tests | 17 passed |
| API docs | `http://localhost:8080/docs` |
| Dashboard | `http://localhost:8501` |

The demo proves that the project can evaluate an Arabic RAG candidate, produce release artifacts, expose the release workflow through FastAPI, and visualize quality gates in Streamlit.

The project also includes an intentional failure path:

```bash
make human-review-demo
make failure-demo
```

The human-review path keeps citations intact but lowers generation quality, producing `HUMAN_REVIEW_REQUIRED`. The failure path removes citations from the mock candidate output and should produce `BLOCK_RELEASE`, proving the release gates can route degraded releases to manual review or block ungrounded RAG behavior.

## CV bullet

Built an Arabic RAG evaluation and observability harness with golden-set regression tests, retrieval metrics, citation validation, Arabic quality scoring, safety checks, lightweight structured traces, append-only run history, and CI/CD release gates for source-grounded Arabic AI systems.

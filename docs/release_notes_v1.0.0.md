# v1.0.0 Portfolio Release

This release marks the Arabic RAG Evaluation & Observability Harness as portfolio-ready.

## Highlights

- Arabic-first RAG evaluation harness with adapter-based integration.
- Golden-set evaluation over realistic Saudi HR and labor-law samples.
- Retrieval metrics: precision, recall, hit rate, MRR, and nDCG.
- Generation metrics: answer relevance, groundedness, completeness, and must-not-include checks.
- Citation validation for source match, coverage, citation count, retrieved-source alignment, and span text.
- Arabic quality checks with normalization, Arabic ratio, readability, and terminology consistency.
- Safety checks for prompt injection, jailbreaks, PII leakage, and policy violations.
- Explicit release decisions:
  - `PROMOTE_TO_STAGING`
  - `HUMAN_REVIEW_REQUIRED`
  - `BLOCK_RELEASE`
- FastAPI evaluation endpoint.
- Streamlit dashboard with release decision proof across promote, human-review, and block reports.
- GitHub Actions CI/CD gate that runs tests, evaluation, report generation, and release enforcement.
- Audit-ready JSON and Markdown release reports.
- Canonical visual blueprint and final demo walkthrough.

## Demo Commands

```bash
make install
make demo
make human-review-demo
make failure-demo
make lint
make test
```

Expected outcomes:

| Command | Expected result |
|---|---|
| `make demo` | `PROMOTE_TO_STAGING` |
| `make human-review-demo` | `HUMAN_REVIEW_REQUIRED` |
| `make failure-demo` | `BLOCK_RELEASE` |
| `make lint` | All checks passed |
| `make test` | 11 tests passed |

## Live Demo

```bash
make api
make dashboard
```

Open:

```text
API docs:  http://localhost:8080/docs
Dashboard: http://localhost:8501
```

## Portfolio Positioning

This is not a generic chatbot demo. It is an Arabic RAG evaluation, observability, audit, and release-governance harness that can wrap an existing enterprise RAG backend and make release decisions explicit.

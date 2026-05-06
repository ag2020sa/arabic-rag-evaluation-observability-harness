# Arabic RAG Evaluation & Observability Harness

Production-minded portfolio MVP for Arabic RAG evaluation, lightweight observability, audit history, and release gates.

## Portfolio Links

- Repository: <https://github.com/ag2020sa/arabic-rag-evaluation-observability-harness>
- Release: <https://github.com/ag2020sa/arabic-rag-evaluation-observability-harness/releases/tag/v1.0.0>
- Canonical visual blueprint: [`visual_blueprint.md`](visual_blueprint.md)
- Final demo walkthrough: [`final_demo_walkthrough.md`](final_demo_walkthrough.md)
- Portfolio case study: [`portfolio_case_study.md`](portfolio_case_study.md)
- CV snippets: [`portfolio_snippets.md`](portfolio_snippets.md)

## What This Project Proves

This is not a generic chatbot demo. It is an Arabic RAG evaluation, lightweight observability, audit-history, and release-governance harness that can wrap an existing RAG backend and make release decisions explicit.

The harness evaluates:

- retrieval quality
- generation relevance and proxy groundedness
- citation accuracy, missing/unsupported citations, and span/page checks when metadata is available
- Arabic answer quality and normalization
- safety risks including prompt injection, jailbreaks, PII leakage, and policy violations
- regression and release readiness

## Release Decisions

The project demonstrates all three release outcomes:

| Demo command | Decision |
|---|---|
| `make demo` | `PROMOTE_TO_STAGING` |
| `make human-review-demo` | `HUMAN_REVIEW_REQUIRED` |
| `make failure-demo` | `BLOCK_RELEASE` |

## Run The Demo

```bash
make install
make demo
make human-review-demo
make failure-demo
make lint
make test
```

Start the local interfaces:

```bash
make api
make dashboard
```

Open:

```text
API docs:  http://localhost:8080/docs
Dashboard: http://localhost:8501
```

## Architecture

The canonical architecture is implemented through:

- Inputs & Test Assets
- RAG System Under Test
- Evaluation Harness
- Observability & Telemetry
- Storage, Registry & Audit
- CI/CD & Decision Gates
- Feedback Loop
- Governance Controls

See [`visual_blueprint.md`](visual_blueprint.md) for the full implementation mapping.

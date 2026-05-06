# Final Demo Walkthrough

Use this walkthrough to present the project as a finished portfolio demo.

## 1. Start With The Blueprint

Open the canonical visual:

`assets/visuals/arabic_rag_eval_observability_harness_portfolio_final_2x.png`

Explain that this is the implementation map for the repository:

- Inputs & Test Assets
- RAG System Under Test
- Evaluation Harness
- Observability & Telemetry
- Storage, Registry & Audit
- CI/CD & Decision Gates
- Feedback Loop
- Governance Controls

## 2. Install And Run The Demo

```bash
make install
make demo
make human-review-demo
make failure-demo
make lint
```

Expected outcomes:

| Command | Expected decision |
|---|---|
| `make demo` | `PROMOTE_TO_STAGING` |
| `make human-review-demo` | `HUMAN_REVIEW_REQUIRED` |
| `make failure-demo` | `BLOCK_RELEASE` |
| `make lint` | `All checks passed` |

## 3. Show Release Reports

Open:

- `reports/latest_release_report.md`
- `reports/human_review_release_report.md`
- `reports/failure_release_report.md`

Point out:

- per-case metrics
- failed gates
- warnings
- critical failures
- final release decision

## 4. Start The API

```bash
make api
```

Open:

`http://localhost:8080/docs`

Run `POST /evaluations/run` from the Swagger UI or with:

```bash
curl -s -X POST http://127.0.0.1:8080/evaluations/run \
  -H 'content-type: application/json' \
  -d '{}'
```

Expected response includes:

```json
{
  "passed": true,
  "decision": "PROMOTE_TO_STAGING"
}
```

## 5. Start The Dashboard

```bash
make dashboard
```

Open:

`http://localhost:8501`

Show:

- Release Decision Proof table
- promote, human review, and block counters
- selected report metrics
- quality gates
- metric averages
- case-level warnings and failures

## 6. Explain The Engineering Value

This project proves:

- Arabic RAG quality is measured, not assumed.
- citations are validated and source grounding is enforced.
- unsafe or ungrounded releases can be blocked.
- degraded but non-critical releases can be routed to human review.
- every run produces audit-ready JSON and Markdown artifacts.
- the adapter pattern can wrap an existing RAG backend.

## 7. Closing Line

This is not a chatbot demo. It is an Arabic RAG evaluation, observability, audit, and release-governance harness that can sit around a real enterprise RAG system.

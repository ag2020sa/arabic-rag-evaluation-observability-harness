# Final Delivery

This project is ready as a portfolio delivery for the Arabic RAG Evaluation & Observability Harness.

## Canonical Blueprint

The primary implementation reference is:

`assets/visuals/arabic_rag_eval_observability_harness_portfolio_final_2x.png`

All implementation work maps back to this visual through:

- `docs/visual_blueprint.md`
- `docs/final_demo_walkthrough.md`
- `README.md`

## Final Verification

Run:

```bash
make install
make demo
make human-review-demo
make failure-demo
make lint
make test
```

Expected decisions:

| Command | Decision |
|---|---|
| `make demo` | `PROMOTE_TO_STAGING` |
| `make human-review-demo` | `HUMAN_REVIEW_REQUIRED` |
| `make failure-demo` | `BLOCK_RELEASE` |

Expected quality checks:

| Check | Expected |
|---|---|
| `make test` | 11 passed |
| `make lint` | All checks passed |

## Live Demo URLs

Start:

```bash
make api
make dashboard
```

Open:

```text
API docs:  http://localhost:8080/docs
Dashboard: http://localhost:8501
```

## Generated Evidence

Portfolio evidence reports:

- `reports/latest_release_report.md`
- `reports/human_review_release_report.md`
- `reports/failure_release_report.md`
- `reports/latest_evaluation_report.json`
- `reports/human_review_evaluation_report.json`
- `reports/failure_evaluation_report.json`

## GitHub Repository

Public repository:

`https://github.com/ag2020sa/arabic-rag-evaluation-observability-harness`

Do not commit local runtime artifacts:

- `.venv/`
- `.pytest_cache/`
- `.ruff_cache/`
- `reports/evaluation_history.sqlite`
- `reports/feedback_events.jsonl`

These are covered by `.gitignore`.

## Final Positioning

This is not a generic chatbot demo. It is an Arabic RAG evaluation, observability, audit, and release-governance harness that can wrap an existing RAG backend and make release decisions explicit.

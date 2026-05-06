# Canonical Visual Blueprint

The project source-of-truth architecture is:

`assets/visuals/arabic_rag_eval_observability_harness_portfolio_final_2x.png`

Use this visual as the primary implementation map for the repository. The harness should stay focused on Arabic RAG evaluation and observability, not drift into a generic chatbot demo.

## Implementation Mapping

| Visual section | Repository implementation |
|---|---|
| Inputs & Test Assets | `data/golden/`, `data/replay/`, `data/corpus/`, `data/policies/`, `configs/` |
| RAG System Under Test | `src/rag_eval_harness/adapters/`, `LocalMockRAGAdapter`, `HTTPRAGAdapter` |
| Evaluation Harness | `src/rag_eval_harness/evaluators/`, `src/rag_eval_harness/metrics/` |
| Citation Validation | `src/rag_eval_harness/metrics/citations.py`, citation tests |
| Arabic Quality | `src/rag_eval_harness/arabic/`, `src/rag_eval_harness/metrics/arabic_quality.py` |
| Safety & Security | `src/rag_eval_harness/metrics/safety.py`, `data/policies/safety_rules.yaml` |
| Regression & Comparison | `src/rag_eval_harness/metrics/regression.py`, release reports |
| LLM-as-Judge + Rules | `src/rag_eval_harness/evaluators/llm_judge.py`, `src/rag_eval_harness/evaluators/rules.py` |
| Observability & Telemetry | `src/rag_eval_harness/observability/`, `monitoring/` |
| Storage, Registry & Audit | `src/rag_eval_harness/storage/`, `reports/evaluation_history.sqlite` |
| CI/CD & Decision Gates | `src/rag_eval_harness/gates/`, `.github/workflows/evaluation.yml` |
| Feedback Loop | `src/rag_eval_harness/api/routes/feedback.py`, `reports/feedback_events.jsonl` |
| Governance Controls | `docs/ci_cd_gates.md`, `docs/risk_register.md`, audit and safety rules |

## Decision Outcomes

The visual's release outcomes are non-negotiable:

- `PROMOTE_TO_STAGING`
- `HUMAN_REVIEW_REQUIRED`
- `BLOCK_RELEASE`

The project must include both success and failure demonstrations so reviewers can see that gates are active.

## Current Demo Paths

Success path:

```bash
make demo
```

Human-review path:

```bash
make human-review-demo
```

Failure path:

```bash
make failure-demo
```

The success path should produce `PROMOTE_TO_STAGING`. The human-review path keeps safety and citations intact but lowers generation quality, producing `HUMAN_REVIEW_REQUIRED`. The failure path intentionally breaks citation grounding and should produce `BLOCK_RELEASE`.

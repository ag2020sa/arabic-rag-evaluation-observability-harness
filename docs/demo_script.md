# Demo Script

For the complete final portfolio path, see `docs/final_demo_walkthrough.md`.

## 3-minute portfolio demo

### 0:00 — Problem

"Arabic enterprise RAG systems need more than a chatbot. They need quality evaluation, citations, safety checks, tracing, and release gates."

### 0:30 — Architecture

Show `assets/visuals/arabic_rag_eval_observability_harness_portfolio_final_2x.png`.

Explain:

- Inputs and golden dataset
- RAG system under test
- Evaluation harness
- Observability and registry
- CI/CD decision gates

### 1:15 — Run evaluation

```bash
make demo
```

Open `reports/latest_release_report.md`.

The demo command runs the complete local release path:

- evaluation over the Arabic golden dataset
- Markdown release report generation
- unit test suite

Then run the intentional failure path:

```bash
make human-review-demo
make failure-demo
```

Explain that low generation quality requires human review, while removed citations block the release.

### 1:45 — Show failed/successful gates

Explain how the harness can block unsafe releases or require human review.

Open the local dashboard:

```bash
make dashboard
```

Show the release decision, pass rate, gates, metric averages, and case-level warnings.

### 2:15 — Connect to real RAG backend

Show `HTTPRAGAdapter` and explain how it wraps an existing FastAPI RAG endpoint.

### 2:30 — Show CI release gate

Open `.github/workflows/evaluation.yml`.

Explain that pull requests, pushes to `main`, nightly runs, and manual runs execute the same release path and fail the workflow when the decision is `BLOCK_RELEASE`.

### 2:45 — Business value

- Higher answer quality
- Lower hallucination risk
- Faster debugging
- Safer Arabic responses
- Release confidence

# CI/CD Quality Gates

## Trigger points

The harness should run on:

- Pull requests
- Nightly scheduled jobs
- Release candidates
- Prompt/model/retriever changes
- Dataset updates
- Production incident replays

This repository includes `.github/workflows/evaluation.yml`, which runs on pull requests, pushes to `main`, nightly schedule, and manual dispatch.

## Gate categories

| Gate | Example threshold |
|---|---:|
| Retrieval Precision@k | >= 0.50 |
| Retrieval Recall@k | >= 0.60 |
| Citation Coverage | >= 0.70 |
| Arabic Ratio | >= 0.60 |
| PII Leakage | 0 incidents |
| Policy Violation | 0 incidents |
| Overall Pass Rate | >= 75% |

## Release outcomes

### Promote to staging
All major gates pass for the candidate demo/release path.

### Human review required
Non-critical gates fail or quality degradation is small but explainable.

### Block release
Critical safety, citation, PII, or policy gates fail.

## Recommended branch policy

- PR cannot merge if `BLOCK_RELEASE`.
- PR can merge with explicit approval if `HUMAN_REVIEW_REQUIRED`.
- PR can merge automatically if `PROMOTE_TO_STAGING` and tests pass.

## Local parity

Use the same release path locally before opening a PR:

```bash
make demo
```

The command evaluates the Arabic golden dataset, generates `reports/latest_release_report.md`, and runs the test suite.

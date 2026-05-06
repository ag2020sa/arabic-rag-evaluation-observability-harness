# Dashboard Specification

## Executive view

- Current release decision
- Release decision proof across promote, human review, and block demo reports
- Pass rate
- Failed gates
- Average latency
- Safety incidents
- Citation pass rate
- Overview tab with selected evaluation summary and metric averages

## Engineering view

- Per-case metrics
- Retrieval diagnostics
- Chunk score distributions
- Prompt/model/retriever version comparison
- Latency breakdown by component
- Token usage and cost
- Case Results tab with case-level answers, warnings, citations, chunks, and audit IDs

## Security/compliance view

- PII leakage incidents
- Prompt injection attempts
- Jailbreak attempts
- Policy violations
- Human-review queue
- Audit event IDs
- Decision Gates tab with severity and failed gate details
- Audit tab with SQLite evaluation history and per-case audit event IDs

## Product view

- Common failure categories
- User feedback ratings
- Production replay regressions
- Arabic quality trends
- Coverage gaps in golden dataset
- Reports tab with release report previews for promote, human-review, and block demos

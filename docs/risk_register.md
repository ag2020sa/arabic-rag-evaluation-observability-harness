# Risk Register

| Risk | Severity | Mitigation |
|---|---|---|
| Hallucinated legal answer | High | Groundedness, citation validation, disclaimer, human review |
| Wrong citation | High | Source match and citation coverage gates |
| PII leakage | Critical | PII detection, redaction, block release gate |
| Prompt injection | Critical | Attack dataset, prompt-injection checks, safety policy |
| Low Arabic quality | Medium | Arabic ratio, terminology consistency, readability checks |
| Regression after prompt change | High | Golden set regression and baseline comparison |
| Missing source coverage | Medium | Dataset expansion and retrieval diagnostics |
| Unclear ownership of release decision | Medium | Explicit CI/CD gate outcomes and manual review path |

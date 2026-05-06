# Observability

## Signals

The harness currently provides lightweight local observability suitable for a portfolio MVP and CI demo. It captures:

- Structured logs
- Local trace span start/end events
- Query/session IDs
- Per-case latency
- Token usage
- Cost estimate
- Retrieval diagnostics
- Error categories
- Hallucination/groundedness flags
- User feedback events

It does not currently provide full production distributed tracing by itself. The repository includes OpenTelemetry collector configuration and Prometheus-compatible metric helpers, but exporting complete end-to-end traces requires wiring the running service to an OpenTelemetry backend and instrumenting the real RAG system under test.

## Key trace attributes

- `run_id`
- `case_id`
- `query_hash`
- `prompt_version`
- `model_name`
- `retriever_version`
- `latency_ms`
- `retrieved_chunk_count`
- `citation_count`

## Example structured log

```json
{
  "event": "span.end",
  "span": "evaluate_case",
  "duration_ms": 128.4,
  "attributes": {
    "case_id": "hr_leave_001",
    "category": "labor_law"
  }
}
```

## Production extension

- Export application spans to the included OpenTelemetry collector.
- Add a Prometheus metrics endpoint for the FastAPI service.
- Build Grafana dashboard for latency, pass rate, failed gates, and safety incidents.
- Store evaluation reports in SQLite/PostgreSQL and immutable object storage if certified auditability is required.

# Observability

## Signals

The harness captures:

- Structured logs
- Trace spans
- Query/session IDs
- Latency breakdown
- Token usage
- Cost estimate
- Retrieval diagnostics
- Error categories
- Hallucination/groundedness flags
- User feedback events

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

- Export traces to OpenTelemetry collector.
- Add Prometheus metrics endpoint.
- Build Grafana dashboard for latency, pass rate, failed gates, and safety incidents.
- Store evaluation reports in SQLite/PostgreSQL and immutable object storage.

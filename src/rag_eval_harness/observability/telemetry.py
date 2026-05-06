from __future__ import annotations

from prometheus_client import Counter, Histogram

EVALUATION_CASES = Counter("rag_eval_cases_total", "Total evaluated RAG cases", ["category", "passed"])
EVALUATION_LATENCY = Histogram("rag_eval_case_latency_ms", "RAG evaluation case latency in milliseconds")
QUALITY_GATE_FAILURES = Counter("rag_eval_quality_gate_failures_total", "Quality gate failures", ["gate", "severity"])


def record_case(category: str, passed: bool, latency_ms: float) -> None:
    EVALUATION_CASES.labels(category=category, passed=str(passed).lower()).inc()
    EVALUATION_LATENCY.observe(latency_ms)


def record_gate_failure(gate: str, severity: str) -> None:
    QUALITY_GATE_FAILURES.labels(gate=gate, severity=severity).inc()

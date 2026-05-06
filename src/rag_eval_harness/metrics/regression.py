from __future__ import annotations

from rag_eval_harness.schemas import EvaluationRunReport


def compare_reports(baseline: EvaluationRunReport, candidate: EvaluationRunReport) -> dict:
    """Compare two evaluation reports at a summary level."""
    base = baseline.summary.get("metric_averages", {})
    cand = candidate.summary.get("metric_averages", {})
    deltas = {}
    for key in sorted(set(base) | set(cand)):
        deltas[key] = cand.get(key, 0.0) - base.get(key, 0.0)
    return {
        "baseline_run_id": baseline.run_id,
        "candidate_run_id": candidate.run_id,
        "baseline_passed": baseline.passed,
        "candidate_passed": candidate.passed,
        "metric_deltas": deltas,
    }

from rag_eval_harness.gates.quality_gates import apply_case_thresholds, case_passed, release_decision
from rag_eval_harness.schemas import GateResult, MetricResult


def test_quality_gate_thresholds():
    thresholds = {"retrieval": {"precision_at_k_min": 0.5}, "safety": {"pii_leakage_detected_max": 0}}
    metrics = {
        "retrieval.precision_at_k": MetricResult(name="retrieval.precision_at_k", value=0.7),
        "safety.pii_leakage_detected": MetricResult(name="safety.pii_leakage_detected", value=0.0),
    }
    metrics = apply_case_thresholds(metrics, thresholds)
    passed, critical, warnings = case_passed(metrics)
    assert passed
    assert not critical
    assert not warnings


def test_release_decision_human_review_for_medium_gate_failure():
    gates = [
        GateResult(name="minimum_cases", passed=True, reason="ok", severity="high"),
        GateResult(name="overall_pass_rate", passed=True, reason="ok", severity="high"),
        GateResult(name="avg_generation.groundedness", passed=False, reason="low", severity="medium"),
    ]

    assert release_decision(gates) == "HUMAN_REVIEW_REQUIRED"

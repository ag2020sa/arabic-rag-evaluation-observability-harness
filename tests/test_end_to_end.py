from rag_eval_harness.adapters.local_mock_adapter import LocalMockRAGAdapter
from rag_eval_harness.evaluators.harness import evaluate_dataset


def test_end_to_end_evaluation_runs():
    report = evaluate_dataset(
        LocalMockRAGAdapter(),
        "data/golden/arabic_hr_golden_set.jsonl",
        "configs/thresholds.yaml",
    )
    assert report.case_results
    assert report.summary["case_count"] >= 3
    assert report.adapter_name == "local_mock"
    assert report.decision in {"PROMOTE_TO_STAGING", "HUMAN_REVIEW_REQUIRED", "BLOCK_RELEASE"}

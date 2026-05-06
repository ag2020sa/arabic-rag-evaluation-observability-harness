from rag_eval_harness.adapters.local_mock_adapter import LocalMockRAGAdapter
from rag_eval_harness.evaluators.harness import evaluate_dataset
from rag_eval_harness.schemas import RagRequest


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


class FailingAdapter(LocalMockRAGAdapter):
    name = "failing_adapter"

    async def ask(self, request: RagRequest):
        if request.metadata.get("case_id") == "hr_leave_001":
            raise RuntimeError("backend unavailable")
        return await super().ask(request)


def test_evaluation_records_case_error_without_aborting_run():
    report = evaluate_dataset(
        FailingAdapter(),
        "data/golden/arabic_hr_golden_set.jsonl",
        "configs/thresholds.yaml",
    )
    failed = next(case for case in report.case_results if case.case_id == "hr_leave_001")
    assert failed.passed is False
    assert "evaluation.runtime_error" in failed.metrics
    assert failed.metrics["evaluation.runtime_error"].details["error_type"] == "RuntimeError"
    assert failed.response.raw["error"]["message"] == "backend unavailable"
    assert report.summary["case_count"] == 6
    assert report.decision == "BLOCK_RELEASE"

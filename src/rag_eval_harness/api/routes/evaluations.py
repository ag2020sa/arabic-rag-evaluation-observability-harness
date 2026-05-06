from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from rag_eval_harness.adapters.local_mock_adapter import LocalMockRAGAdapter
from rag_eval_harness.evaluators.harness import evaluate_dataset_async
from rag_eval_harness.gates.report import render_markdown_report, save_json_report

router = APIRouter()


class EvaluationRequest(BaseModel):
    dataset_path: str = "data/golden/arabic_hr_golden_set.jsonl"
    thresholds_path: str = "configs/thresholds.yaml"
    out_json_path: str = "reports/api_evaluation_report.json"
    out_markdown_path: str = "reports/api_release_report.md"


@router.post("/run")
async def run_evaluation(request: EvaluationRequest) -> dict:
    adapter = LocalMockRAGAdapter()
    report = await evaluate_dataset_async(adapter, request.dataset_path, request.thresholds_path)
    save_json_report(report, request.out_json_path)
    Path(request.out_markdown_path).parent.mkdir(parents=True, exist_ok=True)
    Path(request.out_markdown_path).write_text(render_markdown_report(report), encoding="utf-8")
    return {
        "run_id": report.run_id,
        "passed": report.passed,
        "decision": report.decision,
        "summary": report.summary,
        "json_report": request.out_json_path,
        "markdown_report": request.out_markdown_path,
    }

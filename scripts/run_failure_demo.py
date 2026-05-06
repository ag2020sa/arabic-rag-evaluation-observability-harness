from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rag_eval_harness.adapters.local_mock_adapter import LocalMockRAGAdapter
from rag_eval_harness.evaluators.harness import evaluate_dataset
from rag_eval_harness.gates.report import render_markdown_report, save_json_report
from rag_eval_harness.schemas import RagRequest, RagResponse
from rag_eval_harness.storage.sqlite import save_run


class MissingCitationAdapter(LocalMockRAGAdapter):
    """Demo adapter that intentionally violates citation grounding."""

    name = "failure_demo_missing_citations"

    async def ask(self, request: RagRequest) -> RagResponse:
        response = await super().ask(request)
        response.citations = []
        response.raw["failure_demo"] = "citations_removed"
        return response


def main() -> None:
    parser = argparse.ArgumentParser(description="Run an intentional BLOCK_RELEASE demo.")
    parser.add_argument("--dataset", default="data/golden/arabic_hr_golden_set.jsonl")
    parser.add_argument("--thresholds", default="configs/thresholds.yaml")
    parser.add_argument("--out", default="reports/failure_evaluation_report.json")
    parser.add_argument("--markdown-out", default="reports/failure_release_report.md")
    parser.add_argument("--sqlite-db", default="reports/evaluation_history.sqlite")
    args = parser.parse_args()

    report = evaluate_dataset(MissingCitationAdapter(), args.dataset, args.thresholds)
    save_json_report(report, args.out)
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(render_markdown_report(report), encoding="utf-8")
    save_run(args.sqlite_db, report)

    print(f"Run ID: {report.run_id}")
    print(f"Passed: {report.passed}")
    print(f"Decision: {report.decision}")
    print(f"Report saved to: {Path(args.out).resolve()}")
    print(f"Markdown report saved to: {Path(args.markdown_out).resolve()}")

    if report.decision != "BLOCK_RELEASE":
        raise SystemExit(f"Expected BLOCK_RELEASE, got {report.decision}")


if __name__ == "__main__":
    main()

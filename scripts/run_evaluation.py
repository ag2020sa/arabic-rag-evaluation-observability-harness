from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import argparse

from rag_eval_harness.adapters.local_mock_adapter import LocalMockRAGAdapter
from rag_eval_harness.evaluators.harness import evaluate_dataset
from rag_eval_harness.gates.quality_gates import release_decision
from rag_eval_harness.gates.report import save_json_report
from rag_eval_harness.storage.sqlite import save_run


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Arabic RAG evaluation harness.")
    parser.add_argument("--dataset", default="data/golden/arabic_hr_golden_set.jsonl")
    parser.add_argument("--thresholds", default="configs/thresholds.yaml")
    parser.add_argument("--out", default="reports/latest_evaluation_report.json")
    parser.add_argument("--sqlite-db", default="reports/evaluation_history.sqlite")
    args = parser.parse_args()

    adapter = LocalMockRAGAdapter()
    report = evaluate_dataset(adapter, args.dataset, args.thresholds)
    save_json_report(report, args.out)
    save_run(args.sqlite_db, report)

    print(f"Run ID: {report.run_id}")
    print(f"Passed: {report.passed}")
    print(f"Decision: {release_decision(report.gates)}")
    print(f"Report saved to: {Path(args.out).resolve()}")


if __name__ == "__main__":
    main()

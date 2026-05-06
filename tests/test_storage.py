import sqlite3

import pytest

from rag_eval_harness.schemas import EvaluationRunReport
from rag_eval_harness.storage.sqlite import save_run


def test_evaluation_history_is_append_only_for_run_ids(tmp_path):
    report = EvaluationRunReport(
        run_id="fixed-run-id",
        dataset_path="data/golden/arabic_hr_golden_set.jsonl",
        adapter_name="local_mock",
        case_results=[],
        gates=[],
        passed=True,
        decision="PROMOTE_TO_STAGING",
    )
    db_path = tmp_path / "history.sqlite"
    save_run(db_path, report)
    with pytest.raises(sqlite3.IntegrityError):
        save_run(db_path, report)

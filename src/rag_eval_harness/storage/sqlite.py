from __future__ import annotations

import sqlite3
from pathlib import Path

from rag_eval_harness.schemas import EvaluationRunReport


DDL = """
CREATE TABLE IF NOT EXISTS evaluation_runs (
    run_id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    adapter_name TEXT NOT NULL,
    model_name TEXT NOT NULL,
    prompt_version TEXT NOT NULL,
    retriever_version TEXT NOT NULL,
    passed INTEGER NOT NULL,
    report_json TEXT NOT NULL
);
"""


def init_db(path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.executescript(DDL)


def save_run(path: str | Path, report: EvaluationRunReport) -> None:
    init_db(path)
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            INSERT INTO evaluation_runs
            (run_id, created_at, adapter_name, model_name, prompt_version, retriever_version, passed, report_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                report.run_id,
                report.created_at.isoformat(),
                report.adapter_name,
                report.model_name,
                report.prompt_version,
                report.retriever_version,
                1 if report.passed else 0,
                report.model_dump_json(),
            ),
        )

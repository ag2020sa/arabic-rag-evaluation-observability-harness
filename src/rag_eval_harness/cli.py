from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from rag_eval_harness.adapters.http_rag_adapter import HTTPRAGAdapter
from rag_eval_harness.adapters.local_mock_adapter import LocalMockRAGAdapter
from rag_eval_harness.config import settings
from rag_eval_harness.datasets.loader import load_golden_examples
from rag_eval_harness.evaluators.harness import evaluate_dataset
from rag_eval_harness.gates.quality_gates import release_decision
from rag_eval_harness.gates.report import load_json_report, render_markdown_report, save_json_report
from rag_eval_harness.metrics.regression import compare_reports

app = typer.Typer(help="Arabic RAG Evaluation & Observability Harness CLI")
console = Console()


def _adapter(adapter_name: str):
    if adapter_name == "http":
        if not settings.rag_system_url:
            raise typer.BadParameter("RAG_SYSTEM_URL must be set for http adapter.")
        return HTTPRAGAdapter(settings.rag_system_url, settings.rag_system_timeout_seconds)
    return LocalMockRAGAdapter()


@app.command()
def validate_dataset(dataset: str = "data/golden/arabic_hr_golden_set.jsonl") -> None:
    examples = load_golden_examples(dataset)
    table = Table(title="Golden Dataset")
    table.add_column("ID")
    table.add_column("Category")
    table.add_column("Tags")
    table.add_column("Expected Sources")
    for ex in examples:
        table.add_row(ex.id, ex.category, ",".join(ex.tags), ",".join(ex.expected_sources))
    console.print(table)
    console.print(f"Loaded [bold green]{len(examples)}[/] examples.")


@app.command()
def evaluate(
    dataset: str = "data/golden/arabic_hr_golden_set.jsonl",
    thresholds: str = "configs/thresholds.yaml",
    out: str = "reports/latest_evaluation_report.json",
    adapter_name: str = typer.Option("local", "--adapter", help="local or http"),
) -> None:
    report = evaluate_dataset(_adapter(adapter_name), dataset, thresholds)
    save_json_report(report, out)
    decision = release_decision(report.gates)
    console.print(f"Run ID: [bold]{report.run_id}[/]")
    console.print(f"Passed: [bold]{report.passed}[/]")
    console.print(f"Decision: [bold]{decision}[/]")
    console.print(f"Saved: [green]{out}[/]")


@app.command()
def report(
    source: str = "reports/latest_evaluation_report.json",
    out: str = "reports/latest_release_report.md",
) -> None:
    evaluation = load_json_report(source)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(render_markdown_report(evaluation), encoding="utf-8")
    console.print(f"Saved Markdown report: [green]{out}[/]")


@app.command()
def compare(
    baseline: str,
    candidate: str,
    out: Optional[str] = None,
) -> None:
    result = compare_reports(load_json_report(baseline), load_json_report(candidate))
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if out:
        Path(out).write_text(text, encoding="utf-8")
        console.print(f"Saved comparison: [green]{out}[/]")
    else:
        console.print(text)


if __name__ == "__main__":
    app()

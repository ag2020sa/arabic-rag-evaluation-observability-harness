from __future__ import annotations

import json
from pathlib import Path

from rag_eval_harness.gates.quality_gates import release_decision
from rag_eval_harness.schemas import EvaluationRunReport


def save_json_report(report: EvaluationRunReport, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report.model_dump_json(indent=2), encoding="utf-8")


def load_json_report(path: str | Path) -> EvaluationRunReport:
    return EvaluationRunReport.model_validate(json.loads(Path(path).read_text(encoding="utf-8")))


def render_markdown_report(report: EvaluationRunReport) -> str:
    decision = report.decision if report.decision != "UNKNOWN" else release_decision(report.gates)
    failed_gates = [g for g in report.gates if not g.passed]
    lines = [
        "# Arabic RAG Evaluation Release Report",
        "",
        f"**Run ID:** `{report.run_id}`",
        f"**Created at:** {report.created_at.isoformat()}",
        f"**Dataset:** `{report.dataset_path}`",
        f"**Adapter:** `{report.adapter_name}`",
        f"**Model:** `{report.model_name}`",
        f"**Prompt:** `{report.prompt_version}`",
        f"**Retriever:** `{report.retriever_version}`",
        f"**Decision:** `{decision}`",
        f"**Passed:** `{report.passed}`",
        "",
        "## Summary",
        "",
        "```json",
        json.dumps(report.summary, ensure_ascii=False, indent=2),
        "```",
        "",
        "## Failed Gates",
        "",
    ]
    if failed_gates:
        for gate in failed_gates:
            lines.append(f"- **{gate.name}** ({gate.severity}): {gate.reason}")
    else:
        lines.append("No failed gates.")
    lines.extend(["", "## Case Results", ""])
    for case in report.case_results:
        lines.append(f"### {case.case_id} — {'PASS' if case.passed else 'REVIEW'}")
        lines.append(f"- Query: {case.query}")
        lines.append(f"- Critical failures: {', '.join(case.critical_failures) if case.critical_failures else 'None'}")
        lines.append(f"- Warnings: {', '.join(case.warnings) if case.warnings else 'None'}")
        lines.append("- Key metrics:")
        for name, metric in sorted(case.metrics.items()):
            if metric.threshold is not None:
                lines.append(f"  - `{name}` = {metric.value:.3f} / threshold {metric.threshold:.3f} / passed={metric.passed}")
        lines.append("")
    return "\n".join(lines)

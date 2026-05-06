from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

DEFAULT_REPORTS = {
    "Promote demo": "reports/latest_evaluation_report.json",
    "Human review demo": "reports/human_review_evaluation_report.json",
    "Block demo": "reports/failure_evaluation_report.json",
}

REPORT_LINKS = {
    "Promote demo": "reports/latest_release_report.md",
    "Human review demo": "reports/human_review_release_report.md",
    "Block demo": "reports/failure_release_report.md",
}


def load_report(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def release_overview_rows(report_paths: dict[str, str]) -> list[dict[str, Any]]:
    rows = []
    for label, report_path in report_paths.items():
        path = Path(report_path)
        if not path.exists():
            rows.append(
                {
                    "demo": label,
                    "decision": "MISSING",
                    "passed": None,
                    "case_count": 0,
                    "pass_rate_pct": 0.0,
                    "failed_gates": 0,
                    "warnings": 0,
                    "json_report": report_path,
                    "markdown_report": REPORT_LINKS.get(label, ""),
                }
            )
            continue

        report = load_report(path)
        summary = report.get("summary", {})
        rows.append(
            {
                "demo": label,
                "decision": report.get("decision", "UNKNOWN"),
                "passed": report.get("passed"),
                "case_count": summary.get("case_count", 0),
                "pass_rate_pct": summary.get("pass_rate", 0.0) * 100,
                "failed_gates": len(summary.get("failed_gates", [])),
                "warnings": len(summary.get("warnings", [])),
                "json_report": report_path,
                "markdown_report": REPORT_LINKS.get(label, ""),
            }
        )
    return rows


def metric_average_rows(report: dict[str, Any]) -> list[dict[str, Any]]:
    averages = report.get("summary", {}).get("metric_averages", {})
    rows = []
    for metric, value in sorted(averages.items()):
        group = metric.split(".", maxsplit=1)[0]
        rows.append({"group": group, "metric": metric, "value": value})
    return rows


def case_rows(report: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for case in report.get("case_results", []):
        response = case.get("response", {})
        rows.append(
            {
                "case_id": case.get("case_id"),
                "category": case.get("category"),
                "passed": case.get("passed"),
                "critical_failures": ", ".join(case.get("critical_failures", [])),
                "warnings": ", ".join(case.get("warnings", [])),
                "latency_ms": response.get("latency_ms", 0.0),
                "citations": len(response.get("citations", [])),
                "retrieved_chunks": len(response.get("retrieved_chunks", [])),
                "audit_event_id": response.get("audit_event_id", ""),
                "answer": response.get("answer", ""),
            }
        )
    return rows


def gate_rows(report: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "name": gate.get("name"),
            "passed": gate.get("passed"),
            "severity": gate.get("severity"),
            "reason": gate.get("reason"),
        }
        for gate in report.get("gates", [])
    ]


def observability_rows(report: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for case in report.get("case_results", []):
        response = case.get("response", {})
        token_usage = response.get("token_usage", {})
        rows.append(
            {
                "case_id": case.get("case_id"),
                "latency_ms": response.get("latency_ms", 0.0),
                "prompt_tokens": token_usage.get("prompt_tokens", 0),
                "completion_tokens": token_usage.get("completion_tokens", 0),
                "cost_usd": response.get("cost_usd", 0.0),
                "model": response.get("model_name", "unknown"),
                "prompt": response.get("prompt_version", "unknown"),
                "retriever": response.get("retriever_version", "unknown"),
            }
        )
    return rows


def audit_history_rows(sqlite_path: Path, limit: int = 20) -> list[dict[str, Any]]:
    if not sqlite_path.exists():
        return []
    with sqlite3.connect(sqlite_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT run_id, created_at, adapter_name, model_name, prompt_version,
                   retriever_version, passed
            FROM evaluation_runs
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def render_metric_cards(report: dict[str, Any]) -> None:
    summary = report.get("summary", {})
    cols = st.columns(4)
    cols[0].metric("Decision", report.get("decision", "UNKNOWN"))
    cols[1].metric("Passed", str(report.get("passed")))
    cols[2].metric("Pass Rate", f"{summary.get('pass_rate', 0):.1%}")
    cols[3].metric("Avg Latency ms", f"{summary.get('latency_ms_avg', 0):.0f}")

    meta_cols = st.columns(4)
    meta_cols[0].metric("Cases", summary.get("case_count", 0))
    meta_cols[1].metric("Adapter", report.get("adapter_name", "unknown"))
    meta_cols[2].metric("Model", report.get("model_name", "unknown"))
    meta_cols[3].metric("Retriever", report.get("retriever_version", "unknown"))


st.set_page_config(page_title="Arabic RAG Evaluation Harness", layout="wide")
st.title("Arabic RAG Evaluation & Observability Harness")
st.caption("Quality evaluation, tracing, auditability, and release gates for Arabic RAG systems")

report_path = st.sidebar.text_input("Evaluation report path", "reports/latest_evaluation_report.json")
sqlite_path = Path(st.sidebar.text_input("Evaluation history DB", "reports/evaluation_history.sqlite"))
path = Path(report_path)

overview_rows = release_overview_rows(DEFAULT_REPORTS)
overview_df = pd.DataFrame(overview_rows)

if not path.exists():
    st.warning("Run `make demo` first or choose an existing report path.")
    st.stop()

report = load_report(path)

tabs = st.tabs(
    [
        "Overview",
        "Decision Gates",
        "Case Results",
        "Reports",
        "Audit",
        "Observability",
    ]
)

with tabs[0]:
    st.subheader("Release Decision Proof")
    decision_cols = st.columns(3)
    decision_cols[0].metric(
        "Promote",
        overview_df[overview_df["decision"] == "PROMOTE_TO_STAGING"].shape[0],
    )
    decision_cols[1].metric(
        "Human Review",
        overview_df[overview_df["decision"] == "HUMAN_REVIEW_REQUIRED"].shape[0],
    )
    decision_cols[2].metric(
        "Block",
        overview_df[overview_df["decision"] == "BLOCK_RELEASE"].shape[0],
    )

    st.dataframe(
        overview_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "pass_rate_pct": st.column_config.NumberColumn("pass_rate_pct", format="%.0f%%")
        },
    )

    st.subheader("Selected Evaluation")
    render_metric_cards(report)

    st.subheader("Metric Averages")
    metric_df = pd.DataFrame(metric_average_rows(report))
    st.dataframe(metric_df, use_container_width=True, hide_index=True)

with tabs[1]:
    st.subheader("Quality Gates")
    gates_df = pd.DataFrame(gate_rows(report))
    if gates_df.empty:
        st.info("No gate results found in the selected report.")
    else:
        failed_df = gates_df[gates_df["passed"] == False]  # noqa: E712
        gate_cols = st.columns(3)
        gate_cols[0].metric("Total Gates", len(gates_df))
        gate_cols[1].metric("Failed Gates", len(failed_df))
        gate_cols[2].metric("Critical/High Failures", failed_df["severity"].isin(["critical", "high"]).sum())
        st.dataframe(gates_df, use_container_width=True, hide_index=True)

with tabs[2]:
    st.subheader("Case Results")
    cases_df = pd.DataFrame(case_rows(report))
    if cases_df.empty:
        st.info("No case results found in the selected report.")
    else:
        case_cols = st.columns(4)
        case_cols[0].metric("Cases", len(cases_df))
        case_cols[1].metric("Passed Cases", int(cases_df["passed"].sum()))
        case_cols[2].metric("Warnings", int((cases_df["warnings"] != "").sum()))
        case_cols[3].metric("Critical Failures", int((cases_df["critical_failures"] != "").sum()))
        st.dataframe(cases_df, use_container_width=True, hide_index=True)

with tabs[3]:
    st.subheader("Reports")
    report_rows = []
    for label, json_path in DEFAULT_REPORTS.items():
        markdown_path = REPORT_LINKS.get(label, "")
        report_rows.append(
            {
                "demo": label,
                "json_report": json_path,
                "markdown_report": markdown_path,
                "json_exists": Path(json_path).exists(),
                "markdown_exists": Path(markdown_path).exists(),
            }
        )
    st.dataframe(pd.DataFrame(report_rows), use_container_width=True, hide_index=True)

    selected_markdown = st.selectbox("Preview release report", list(REPORT_LINKS.values()))
    markdown_path = Path(selected_markdown)
    if markdown_path.exists():
        st.markdown(markdown_path.read_text(encoding="utf-8"))
    else:
        st.warning(f"Report not found: {selected_markdown}")

with tabs[4]:
    st.subheader("Audit History")
    audit_df = pd.DataFrame(audit_history_rows(sqlite_path))
    if audit_df.empty:
        st.info("No SQLite audit history found. Run `make demo` to populate it.")
    else:
        st.dataframe(audit_df, use_container_width=True, hide_index=True)

    st.subheader("Audit Event IDs In Selected Report")
    audit_ids = [
        {
            "case_id": row["case_id"],
            "audit_event_id": row["audit_event_id"],
        }
        for row in case_rows(report)
    ]
    st.dataframe(pd.DataFrame(audit_ids), use_container_width=True, hide_index=True)

with tabs[5]:
    st.subheader("Observability")
    obs_df = pd.DataFrame(observability_rows(report))
    if obs_df.empty:
        st.info("No observability rows found in the selected report.")
    else:
        obs_cols = st.columns(4)
        obs_cols[0].metric("Avg Latency ms", f"{obs_df['latency_ms'].mean():.0f}")
        obs_cols[1].metric("Prompt Tokens", int(obs_df["prompt_tokens"].sum()))
        obs_cols[2].metric("Completion Tokens", int(obs_df["completion_tokens"].sum()))
        obs_cols[3].metric("Cost USD", f"{obs_df['cost_usd'].sum():.4f}")
        st.dataframe(obs_df, use_container_width=True, hide_index=True)
        st.bar_chart(obs_df.set_index("case_id")["latency_ms"])

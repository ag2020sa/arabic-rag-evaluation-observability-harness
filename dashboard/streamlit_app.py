from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

DEFAULT_REPORTS = {
    "Promote demo": "reports/latest_evaluation_report.json",
    "Human review demo": "reports/human_review_evaluation_report.json",
    "Block demo": "reports/failure_evaluation_report.json",
}


def load_report(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def release_overview_rows(report_paths: dict[str, str]) -> list[dict]:
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
                "report_path": report_path,
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
                "report_path": report_path,
            }
        )
    return rows


st.set_page_config(page_title="Arabic RAG Evaluation Harness", layout="wide")
st.title("Arabic RAG Evaluation & Observability Harness")
st.caption("Quality evaluation, tracing, and release gates for Arabic RAG systems")

report_path = st.sidebar.text_input("Evaluation report path", "reports/latest_evaluation_report.json")
path = Path(report_path)

st.subheader("Release Decision Proof")
overview_rows = release_overview_rows(DEFAULT_REPORTS)
overview_df = pd.DataFrame(overview_rows)

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
    column_config={
        "pass_rate_pct": st.column_config.NumberColumn("pass_rate_pct", format="%.0f%%")
    },
)

if not path.exists():
    st.warning("Run `make evaluate` first or choose an existing report path.")
    st.stop()

report = load_report(path)
summary = report.get("summary", {})

st.subheader("Selected Evaluation Report")
cols = st.columns(4)
cols[0].metric("Decision", report.get("decision", "UNKNOWN"))
cols[1].metric("Passed", str(report.get("passed")))
cols[2].metric("Pass Rate", f"{summary.get('pass_rate', 0):.1%}")
cols[3].metric("Avg Latency ms", f"{summary.get('latency_ms_avg', 0):.0f}")

meta_cols = st.columns(4)
meta_cols[0].metric("Case Count", summary.get("case_count", 0))
meta_cols[1].metric("Adapter", report.get("adapter_name", "unknown"))
meta_cols[2].metric("Model", report.get("model_name", "unknown"))
meta_cols[3].metric("Retriever", report.get("retriever_version", "unknown"))

st.subheader("Quality Gates")
gates_df = pd.DataFrame(report.get("gates", []))
st.dataframe(gates_df, use_container_width=True)

st.subheader("Metric Averages")
metric_avg = summary.get("metric_averages", {})
st.dataframe(pd.DataFrame([{"metric": k, "value": v} for k, v in metric_avg.items()]), use_container_width=True)

st.subheader("Case Results")
rows = []
for case in report.get("case_results", []):
    rows.append({
        "case_id": case.get("case_id"),
        "category": case.get("category"),
        "passed": case.get("passed"),
        "critical_failures": ", ".join(case.get("critical_failures", [])),
        "warnings": ", ".join(case.get("warnings", [])),
        "answer": case.get("response", {}).get("answer", ""),
    })
st.dataframe(pd.DataFrame(rows), use_container_width=True)

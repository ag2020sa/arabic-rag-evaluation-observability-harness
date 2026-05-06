from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import argparse

from rag_eval_harness.gates.report import load_json_report, render_markdown_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Markdown release report.")
    parser.add_argument("--report", default="reports/latest_evaluation_report.json")
    parser.add_argument("--out", default="reports/latest_release_report.md")
    args = parser.parse_args()

    report = load_json_report(args.report)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(render_markdown_report(report), encoding="utf-8")
    print(f"Markdown report saved to: {Path(args.out).resolve()}")


if __name__ == "__main__":
    main()

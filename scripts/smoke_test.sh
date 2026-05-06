#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON:-python3}"

"${PYTHON_BIN}" scripts/run_evaluation.py --dataset data/golden/arabic_hr_golden_set.jsonl --thresholds configs/thresholds.yaml --out reports/latest_evaluation_report.json
"${PYTHON_BIN}" scripts/generate_report.py --report reports/latest_evaluation_report.json --out reports/latest_release_report.md
"${PYTHON_BIN}" -m pytest -q

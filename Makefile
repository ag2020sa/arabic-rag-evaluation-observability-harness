VENV_PYTHON := .venv/bin/python
PYTHON ?= $(shell if [ -x $(VENV_PYTHON) ]; then printf '%s' '$(VENV_PYTHON)'; else printf '%s' 'python3'; fi)

.PHONY: install test evaluate report demo human-review-demo failure-demo api dashboard docker lint clean

install:
	python3 -m venv .venv
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -e '.[dev,dashboard]'

test:
	$(PYTHON) -m pytest -q

evaluate:
	$(PYTHON) scripts/run_evaluation.py --dataset data/golden/arabic_hr_golden_set.jsonl --thresholds configs/thresholds.yaml --out reports/latest_evaluation_report.json

report:
	$(PYTHON) scripts/generate_report.py --report reports/latest_evaluation_report.json --out reports/latest_release_report.md

demo:
	PYTHON=$(PYTHON) bash scripts/smoke_test.sh

human-review-demo:
	$(PYTHON) scripts/run_human_review_demo.py

failure-demo:
	$(PYTHON) scripts/run_failure_demo.py

api:
	$(PYTHON) -m uvicorn rag_eval_harness.api.main:app --reload --host 0.0.0.0 --port 8080

dashboard:
	$(PYTHON) -m streamlit run dashboard/streamlit_app.py --server.port 8501

docker:
	docker compose up --build

lint:
	$(PYTHON) -m ruff check src tests scripts dashboard

clean:
	rm -rf .pytest_cache .ruff_cache __pycache__ dist build *.egg-info reports/latest_*.json reports/latest_*.md

from fastapi.testclient import TestClient

from rag_eval_harness.api.main import app


def test_health_endpoint():
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_evaluation_route_returns_structured_file_error():
    response = TestClient(app).post(
        "/evaluations/run",
        json={
            "dataset_path": "data/golden/does_not_exist.jsonl",
            "thresholds_path": "configs/thresholds.yaml",
            "out_json_path": "reports/api_evaluation_report.json",
            "out_markdown_path": "reports/api_release_report.md",
        },
    )
    assert response.status_code == 400
    detail = response.json()["detail"]
    assert detail["error_type"] == "FileNotFoundError"
    assert "request_id" in detail
    assert "does_not_exist" in detail["message"]

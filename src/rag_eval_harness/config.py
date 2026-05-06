from __future__ import annotations

from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    app_env: str = "local"
    app_name: str = "arabic-rag-evaluation-harness"
    log_level: str = "INFO"

    rag_system_url: Optional[str] = None
    rag_system_timeout_seconds: int = 30

    llm_judge_provider: str = "disabled"
    llm_judge_model: str = "arabic-aware-judge"
    llm_judge_api_key: Optional[str] = None

    sqlite_db_path: Path = Path("reports/evaluation_history.sqlite")

    otel_service_name: str = "arabic-rag-eval-harness"
    otel_exporter_otlp_endpoint: str = "http://otel-collector:4317"
    prometheus_port: int = 9100

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()

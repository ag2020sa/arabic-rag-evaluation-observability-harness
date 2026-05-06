from __future__ import annotations

import json
import logging
from typing import Any

try:
    import structlog  # type: ignore
except Exception:  # pragma: no cover - fallback for minimal environments
    structlog = None


class _FallbackLogger:
    def __init__(self, name: str) -> None:
        self.logger = logging.getLogger(name)

    def info(self, event: str, **kwargs: Any) -> None:
        self.logger.info(json.dumps({"event": event, **kwargs}, ensure_ascii=False, default=str))

    def warning(self, event: str, **kwargs: Any) -> None:
        self.logger.warning(json.dumps({"event": event, **kwargs}, ensure_ascii=False, default=str))

    def error(self, event: str, **kwargs: Any) -> None:
        self.logger.error(json.dumps({"event": event, **kwargs}, ensure_ascii=False, default=str))


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO), format="%(message)s")
    if structlog is not None:
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.add_log_level,
                structlog.processors.JSONRenderer(ensure_ascii=False),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, level.upper(), logging.INFO)),
        )


def get_logger(name: str = "rag_eval_harness"):
    if structlog is not None:
        return structlog.get_logger(name)
    return _FallbackLogger(name)

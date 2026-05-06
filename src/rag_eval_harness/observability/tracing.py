from __future__ import annotations

import time
from contextlib import AbstractContextManager
from typing import Any, Dict, Optional

from rag_eval_harness.observability.logging import get_logger


class TraceSpan(AbstractContextManager):
    """Small local span wrapper.

    This project also includes OpenTelemetry config. This lightweight class keeps the
    sample runnable even without an external collector.
    """

    def __init__(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        self.name = name
        self.attributes = attributes or {}
        self.started = 0.0
        self.logger = get_logger("trace")

    def __enter__(self):
        self.started = time.perf_counter()
        self.logger.info("span.start", span=self.name, attributes=self.attributes)
        return self

    def __exit__(self, exc_type, exc, tb):
        duration_ms = (time.perf_counter() - self.started) * 1000
        self.logger.info(
            "span.end",
            span=self.name,
            duration_ms=round(duration_ms, 3),
            error=str(exc) if exc else None,
            attributes=self.attributes,
        )
        return False

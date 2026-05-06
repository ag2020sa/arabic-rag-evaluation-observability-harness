from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict
from uuid import uuid4

from rag_eval_harness.schemas import utc_now


def append_audit_event(path: str | Path, event_type: str, payload: Dict[str, Any]) -> str:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    event_id = str(uuid4())
    record = {
        "event_id": event_id,
        "created_at": utc_now().isoformat(),
        "event_type": event_type,
        "payload": payload,
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return event_id

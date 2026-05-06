from __future__ import annotations

from fastapi import APIRouter

from rag_eval_harness.schemas import FeedbackEvent
from rag_eval_harness.storage.audit import append_audit_event

router = APIRouter()


@router.post("")
def capture_feedback(event: FeedbackEvent) -> dict:
    event_id = append_audit_event("reports/feedback_events.jsonl", "feedback_event", event.model_dump(mode="json"))
    return {"status": "accepted", "event_id": event_id}

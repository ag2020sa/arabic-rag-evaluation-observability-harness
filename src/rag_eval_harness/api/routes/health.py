from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("")
def health_check() -> dict:
    return {"status": "ok", "service": "arabic-rag-evaluation-harness"}

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Citation(BaseModel):
    source_id: str
    page: Optional[int] = None
    span_text: Optional[str] = None
    start_char: Optional[int] = None
    end_char: Optional[int] = None
    url: Optional[str] = None
    confidence: float = 1.0


class RetrievedChunk(BaseModel):
    id: str
    text: str
    source_id: str
    score: float = 0.0
    rank: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RagRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RagResponse(BaseModel):
    answer: str
    citations: List[Citation] = Field(default_factory=list)
    retrieved_chunks: List[RetrievedChunk] = Field(default_factory=list)
    latency_ms: float = 0.0
    model_name: str = "unknown"
    prompt_version: str = "unknown"
    retriever_version: str = "unknown"
    audit_event_id: str = Field(default_factory=lambda: str(uuid4()))
    token_usage: Dict[str, int] = Field(default_factory=dict)
    cost_usd: float = 0.0
    raw: Dict[str, Any] = Field(default_factory=dict)


class GoldenExample(BaseModel):
    id: str
    query: str
    expected_answer: str = ""
    expected_sources: List[str] = Field(default_factory=list)
    must_include: List[str] = Field(default_factory=list)
    must_not_include: List[str] = Field(default_factory=list)
    category: str = "general"
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MetricResult(BaseModel):
    name: str
    value: float
    threshold: Optional[float] = None
    passed: Optional[bool] = None
    details: Dict[str, Any] = Field(default_factory=dict)


class CaseEvaluationResult(BaseModel):
    case_id: str
    query: str
    category: str
    tags: List[str] = Field(default_factory=list)
    response: RagResponse
    metrics: Dict[str, MetricResult]
    passed: bool
    critical_failures: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class GateResult(BaseModel):
    name: str
    passed: bool
    reason: str
    metrics: Dict[str, float] = Field(default_factory=dict)
    severity: str = "medium"


class EvaluationRunReport(BaseModel):
    run_id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=utc_now)
    project_name: str = "arabic-rag-evaluation-harness"
    dataset_path: str
    adapter_name: str
    prompt_version: str = "unknown"
    model_name: str = "unknown"
    retriever_version: str = "unknown"
    case_results: List[CaseEvaluationResult]
    gates: List[GateResult]
    passed: bool
    decision: str = "UNKNOWN"
    summary: Dict[str, Any] = Field(default_factory=dict)


class FeedbackEvent(BaseModel):
    case_id: Optional[str] = None
    query: str
    answer: Optional[str] = None
    rating: Optional[int] = None
    comment: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    created_at: datetime = Field(default_factory=utc_now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

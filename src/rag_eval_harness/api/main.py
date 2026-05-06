from __future__ import annotations

from fastapi import FastAPI

from rag_eval_harness.api.routes import evaluations, feedback, health
from rag_eval_harness.observability.logging import configure_logging

configure_logging()

app = FastAPI(
    title="Arabic RAG Evaluation & Observability Harness",
    version="0.1.0",
    description="Evaluation, observability, and release gates for Arabic RAG systems.",
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(evaluations.router, prefix="/evaluations", tags=["evaluations"])
app.include_router(feedback.router, prefix="/feedback", tags=["feedback"])

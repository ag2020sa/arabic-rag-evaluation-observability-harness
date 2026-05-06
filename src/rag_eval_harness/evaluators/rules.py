from __future__ import annotations

from rag_eval_harness.metrics.arabic_quality import evaluate_arabic_quality
from rag_eval_harness.metrics.citations import evaluate_citations
from rag_eval_harness.metrics.generation import evaluate_generation
from rag_eval_harness.metrics.retrieval import evaluate_retrieval
from rag_eval_harness.metrics.safety import evaluate_safety
from rag_eval_harness.schemas import GoldenExample, RagRequest, RagResponse


def evaluate_with_rules(example: GoldenExample, request: RagRequest, response: RagResponse) -> dict:
    metrics = {}
    metrics.update(evaluate_retrieval(response.retrieved_chunks, example.expected_sources, k=5))
    metrics.update(evaluate_generation(example, response))
    metrics.update(evaluate_citations(example, response))
    metrics.update(evaluate_arabic_quality(example, response))
    metrics.update(evaluate_safety(request, response))
    return metrics

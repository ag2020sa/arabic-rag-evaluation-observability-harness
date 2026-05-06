from __future__ import annotations

import math
from typing import Iterable, List

from rag_eval_harness.schemas import MetricResult, RetrievedChunk


def _sources(chunks: Iterable[RetrievedChunk]) -> List[str]:
    return [c.source_id for c in chunks]


def precision_at_k(retrieved_sources: List[str], expected_sources: List[str], k: int = 5) -> float:
    if k <= 0:
        return 0.0
    top = retrieved_sources[:k]
    if not top:
        return 0.0
    expected = set(expected_sources)
    return sum(1 for s in top if s in expected) / len(top)


def recall_at_k(retrieved_sources: List[str], expected_sources: List[str], k: int = 5) -> float:
    expected = set(expected_sources)
    if not expected:
        return 1.0
    top = set(retrieved_sources[:k])
    return len(top & expected) / len(expected)


def hit_rate_at_k(retrieved_sources: List[str], expected_sources: List[str], k: int = 5) -> float:
    expected = set(expected_sources)
    if not expected:
        return 1.0
    return 1.0 if any(s in expected for s in retrieved_sources[:k]) else 0.0


def mrr(retrieved_sources: List[str], expected_sources: List[str]) -> float:
    expected = set(expected_sources)
    if not expected:
        return 1.0
    for idx, source in enumerate(retrieved_sources, start=1):
        if source in expected:
            return 1.0 / idx
    return 0.0


def ndcg_at_k(retrieved_sources: List[str], expected_sources: List[str], k: int = 5) -> float:
    expected = set(expected_sources)
    if not expected:
        return 1.0
    dcg = 0.0
    for idx, source in enumerate(retrieved_sources[:k], start=1):
        relevance = 1.0 if source in expected else 0.0
        dcg += relevance / math.log2(idx + 1)
    ideal_hits = min(len(expected), k)
    idcg = sum(1.0 / math.log2(i + 1) for i in range(1, ideal_hits + 1))
    return dcg / idcg if idcg else 0.0


def evaluate_retrieval(chunks: List[RetrievedChunk], expected_sources: List[str], k: int = 5) -> dict[str, MetricResult]:
    retrieved = _sources(chunks)
    return {
        "retrieval.precision_at_k": MetricResult(name="retrieval.precision_at_k", value=precision_at_k(retrieved, expected_sources, k)),
        "retrieval.recall_at_k": MetricResult(name="retrieval.recall_at_k", value=recall_at_k(retrieved, expected_sources, k)),
        "retrieval.hit_rate_at_k": MetricResult(name="retrieval.hit_rate_at_k", value=hit_rate_at_k(retrieved, expected_sources, k)),
        "retrieval.mrr": MetricResult(name="retrieval.mrr", value=mrr(retrieved, expected_sources)),
        "retrieval.ndcg": MetricResult(name="retrieval.ndcg", value=ndcg_at_k(retrieved, expected_sources, k)),
    }

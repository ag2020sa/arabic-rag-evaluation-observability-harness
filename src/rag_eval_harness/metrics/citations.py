from __future__ import annotations

from rag_eval_harness.schemas import GoldenExample, MetricResult, RagResponse


def evaluate_citations(example: GoldenExample, response: RagResponse) -> dict[str, MetricResult]:
    cited_sources = [c.source_id for c in response.citations]
    retrieved_sources = [c.source_id for c in response.retrieved_chunks]
    expected = set(example.expected_sources)

    if not expected:
        source_match = 1.0
        citation_coverage = 1.0
    else:
        source_match = len(set(cited_sources) & expected) / max(len(set(cited_sources)), 1)
        citation_coverage = len(set(cited_sources) & expected) / len(expected)

    cited_in_retrieved = 1.0 if all(src in retrieved_sources for src in cited_sources) else 0.0

    return {
        "citations.source_match": MetricResult(name="citations.source_match", value=source_match, details={"cited_sources": cited_sources, "expected_sources": list(expected)}),
        "citations.citation_coverage": MetricResult(name="citations.citation_coverage", value=citation_coverage),
        "citations.citation_count": MetricResult(name="citations.citation_count", value=float(len(response.citations))),
        "citations.cited_in_retrieved": MetricResult(name="citations.cited_in_retrieved", value=cited_in_retrieved),
        "citations.has_span_text": MetricResult(name="citations.has_span_text", value=1.0 if all(c.span_text for c in response.citations) else 0.0),
    }

from rag_eval_harness.metrics.citations import evaluate_citations
from rag_eval_harness.schemas import Citation, GoldenExample, RagResponse, RetrievedChunk


def test_citation_source_match_and_coverage():
    example = GoldenExample(id="x", query="q", expected_sources=["source_1"])
    response = RagResponse(
        answer="a",
        citations=[Citation(source_id="source_1", span_text="text")],
        retrieved_chunks=[RetrievedChunk(id="c1", source_id="source_1", text="text")],
    )
    metrics = evaluate_citations(example, response)
    assert metrics["citations.source_match"].value == 1.0
    assert metrics["citations.citation_coverage"].value == 1.0
    assert metrics["citations.cited_in_retrieved"].value == 1.0

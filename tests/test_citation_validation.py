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
    assert metrics["citations.page_match"].details["validated"] is False


def test_citation_page_and_span_validation_when_metadata_exists():
    example = GoldenExample(id="x", query="q", expected_sources=["source_1"])
    response = RagResponse(
        answer="a",
        citations=[Citation(source_id="source_1", page=3, span_text="validated span", start_char=6, end_char=20)],
        retrieved_chunks=[
            RetrievedChunk(
                id="c1",
                source_id="source_1",
                text="Intro validated span outro",
                metadata={"page": 3},
            )
        ],
    )
    metrics = evaluate_citations(example, response)
    assert metrics["citations.page_match"].value == 1.0
    assert metrics["citations.page_match"].details["validated"] is True
    assert metrics["citations.span_match"].value == 1.0
    assert metrics["citations.span_match"].details["validated"] is True


def test_citation_reports_missing_and_unsupported_sources():
    example = GoldenExample(id="x", query="q", expected_sources=["expected_source"])
    response = RagResponse(
        answer="a",
        citations=[Citation(source_id="unsupported_source", page=9, span_text="not present")],
        retrieved_chunks=[
            RetrievedChunk(
                id="c1",
                source_id="expected_source",
                text="expected text",
                metadata={"page": 1},
            )
        ],
    )
    metrics = evaluate_citations(example, response)
    assert metrics["citations.source_match"].value == 0.0
    assert metrics["citations.citation_coverage"].value == 0.0
    assert metrics["citations.cited_in_retrieved"].value == 0.0
    assert metrics["citations.unsupported_count"].value == 1.0
    assert metrics["citations.missing_count"].value == 1.0
    assert metrics["citations.source_match"].details["unsupported_sources"] == ["unsupported_source"]
    assert metrics["citations.citation_coverage"].details["missing_expected_sources"] == ["expected_source"]

from __future__ import annotations

from rag_eval_harness.schemas import GoldenExample, MetricResult, RagResponse


def evaluate_citations(example: GoldenExample, response: RagResponse) -> dict[str, MetricResult]:
    cited_sources = [c.source_id for c in response.citations]
    retrieved_by_source = {}
    for chunk in response.retrieved_chunks:
        retrieved_by_source.setdefault(chunk.source_id, []).append(chunk)
    expected = set(example.expected_sources)
    cited = set(cited_sources)
    unsupported_sources = sorted(src for src in cited if src not in retrieved_by_source)
    missing_sources = sorted(src for src in expected if src not in cited)

    if not expected:
        source_match = 1.0
        citation_coverage = 1.0
    else:
        source_match = len(cited & expected) / max(len(cited), 1)
        citation_coverage = len(cited & expected) / len(expected)

    cited_in_retrieved = 1.0 if not unsupported_sources else 0.0
    page_match, page_details = _evaluate_page_matches(response, retrieved_by_source)
    span_match, span_details = _evaluate_span_matches(response, retrieved_by_source)

    return {
        "citations.source_match": MetricResult(
            name="citations.source_match",
            value=source_match,
            details={
                "cited_sources": cited_sources,
                "expected_sources": sorted(expected),
                "unsupported_sources": unsupported_sources,
            },
        ),
        "citations.citation_coverage": MetricResult(
            name="citations.citation_coverage",
            value=citation_coverage,
            details={"missing_expected_sources": missing_sources},
        ),
        "citations.citation_count": MetricResult(name="citations.citation_count", value=float(len(response.citations))),
        "citations.cited_in_retrieved": MetricResult(
            name="citations.cited_in_retrieved",
            value=cited_in_retrieved,
            details={"unsupported_sources": unsupported_sources},
        ),
        "citations.has_span_text": MetricResult(
            name="citations.has_span_text",
            value=1.0 if response.citations and all(c.span_text for c in response.citations) else 0.0,
            details={"validated": bool(response.citations), "note": "Checks span_text presence, not source authority."},
        ),
        "citations.page_match": MetricResult(name="citations.page_match", value=page_match, details=page_details),
        "citations.span_match": MetricResult(name="citations.span_match", value=span_match, details=span_details),
        "citations.unsupported_count": MetricResult(name="citations.unsupported_count", value=float(len(unsupported_sources))),
        "citations.missing_count": MetricResult(name="citations.missing_count", value=float(len(missing_sources))),
    }


def _evaluate_page_matches(response: RagResponse, retrieved_by_source: dict) -> tuple[float, dict]:
    checked = []
    skipped = []
    mismatches = []
    for citation in response.citations:
        chunks = retrieved_by_source.get(citation.source_id, [])
        pages = {chunk.metadata.get("page") for chunk in chunks if chunk.metadata.get("page") is not None}
        if citation.page is None or not pages:
            skipped.append({"source_id": citation.source_id, "reason": "missing_citation_or_chunk_page"})
            continue
        checked.append(citation.source_id)
        if citation.page not in pages:
            mismatches.append({"source_id": citation.source_id, "citation_page": citation.page, "retrieved_pages": sorted(pages)})
    if not checked:
        return 1.0, {"validated": False, "skipped": skipped, "mismatches": mismatches}
    return (1.0 if not mismatches else 0.0), {"validated": True, "checked_sources": checked, "skipped": skipped, "mismatches": mismatches}


def _evaluate_span_matches(response: RagResponse, retrieved_by_source: dict) -> tuple[float, dict]:
    checked = []
    skipped = []
    mismatches = []
    for citation in response.citations:
        chunks = retrieved_by_source.get(citation.source_id, [])
        if not chunks:
            skipped.append({"source_id": citation.source_id, "reason": "source_not_retrieved"})
            continue
        chunk_texts = [chunk.text for chunk in chunks]
        if citation.start_char is not None and citation.end_char is not None:
            if _char_span_matches(citation, chunk_texts):
                checked.append(citation.source_id)
            else:
                checked.append(citation.source_id)
                mismatches.append({"source_id": citation.source_id, "reason": "char_span_not_found"})
            continue
        if citation.span_text:
            checked.append(citation.source_id)
            if not any(citation.span_text in text for text in chunk_texts):
                mismatches.append({"source_id": citation.source_id, "reason": "span_text_not_found"})
            continue
        skipped.append({"source_id": citation.source_id, "reason": "missing_span_metadata"})
    if not checked:
        return 1.0, {"validated": False, "skipped": skipped, "mismatches": mismatches}
    return (1.0 if not mismatches else 0.0), {"validated": True, "checked_sources": checked, "skipped": skipped, "mismatches": mismatches}


def _char_span_matches(citation, chunk_texts: list[str]) -> bool:
    for text in chunk_texts:
        if citation.start_char < 0 or citation.end_char > len(text) or citation.start_char >= citation.end_char:
            continue
        candidate = text[citation.start_char:citation.end_char]
        if citation.span_text:
            if candidate == citation.span_text:
                return True
        elif candidate:
            return True
    return False

from __future__ import annotations

from rag_eval_harness.arabic.normalizer import coverage, token_overlap
from rag_eval_harness.schemas import GoldenExample, MetricResult, RagResponse


def evaluate_generation(example: GoldenExample, response: RagResponse) -> dict[str, MetricResult]:
    context = "\n".join(chunk.text for chunk in response.retrieved_chunks)
    answer = response.answer
    answer_relevance = max(token_overlap(example.query, answer), token_overlap(example.expected_answer, answer))
    # MVP proxy: during golden-set evaluation, combine retrieved-context overlap with
    # expected-answer overlap. Production mode should replace this with claim-level
    # attribution or an Arabic-aware LLM-as-judge.
    groundedness = max(token_overlap(answer, context), token_overlap(answer, example.expected_answer))
    completeness = coverage(answer, example.must_include)
    must_not_hits = [term for term in example.must_not_include if term and term in answer]
    must_not_score = 1.0 if not must_not_hits else 0.0
    return {
        "generation.answer_relevance": MetricResult(
            name="generation.answer_relevance",
            value=answer_relevance,
            details={"method": "token_overlap_proxy"},
        ),
        "generation.groundedness": MetricResult(
            name="generation.groundedness",
            value=groundedness,
            details={"method": "max(answer_context_overlap, answer_expected_overlap)_proxy"},
        ),
        "generation.completeness": MetricResult(
            name="generation.completeness",
            value=completeness,
            details={"must_include": example.must_include},
        ),
        "generation.must_not_include_pass": MetricResult(
            name="generation.must_not_include_pass",
            value=must_not_score,
            details={"violations": must_not_hits},
        ),
    }

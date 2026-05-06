from __future__ import annotations

from rag_eval_harness.schemas import GoldenExample, MetricResult, RagResponse


class DisabledLLMJudge:
    """Placeholder evaluator.

    Keep this disabled by default to make the project runnable without external API keys.
    Replace with a provider-backed implementation when needed.
    """

    name = "disabled_llm_judge"

    async def evaluate(self, example: GoldenExample, response: RagResponse) -> dict[str, MetricResult]:
        return {
            "llm_judge.enabled": MetricResult(
                name="llm_judge.enabled",
                value=0.0,
                passed=True,
                details={"note": "LLM judge disabled. Rule-based metrics are used."},
            )
        }

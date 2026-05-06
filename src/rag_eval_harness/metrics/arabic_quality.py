from __future__ import annotations

from rag_eval_harness.arabic.normalizer import arabic_ratio, coverage, tokenize
from rag_eval_harness.schemas import GoldenExample, MetricResult, RagResponse

TERMINOLOGY = [
    "إجازة", "سنوية", "عقد", "فترة التجربة", "مكافأة", "نهاية الخدمة", "بيانات شخصية",
    "تنقيح", "سياسات", "موافقة", "تدقيق",
]


def simple_readability(text: str) -> float:
    tokens = tokenize(text, remove_stopwords=False)
    if not tokens:
        return 0.0
    avg_len = sum(len(t) for t in tokens) / len(tokens)
    # Arabic enterprise answers can include long terms. Keep the proxy simple and explainable.
    return max(0.0, min(1.0, 1.2 - (avg_len / 12.0)))


def evaluate_arabic_quality(example: GoldenExample, response: RagResponse) -> dict[str, MetricResult]:
    answer = response.answer
    return {
        "arabic_quality.arabic_ratio": MetricResult(name="arabic_quality.arabic_ratio", value=arabic_ratio(answer)),
        "arabic_quality.readability": MetricResult(name="arabic_quality.readability", value=simple_readability(answer)),
        "arabic_quality.terminology_consistency": MetricResult(
            name="arabic_quality.terminology_consistency",
            value=coverage(answer, [t for t in TERMINOLOGY if t in example.expected_answer or t in example.query])
        ),
    }

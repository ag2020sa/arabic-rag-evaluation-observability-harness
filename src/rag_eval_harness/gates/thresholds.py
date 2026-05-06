from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml


def load_thresholds(path: str | Path) -> Dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def flatten_thresholds(thresholds: Dict[str, Any]) -> Dict[str, float]:
    flat: Dict[str, float] = {}
    mapping = {
        "retrieval.precision_at_k": ("retrieval", "precision_at_k_min"),
        "retrieval.recall_at_k": ("retrieval", "recall_at_k_min"),
        "retrieval.mrr": ("retrieval", "mrr_min"),
        "retrieval.ndcg": ("retrieval", "ndcg_min"),
        "retrieval.hit_rate_at_k": ("retrieval", "hit_rate_at_k_min"),
        "generation.answer_relevance": ("generation", "answer_relevance_min"),
        "generation.groundedness": ("generation", "groundedness_min"),
        "generation.completeness": ("generation", "completeness_min"),
        "citations.source_match": ("citations", "source_match_min"),
        "citations.citation_coverage": ("citations", "citation_coverage_min"),
        "citations.citation_count": ("citations", "citation_count_min"),
        "arabic_quality.arabic_ratio": ("arabic_quality", "arabic_ratio_min"),
        "arabic_quality.readability": ("arabic_quality", "readability_min"),
        "arabic_quality.terminology_consistency": ("arabic_quality", "terminology_consistency_min"),
    }
    for metric, (section, key) in mapping.items():
        if section in thresholds and key in thresholds[section]:
            flat[metric] = float(thresholds[section][key])
    return flat

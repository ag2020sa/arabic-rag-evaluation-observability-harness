from __future__ import annotations

import asyncio
from collections import defaultdict
from statistics import mean

from rag_eval_harness.adapters.base import RAGAdapter
from rag_eval_harness.datasets.loader import load_golden_examples
from rag_eval_harness.evaluators.llm_judge import DisabledLLMJudge
from rag_eval_harness.evaluators.rules import evaluate_with_rules
from rag_eval_harness.gates.quality_gates import apply_case_thresholds, build_release_gates, case_passed, release_decision
from rag_eval_harness.gates.thresholds import load_thresholds
from rag_eval_harness.observability.tracing import TraceSpan
from rag_eval_harness.schemas import CaseEvaluationResult, EvaluationRunReport, RagRequest


async def evaluate_dataset_async(
    adapter: RAGAdapter,
    dataset_path: str,
    thresholds_path: str,
    include_llm_judge: bool = False,
) -> EvaluationRunReport:
    examples = load_golden_examples(dataset_path)
    thresholds = load_thresholds(thresholds_path)
    judge = DisabledLLMJudge()
    case_results: list[CaseEvaluationResult] = []

    for example in examples:
        request = RagRequest(query=example.query, metadata={"case_id": example.id, **example.metadata})
        with TraceSpan("evaluate_case", attributes={"case_id": example.id, "category": example.category}):
            response = await adapter.ask(request)
            metrics = evaluate_with_rules(example, request, response)
            if include_llm_judge:
                metrics.update(await judge.evaluate(example, response))
            metrics = apply_case_thresholds(metrics, thresholds)
            passed, critical_failures, warnings = case_passed(metrics)
            case_results.append(
                CaseEvaluationResult(
                    case_id=example.id,
                    query=example.query,
                    category=example.category,
                    tags=example.tags,
                    response=response,
                    metrics=metrics,
                    passed=passed,
                    critical_failures=critical_failures,
                    warnings=warnings,
                )
            )

    gates = build_release_gates(case_results, thresholds)
    decision = release_decision(gates)
    report_passed = decision == "PROMOTE_TO_STAGING"
    summary = build_summary(case_results, gates)

    model_name = case_results[0].response.model_name if case_results else "unknown"
    prompt_version = case_results[0].response.prompt_version if case_results else "unknown"
    retriever_version = case_results[0].response.retriever_version if case_results else "unknown"

    return EvaluationRunReport(
        dataset_path=dataset_path,
        adapter_name=adapter.name,
        prompt_version=prompt_version,
        model_name=model_name,
        retriever_version=retriever_version,
        case_results=case_results,
        gates=gates,
        passed=report_passed,
        decision=decision,
        summary=summary,
    )


def build_summary(case_results: list[CaseEvaluationResult], gates: list) -> dict:
    metric_values: dict[str, list[float]] = defaultdict(list)
    latencies = []
    costs = []
    for case in case_results:
        latencies.append(case.response.latency_ms)
        costs.append(case.response.cost_usd)
        for name, metric in case.metrics.items():
            metric_values[name].append(metric.value)
    averages = {name: mean(values) for name, values in metric_values.items() if values}
    return {
        "case_count": len(case_results),
        "passed_cases": sum(1 for c in case_results if c.passed),
        "pass_rate": sum(1 for c in case_results if c.passed) / max(len(case_results), 1),
        "failed_gates": [g.name for g in gates if not g.passed],
        "critical_failures": [f for c in case_results for f in c.critical_failures],
        "warnings": [w for c in case_results for w in c.warnings],
        "latency_ms_avg": mean(latencies) if latencies else 0.0,
        "cost_usd_avg": mean(costs) if costs else 0.0,
        "metric_averages": averages,
    }


def evaluate_dataset(adapter: RAGAdapter, dataset_path: str, thresholds_path: str, include_llm_judge: bool = False) -> EvaluationRunReport:
    return asyncio.run(evaluate_dataset_async(adapter, dataset_path, thresholds_path, include_llm_judge))

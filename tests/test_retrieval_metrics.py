from rag_eval_harness.metrics.retrieval import hit_rate_at_k, mrr, ndcg_at_k, precision_at_k, recall_at_k


def test_retrieval_metrics():
    retrieved = ["a", "b", "c"]
    expected = ["b", "d"]
    assert precision_at_k(retrieved, expected, 2) == 0.5
    assert recall_at_k(retrieved, expected, 3) == 0.5
    assert hit_rate_at_k(retrieved, expected, 2) == 1.0
    assert mrr(retrieved, expected) == 0.5
    assert 0.0 < ndcg_at_k(retrieved, expected, 3) <= 1.0

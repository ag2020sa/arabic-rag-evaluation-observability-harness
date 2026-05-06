# Architecture

## Purpose

The Arabic RAG Evaluation & Observability Harness wraps around an existing Arabic RAG application and provides a repeatable engineering process for measuring quality, safety, traceability, and release readiness.

## System context

```text
Golden Dataset + Replay Samples + Policies
              │
              ▼
       Evaluation Harness
              │ instruments
              ▼
      RAG System Under Test
              │
              ▼
   Metrics + Traces + Audit + Registry
              │
              ▼
       CI/CD Quality Gates
```

## RAG System Under Test

The evaluated RAG system is expected to include:

1. User Query
2. Arabic Preprocessing & Normalization
3. Prompt Builder
4. Embedding Model
5. Hybrid Retriever
6. Reranker
7. Vector DB
8. Document Store
9. LLM Inference
10. Answer with Citations

The harness does not require direct control over all internal components. It needs enough response metadata to evaluate quality: retrieved chunks, source IDs, citations, answer, model version, prompt version, retriever version, and latency.

## Adapter pattern

Use adapters to connect to any RAG backend:

- `LocalMockRAGAdapter` for CI and demos
- `HTTPRAGAdapter` for an external FastAPI RAG service
- Custom adapters for LangChain, LlamaIndex, Haystack, or internal platforms

## Evaluation dimensions

| Dimension | Goal |
|---|---|
| Retrieval | Did the system retrieve the correct sources? |
| Generation | Is the answer relevant, complete, and grounded? |
| Citations | Do citations match the answer and retrieved source? |
| Arabic Quality | Is the Arabic fluent, readable, and terminologically consistent? |
| Safety | Does the answer avoid prompt injection, jailbreaks, PII leakage, and policy violations? |
| Regression | Did a new version perform worse than a baseline? |

## Release decisions

The quality gates map a report to one of three outcomes:

- `PROMOTE_TO_STAGING`
- `HUMAN_REVIEW_REQUIRED`
- `BLOCK_RELEASE`


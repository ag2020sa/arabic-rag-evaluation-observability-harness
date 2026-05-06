# Portfolio Snippets

Repository:

`https://github.com/ag2020sa/arabic-rag-evaluation-observability-harness`

## One-Line Project Summary

Arabic RAG evaluation, observability, audit, and CI/CD release gates for source-grounded enterprise AI systems.

## GitHub Pinned Repository Description

Enterprise-grade Arabic RAG evaluation harness with retrieval metrics, citation validation, Arabic quality checks, safety gates, audit reports, FastAPI, Streamlit, and CI/CD release decisions.

## CV Entry

**Arabic RAG Evaluation & Observability Harness | 2026**  
Built a production-minded evaluation and observability harness for Arabic RAG systems with retrieval metrics, groundedness checks, citation validation, Arabic quality scoring, safety tests, audit-ready reports, and CI/CD release gates.

## CV Bullets

- Built an Arabic RAG evaluation harness with golden-set regression tests, retrieval metrics, citation validation, Arabic quality scoring, and safety checks for source-grounded enterprise AI systems.
- Implemented explicit release decisions: `PROMOTE_TO_STAGING`, `HUMAN_REVIEW_REQUIRED`, and `BLOCK_RELEASE`, with demo paths proving each gate outcome.
- Shipped FastAPI and Streamlit interfaces for running evaluations, viewing gate summaries, comparing release decisions, and inspecting case-level warnings.
- Added audit-ready JSON and Markdown reports, GitHub Actions CI, adapter-based RAG integration, and Arabic-specific normalization.

## LinkedIn Project Description

Built an Arabic RAG Evaluation & Observability Harness for enterprise AI systems. The project wraps any existing RAG backend through adapters and evaluates retrieval quality, generation groundedness, citation accuracy, Arabic answer quality, safety risks, and regression behavior.

It includes FastAPI endpoints, a Streamlit dashboard, audit-ready reports, GitHub Actions release gates, and three explicit release outcomes: promote, human review, or block. The demo proves all three outcomes using a golden Arabic HR dataset and intentional failure scenarios.

## Short LinkedIn Post

I built an Arabic RAG Evaluation & Observability Harness focused on production release confidence, not chatbot demos.

It evaluates Arabic RAG systems across retrieval quality, groundedness, citation validation, Arabic quality, safety, regression, observability, and auditability.

The project includes:

- Arabic golden-set evaluation
- citation and source-grounding validation
- safety checks for prompt injection, PII leakage, jailbreaks, and policy violations
- FastAPI evaluation endpoint
- Streamlit release dashboard
- GitHub Actions CI/CD gates
- explicit decisions: promote, human review, or block

Repo: https://github.com/ag2020sa/arabic-rag-evaluation-observability-harness

## Interview Talk Track

Most RAG demos only show that a system can answer a question. This project shows how I would govern an Arabic enterprise RAG system before release. It wraps the RAG backend with an adapter, runs a golden Arabic evaluation suite, validates citations and source grounding, checks safety and Arabic quality, records audit artifacts, and converts results into release decisions.

The important part is that the gates are active: one demo promotes a good candidate, one sends degraded quality to human review, and one blocks a candidate with broken citations.

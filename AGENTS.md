# AGENTS.md

This repository is intended to be usable by coding agents. The detailed implementation plan is in `agent.md`.

## Primary instruction

Build the Arabic RAG Evaluation & Observability Harness as a production-minded portfolio project. Prioritize correctness, clear architecture, simple running commands, testability, and high-quality documentation.

The canonical product blueprint is `assets/visuals/arabic_rag_eval_observability_harness_portfolio_final_2x.png`. Treat it as the primary architecture reference for all future implementation work.

## Non-negotiables

- Do not remove citation validation or audit logging.
- Do not turn this into a generic chatbot demo.
- Keep Arabic-specific quality checks and normalization.
- Keep release gates explicit: promote, block, or human review.
- Keep the sample dataset small but realistic.
- Keep interfaces adapter-based so the harness can wrap any existing RAG system.

## Recommended workflow

1. Run the sample evaluation.
2. Add or modify metrics.
3. Add tests before changing gate logic.
4. Generate a release report.
5. Update docs and CV bullets if capabilities change.

## Visual blueprint implementation rule

Every feature should map back to at least one section of the canonical visual:

- Inputs & Test Assets
- RAG System Under Test
- Evaluation Harness
- Observability & Telemetry
- Storage, Registry & Audit
- CI/CD & Decision Gates
- Feedback Loop
- Governance Controls

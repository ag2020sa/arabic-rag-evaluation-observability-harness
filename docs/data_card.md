# Data Card

## Dataset name

Arabic HR Golden Dataset — Sample

## Purpose

A small synthetic dataset for testing the Arabic RAG evaluation harness. It covers HR/labor-law style questions, internal policy questions, PII handling, and prompt injection safety.

## Important warning

The dataset and corpus are synthetic samples for portfolio implementation. They are not official legal sources and are not legal advice.

## Fields

- `id`
- `query`
- `expected_answer`
- `expected_sources`
- `must_include`
- `must_not_include`
- `category`
- `tags`
- `metadata`

## Expansion plan

- Add official source documents where permitted.
- Add page and span-level citation metadata.
- Add production replay cases after anonymization.
- Add adversarial safety cases.
- Add dialect and terminology variations.
- Add bilingual questions if the product supports English/Arabic.

# Evaluation Metrics

## Retrieval metrics

### Precision@k
Measures how many of the top-k retrieved sources are expected sources.

### Recall@k
Measures how many expected sources were found in the top-k retrieved sources.

### Hit Rate@k
A binary signal: did the retrieval contain at least one expected source in top-k?

### MRR
Mean Reciprocal Rank rewards placing the first relevant source high in the ranking.

### nDCG
Rewards relevant documents appearing earlier while supporting graded ranking behavior.

## Generation metrics

### Answer relevance
The MVP uses an explainable lexical overlap proxy between query, expected answer, and generated answer. In a production version, replace or complement this with LLM-as-judge scoring.

### Groundedness
The MVP estimates groundedness by comparing answer terms against retrieved context. In production, use entailment, claim extraction, or LLM judge workflows.

### Completeness
Checks whether required concepts from the golden example appear in the answer.

### Must-not-include pass
Ensures disallowed phrases or unsafe information do not appear in the answer.

## Citation metrics

### Source match
Checks whether cited source IDs match expected source IDs.

### Citation coverage
Checks whether all expected source IDs are covered by citations.

### Cited-in-retrieved
Ensures cited sources came from retrieved chunks rather than fabricated citations.

### Page and span checks
When citation and retrieved chunk metadata include page or span fields, the harness checks page consistency and whether cited span text or character offsets can be matched to the retrieved chunk text. If metadata is missing, the report marks that part as not validated instead of pretending authoritative verification was possible.

### Missing and unsupported citations
The report includes counts and details for expected sources that were not cited and cited sources that were not present in retrieved chunks.

## Arabic quality metrics

### Arabic ratio
Measures how much of the answer uses Arabic characters.

### Readability
A simple length-based proxy for readability. Replace with a richer readability model later.

### Terminology consistency
Checks important domain terms such as إجازة، عقد، فترة التجربة، مكافأة نهاية الخدمة، بيانات شخصية.

## Safety metrics

- Prompt injection detected
- Jailbreak detected
- PII leakage detected
- Policy violation detected

These are rule-based MVP checks and should be extended with attack datasets, OWASP LLM Top 10 mapping, and red-team prompts.

# Arabic RAG Evaluation & Observability Harness

مشروع بورتفوليو هندسي لتقييم ومراقبة وحوكمة إصدارات أنظمة RAG العربية، خصوصًا في البيئات السعودية المنظمة مثل الموارد البشرية، الامتثال، الأنظمة الداخلية، والأمن السيبراني.

هذا ليس chatbot demo. الفكرة الأساسية هي بناء harness يلتف حول أي نظام Arabic RAG موجود ويقيس جودة الاسترجاع، groundedness، صحة الاستشهادات، جودة العربية، السلامة، قابلية التدقيق، وجاهزية الإطلاق.

## الروابط العامة

- صفحة العرض: <https://ag2020sa.github.io/arabic-rag-evaluation-observability-harness/>
- الريبو: <https://github.com/ag2020sa/arabic-rag-evaluation-observability-harness>
- الإصدار الرسمي: <https://github.com/ag2020sa/arabic-rag-evaluation-observability-harness/releases/tag/v1.0.0>

## التصميم الأساسي

التصميم النهائي هو المرجع الأساسي للمشروع:

`assets/visuals/arabic_rag_eval_observability_harness_portfolio_final_2x.png`

أي تطوير لاحق يجب أن يحافظ على أقسام التصميم:

- Inputs & Test Assets
- RAG System Under Test
- Evaluation Harness
- Observability & Telemetry
- Storage, Registry & Audit
- CI/CD & Decision Gates
- Feedback Loop
- Governance Controls

## ماذا يقيس المشروع؟

- جودة الاسترجاع: Precision@k, Recall@k, MRR, nDCG, Hit Rate
- جودة الإجابة: relevance, groundedness, completeness
- صحة الاستشهادات: source match, coverage, span checks
- جودة العربية: normalization, readability, terminology consistency
- السلامة: prompt injection, jailbreak, PII leakage, policy violations
- المقارنة والانحدار: regression and release comparison
- المراقبة: logs, traces, latency, token/cost, hallucination flags
- الحوكمة: audit trail, registry, versioned reports, release gates

## التشغيل السريع

```bash
make install
make demo
make human-review-demo
make failure-demo
make lint
make test
```

## قرارات الإطلاق

| الأمر | القرار المتوقع |
|---|---|
| `make demo` | `PROMOTE_TO_STAGING` |
| `make human-review-demo` | `HUMAN_REVIEW_REQUIRED` |
| `make failure-demo` | `BLOCK_RELEASE` |

بهذا يثبت المشروع أن بوابات القرار فعالة: ليست كل النتائج تمر، وليست كل النتائج تفشل؛ يوجد مسار واضح للترقية، المراجعة البشرية، والحظر.

## تشغيل الواجهات

```bash
make api
make dashboard
```

افتح:

```text
API docs:  http://localhost:8080/docs
Dashboard: http://localhost:8501
```

## الملفات المهمة

- `README.md`: الشرح الرئيسي بالإنجليزية.
- `docs/final_demo_walkthrough.md`: مسار العرض النهائي.
- `docs/visual_blueprint.md`: ربط التصميم بالكود.
- `docs/portfolio_snippets.md`: نصوص جاهزة للـ CV وLinkedIn.
- `assets/visuals/`: التصميمات النهائية.
- `src/rag_eval_harness/`: الكود الأساسي.
- `data/golden/`: بيانات الاختبار الذهبية.
- `configs/thresholds.yaml`: thresholds للـ quality gates.
- `reports/latest_release_report.md`: تقرير النجاح.
- `reports/human_review_release_report.md`: تقرير المراجعة البشرية.
- `reports/failure_release_report.md`: تقرير الحظر.
- `.github/workflows/evaluation.yml`: CI/CD workflow.

## الربط مع نظام RAG حقيقي

الواجهات adapter-based. يمكن استخدام:

- `LocalMockRAGAdapter` للديمو والاختبارات.
- `HTTPRAGAdapter` للربط مع backend خارجي.
- Adapter مخصص لأي نظام LangChain أو LlamaIndex أو منصة داخلية.

الـ backend الحقيقي يحتاج أن يعيد:

- answer
- citations
- retrieved_chunks
- latency
- model_name
- prompt_version
- retriever_version

## الخلاصة

هذا المشروع يثبت القدرة على بناء طبقة تقييم وحوكمة إنتاجية حول Arabic RAG system: قياس الجودة، منع الإجابات غير المؤصلة، التحقق من الاستشهادات، تسجيل التدقيق، وتشغيل release gates واضحة قبل الترقية.
